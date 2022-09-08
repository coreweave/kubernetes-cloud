from typing import Dict
import accelerate
import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument("--model-id", type=str, default="EleutherAI/gpt-j-6B")
parser.add_argument("--model-cache", type=str, default="/mnt/models")
parser.add_argument("--model-precision", type=str, default="float16")
parser.add_argument("--model-type", type=str, default="text-generation")
parser.add_argument("--model-device", type=int, default=0)
parser.add_argument("--model-config", type=str, default="")
parser.add_argument("--min-length", type=int, default=1)
parser.add_argument("--max-length", type=int, default=1024)
parser.add_argument("--temperature", type=float, default=1.0)
parser.add_argument("--top-k", type=int, default=50)
parser.add_argument("--top-p", type=float, default=0.9)
parser.add_argument("--repetition-penalty", type=float, default=1.0)
parser.add_argument("--benchmark-sequence-length", type=int, default=8)
args = parser.parse_args()

options = {
    "SERVER_NUM_WORKERS": int(os.getenv("SERVER_NUM_WORKERS", 1)),
    "SERVER_PORT": int(os.getenv("SERVER_PORT", 8080)),
    "MODEL_ID": os.getenv("MODEL_NAME", args.model_id),
    "MODEL_CACHE": os.getenv("MODEL_CACHE", args.model_cache),
    "MODEL_PATH": os.path.join(args.model_cache, args.model_id),
    "MODEL_PRECISION": os.getenv("MODEL_PRECISION", args.model_precision).lower(),
    "MODEL_TYPE": os.getenv("MODEL_TYPE", args.model_type),
    "MODEL_NAME": re.sub(r"[^\w-]", "-", args.model_id).lower(),
    "MODEL_DEVICE": int(os.getenv("MODEL_DEVICE", args.model_device)),
    "MODEL_CONFIG": os.getenv("MODEL_CONFIG", args.model_config),
    "MODEL_DOWNLOAD_TIMEOUT": int(os.getenv("MODEL_DOWNLOAD_TIMEOUT", 300)),
}

model_params = {
    "MIN_LENGTH": int(os.getenv("MIN_LENGTH", args.min_length)),
    "MAX_LENGTH": int(os.getenv("MAX_LENGTH", args.max_length)),
    "TEMPERATURE": float(os.getenv("TEMPERATURE", args.temperature)),
    "TOP_K": int(os.getenv("TOP_K", args.top_k)),
    "TOP_P": float(os.getenv("TOP_P", args.top_p)),
    "REPETITION_PENALTY": float(
        os.getenv("REPETITION_PENALTY", args.repetition_penalty)
    ),
    "BENCHMARK_SEQUENCE_LENGTH": os.getenv(
        "BENCHMARK_SEQUENCE_LENGTH", args.benchmark_sequence_length
    ),
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
        self.dataset = None

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
        if options["MODEL_PRECISION"] == "float16":
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
            low_cpu_mem_usage=True,
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

    def configure_request(self, request):
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

        if "benchmark" in request:
            request_params["BENCHMARK"] = True
            request_params["MIN_LENGTH"] = request_params["MAX_LENGTH"]
        else:
            request_params["BENCHMARK"] = False

        if "instances" in request:
            request_params["INSTANCES"] = request["instances"]

        return request_params

    def _predict(self, request_params):
        return {
            "predictions": self.generator(
                request_params["INSTANCES"][0],
                do_sample=False,
                min_length=request_params["MIN_LENGTH"],
                max_length=request_params["MAX_LENGTH"],
                temperature=request_params["TEMPERATURE"],
                top_k=request_params["TOP_K"],
                top_p=request_params["TOP_P"],
                repetition_penalty=request_params["REPETITION_PENALTY"],
                pad_token_id=self.tokenizer.eos_token_id,
            )
        }

    def predict(self, request: Dict) -> Dict:
        request_params = self.configure_request(request)
        if request_params["BENCHMARK"] is True:
            return self.benchmark(request_params)
        else:
            return self._predict(request_params)

    def load_dataset(self):
        data = open("the-time-machine.txt", "r").read()
        tokens = self.tokenizer.encode(data)
        sequence_start = random.randrange(len(tokens) - 2048)
        sequence_end = sequence_start + 2048
        return tokens[sequence_start:sequence_end]

    def benchmark(self, request_params):
        if self.dataset is None:
            self.dataset = self.load_dataset()

        assert (
            request_params["BENCHMARK_SEQUENCE_LENGTH"] < request_params["MAX_LENGTH"]
        )

        sequence_start = random.randrange(
            len(self.dataset) - request_params["BENCHMARK_SEQUENCE_LENGTH"]
        )
        sequence_end = sequence_start + request_params["BENCHMARK_SEQUENCE_LENGTH"]
        random_sequence_encoded = self.dataset[sequence_start:sequence_end]
        random_sequence = self.tokenizer.decode(random_sequence_encoded)

        request_params["INSTANCES"] = [random_sequence]

        start = time.time()
        predicitions = self._predict(request_params)
        end = time.time()
        generation_time = end - start

        logger.info(
            f'Tokens In: {request_params["BENCHMARK_SEQUENCE_LENGTH"]}, New Tokens: {request_params["MAX_LENGTH"]- request_params["BENCHMARK_SEQUENCE_LENGTH"]}, Generation Time: {generation_time}'
        )

        return {
            "benchmark_results": {
                "input_sequence_length": request_params["BENCHMARK_SEQUENCE_LENGTH"],
                "generated_tokens": request_params["MAX_LENGTH"]
                - request_params["BENCHMARK_SEQUENCE_LENGTH"],
                "time": generation_time,
            }
        }

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
