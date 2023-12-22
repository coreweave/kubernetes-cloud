import json
import logging
import os
import re
import time
import traceback
from argparse import ArgumentParser
from typing import List, Optional

import tensorizer
import torch
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    TextGenerationPipeline,
)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

# Argument parser setup
model_uri_default = (
    os.getenv("MODEL_URI") or "s3://tensorized/EleutherAI/pythia-70m"
)
s3_access_key_default = os.getenv("S3_KEY") or None
s3_secret_access_key_default = os.getenv("S3_SECRET") or None
s3_endpoint_default = os.getenv("S3_HOST") or "accel-object.ord1.coreweave.com"

parser = ArgumentParser()
parser.add_argument("--model-uri", default=model_uri_default, type=str)
parser.add_argument(
    "--precision", choices=["float16", "float32"], default="float16", type=str
)
parser.add_argument(
    "--device-id",
    default=0,
    help="GPU ID to use for inference, or -1 for CPU [default = 0]",
)
parser.add_argument(
    "--port",
    default=80,
    help="Port to listen on [default = 80 (http)]",
    type=int,
)
parser.add_argument(
    "--ip",
    type=str,
    default="0.0.0.0",
    help="IP address to listen on [default = 0.0.0.0 (all interfaces)]",
)
parser.add_argument("--s3-access-key", default=s3_access_key_default, type=str)
parser.add_argument(
    "--s3-secret-access-key", default=s3_secret_access_key_default, type=str
)
parser.add_argument("--s3-endpoint", default=s3_endpoint_default, type=str)
args = parser.parse_args()


def load_artifact(path_uri: str, module: torch.nn.Module) -> None:
    deserializer = tensorizer.TensorDeserializer(
        file_obj=tensorizer.stream_io.open_stream(
            path_uri=path_uri,
            mode="rb",
            s3_access_key_id=args.s3_access_key,
            s3_secret_access_key=args.s3_secret_access_key,
            s3_endpoint=args.s3_endpoint,
            s3_config_path=None,
        ),
        plaid_mode=True,
    )
    deserializer.load_into_module(module)
    deserializer.close()
    logger.info(f"Loaded tensorized S3 artifact from {path_uri}")


def load_model_s3(path_uri: str) -> TextGenerationPipeline:
    match = re.match(
        (
            r"s3://"
            r"(?P<bucket>[^/]+)"
            r"/(?P<id>[^/]+(?:/[^/]+)??)"
            r"(?:/fp16)?"
            r"(?:/$)?"
            r"(?:/model.tensors)?"
            r"$"
        ),
        path_uri,
    )
    if not match:
        raise ValueError(
            f"Could not parse S3 URI: {path_uri!r}"
            "\nExpected format: s3://<bucket name>/<HuggingFace ID>"
            "\nFor example:"
            "\n  - s3://tensorized/EleutherAI/pythia-70m"
            "\n  - s3://my-private-bucket/distilgpt2"
        )
    hf_id = match.group("id")
    config = AutoConfig.from_pretrained(hf_id)
    tokenizer = AutoTokenizer.from_pretrained(hf_id)

    with tensorizer.utils.no_init_or_tensor():
        model = AutoModelForCausalLM.from_config(config)

    model_file = (
        "fp16/model.tensors" if args.precision == "float16" else "model.tensors"
    )
    bucket = match.group("bucket")
    s3_uri = "s3://" + "/".join((bucket, hf_id, model_file))
    start = time.monotonic()
    load_artifact(s3_uri, model)
    end = time.monotonic()
    logger.info(f"Model loaded successfully in {end - start:.2f} seconds")

    return TextGenerationPipeline(
        model=model, tokenizer=tokenizer, device=args.device_id
    )


def load_model_local(path_uri: str) -> TextGenerationPipeline:
    dtype = torch.float16 if args.precision == "float16" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(path_uri, torch_dtype=dtype)
    tokenizer = AutoTokenizer.from_pretrained(path_uri)
    return TextGenerationPipeline(
        model=model, tokenizer=tokenizer, device=args.device_id
    )


def load_model(path_uri: str) -> TextGenerationPipeline:
    logger.info(f"Loading {args.precision} model from: {path_uri}")
    if path_uri.startswith("s3://"):
        return load_model_s3(path_uri)
    else:
        return load_model_local(path_uri)


class Completion(BaseModel):
    prompt: str
    max_new_tokens: Optional[int] = 10
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    typical_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    do_sample: Optional[bool] = False
    penalty_alpha: Optional[float] = None
    num_return_sequences: Optional[int] = 1
    stop_sequence: Optional[str] = None
    bad_words: Optional[List] = None


app = FastAPI(title="LLM Inference API")
logger.info(f"Setting CUDA device ID: {args.device_id}")
torch.cuda.set_device(args.device_id)
pipe = load_model(args.model_uri)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_health():
    logger.debug("Health check requested")
    return "OK"


@app.post("/completion")
async def completion(completion: Completion):
    try:
        output = pipe(
            completion.prompt,
            max_new_tokens=completion.max_new_tokens,
            temperature=completion.temperature,
            top_p=completion.top_p,
            top_k=completion.top_k,
            repetition_penalty=completion.repetition_penalty,
            do_sample=completion.do_sample,
            penalty_alpha=completion.penalty_alpha,
            num_return_sequences=completion.num_return_sequences,
            stop_sequence=completion.stop_sequence,
            pad_token_id=pipe.tokenizer.eos_token_id,
        )
        return Response(
            content=json.dumps(output),
            media_type="application/json",
            status_code=200,
        )
    except Exception as e:
        logger.error(traceback.format_exc())
        return Response(
            content=(
                f"Server encountered an error of type {type(e).__name__}."
                "\nSee logs for details."
            ),
            media_type="text/plain",
            status_code=500,
        )


if __name__ == "__main__":
    logger.info(f"Starting inference server at {args.ip}:{args.port}")
    uvicorn.run(app, host=args.ip, port=int(args.port))
