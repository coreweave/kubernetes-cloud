# Open AI GPT-2

This tutorial demonstrates deploying a few different components in order to serve an [OpenAI GPT-2 text generation model](https://github.com/openai/gpt-2) via REST API, which may be queried using the Internet.

### Example query

{% code overflow="wrap" %}
```bash
$ curl -XPOST -H '{"instances": ["That was easy"]}' http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-s3:predict
{"predictions": ["That was easy to say, what else would you do, what would you do, would you say to your daughter and say to her, 'Where is the work you're doing, where is the work you're working on, and how are you doing it?' and she was like, 'I'm not going to be here, I can't do it!' and she became, you know, frustrated. And I think there's a different type of anxiety. There's this self-pity that comes in, and that's also why they call their child a 'brilliant' child.\n\nShe was always saying that when she was a little girl, there was something really important to do. But she really doesn't go. She knows that whatever she does, when she's ready, she's going to go into any school or program and that she's going to do. And she really needs to do that, because it's just so much more exciting to her now.\n\nIt made her less able to put her mind at the 'solution' to her child's difficulties \u2013 even as she had more opportunities than I or anyone could ever do, and at a time when we were trying a lot of things to find the balance in the world. And I"]}
```
{% endcode %}

## Tutorial source code

To follow along, first clone the manifests from [GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/gpt-2).

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/gpt-2" %}

## Procedure

### Step 1: Deploy Jupyter notebook

[Create a containerized instance of Jupyter notebook](jupyter-pvc.md) to understand how the model is packaged for serving and for storing using [CoreWeave Storage](../../../../../storage/storage/#shared-filesystem). This notebook will be allocated a GPU, so it can be used for finetuning as well.

### Step 2: Serve the PVC model

[Serve the model](service-pvc.md) exported from Jupyter from the storage volume.

### Step 3: Deploy a simple transformer or serve a model from S3

[Deploy a simple transformer](transformer.md) for encoding and decoding text. (It is not necessary to build this yourself in order to try the examples; you may use the public image available in Docker Hub.)

OR

[Serve a model stored in Amazon S3](service-s3.md), including a transformer to encode and decode inputs and outputs to clear text.
