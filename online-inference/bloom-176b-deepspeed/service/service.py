from argparse import ArgumentParser
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from transformers.deepspeed import HfDeepSpeedConfig
from transformers.models.bloom.modeling_bloom import BloomBlock as BloomBlock
from transformers.utils import is_offline_mode
from transformers import pipeline
import deepspeed
import gc
import glob
import io
import json
import math
import os
import sys
import time
import torch
import torch.distributed as dist
import logging
import kserve
from typing import Dict

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger("bloom-deepspeed-inference-fp16")

ds_dist_backend = "nccl"
deepspeed.init_distributed(ds_dist_backend)

rank = dist.get_rank()

def log_rank0(level, msg):
    if rank != 0:
        return
    logger.log(level, "+++ " + msg)

log_rank0(
    logging.INFO, f"Deepspeed distributed intialized with backend {ds_dist_backend}"
)

t_start = time.time()

parser = ArgumentParser()
parser.add_argument(
    "--model-id",
    default="microsoft/bloom-deepspeed-inference-fp16",
    type=str,
    help="model_id",
)
parser.add_argument("--model-revision", default="main")
parser.add_argument("--hf-home", default="/mnt/models/hub")
parser.add_argument(
    "--local_rank", required=False, type=int, help="used by dist launchers"
)
parser.add_argument("--min-length", type=int, default=1)
parser.add_argument("--max-length", type=int, default=128)
parser.add_argument("--temperature", type=float, default=1.0)
parser.add_argument("--top-k", type=int, default=50)
parser.add_argument("--top-p", type=float, default=1.0)
parser.add_argument("--repetition-penalty", type=float, default=1.0)
args = parser.parse_args()

local_rank = args.local_rank

world_size = 8

log_rank0(logging.INFO, f"Huggingace Model ID: {args.model_id}")

model_id_split = args.model_id.split("/")
model_org = model_id_split[0]
log_rank0(logging.INFO, f"Huggingace Model Org: {model_org}")
model_repo = model_id_split[1]
log_rank0(logging.INFO, f"Huggingace Model Repo: {model_repo}")

model_directory = "models" + "--" + model_org + "--" + model_repo

model_path = os.path.join(args.hf_home, model_directory)
log_rank0(logging.INFO, f"Model path {model_path}")
model_ref_path = os.path.join(model_path, "refs", args.model_revision)

with open(model_ref_path, "r") as f:
    model_git_ref = f.readlines()[0]

model_snapshot_path = os.path.join(model_path, "snapshots", model_git_ref)
log_rank0(logging.INFO, f"Loading model from {model_snapshot_path}")

dtype = torch.float16

model_params = {
    'MIN_LENGTH': int(os.getenv('MIN_LENGTH', args.min_length)),
    'MAX_LENGTH': int(os.getenv('MAX_LENGTH', args.max_length)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', args.temperature)),
    'TOP_K': int(os.getenv('TOP_K', args.top_k)),
    'TOP_P': float(os.getenv('TOP_P', args.top_p)),
    'REPETITION_PENALTY': float(os.getenv('REPETITION_PENALTY', args.repetition_penalty)),
}

class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.tokenizer = None
        self.config = None
        self.model = None
        self.pipeline = None

    def _load_model(self):
        with deepspeed.OnDevice(dtype=dtype, device="meta"):
            log_rank0(logging.INFO, f"Initializing meta tensors on {rank}")
            model = AutoModelForCausalLM.from_config(self.config, torch_dtype=dtype)
            log_rank0(logging.INFO, f"Meta tensors initialized on {rank}")

        model = model.eval()

        checkpoints_config = os.path.join(
            model_snapshot_path, "ds_inference_config.json"
        )

        log_rank0(logging.INFO, "Checkpoints config: {checkpoints_config}")

        log_rank0(logging.INFO, "Initializing Deepspeed engine")
        model = deepspeed.init_inference(
            model,
            mp_size=world_size,
            dtype=dtype,
            checkpoint=checkpoints_config,
            base_dir=model_snapshot_path,
            replace_with_kernel_inject=True,
        )
        log_rank0(logging.INFO, "Deepspeed engine initialized")

        model = model.module

        return model

    def load(self):
        log_rank0(logging.INFO, "Loading tokenizer")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_snapshot_path, local_files_only=True
        )

        log_rank0(logging.INFO, "Loading config")
        self.config = AutoConfig.from_pretrained(
            model_snapshot_path, local_files_only=True
        )

        log_rank0(logging.INFO, "Loading model")
        self.model = self._load_model()

        t_end = time.time()
        t_ready = t_end - t_start
        log_rank0(logging.INFO, f"Time to model ready: {t_ready}")

        log_rank0(logging.INFO, "Loading pipeline")
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=local_rank,
        )

        self.ready = True

    def predict(self, request: Dict) -> Dict:
        request_params = model_params.copy()

        if 'parameters' in request:
            parameters = request['parameters']
            for k, pv in parameters.items():
                pk = k.upper()
                if pk in request_params:
                    logger.debug(f'Parameter {pk} changed from {request_params[pk]} to {pv}')
                    request_params[pk] = pv

        return {'predictions': self.pipeline(
            request['instances'],
            do_sample=True,
            min_length=request_params['MIN_LENGTH'],
            max_length=request_params['MAX_LENGTH'],
            temperature=request_params['TEMPERATURE'],
            top_k=request_params['TOP_K'],
            top_p=request_params['TOP_P'],
            repetition_penalty=request_params['REPETITION_PENALTY']
        )}



if __name__ == "__main__":
    model = Model(name=model_repo)
    model.load()
    if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
        kserve.ModelServer().start([model])
