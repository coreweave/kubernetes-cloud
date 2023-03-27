import collections
import json
import tempfile
import time

import kserve
import logging
import os
from typing import Dict, Union, Optional
from argparse import ArgumentParser, Namespace
from io import BytesIO

import tensorizer

import torch
from torch import autocast
from diffusers import (
    StableDiffusionPipeline,
    LMSDiscreteScheduler,
    AutoencoderKL,
    UNet2DConditionModel, ModelMixin, ConfigMixin,
)
from transformers import CLIPTextModel, CLIPTextConfig, CLIPTokenizer, AutoConfig, PreTrainedModel

HF_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger()


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--model-id", default=os.getenv("MODEL_ID", "/mnt/models/CompVis/stable-diffusion-v1-4"), type=str,
    )
    parser.add_argument(
        "--precision", choices=["float16", "float32"], default="float16", type=str
    )
    parser.add_argument("--guidance-scale", default=float(os.getenv("CONDITION_SCALE", 7.0)), type=float)
    parser.add_argument("--num-inference-steps", default=int(os.getenv("NUM_INFERENCE_STEPS", 50)), type=int)
    parser.add_argument("--seed", default=os.getenv("SEED"), type=int)
    parser.add_argument("--width", default=int(os.getenv("WIDTH", 512)), type=int)
    parser.add_argument("--height", default=int(os.getenv("HEIGHT", 512)), type=int)
    parser.add_argument("--tensorized", default=False, action="store_true")
    args = parser.parse_args()

    args.model_name = args.model_id.split("/")[-1]

    return args


def set_logger(name: str):
    global logger
    logger = logging.getLogger(name)


def load_tensorizer_model(
    path_uri: str,
    modelclass: Union[PreTrainedModel, ModelMixin, ConfigMixin] = None,
    configclass: Optional[Union[ConfigMixin, AutoConfig]] = None,
    model_prefix: str = "model",
    device: torch.device = tensorizer.utils.get_device(),
    dtype: str = None
) -> torch.nn.Module:
    """
    Given a path prefix, load the model with a custom extension
    Args:
        path_uri: path to the model. Can be a local path or a URI
        modelclass: The model class to load the tensors into.
        configclass: The config class to load the model config into. This must be
            set if you are loading a model from HuggingFace Transformers.
        model_prefix: The prefix to use to distinguish between multiple serialized
            models. The default is "model".
        device: The device to load the tensors to.
        dtype: The dtype to load the tensors into. If None, the dtype is inferred from
            the model.
    """

    if model_prefix is None:
        model_prefix = "model"

    begin_load = time.time()
    ram_usage = tensorizer.utils.get_mem_usage()

    config_uri = f"{path_uri}/{model_prefix}-config.json"
    tensors_uri = f"{path_uri}/{model_prefix}.tensors"
    tensor_stream = tensorizer.stream_io.open_stream(tensors_uri)

    logger.info(f"Loading {tensors_uri}, {ram_usage}")

    tensor_deserializer = tensorizer.TensorDeserializer(
        tensor_stream, device=device, dtype=dtype, lazy_load=True
    )

    if configclass is not None:
        try:
            with tempfile.TemporaryDirectory() as dir:
                open(os.path.join(dir, "config.json"), "w").write(
                    tensorizer.stream_io.open_stream(config_uri).read().decode("utf-8")
                )
                config = configclass.from_pretrained(dir)
                config.gradient_checkpointing = True
        except ValueError:
            config = configclass.from_pretrained(config_uri)
        model = tensorizer.utils.no_init_or_tensor(
            lambda: modelclass.from_pretrained(
                None, config=config, state_dict=collections.OrderedDict()
            )
        )
    else:
        try:
            config = json.loads(
                tensorizer.stream_io.open_stream(config_uri).read().decode("utf-8")
            )
        except ValueError:
            with open(config_uri, "r") as f:
                config = json.load(f)
        model = tensorizer.utils.no_init_or_tensor(lambda: modelclass(**config))

    tensor_deserializer.load_into_module(model)

    tensor_load_s = time.time() - begin_load
    rate_str = tensorizer.utils.convert_bytes(
        tensor_deserializer.total_bytes_read / tensor_load_s
    )
    tensors_sz = tensorizer.utils.convert_bytes(tensor_deserializer.total_bytes_read)
    logger.info(
        f"Model tensors loaded in {tensor_load_s:0.2f}s, read "
        + f"{tensors_sz} @ {rate_str}/s, {tensorizer.utils.get_mem_usage()}"
    )

    return model


class Model(kserve.Model):
    def __init__(self,
                 model_name: str,
                 model_id: str,
                 precision: str,
                 guidance_scale: float,
                 num_inference_steps: int,
                 width: int,
                 height: int,
                 tensorized: bool,
                 seed: int):
        super().__init__(model_name)

        self.ready = False
        self.pipeline = None
        self.model_name = model_name
        self.model_id = model_id
        self.precision = precision
        self.tensorized = tensorized

        self.parameters = {
            "GUIDANCE_SCALE": guidance_scale,
            "NUM_INFERENCE_STEPS": num_inference_steps,
            "SEED": seed,
            "WIDTH": width,
            "HEIGHT": height,
        }

    def load_diffusers(self):
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=getattr(torch, self.precision),
            scheduler=LMSDiscreteScheduler.from_pretrained(
                self.model_id, subfolder="scheduler"
            ),
            local_files_only=True,
        )

    def load_tensorizer(self):
        vae = load_tensorizer_model(self.model_id, AutoencoderKL, None, "vae")
        unet = load_tensorizer_model(
            self.model_id, UNet2DConditionModel, None, "unet"
        )
        encoder = load_tensorizer_model(
            self.model_id, CLIPTextModel, CLIPTextConfig, "encoder"
        )

        scheduler = LMSDiscreteScheduler.from_pretrained(
            self.model_id, subfolder="scheduler", use_auth_token=HF_TOKEN
        )

        tokenizer = CLIPTokenizer.from_pretrained(
            self.model_id, subfolder="tokenizer", use_auth_token=HF_TOKEN
        )

        self.pipeline = StableDiffusionPipeline(
            text_encoder=encoder,
            vae=vae,
            unet=unet,
            scheduler=scheduler,
            tokenizer=tokenizer,
            safety_checker=None,
            feature_extractor=None,
        )

    def load(self):
        logger.info(f"Loading {self.model_name}")

        if self.tensorized:
            self.load_tensorizer()
        else:
            self.load_diffusers()

        logger.info(f"Loaded {self.model_name}")

        logger.info(f"Loading {self.model_name} to accelerator")
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
        request_parameters = self.parameters.copy()
        if "parameters" in request:
            logger.debug(f"Configuring request")
            request_parameters = self.configure_request(
                request, request_parameters
            )
            logger.debug(f"Request configured")

        generator = None
        if request_parameters["SEED"] is not None:
            generator = torch.Generator("cuda").manual_seed(
                request_parameters["SEED"]
            )

        logger.debug(f"Generating image")
        with autocast("cuda"):
            image = self.pipeline(
                request["prompt"],
                height=request_parameters["HEIGHT"],
                width=request_parameters["WIDTH"],
                guidance_scale=request_parameters["GUIDANCE_SCALE"],
                num_inference_steps=request_parameters["NUM_INFERENCE_STEPS"],
                generator=generator,
            ).images[0]
        logger.debug(f"Image generated")

        image_file = BytesIO()
        image.save(image_file, format="PNG")
        response = image_file.getvalue()

        return response


def main():
    args = get_args()
    set_logger(args.model_name)
    logger.info(f"Model Name: {args.model_name}")
    logger.info(f'Model ID: {args.model_id}')

    model = Model(**vars(args))
    model.load()
    kserve.ModelServer().start([model])


if __name__ == "__main__":
    main()
