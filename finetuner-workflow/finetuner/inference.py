from typing import List, Optional

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

from utils import DashParser
from utils import validation as val

parser = DashParser(description="Text model inference HTTP server")

parser.add_argument(
    "--model",
    type=str,
    default="distilgpt2",
    help="Model to use for inference (directory, or HuggingFace ID) [default = distilgpt2]",
)
parser.add_argument(
    "--device-id",
    type=val.non_negative(int, special_val=-1),
    default=0,
    help="GPU ID to use for inference, or -1 for CPU [default = 0]",
)
parser.add_argument(
    "--port",
    type=val.non_negative(int),
    default=80,
    help="Port to listen on [default = 80 (http)]",
)
parser.add_argument(
    "--ip",
    type=str,
    default="0.0.0.0",
    help="IP address to listen on [default = 0.0.0.0 (all interfaces)]",
)

args = parser.parse_args()


class Completion(BaseModel):
    prompt: str
    max_new_tokens: Optional[int] = 10
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    typical_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    do_sample: Optional[bool] = True
    penalty_alpha: Optional[float] = None
    num_return_sequences: Optional[int] = 1
    stop_sequence: Optional[str] = None
    bad_words: Optional[List] = None


app = FastAPI(title="Inference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = pipeline(
    "text-generation",
    model=args.model,
    torch_dtype=None if args.device_id == -1 else torch.float16,
    device=args.device_id,
)


@app.get("/")
def get_health():
    return "OK"


@app.post("/completion")
def completion(completion: Completion):
    try:
        return model(
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
        )
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("inference:app", host=args.ip, port=args.port)
