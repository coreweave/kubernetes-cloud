import time

import torch
from flask import Flask, Response
from tensorizer import TensorDeserializer
from tensorizer.utils import convert_bytes, get_mem_usage, no_init_or_tensor
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer


class Transformer:
    def __init__(self):
        self.model_ref = "EleutherAI/gpt-j-6B"

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
    return 200


@app.route("/predict/<text>")
def predict(text):
    input_ids = llm.encode(text)
    output = llm.decode(input_ids)

    return Response(output, mimetype="text/plain", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
