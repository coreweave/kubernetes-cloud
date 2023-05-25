from typing import List, Dict
import logging
import requests
import numpy as np
import base64
import time
import torch
from flask import Flask
from tensorizer import TensorDeserializer
from tensorizer.stream_io import open_stream
from tensorizer.utils import no_init_or_tensor, convert_bytes, get_mem_usage
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig

# The signature name is defined at time of export, in signature_def_map supplied to builder
# Tensorflows default is serving_default

class Transformer(object):
    def __init__(self):
        self.model_ref = "EleutherAI/gpt-j-6B"
        
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


    # Accept input either in base64 format or as a url
    def encode(self, input):
        input_ids = self.tokenizer.encode(
            input, return_tensors="pt"
        ).to("cuda")
            
        return input_ids

    # Match up the most likely prediction to the labels
    def decode(self, input_ids):
        eos = self.tokenizer.eos_token_id
        
        output_ids = self.model.generate(
        input_ids, max_new_tokens=50, do_sample=True, pad_token_id=eos
        )

        print(f"tensor output IDS : {output_ids}")

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

    print(f"Output for {text} : {output}")

    return output, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)