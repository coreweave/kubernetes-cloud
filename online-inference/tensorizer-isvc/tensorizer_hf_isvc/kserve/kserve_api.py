import logging
import os
from typing import Dict

import kserve
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

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        # Ensure that the request has the appropriate type to process
        assert type(payload) == Dict

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

        return {"output": output}


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])
