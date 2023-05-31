import time

import torch
from flask import Flask
from transformers import AutoTokenizer, GPTJForCausalLM


class Transformer:
    def __init__(self):
        device = "cuda"
        start = time.time()
        self.model = GPTJForCausalLM.from_pretrained(
            "/mnt/pvc", torch_dtype=torch.float16
        ).to(device)
        print(f"Start time : {time.time() - start} seconds")
        
        self.model.eval()
        torch.manual_seed(100)
        
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        self.eos = self.tokenizer.eos_token_id

    # Accept input either in base64 format or as a url
    def encode(self, input):
        input_ids = self.tokenizer.encode(input, return_tensors="pt").to("cuda")

        return input_ids

    # Match up the most likely prediction to the labels
    def decode(self, input_ids):
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids, max_new_tokens=50, do_sample=True, pad_token_id=self.eos
            )

        print(f"tensor output IDs : {output_ids}")

        output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"tensor output : {output}")

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

    return output, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
