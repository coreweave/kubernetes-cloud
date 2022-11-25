import kserve
import logging
import os
from typing import Dict
from argparse import ArgumentParser
from io import BytesIO

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler

parser = ArgumentParser()
parser.add_argument("--model-id", default="CompVis/stable-diffusion-v1-4", type=str)
parser.add_argument("--hf-home", default="/mnt/models/hub", type=str)
parser.add_argument(
    "--precision", choices=["float16", "float32"], default="float16", type=str
)
parser.add_argument("--guidance-scale", default=7.0, type=float)
parser.add_argument("--num-inference-steps", default=50, type=int)
parser.add_argument("--seed", default=None, type=int)
parser.add_argument("--width", default=512, type=int)
parser.add_argument("--height", default=512, type=int)
parser.add_argument("--beta-start", default=0.00085, type=float)
parser.add_argument("--beta-end", default=0.012, type=float)
parser.add_argument("--num-train-timesteps", default=1000, type=int)
args = parser.parse_args()

options = {
    "MODEL_ID": os.getenv("MODEL_ID", default=args.model_id),
    "MODEL_CACHE": os.getenv("HF_HOME", default=args.hf_home),
    "PRECISION": str(os.getenv("PRECISION", default=args.precision)),
    "BETA_START": float(os.getenv("BETA_START", default=args.beta_start)),
    "BETA_END": float(os.getenv("BETA_END", default=args.beta_end)),
    "NUM_TRAIN_TIMESTEPS": int(
        os.getenv("NUM_TRAIN_TIMESTEPS", default=args.num_train_timesteps)
    ),
}

try:
    MODEL_NAME = options["MODEL_ID"].split("/")[-1]
except:
    MODEL_NAME = options["MODEL_ID"]

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(MODEL_NAME)
logger.info(f"Model Name: {MODEL_NAME}")
logger.info(f'Model ID: {options["MODEL_ID"]}')
logger.info(f'Model Cache: {options["MODEL_CACHE"]}')

parameters = {
    "GUIDANCE_SCALE": float(os.getenv("CONDITION_SCALE", default=args.guidance_scale)),
    "NUM_INFERENCE_STEPS": int(
        os.getenv("NUM_INFERENCE_STEPS", default=args.num_inference_steps)
    ),
    "SEED": os.getenv("SEED", default=args.seed),
    "WIDTH": int(os.getenv("WIDTH", default=args.width)),
    "HEIGHT": int(os.getenv("HEIGHT", default=args.height)),
}


class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.pipeline = None
        self.model_name = name

    def load(self):
        logger.info(f"Loading {MODEL_NAME}")
        lms = LMSDiscreteScheduler(
            beta_start=options["BETA_START"],
            beta_end=options["BETA_END"],
            beta_schedule="scaled_linear",
            num_train_timesteps=options["NUM_TRAIN_TIMESTEPS"],
        )

        self.pipeline = StableDiffusionPipeline.from_pretrained(
            options["MODEL_ID"],
            cache_dir=options["MODEL_CACHE"],
            torch_dtype=getattr(torch, options["PRECISION"]),
            scheduler=lms,
            local_files_only=True,
        )
        logger.info(f"Loaded {MODEL_NAME}")

        logger.info(f"Loading {MODEL_NAME} to accelerator")
        self.pipeline.to("cuda")
        logger.info(f"Accelerator loaded")

        self.ready = True

    def configure_request(self, request: Dict, request_parameters) -> Dict:
        parameters = request["parameters"]
        for k, pv in parameters.items():
            pk = k.upper()
            if pk in request_parameters:
                request_parameters[pk] = pv
                logger.debug(
                    f"Parameter {pk} changed from {request_parameters[pk]} to {pv}"
                )

        return request_parameters

    def predict(self, request: Dict) -> Dict:
        request_parameters = parameters.copy()
        if "parameters" in request:
            logger.debug(f"Configuring request")
            request_parameters = self.configure_request(request, request_parameters)
            logger.debug(f"Request configured")

        generator = None
        if request_parameters["SEED"] is not None:
            generator = torch.Generator("cuda").manual_seed(request_parameters["SEED"])

        logger.debug(f"Generating image")
        with autocast("cuda"):
            image = self.pipeline(
                request["prompt"],
                height=request_parameters["HEIGHT"],
                width=request_parameters["WIDTH"],
                guidance_scale=request_parameters["GUIDANCE_SCALE"],
                num_inference_steps=request_parameters["NUM_INFERENCE_STEPS"],
                generator=generator,
            )["sample"][0]
        logger.debug(f"Image generated")

        image_file = BytesIO()
        image.save(image_file, format="PNG")
        response = image_file.getvalue()

        return response


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])
