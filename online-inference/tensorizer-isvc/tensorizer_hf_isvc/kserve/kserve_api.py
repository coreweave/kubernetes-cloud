import logging
import os
from typing import Dict

import kserve
import kserve.errors
import torch
from load_model import load_model_based_on_type
from transformers import AutoTokenizer

MODEL_NAME = "gptj"
MODEL_LOAD_TYPE = os.getenv("MODEL_LOAD_TYPE")

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(MODEL_NAME)
logger.info(f"Model Name: {MODEL_NAME}")


class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.model = None
        self.tokenizer = None
        self.eos = None
        self.ready = False

    def load(self):
        logger.info(f"Loading {MODEL_NAME}")

        self.model = load_model_based_on_type(model_load_type=MODEL_LOAD_TYPE)

        self.model.eval()
        torch.manual_seed(100)

        self.tokenizer = AutoTokenizer.from_pretrained("/mnt/pvc/tokenizer")
        self.eos = self.tokenizer.eos_token_id

        self.ready = True

    def validate(self, payload: Dict):
        # Ensure that the request has the appropriate type to process
        if not isinstance(payload, Dict):
            raise kserve.errors.InvalidInput("Expected payload to be a dict")
        return super().validate(payload)

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        inputs = payload.get("instances") or ["Please input some text"]
        outputs = []
        for text in inputs:
            input_ids = self.tokenizer.encode(text, return_tensors="pt").to(
                "cuda"
            )

            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids,
                    max_new_tokens=50,
                    do_sample=True,
                    pad_token_id=self.eos,
                )

            print(f"tensor output IDs: {output_ids}")

            output = self.tokenizer.decode(
                output_ids[0], skip_special_tokens=True
            )
            outputs.append(output)

            print(f"tensor output: {output}")

        return {"predictions": outputs}


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])
