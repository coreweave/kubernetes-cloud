import os
import logging
import time
import re
import kserve
from typing import Dict

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

#dev_map = {'transformer.word_embeddings': 0, 'lm_head': 0, 'transformer.word_embeddings_layernorm': 0, 'transformer.h.0': 0, 'transformer.h.1': 0, 'transformer.h.2': 0, 'transformer.h.3': 0, 'transformer.h.4': 0, 'transformer.h.5': 1, 'transformer.h.6': 1, 'transformer.h.7': 1, 'transformer.h.8': 1, 'transformer.h.9': 1, 'transformer.h.10': 1, 'transformer.h.11': 1, 'transformer.h.12': 1, 'transformer.h.13': 1, 'transformer.h.14': 2, 'transformer.h.15': 2, 'transformer.h.16': 2, 'transformer.h.17': 2, 'transformer.h.18': 2, 'transformer.h.19': 2, 'transformer.h.20': 2, 'transformer.h.21': 2, 'transformer.h.22': 2, 'transformer.h.23': 3, 'transformer.h.24': 3, 'transformer.h.25': 3, 'transformer.h.26': 3, 'transformer.h.27': 3, 'transformer.h.28': 3, 'transformer.h.29': 3, 'transformer.h.30': 3, 'transformer.h.31': 3, 'transformer.h.32': 4, 'transformer.h.33': 4, 'transformer.h.34': 4, 'transformer.h.35': 4, 'transformer.h.36': 4, 'transformer.h.37': 4, 'transformer.h.38': 4, 'transformer.h.39': 4, 'transformer.h.40': 4, 'transformer.h.41': 5, 'transformer.h.42': 5, 'transformer.h.43': 5, 'transformer.h.44': 5, 'transformer.h.45': 5, 'transformer.h.46': 5, 'transformer.h.47': 5, 'transformer.h.48': 5, 'transformer.h.49': 5, 'transformer.h.50': 6, 'transformer.h.51': 6, 'transformer.h.52': 6, 'transformer.h.53': 6, 'transformer.h.54': 6, 'transformer.h.55': 6, 'transformer.h.56': 6, 'transformer.h.57': 6, 'transformer.h.58': 7, 'transformer.h.59': 7, 'transformer.h.60': 7, 'transformer.h.61': 7, 'transformer.h.62': 7, 'transformer.h.63': 7, 'transformer.h.64': 7, 'transformer.h.65': 7, 'transformer.h.66': 7, 'transformer.h.67': 0, 'transformer.h.68': 3, 'transformer.h.69': 5, 'transformer.ln_f': 7}

model_id = os.getenv('MODEL_ID', "bigscience/bloom")

options = {
    'MODEL_PATH': os.getenv('MODEL_PATH', "/mnt/pvc/bloom"),
    'MODEL_NAME': re.sub(r'[^\w-]', '-', model_id).lower(),
    'MODEL_TYPE': os.getenv('MODEL_TYPE', 'text-generation'),
    #'DEVICE_MAP': os.getenv('DEVICE_MAP', "auto"),
    'MODEL_DOWNLOAD_TIMEOUT': int(os.getenv('MODEL_DOWNLOAD_TIMEOUT', 300))
}

model_params = {
    'MIN_LENGTH': int(os.getenv('MIN_LENGTH', 1)),
    'MAX_LENGTH': int(os.getenv('MAX_LENGTH', 250)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', 0.5)),
    'TOP_K': int(os.getenv('TOP_K', 5)),
    'TOP_P': float(os.getenv('TOP_P', 0.5)),
    'REPETITION_PENALTY': float(os.getenv('REPETITION_PENALTY', 0.125)),
}

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(options['MODEL_NAME'])

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
        self.model = AutoModelForCausalLM.from_pretrained(options["MODEL_PATH"], device_map="auto", torch_dtype=torch.bfloat16, local_files_only=True)
        self.model.bfloat16().eval()
        self.tokenizer = AutoTokenizer.from_pretrained(options["MODEL_PATH"], local_files_only=True)
        self.generator = pipeline(
            options['MODEL_TYPE'],
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
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
            #do_sample=True,
            min_length=request_params['MIN_LENGTH'],
            max_length=request_params['MAX_LENGTH'],
            temperature=request_params['TEMPERATURE'],
            top_k=request_params['TOP_K'],
            top_p=request_params['TOP_P'],
            repetition_penalty=request_params['REPETITION_PENALTY']
        )}

    @staticmethod
    def is_ready():
        ready_path = os.path.join(options['MODEL_PATH'], '.ready.txt')
        logger.info(f'Waiting for download to be ready ...')
        interval_time = 10
        intervals = options['MODEL_DOWNLOAD_TIMEOUT'] // interval_time
        for i in range(intervals):
            time.sleep(interval_time)
            if os.path.exists(ready_path):
                logger.info('Download ready')
                return
        raise Exception(f'Download timeout {interval_time * intervals}!')

if __name__ == '__main__':
    Model.is_ready()
    with torch.no_grad():
        model = Model(options['MODEL_NAME'])
        model.load()
        kserve.ModelServer().start([model])
   