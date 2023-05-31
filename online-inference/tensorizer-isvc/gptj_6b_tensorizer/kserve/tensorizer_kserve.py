import logging
import time
from typing import Dict

import kserve
import torch
from tensorizer import TensorDeserializer
from tensorizer.utils import convert_bytes, get_mem_usage, no_init_or_tensor
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "gptj"

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

        # Lazy load the tensors from PVC into the model.
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
        print(
            f"Deserialized {total_bytes_str} in {end - start:0.2f}s," f" {per_second}/s"
        )
        print(f"Memory usage before: {before_mem}")
        print(f"Memory usage after: {after_mem}")

        self.model.eval()
        torch.manual_seed(100)

        # Tokenize and generate
        self.tokenizer = AutoTokenizer.from_pretrained("/mnt/pvc/")
        self.eos = self.tokenizer.eos_token_id
        self.ready = True

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        if "text" in payload:
            input_ids = self.tokenizer.encode(payload["text"], return_tensors="pt").to(
                "cuda"
            )
        else:
            input_ids = self.tokenizer.encode(
                "Please input some text", return_tensors="pt"
            ).to("cuda")

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=50,
                do_sample=True,
                pad_token_id=self.eos,
            )

        print(f"tensor output IDs: {output_ids}")

        output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"tensor output: {output}")

        return output


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])