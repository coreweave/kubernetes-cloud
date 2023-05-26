import os
from typing import List, Optional

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline


class Completion(BaseModel):
    prompt: str
    engine: Optional[str] = None
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

args = {
    "model": os.getenv("INFERENCE_MODEL", "distilgpt2"),
    "device": int(os.getenv("INFERENCE_DEVICE", 0)),
    "port": int(os.getenv("INFERENCE_PORT", 80)),
}

model = pipeline(
    "text-generation",
    model=args["model"],
    torch_dtype=torch.float16,
    device=args["device"],
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
    uvicorn.run("inference:app", host="0.0.0.0", port=args["port"])
