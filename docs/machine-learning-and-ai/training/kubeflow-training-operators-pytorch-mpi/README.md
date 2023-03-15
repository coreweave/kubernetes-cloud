---
description: >-
  Easily run distributed training using PyTorch and MPI Operators with Kubeflow
  on CoreWeave Cloud
---

# Kubeflow Training Operators - PyTorch/MPI

The[ Kubeflow project](https://www.kubeflow.org/) is dedicated to making deployments of Machine Learning (ML) workflows on Kubernetes simple, portable, and scalable. The goal is not to recreate other services, but to provide a straightforward way to deploy best-of-breed open-source systems for ML to diverse infrastructures. Anywhere you are running Kubernetes, you should be able to run Kubeflow.

Below you will find a general introduction to distributed training and Kubeflow training operators. Links to numerous open source, end-to-end examples built to be run on CoreWeave can be found under [Examples](./#examples).

## Kubeflow Training Operators

CoreWeave Cloud supports running [Kubeflow Training Operators](https://www.kubeflow.org/docs/components/training/) to easily train your Machine Learning models across a variety of frameworks and backends. The diagram below shows some of the Training Operators that Kubeflow supports - the full list can be found in the [Kubeflow official documentation](https://www.kubeflow.org/docs/components/training/) as well as the [source code](https://github.com/kubeflow/training-operator).

<figure><img src="../../../.gitbook/assets/image (1) (1).png" alt="Kubeflow Training Operators support diagram"><figcaption><p>Kubeflow Training Operators</p></figcaption></figure>

It can be confusing at first, so it is important to understand the distinction between the different categories in this chart, and how it impacts the code.

### PyTorch Operator

The first operator used in this example is the [PyTorch operator](https://www.kubeflow.org/docs/components/training/pytorch/). As the name suggests, it uses PyTorch as the framework which includes packages like `torch.distributed` and `torch.nn.parallel`. For a more in depth explanation to distributed training with PyTorch see the [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist\_overview.html) documentation page.

### MPI Operator

Unlike the PyTorch operator, the [MPI Operator](https://www.kubeflow.org/docs/components/training/mpi/) is decoupled from underlying frameworks. It does this by leveraging a distributed deep learning training framework called [Horovod](https://horovod.ai/). Horovod supports many frameworks by implementing simple wrappers like its `DistributedOptimizer`. For a more in depth explanation, see the [Introduction to Kubeflow MPI Operator and Industry Adoption blog post](https://medium.com/kubeflow/introduction-to-kubeflow-mpi-operator-and-industry-adoption-296d5f2e6edc) that was created when the MPI Operator was originally released.&#x20;

## Frameworks

A "framework" is what is used to define your machine learning model. The most popular frameworks are [TensorFlow](https://www.tensorflow.org/) and [PyTorch](https://pytorch.org/), but Kubeflow also supports other frameworks such as [MXNet](https://mxnet.apache.org/versions/1.9.1/) and [XGBoost](https://xgboost.readthedocs.io/en/stable/).

## Distribution strategy

A "distribution strategy" is the package that used in code that handles distribution. This is the main distinction between the three operators in the chart above. The distribution strategy is often implemented as a wrapper for different parts of your framework, such as the model and optimizer.&#x20;

## Backend

The "Backend" is the library that is used to facilitate the communication between devices that is required by distributed training. You will often not need to deal with these backends directly as the distribution strategy implements the use of them for you. The [NVIDIA Collective Communication Library](https://developer.nvidia.com/nccl) (NCCL) is optimized for the NVIDIA GPUs and Networking in CoreWeave Cloud so that is what we will be using in this example.

## Data parallelism

The provided examples use models that are trained on very large datasets including [ImageNet](https://www.image-net.org/) and [The Pile](https://pile.eleuther.ai/). Utilizing parallelism techniques can greatly reduce the total training time.

One of these parallelism techniques is called "data parallelism". This involves running an instance of the model is running on every GPU. During training, each batch is split into "micro-batches," where every GPU gets a single micro batch. The gradient is averaged across all micro-batches, and every instance of the model is updated.

When scaling up distributed training using data parallelism, it is considered best practice to follow the "[Linear Scaling Rule](https://arxiv.org/abs/1706.02677)," as presented in the [Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour paper](https://arxiv.org/abs/1706.02677):

> When the minibatch size is multiplied by `k`, multiply the learning rate by `k`.

This means that if the total number of processes is doubled - which doubles the effective batch size - the learning rate should also be doubled. This prevents the accuracy from decreasing as the number of processes is scaled up while also matching the training curves when scaling up, meaning similar convergence rates in the same number of epochs.

{% hint style="info" %}
**Note**

In the language of the rule, "minibatch" refers to the entire batch that then gets split into micro-batches. &#x20;
{% endhint %}

## Examples

{% hint style="info" %}
**Note**

You might see the `launcher` pod fail a couple of times if the `worker` pod is still starting up. This is an expected race condition which often happens if the Docker image is already cached on the launcher machine, causing it to start up much more quickly. Once the `worker` pod is fully created, the launcher will be able to communicate with it via SSH.
{% endhint %}

{% hint style="warning" %}
**Important**

The names of MPIJobs are unique. An old job must be deleted before a new one can be created with the same name.
{% endhint %}

| Example title                                                                   | Description                                          |
| ------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [ResNet-50](train-resnet-50-with-imagenet.md)                                   | PyTorchJob and MPIJob to train ResNet-50 on ImageNet |
| [GPT-NeoX-20B](../argo-workflows/fine-tune-gpt-neox-20b-with-argo-workflows.md) | Argo Workflow to fine-tune GPT-NeoX-20B with MPIJob  |

