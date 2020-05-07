import kfserving
from typing import List, Dict
import logging
import requests
import numpy as np
import base64

# The signature name is defined at time of export, in signature_def_map supplied to builder
# Tensorflows default is serving_default
SERVING_SIGNATURE_NAME = 'serving_default'

logging.basicConfig(level=kfserving.constants.KFSERVING_LOGLEVEL)

class Transformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

        self.labels = requests.get(
            "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
        ).text.split("\n")


    # Accept input either in base64 format or as a url
    def encode(self, input):
        if 'b64' in input:
            b64 = input['b64']
        else:
            image = requests.get(input["url"]).content
            b64 = base64.b64encode(image).decode("utf-8")

        # Input name is defined when exporting the module
        # Tensorflow Serving decodes base64 encoded images when sent in an object with the b64 key.
        # https://towardsdatascience.com/serving-image-based-deep-learning-models-with-tensorflow-servings-restful-api-d365c16a7dc4
        return {"image_bytes": {"b64": b64 } }

    # Match up the most likely prediction to the labels
    def decode(self, prediction):
        return {
            'class': self.labels[np.argmax(prediction)],
            'score': max(prediction)
        }

    def preprocess(self, inputs: Dict) -> Dict:
        return {'signature_name': SERVING_SIGNATURE_NAME, 'instances': [self.encode(instance) for instance in inputs['instances']]}


    def postprocess(self, inputs: List) -> List:
        return {'predictions': [self.decode(prediction) for prediction in inputs['predictions']]}