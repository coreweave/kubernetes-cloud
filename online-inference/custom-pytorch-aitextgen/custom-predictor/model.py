import kfserving
from typing import List, Dict

from aitextgen import aitextgen

class Model(kfserving.KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False

    def load(self):
        self.ai = aitextgen(tf_gpt2="1558M", to_gpu=True, to_fp16=True)
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        payload = request["text"]

        prediction = self.ai.generate_one(prompt=payload, max_length=request.get("length", 64))

        return { 'prediction': prediction }

if __name__ == "__main__":
    model = Model('aitextgen')
    model.load()
    kfserving.KFServer(workers=1).start([model])
