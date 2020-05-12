import kfserving
from typing import List, Dict

from fastai.text import load_learner

class Model(kfserving.KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False

    def load(self):
        self.model = load_learner("/mnt/models")
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        # Request and response follows the Tensorflow V1 HTTP API,
        # but does not have to.
        # No batching, grab the first instance only
        payload = request["instances"][0]

        predictions = self.model.predict(payload)
        prediction = predictions[0].obj

        return { 'predictions': [prediction] }

if __name__ == "__main__":
    model = Model('sentiment')
    model.load()
    kfserving.KFServer(workers=1).start([model])
