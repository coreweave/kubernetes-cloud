### Introduction

This example consists of multiple components to demonstrate serving as well as working with the [OpenAI GPT-2 text generation model](https://github.com/openai/gpt-2). The model is served up via a REST API, and can be queried over the Internet
```bash
$ curl -d '{"instances": ["That was easy"]}' http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-s3:predict
{"predictions": ["That was easy to say, what else would you do, what would you do, would you say to your daughter and say to her, 'Where is the work you're doing, where is the work you're working on, and how are you doing it?' and she was like, 'I'm not going to be here, I can't do it!' and she became, you know, frustrated. And I think there's a different type of anxiety. There's this self-pity that comes in, and that's also why they call their child a 'brilliant' child.\n\nShe was always saying that when she was a little girl, there was something really important to do. But she really doesn't go. She knows that whatever she does, when she's ready, she's going to go into any school or program and that she's going to do. And she really needs to do that, because it's just so much more exciting to her now.\n\nIt made her less able to put her mind at the 'solution' to her child's difficulties \u2013 even as she had more opportunities than I or anyone could ever do, and at a time when we were trying a lot of things to find the balance in the world. And I"]}
```

- [S3 Model Serving](./service-s3) (Start Here)  
Serves a model stored in Amazon S3, including a transformer to encode/decode inputs and outputs to clear text
- [Transformer](./transformer)  
A simple transformer for encoding/decoding text. It is not necesary to build this yourself to try the examples, a public image is available in Docker Hub
- [Jupyter PVC](./jupyter-pvc)  
A Jupyter notebook and a container serving it demonstrating packaging the model for serving and storing it to a CoreWeave `ReadWriteMany` [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)