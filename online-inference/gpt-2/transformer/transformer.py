from .encoder import get_encoder
import json
import kfserving
from typing import List, Dict
import logging
import io

logging.basicConfig(level=kfserving.constants.KFSERVING_LOGLEVEL)

class Transformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.encoder = get_encoder()

    def preprocess(self, inputs: Dict) -> Dict:
        return {'signature_name':'predict','instances': [self.encoder.encode(instance) for instance in inputs['instances']]}

    def postprocess(self, inputs: List) -> List:
        return {'predictions': [self.encoder.decode(prediction) for prediction in inputs['predictions']]}
