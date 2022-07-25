import os
import time
import re
import logging
import kserve
from typing import Dict

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

mem_map = {0: '71GIB', 1: '71GIB', 2: '71GIB', 3: '71GIB', 4: '71GIB'}

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
    'MAX_LENGTH': int(os.getenv('MAX_LENGTH', 40)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', 1.0)),
    'TOP_K': int(os.getenv('TOP_K', 50)),
    'TOP_P': float(os.getenv('TOP_P', 1.0)),
    'REPETITION_PENALTY': float(os.getenv('REPETITION_PENALTY', 1.0)),
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
        self.model = AutoModelForCausalLM.from_pretrained(options["MODEL_PATH"], device_map="auto", max_memory=mem_map, torch_dtype=torch.bfloat16, local_files_only=True)
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
   