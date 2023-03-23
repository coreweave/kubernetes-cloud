import argparse
import os
import json
from typing import Optional, Union

import torch
from diffusers import StableDiffusionPipeline
from diffusers.configuration_utils import ConfigMixin
from tensorizer import TensorSerializer
from transformers import AutoConfig


def serialize_model(
        model: torch.nn.Module,
        config: Optional[Union[ConfigMixin, AutoConfig, dict]],
        model_directory: str,
        model_prefix: str = "model",
):
    """
    Remove the tensors from a PyTorch model, convert them to NumPy
    arrays and serialize them to GooseTensor format. The stripped
    model is also serialized to pytorch format.
    Args:
        model: The model to serialize.
        config: The model's configuration. This is optional and only
            required for HuggingFace Transformers models. Diffusers
            models do not require this.
        model_directory: The directory to save the serialized model to.
        model_prefix: The prefix to use for the serialized model files. This
            is purely optional and it allows for multiple models to be
            serialized to the same directory. A good example are Stable
            Diffusion models. Default is "model".
    """

    os.makedirs(model_directory, exist_ok=True)
    dir_prefix = f"{model_directory}/{model_prefix}"

    if config is None:
        config = model
    if config is not None:
        if hasattr(config, "to_json_file"):
            config.to_json_file(f"{dir_prefix}-config.json")
        if isinstance(config, dict):
            open(f"{dir_prefix}-config.json", "w").write(
                json.dumps(config, indent=2)
            )

    ts = TensorSerializer(f"{dir_prefix}.tensors")
    ts.write_module(model)
    ts.close()


def main():
    token = os.environ.get("HUGGING_FACE_HUB_TOKEN")

    parser = argparse.ArgumentParser()
    parser.add_argument('--model-id', default="CompVis/stable-diffusion-v1-4")
    parser.add_argument('--save-path', default="CompVis/stable-diffusion-v1-4")
    args = parser.parse_args()

    pipeline = StableDiffusionPipeline.from_pretrained(
        args.model_id,
        use_auth_token=token,
    )

    os.makedirs(args.save_path, exist_ok=True)

    serialize_model(pipeline.text_encoder.eval(),
                    pipeline.text_encoder.config,
                    args.save_path,
                    "encoder")
    serialize_model(pipeline.vae.eval(), None, args.save_path, "vae")
    serialize_model(pipeline.unet.eval(), None, args.save_path, "unet")

    pipeline.tokenizer.save_pretrained(args.save_path)


if __name__ == "__main__":
    main()
