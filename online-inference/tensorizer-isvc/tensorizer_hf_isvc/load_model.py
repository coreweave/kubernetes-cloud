import time
from typing import Literal

import torch
from tensorizer import TensorDeserializer
from tensorizer.utils import convert_bytes, get_mem_usage, no_init_or_tensor
from transformers import AutoConfig, AutoModelForCausalLM, GPTJForCausalLM

DEVICE = "cuda"


def load_model_based_on_type(
    model_load_type: Literal["tensorizer", "hf"] = "tensorizer",
    model_path: str = "/mnt/pvc",
):
    """
    Loads the model using Tensorizer or HuggingFace.

    Args:
        model_load_type: Method to load the model [Options: "tensorizer", "hf"]
        model_path: Path to the model files
    """
    if model_load_type not in ("tensorizer", "hf"):
        raise ValueError(
            'model_load_type must be either "tensorizer" or "hf";'
            f" got {model_load_type}"
        )

    if model_load_type == "hf":
        start = time.time()
        model = GPTJForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16
        ).to(DEVICE)
        duration = time.time() - start
        print(
            f"Deserialized model in {duration:0.2f}s"
            " using HuggingFace Transformers"
        )

        return model

    # If the config file were not pre-downloaded along with the HuggingFace
    # model as in this example, this could use a HuggingFace model reference
    # instead of a path for a small download of just the relevant config file.
    # model_ref = "EleutherAI/gpt-j-6B"
    config = AutoConfig.from_pretrained(model_path)

    # This ensures that the model is not initialized.
    with no_init_or_tensor():
        model = AutoModelForCausalLM.from_config(config)

    before_mem = get_mem_usage()

    # Lazy load the tensors from PVC into the model.
    start = time.time()
    deserializer = TensorDeserializer(
        f"{model_path}/gptj.tensors", plaid_mode=True
    )
    deserializer.load_into_module(model)
    end = time.time()

    # Brag about how fast we are.
    total_bytes_str = convert_bytes(deserializer.total_tensor_bytes)
    duration = end - start
    per_second = convert_bytes(deserializer.total_tensor_bytes / duration)
    after_mem = get_mem_usage()
    deserializer.close()
    print(
        f"Deserialized {total_bytes_str} in {duration:0.2f}s, {per_second}/s"
        " using Tensorizer"
    )
    print(f"Memory usage before: {before_mem}")
    print(f"Memory usage after: {after_mem}")

    return model
