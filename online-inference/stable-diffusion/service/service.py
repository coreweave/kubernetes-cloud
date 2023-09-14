import os
import io
import logging
import time
from typing import Optional
from argparse import ArgumentParser

import uvicorn
import torch
import tensorizer
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import CLIPTextModel, CLIPTextConfig, CLIPTokenizer
from diffusers import (
    StableDiffusionPipeline,
    LMSDiscreteScheduler,
    AutoencoderKL,
    UNet2DConditionModel
)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

# Argument parser setup
parser = ArgumentParser()
parser.add_argument("--model-uri", default=os.getenv("MODEL_URI", "s3://tensorized/runwayml/stable-diffusion-v1-5"), type=str)
parser.add_argument("--precision", choices=["float16", "float32"], default="float16", type=str)
parser.add_argument("--device-id", default=0, help="GPU ID to use for inference, or -1 for CPU [default = 0]")
parser.add_argument("--port", default=8080, help="Port to listen on [default = 80 (http)]", type=int)
parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP address to listen on [default = 0.0.0.0 (all interfaces)]")
parser.add_argument("--s3-access-key", default=os.getenv("AWS_KEY"), type=str)
parser.add_argument("--s3-secret-access-key", default=os.getenv("AWS_SECRET"), type=str)
parser.add_argument("--s3-endpoint", default=os.getenv("AWS_HOST", "accel-object.ord1.coreweave.com"), type=str)
args = parser.parse_args()

def load_artifact(path_uri, module) -> None:
    deserializer = tensorizer.TensorDeserializer(
        file_obj=tensorizer.stream_io.open_stream(
            path_uri=path_uri,
            mode="rb",
            s3_access_key_id = args.s3_access_key,
            s3_secret_access_key = args.s3_secret_access_key,
            s3_endpoint = args.s3_endpoint,
            s3_config_path=None,
        ),
        plaid_mode=True
    )
    deserializer.load_into_module(module)
    deserializer.close()
    logger.info(f"Loaded tensorized S3 artifact from {path_uri}")

def load_model_s3(path_uri) -> StableDiffusionPipeline:
    logger.info(f"Loading {args.precision} model from S3 URI: {path_uri}")
    hf_id = '/'.join(path_uri.split("/")[-2:])
    text_encoder_config = CLIPTextConfig.from_pretrained(hf_id, subfolder="text_encoder")

    with tensorizer.utils.no_init_or_tensor():
        unet = UNet2DConditionModel.from_config(UNet2DConditionModel.load_config(hf_id, subfolder="unet"))
        vae = AutoencoderKL.from_config(AutoencoderKL.load_config(hf_id, subfolder="vae"))
        text_encoder = CLIPTextModel(text_encoder_config)

    dtype_str = "/fp16" if args.precision == "float16" else ""

    start = time.time()

    load_artifact(f"{path_uri}{dtype_str}/unet.tensors", unet)
    load_artifact(f"{path_uri}{dtype_str}/vae.tensors", vae)
    load_artifact(f"{path_uri}{dtype_str}/text_encoder.tensors", text_encoder)

    logger.info(f"All artifacts loaded successfully in {time.time() - start:.2f} seconds")

    return StableDiffusionPipeline(
        vae=vae,
        text_encoder=text_encoder,
        unet=unet,
        tokenizer=CLIPTokenizer.from_pretrained(hf_id, subfolder="tokenizer"),
        scheduler=LMSDiscreteScheduler.from_pretrained(hf_id, subfolder="scheduler"),
        safety_checker=None,
        feature_extractor=None,
        requires_safety_checker=False
    )

def load_model_local(path_uri) -> StableDiffusionPipeline:
    logger.info(f"Loading local model from URI: {path_uri}")
    return StableDiffusionPipeline.from_pretrained(path_uri, dtype=getattr(torch, args.precision))

def load_model(path_uri) -> StableDiffusionPipeline:
    if path_uri.startswith("s3://"):
        return load_model_s3(path_uri)
    else:
        return load_model_local(path_uri)

class Generation(BaseModel):
    prompt: str
    guidance_scale: Optional[float] = 7.0
    num_inference_steps: Optional[int] = 28
    seed: Optional[int] = None
    width: Optional[int] = 512
    height: Optional[int] = 512

app = FastAPI(title="Stable Diffusion Inference API")
logger.info(f"Setting CUDA device ID: {args.device_id}")
torch.cuda.set_device(args.device_id)
pipe = load_model(args.model_uri).to('cuda')
pipe.set_progress_bar_config(disable=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_health():
    logger.info("Health check requested")
    return "OK"

@app.post("/generate")
def generate(generation: Generation):
    try:
        generator = None
        image = io.BytesIO()

        if generation.seed is not None:
            generator = torch.Generator(device='cuda').manual_seed(generation.seed)

        pipe(
            prompt=generation.prompt,
            height=generation.height,
            width=generation.width,
            num_inference_steps=generation.num_inference_steps,
            guidance_scale=generation.guidance_scale,
            generator=generator,
            output_type="pil"
        ).images[0].save(image, format='PNG')

        return Response(content=image.getvalue(), media_type="image/png")
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=500)

if __name__ == '__main__':
    logger.info(f"Starting inference server at {args.ip}:{args.port}")
    uvicorn.run(app, host=args.ip, port=int(args.port))
