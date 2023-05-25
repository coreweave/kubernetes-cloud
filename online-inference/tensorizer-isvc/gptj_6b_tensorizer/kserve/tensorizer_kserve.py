import kserve
import logging
import os
import time
from typing import Dict
from argparse import ArgumentParser
from io import BytesIO

import torch

from tensorizer import TensorDeserializer
from tensorizer.stream_io import open_stream
from tensorizer.utils import no_init_or_tensor, convert_bytes, get_mem_usage
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig

MODEL_NAME="gptj"

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(MODEL_NAME)
logger.info(f"Model Name: {MODEL_NAME}")


class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.model_name = name
        self.model_ref = "EleutherAI/gpt-j-6B"

    def load(self):
        logger.info(f"Loading {MODEL_NAME}")
    
        config = AutoConfig.from_pretrained(self.model_ref)

        # This ensures that the model is not initialized.
        with no_init_or_tensor():
            self.model = AutoModelForCausalLM.from_config(config)

        before_mem = get_mem_usage()

        # Lazy load the tensors from S3 into the model.
        start = time.time()
        deserializer = TensorDeserializer("/mnt/pvc/gptj.tensors", plaid_mode=True)
        deserializer.load_into_module(self.model)
        end = time.time()

        # Brag about how fast we are.
        total_bytes_str = convert_bytes(deserializer.total_tensor_bytes)
        duration = end - start
        per_second = convert_bytes(deserializer.total_tensor_bytes / duration)
        after_mem = get_mem_usage()
        deserializer.close()
        print(f"Deserialized {total_bytes_str} in {end - start:0.2f}s, {per_second}/s")
        print(f"Memory usage before: {before_mem}")
        print(f"Memory usage after: {after_mem}")

        # Tokenize and generate
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_ref)

        self.ready = True

    def predict(self) -> Dict:
        if "text" in request:
            input_ids = self.tokenizer.encode(
                request["text"], return_tensors="pt"
            ).to("cuda")
        else:
            input_ids = self.tokenizer.encode(
                "Please input some text", return_tensors="pt"
            ).to("cuda")

        eos = self.tokenizer.eos_token_id
        
        output_ids = self.model.generate(
        input_ids, max_new_tokens=50, do_sample=True, pad_token_id=eos
        )

        print(f"tensor output IDS : {output_ids}")

        output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"tensor output : {output}")

        return output


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])
