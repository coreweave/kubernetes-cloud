import os
import kserve
import logging
import torch
from typing import Dict
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(__name__)

options = {
    'MODEL_PATH': os.getenv('MODEL_PATH'),
    'MODEL_NAME': os.getenv('MODEL_NAME'),
}

default_params = {
    'MIN_LENGTH': int(os.getenv('MIN_LENGTH', 1)),
    'MAX_LENGTH': int(os.getenv('MAX_LENGTH', 100)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', 1.0)),
    'TOP_K': int(os.getenv('TOP_K', 50)),
    'TOP_P': float(os.getenv('TOP_P', 0.95)),
    'REPETITION_PENALTY': float(os.getenv('REPETITION_PENALTY', 1.0)),
    'NUM_RETURN_SEQUENCES': int(os.getenv('NUM_RETURN_SEQUENCES', 1)),
}

class Model(kserve.Model):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.model_name = name
        self.ready = False
    
    def load(self) -> None:
        logger.info(f'Loading model from {options["MODEL_PATH"]}')
        self.model = AutoModelForCausalLM.from_pretrained(options["MODEL_PATH"]).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(options["MODEL_PATH"])
        self.generator = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1,
        )
        self.ready = True

    def predict(self, request: Dict, headers: Dict) -> Dict:
        request_params = default_params.copy()

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
    with torch.no_grad():
        model.load()
        kserve.ModelServer().start([model])
