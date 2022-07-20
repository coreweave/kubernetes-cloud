import os
import re
import kserve
from typing import Dict

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

model_id = os.getenv('MODEL_NAME', "bigscience/bloom")
options = {
    'MODEL_ID': model_id,
    'MODEL_NAME': re.sub(r'[^\w-]', '-', model_id).lower(),
    'MODEL_TYPE': os.getenv('MODEL_TYPE', 'text-generation'),
    'DEVICE_MAP': os.getenv('DEVICE_MAP', "auto"),
}

model_params = {
    'MIN_LENGTH': int(os.getenv('MIN_LENGTH', -2)),
    'MAX_LENGTH': int(os.getenv('MAX_LENGTH', -2)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', -2)),
    'TOP_K': int(os.getenv('TOP_K', -2)),
    'TOP_P': float(os.getenv('TOP_P', -2)),
    'REPETITION_PENALTY': float(os.getenv('REPETITION_PENALTY', 0.125)),
}

class Model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.model_name = options['MODEL_NAME']

    def load(self):
        self.model = AutoModelForCausalLM.from_pretrained(options["MODEL_ID"], device_map=options["DEVICE_MAP"], torch_dtype=torch.bfloat16)
        self.tokenizer = AutoTokenizer.from_pretrained(options["MODEL_ID"])
        self.generator = pipeline(
            options['MODEL_TYPE'],
            model=self.model,
            tokenizer=self.tokenizer,
            device_map=options['DEVICE_MAP'],
        )
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        request_params = model_params.copy()

        if 'parameters' in request:
            parameters = request['parameters']
            for k, pv in parameters.items():
                pk = k.upper()
                if pk in request_params:
                    logger.debug(f'Parameter {pk} changed from {request_params[pk]} to {pv}')
                    request_params[pk] = pv

        return {'predictions': self.generator(
            request['instances'],
            do_sample=True,
            min_length=request_params['MIN_LENGTH'],
            max_length=request_params['MAX_LENGTH'],
            temperature=request_params['TEMPERATURE'],
            top_k=request_params['TOP_K'],
            top_p=request_params['TOP_P'],
            repetition_penalty=request_params['REPETITION_PENALTY'],
        )}

if __name__ == '__main__':
    model = Model(options['MODEL_NAME'])
    model.load()
    kserve.ModelServer().start([model])
    