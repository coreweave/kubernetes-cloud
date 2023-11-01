import os
import time

import torch
from tensorizer import TensorSerializer, TensorDeserializer, stream_io
from tensorizer.utils import no_init_or_tensor, convert_bytes, get_mem_usage
from transformers import AutoModelForCausalLM
from transformers.models.mistral import MistralConfig
from vllm.model_executor.models.mistral import MistralForCausalLM
from vllm.model_executor.parallel_utils.parallel_state import \
    initialize_model_parallel

BUCKET = "tensorized"
MODEL_NAME = "mistral-7b-instruct-vllm"
S3_URI = f"s3://{BUCKET}/{MODEL_NAME}.tensors"

MODEL_REF = "mistralai/Mistral-7B-Instruct-v0.1"
MODEL_PATH = "/tmp/Mistral-7B-Instruct-v0.1"


def serialize():
    model = AutoModelForCausalLM.from_pretrained(MODEL_REF, device_map="auto",
                                                 torch_dtype="auto")
    model.save_pretrained(MODEL_PATH)

    torch.set_default_dtype(torch.bfloat16)
    mistral_config = MistralConfig()
    model = MistralForCausalLM(mistral_config)
    model.load_weights(MODEL_PATH)

    stream = stream_io.open_stream(S3_URI, "wb")
    serializer = TensorSerializer(stream)
    serializer.write_module(model)
    serializer.close()


def deserialize():
    mistral_config = MistralConfig()

    with no_init_or_tensor():
        model = MistralForCausalLM(mistral_config)
        model.to(torch.bfloat16)

    before_mem = get_mem_usage()
    # Lazy load the tensors from S3 into the model.
    start = time.time()
    stream = stream_io.open_stream(S3_URI, "rb")
    deserializer = TensorDeserializer(stream, plaid_mode=True)
    deserializer.load_into_module(model)
    end = time.time()

    # Brag about how fast we are.
    total_bytes_str = convert_bytes(deserializer.total_tensor_bytes)
    duration = end - start
    per_second = convert_bytes(deserializer.total_tensor_bytes / duration)
    after_mem = get_mem_usage()
    deserializer.close()
    print(
        f"Deserialized {total_bytes_str} in {end - start:0.2f}s, {per_second}/s")
    print(f"Memory usage before: {before_mem}")
    print(f"Memory usage after: {after_mem}")

    return model


if __name__ == "__main__":
    os.environ["MASTER_ADDR"] = "0.0.0.0"
    os.environ["MASTER_PORT"] = "8080"
    torch.distributed.init_process_group(world_size=1, rank=0)
    initialize_model_parallel()

    print("Serializing...")
    serialize()
    print("Testing a deserialization...")
    deserialize()
