import logging
import time
from typing import Dict

import kserve
import torch
from transformers import AutoTokenizer, GPTJForCausalLM

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

        device = "cuda"
        start = time.time()
        self.model = GPTJForCausalLM.from_pretrained(
            "/mnt/pvc", torch_dtype=torch.float16
        ).to(device)
        print(f"Start time : {time.time() - start} seconds")
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        torch.manual_seed(100)
        self.eos = self.tokenizer.eos_token_id
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        if "text" in request:
            input_ids = self.tokenizer.encode(
                request["text"], return_tensors="pt"
            ).to("cuda")
        else:
            input_ids = self.tokenizer.encode(
                "Please input some text", return_tensors="pt"
            ).to("cuda")

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids, max_new_tokens=50, do_sample=True, pad_token_id=self.eos
            )

        print(f"tensor output IDs : {output_ids}")

        output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"tensor output : {output}")

        return output


if __name__ == "__main__":
    model = Model(name=MODEL_NAME)
    model.load()
    kserve.ModelServer().start([model])
