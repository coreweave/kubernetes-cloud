# Transformer

### Introduction

A Machine Learning model takes tensors as inputs and outputs. Often you will want to submit and receive data in other formats, such as text or images. A transformer can be used to encode/decode the data as part of the Inference Service. Additional Transformer examples can be found in the [KFServe Documentation](https://github.com/kubeflow/kfserving/tree/master/docs/samples/transformer/image\_transformer).

The transformer in this repository encodes text for the GPT-2 model. You can use it without building by referencing [pre-build images in Docker Hub](https://hub.docker.com/repository/docker/coreweave/gpt-transformer).

## Modifying

The transformation logic is implemnted in `transformer.py`. `preprocess` is called on data before it is sent to model and `postprocess` on the result. In the GPT-2 example, the model is saved with signature name predict. This is added via the transformer for correct querying.

```python
class Transformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.encoder = get_encoder()

    def preprocess(self, inputs: Dict) -> Dict:
        print (inputs)
        return {'signature_name':'predict','instances': [self.encoder.encode(instance) for instance in inputs['instances']]}

    def postprocess(self, inputs: List) -> List:
        return {'predictions': [self.encoder.decode(prediction) for prediction in inputs['predictions']]}
```

### Building

When making modifications you can easily build and upload your own version of the image to [Docker Hub](http://hub.docker.com).

```bash
docker build -t dockerHubAccountName/imagename:0.1 .
docker push dockerHubAccountName/imagename:0.1
```
