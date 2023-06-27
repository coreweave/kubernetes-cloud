---
description: Welcome to Machine Learning on CoreWeave Cloud
---

# Model Training and Fine-tuning

Training [Machine Learning](broken-reference) models, especially models of modern Deep Neural Networks, is at the center of CoreWeave Cloud's architecture. The entire CoreWeave Cloud stack is purpose-built to enable highly scalable, cost-efficient model training.

* [**Bare-metal nodes**](../../../coreweave-kubernetes/node-types.md) sport a wide range of **NVIDIA GPUs** to offer top-of-the-line **intensive compute power**.
* The CoreWeave [network stack](broken-reference) features [**InfiniBand Interconnect**](../../coreweave-kubernetes/networking/hpc-interconnect.md), allowing for **extremely fast, low-latency** network connections.
* [**High-performance, network-attached storage**](../../storage/storage/) loads and writes checkpoints at **terabit speeds** to our software control plane, enabling large distributed training jobs to be scaled up **in seconds**.

In addition to its core tech stack, CoreWeave has a history of supporting our customers with cutting-edge Machine Learning research through in-house expertise, industry partnerships, and contributions to research organizations. Our team has extensive experience in training large transformer architectures, optimizing [Hugging Face code](https://huggingface.co/), and selecting the right hardware for any given job.

{% hint style="success" %}
**Did You Know?**

CoreWeave partnered with the open source research collective [EleutherAI](https://www.eleuther.ai/) to develop and train the worlds largest open source NLP Model, [GPT-NeoX-20B](https://blog.eleuther.ai/announcing-20b/)!
{% endhint %}

There are many ways to run Machine Learning tasks on CoreWeave, and, as is typical of the space, there are many methods to achieve the same result.

## Frameworks and tools

### :brain:[ **Determined AI**](determined-ai.md)

Determined AI is an experiment-oriented MLOps platform featuring hyperparameter search. Experiments are run in containers on CoreWeave Kubernetes, abstracting the DevOps portions via a simple CLI and UI, and can be deployed with a single click from the [CoreWeave Application Catalog](https://apps.coreweave.com/). Determined AI is a great way to run large distributed training jobs, with support for most popular frameworks.

### :squid: [**Argo Workflows**](../how-to-guides-and-tutorials/model-training-guides/fine-tuning/finetuning-machine-learning-models.md)

Our favorite workflow runner, Argo Workflows, can easily be tasked to train or fine-tune a model and automatically deploy an [Inference endpoint](../how-to-guides-and-tutorials/model-training-guides/fine-tuning/finetuning-machine-learning-models.md#inference-endpoint) when finished.

### :person\_running:[**Kubeflow Training Operators**](kubeflow-training-operators-pytorch-mpi.md)

Training Operators offer a Kubernetes-native way to run distributed training jobs. Supports Tensorflow, PyTorch Distributed and any MPI style framework such as DeepSpeed.
