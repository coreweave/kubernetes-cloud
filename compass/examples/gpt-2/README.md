# TensorFlow - Open AI GPT-2

This example consists of multiple components to demonstrate serving as well as working with the [OpenAI GPT-2 text generation model](https://github.com/openai/gpt-2). The model is served up via a REST API, and can be queried over the Internet. To follow along, please clone the manifests from [GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/gpt-2).

```bash
$ curl -d '{"instances": ["That was easy"]}' http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-s3:predict
{"predictions": ["That was easy to say, what else would you do, what would you do, would you say to your daughter and say to her, 'Where is the work you're doing, where is the work you're working on, and how are you doing it?' and she was like, 'I'm not going to be here, I can't do it!' and she became, you know, frustrated. And I think there's a different type of anxiety. There's this self-pity that comes in, and that's also why they call their child a 'brilliant' child.\n\nShe was always saying that when she was a little girl, there was something really important to do. But she really doesn't go. She knows that whatever she does, when she's ready, she's going to go into any school or program and that she's going to do. And she really needs to do that, because it's just so much more exciting to her now.\n\nIt made her less able to put her mind at the 'solution' to her child's difficulties \u2013 even as she had more opportunities than I or anyone could ever do, and at a time when we were trying a lot of things to find the balance in the world. And I"]}
```

*   [Jupyter PVC](../../../docs/compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1/jupyter-pvc.md) (Start here and work your way down)

    A Jupyter notebook and a container serving it demonstrating packaging the model for serving and storing it to a [CoreWeave Storage](../../../docs/storage/storage.md#shared-filesystem).

    This notebook will be allocated a GPU and can be used for finetuning as well.
*   [PVC Model Serving](../../../docs/compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1/service-pvc.md)

    Serves the model exported from Jupyter from the storage volume.
* [Transformer](transformer.md)
* A simple transformer for encoding/decoding text. It is not necesary to build this yourself to try the examples, a public image is available in Docker Hub
*   [S3 Model Serving](../../../docs/compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1/service-s3.md) (alternative)

    Serves a model stored in Amazon S3, including a transformer to encode/decode inputs and outputs to clear text
