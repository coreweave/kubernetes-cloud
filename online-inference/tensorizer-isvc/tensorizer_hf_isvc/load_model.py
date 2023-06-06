import time

import torch
from tensorizer import TensorDeserializer
from tensorizer.utils import convert_bytes, get_mem_usage, no_init_or_tensor
from transformers import AutoConfig, AutoModelForCausalLM, GPTJForCausalLM

# GLOBALS

DEVICE = "cuda"

"""
Loads the model using Tensorizer or Huggingface.

params:
- model_load_type (str): Type of model load [Options: "tensorizer", "hf"]
"""


def load_model_based_on_type(
    model_load_type: str = "tensorizer", model_path: str = "/mnt/pvc"
):
    assert model_load_type == "hf" or model_load_type == "tensorizer"

    if model_load_type == "hf":
        start = time.time()
        model = GPTJForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16
        ).to(DEVICE)
        print(
            f"Start time for model load from HF: {time.time() - start} seconds"
        )

        return model

    model_ref = "EleutherAI/gpt-j-6B"
    config = AutoConfig.from_pretrained(model_ref)

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
        f"Deserialized {total_bytes_str} in {end - start:0.2f}s,"
        f" {per_second}/s"
    )
    print(f"Memory usage before: {before_mem}")
    print(f"Memory usage after: {after_mem}")

    return model
