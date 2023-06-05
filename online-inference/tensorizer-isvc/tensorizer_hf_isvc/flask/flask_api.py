import os

import torch
from flask import Flask, Response
from load_model import load_model_based_on_type
from transformers import AutoTokenizer

MODEL_LOAD_TYPE = os.getenv("MODEL_LOAD_TYPE")


class Transformer:
    def __init__(self):
        self.model = load_model_based_on_type(model_load_type=MODEL_LOAD_TYPE)

        self.model.eval()
        torch.manual_seed(100)

        self.tokenizer = AutoTokenizer.from_pretrained("/mnt/pvc")
        self.eos = self.tokenizer.eos_token_id

    def encode(self, input):
        input_ids = self.tokenizer.encode(input, return_tensors="pt").to("cuda")

        return input_ids

    # Match up the most likely prediction to the labels
    def decode(self, input_ids):
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


llm = Transformer()
app = Flask(__name__)


@app.route("/")
def index():
    return Response(status=200)


@app.route("/predict/<text>")
def predict(text):
    input_ids = llm.encode(text)
    output = llm.decode(input_ids)

    return Response(output, mimetype="text/plain", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
