---
description: Welcome to Machine Learning on CoreWeave Cloud
---

# Training

Training [Machine Learning](broken-reference) models, especially models of modern Deep Neural Networks, is at the center of CoreWeave Cloud's architecture. The entire CoreWeave Cloud stack is purpose-built to enable highly scalable, cost-efficient model training.

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4aa">💪</span> Our <a href="../../../coreweave-kubernetes/node-types.md"><strong>bare-metal nodes</strong></a> sport a wide range of <strong>NVIDIA GPUs</strong> to offer top-of-the-line <strong>intensive compute power</strong>.</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f310">🌐</span>The CoreWeave <a href="broken-reference">network stack</a> features <a href="../../coreweave-kubernetes/networking/hpc-interconnect.md"><strong>InfiniBand Interconnect</strong></a>, allowing for <strong>extremely fast, low-latency</strong> network connections.</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="26a1">⚡</span> <a href="../../storage/storage/"><strong>High-performance, network-attached storage</strong></a> loads and writes checkpoints at <strong>terabit speeds</strong> to our software control plane, enabling large distributed training jobs to be scaled up <strong>in seconds</strong>.</td><td></td><td></td></tr></tbody></table>

In addition to our core tech stack, CoreWeave has a history of supporting our customers with cutting-edge Machine Learning research through in-house expertise, industry partnerships, and contributions to research organizations. Our team has extensive experience in training large transformer architectures, optimizing [Hugging Face code](https://huggingface.co/), and selecting the right hardware for any given job.

{% hint style="success" %}
**Did You Know?**

CoreWeave partnered with the open source research collective [EleutherAI](https://www.eleuther.ai/) to develop and train the worlds largest open source NLP Model, [GPT-NeoX-20B](https://blog.eleuther.ai/announcing-20b/)!
{% endhint %}

## Machine Learning on CoreWeave

There are many ways to run Machine Learning tasks on CoreWeave, and, as is typical of the space, there are many methods to achieve the same result. These are the tools CoreWeave offers to achieve Machine Learning tasks:

### :desktop: [**Virtual Servers**](../../../virtual-servers/getting-started.md)

The most vanilla of our compute offerings. Virtual Machines are great for few-GPU experimentation in a familiar environment, but administrative and performance overheads make them less desirable for distributed tasks.

### :sailboat: [**Kubernetes**](../../coreweave-kubernetes/getting-started.md)

Our Kubernetes offering differs from most of the other leading cloud providers by offering a **fully managed cluster** with thousands of GPUs pre-populated. There is no need to worry about cluster scaling, or idle virtual machines incurring cost. You only pay for exactly what you use. Kubernetes access gives experienced MLOps teams the power to deploy their own stacks in a bare metal container environment. The Kubernetes environment fully supports massive distributed training on our NVIDIA A100 HGX clusters with RDMA GPUDirect InfiniBand.

### :brain: [**Determined.AI**](broken-reference)

A experiment-oriented MLOps platform featuring hyperparameter search. Determined.AI runs experiments in containers on CoreWeave Kubernetes, abstracting the DevOps portions via a simple CLI and UI. DeterminedAI can be deployed with a single click from the [CoreWeave application Catalog](https://apps.coreweave.com/). DeterminedAI is a great way to run large distributed training jobs with support for most popular frameworks.

### ****:squid: **** [**Argo Workflows**](kubeflow-training-operators/finetuning-machine-learning-models.md)

Our favorite workflow runner can easily be tasked to train or finetune a model and automatically deploy an [Inference endpoint](kubeflow-training-operators/finetuning-machine-learning-models.md#inference-endpoint) when finished.

### ****:person\_running: **** [**Training Operators**](broken-reference)

A Kubernetes-native way to run distributed training jobs. Supports Tensorflow, PyTorch Distributed and any MPI style framework such as DeepSpeed.

### ****:anchor: **Sunk: SLURM on Kubernetes**

SLURM is the incumbent job scheduler of the HPC world. Sunk, CoreWeave's implementation of SLURM on Kubernetes, allows you to leverage the resource management of Sunk on Kubernetes.

{% hint style="info" %}
**Note**

SLURM support is currently available for reserved instance customers only. Please [contact support](https://cloud.coreweave.com/contact) for more information.
{% endhint %}
