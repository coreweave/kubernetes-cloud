from typing import Dict
import logging
import os
import re
import time
import json
import random
import kserve
import deepspeed

from transformers import AutoConfig, AutoTokenizer, pipeline, AutoModelForCausalLM
import torch

model_name_origin = os.getenv("MODEL_NAME", "EleutherAI/gpt-j-6B")

options = {
    "SERVER_NUM_WORKERS": int(os.getenv("SERVER_NUM_WORKERS", 1)),
    "SERVER_PORT": int(os.getenv("SERVER_PORT", 8080)),
    "MODEL_PATH": os.getenv("MODEL_PATH", "/model-cache/"),
    "MODEL_NAME": re.sub(r"[^\w-]", "-", model_name_origin).lower(),
    "MODEL_TYPE": os.getenv("MODEL_TYPE", "text-generation"),
    "MODEL_PRECISION": os.getenv("MODEL_PRECISION", "fp16").lower(),
    "MODEL_DEVICE": int(os.getenv("MODEL_DEVICE", 0)),
    "MODEL_CONFIG": os.getenv("MODEL_CONFIG", ""),
    "BENCHMARK_WARMUP_ROUNDS": int(os.getenv("BENCHMARK_WARMUP_ROUNDS", 0)),
    "BENCHMARK_SEQUENCE_ROUNDS": int(os.getenv("BENCHMARK_SEQUENCE_ROUNDS", 10)),
    "BENCHMARK_BATCH_SIZE": int(os.getenv("BENCHMARK", 0)),
    "MODEL_DOWNLOAD_TIMEOUT": int(os.getenv("MODEL_DOWNLOAD_TIMEOUT", 300)),
}

options["MODEL_PATH"] = os.path.join(options["MODEL_PATH"], model_name_origin)

model_params = {
    "MIN_LENGTH": int(os.getenv("MIN_LENGTH", 1)),
    "MAX_LENGTH": int(os.getenv("MAX_LENGTH", -1)),
    "TEMPERATURE": float(os.getenv("TEMPERATURE", -1)),
    "TOP_K": int(os.getenv("TOP_K", -1)),
    "TOP_P": float(os.getenv("TOP_P", -1)),
    "REPETITION_PENALTY": float(os.getenv("REPETITION_PENALTY", 1.125)),
}

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(options["MODEL_NAME"])

for key, value in options.items():
    logger.info(f"{key}:{value}")


class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = options["MODEL_NAME"]
        self.ready = False
        self.config = None
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.wiki_corpus = None

    def load_config(self):
        logger.info(f'Loading config from {options["MODEL_PATH"]} ...')
        self.config = AutoConfig.from_pretrained(
            options["MODEL_PATH"], local_files_only=True
        )
        if options["MODEL_CONFIG"] != "":
            cfg = json.loads(options["MODEL_CONFIG"])
            for ck, cv in cfg.items():
                logger.info(f"{ck}:{cv}")
                if hasattr(self.config, ck):
                    logger.info(
                        f"Config.{ck} changed from {getattr(self.config, ck)} to {cv}"
                    )
                    setattr(self.config, ck, cv)
        logger.info(f"Config loaded.")

    def get_config_param(self, param_name):
        if model_params[param_name] > 0:
            return True
        model_params[param_name] = getattr(self.config, param_name.lower())
        return False

    def apply_params(self):
        for ck in model_params:
            if self.get_config_param(ck):
                logger.info(f"Apply parameter {ck}={model_params[ck]}")

    def optimize(self):
        if options["MODEL_PRECISION"] == "bfloat16":
            self.model.bfloat16().eval().cuda()
            logger.info("Model uses bfloat16.")
        if options["MODEL_PRECISION"] == "fp16":
            logger.info("Model uses mixed precision (FP16).")
            self.model.half().eval().cuda()
        else:
            self.model.eval().cuda()

    def load_tokenizer(self):
        tokenizer_path = options["MODEL_PATH"]

        # Check if tokenizer comes from different model
        if os.path.isfile(os.path.join(tokenizer_path, "tokenizer.txt")):
            with open(os.path.join(tokenizer_path, "tokenizer.txt"), "r") as file:
                tokenizer_path = os.path.join(
                    tokenizer_path, "tokenizer", file.read().replace("\n", "")
                )
                logger.info(f"Tokenizer path: {tokenizer_path}")

            if not os.path.isdir(tokenizer_path):
                raise Exception(f"Tokenizer {tokenizer_path} does not exist")

        logger.info(f"Loading tokenizer from {tokenizer_path} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path, local_files_only=True
        )
        logger.info(f"Tokenizer loaded.")

    def load(self):
        start_time = time.perf_counter()

        self.load_config()
        self.apply_params()

        self.load_tokenizer()

        logger.info(
            f'Loading model from {options["MODEL_PATH"]} into device {options["MODEL_DEVICE"]}:{torch.cuda.get_device_name(options["MODEL_DEVICE"])}'
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            options["MODEL_PATH"],
            config=self.config,
            torch_dtype=torch.float16,
            local_files_only=True,
        )
        self.optimize()
        logger.info(f"Model loaded.")

        logger.info(f"Creating generator for model ...")
        self.generator = pipeline(
            options["MODEL_TYPE"],
            config=self.config,
            model=self.model,
            tokenizer=self.tokenizer,
            device=options["MODEL_DEVICE"],
        )

        logger.info(f"Initializing DeepSpeed...")
        self.generator.model = deepspeed.init_inference(
            self.generator.model,
            dtype=torch.float16,
            replace_method="auto",
            replace_with_kernel_inject=True,
            enable_cuda_graph=True,
        )
        logger.info(f"DeepSpeed initialized.")

        logger.info(
            f"Model is ready in {str(time.perf_counter() - start_time)} seconds."
        )
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        request_params = model_params.copy()

        if "parameters" in request:
            parameters = request["parameters"]
            for k, pv in parameters.items():
                pk = k.upper()
                if pk in request_params:
                    logger.debug(
                        f"Parameter {pk} changed from {request_params[pk]} to {pv}"
                    )
                    request_params[pk] = pv

        return {
            "predictions": self.generator(
                request["instances"],
                do_sample=False,
                min_length=request_params["MIN_LENGTH"],
                max_length=request_params["MAX_LENGTH"],
                temperature=request_params["TEMPERATURE"],
                top_k=request_params["TOP_K"],
                top_p=request_params["TOP_P"],
                repetition_penalty=request_params["REPETITION_PENALTY"],
            )
        }

    def warmup(self):
        logger.info(f'Warmup model {options["MODEL_NAME"]}')
        logger.info(
            f'Device {options["MODEL_DEVICE"]}:{torch.cuda.get_device_name(options["MODEL_DEVICE"])}'
        )
        for i in range(1, options["BENCHMARK_WARMUP_ROUNDS"]):
            seq_len = random.randrange(128, 1920)
            self.wiki_corpus.reset()
            text = self.wiki_corpus.get(seq_len)
            input_ids = (
                self.tokenizer(text, return_tensors="pt").input_ids.long().cuda()
            )
            min_len = seq_len + 40
            max_len = random.randrange(min_len, 2048)
            self.model.generate(
                input_ids,
                do_sample=True,
                min_length=min_len,
                max_length=max_len,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            logger.info("Warming up ...")
        logger.info(f"Warmup done")

    def benchmark(self):
        self.wiki_corpus = WikiCorpus("wiki_corpus.txt")
        self.wiki_corpus.load()
        self.wiki_corpus.sort()

        if options["BENCHMARK_WARMUP_ROUNDS"] > 0:
            self.warmup()

        benchmark_start_time = time.perf_counter()
        logger.info(f'Benchmarking model {options["MODEL_NAME"]}')
        logger.info(
            f'Device {options["MODEL_DEVICE"]}:{torch.cuda.get_device_name(options["MODEL_DEVICE"])}'
        )
        logger.info(
            "{:<10} {:<10} {:<10} {:<10}".format(
                "Batch size", "Seq len", "Max len", "time"
            )
        )
        max_batch_size = options["BENCHMARK_BATCH_SIZE"]
        for batch_size in range(1, max_batch_size + 1):
            self.wiki_corpus.reset()
            for seq_len in range(128, 2049, 128):
                text = self.wiki_corpus.get(seq_len)
                input_ids = (
                    self.tokenizer(text, return_tensors="pt").input_ids.long().cuda()
                )
                max_length = min(2049, seq_len + 40)
                benchmark_time = 0
                for i in range(options["BENCHMARK_SEQUENCE_ROUNDS"]):
                    current_time = time.perf_counter()
                    self.model.generate(
                        input_ids,
                        do_sample=True,
                        min_length=max_length,
                        max_length=max_length,
                        pad_token_id=self.tokenizer.eos_token_id,
                    )
                    benchmark_time += time.perf_counter() - current_time
                logger.info(
                    "{:>10} {:<10} {:<10} {:<10}".format(
                        batch_size,
                        seq_len,
                        max_length,
                        round(benchmark_time / options["BENCHMARK_SEQUENCE_ROUNDS"], 2),
                    )
                )
        logger.info(
            f"Total benchmark time {round(time.perf_counter() - benchmark_start_time, 2)}s"
        )

    @staticmethod
    def is_ready():
        ready_path = os.path.join(options["MODEL_PATH"], ".ready.txt")
        logger.info(f"Waiting for download to be ready ...")
        if os.path.exists(ready_path):
            logger.info("Download ready")
            return
        interval_time = 10
        intervals = options["MODEL_DOWNLOAD_TIMEOUT"] // interval_time
        for i in range(intervals):
            time.sleep(interval_time)
            if os.path.exists(ready_path):
                logger.info("Download ready")
                return
        raise Exception(f"Download timeout {interval_time * intervals}!")


if __name__ == "__main__":
    Model.is_ready()
    model = Model(options["MODEL_NAME"])
    model.load()
    kserve.ModelServer().start([model])
