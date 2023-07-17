---
description: >-
  Get extremely fast model loads from HTTP/HTTPS and S3 endpoints with CoreWeave
  Tensorizer
---

# Tensorizer

[CoreWeave's Tensorizer](https://github.com/coreweave/tensorizer/) is a module, model, and tensor serializer and deserializer that makes it possible to load models **in less than five seconds**, making it easier, more flexible, and more cost-efficient to serve models at scale.

{% hint style="success" %}
**Did You Know?**

Compared to Hugging Face:

* Tensorizer's latency per request is more than five times faster.
* Tensorizer containers spin up faster, requiring fewer Pods to serve more requests.
* Tensorizor uses significantly less RAM for “lazy loading.”

To learn more, see [Decrease PyTorch Model Load Times with CoreWeave’s Tensorizer](https://coreweave.com/blog/coreweaves-tensorizer-decrease-pytorch-model-load-times).
{% endhint %}

## Features

### :chart\_with\_upwards\_trend: Reduction in resource usage

Because transfers occur nearly instantly to the GPU when using Tensorizer, the amount of CPU and RAM necessary for the instance is also reduced, resulting in lower incurred costs by a reduction in the amount of resources used.

### :thumbsup: S3-compatible

Tensorizer serializes models and their associated tensors into a single file, which can then be loaded quickly and efficiently from an HTTP/HTTPS or S3 endpoint. Serialized models may also be stored in [CoreWeave's S3-compatible Object Storage](../how-to-guides-and-tutorials/examples/tensorflow-guides/gpt-2/service-s3.md), enabling model streams directly from S3 into the container without having to download the model to the container's local filesystem.

### :zap: Extremely fast model loading speeds

By avoiding embedding the model in the container image, the container image size is greatly reduced; thus, so is the time it takes to load the model. This is especially important for models that are already large, such as [EleutherAI/gpt-neox-20B](https://huggingface.co/EleutherAI/gpt-neox-20B), which weighs in at `~40GB`.

### :pencil2: Flexible iteration

By decoupling the model from the container image, model updates do not require having to rebuild container images, which allows for quick iterations on the model itself, as well as the ability to deploy new versions without having to wait for the container image to build, or for the container image cache to be populated.

{% hint style="success" %}
**Tip**

The same is true with regards to HTTP/HTTPS endpoints, as S3 is really just another HTTP/HTTPS endpoint.
{% endhint %}

### :house\_with\_garden: **Local filesystem support**

Tensorizer also has support for loading models from a local filesystem, so it can be used to serialize models locally and load them locally. This option provides extremely fast load times, as the same principles that make it fast for HTTP/HTTPS and S3 endpoints also apply to local filesystems.

## Pre-Tensorized models on CoreWeave

Several pre-Tensorized models are available on the CoreWeave Cloud for free, and can be used with the `TensorDeserializer` class. Object Storage support defaults to the `accel-object.ord1.coreweave.com` endpoint, and the bucket to use `tensorized`.

{% hint style="info" %}
**Additional Resources**

Read more about [CoreWeave Object Storage endpoints](../../storage/object-storage.md).
{% endhint %}

See all available pre-Tensorized models in the source code GitHub repository's `README` file:

{% embed url="https://github.com/coreweave/tensorizer/#available-pre-tensorized-models-on-the-coreweave-cloud" %}

## Benchmarks

Currently, two benchmarks are available for Tensorizer.

### Real world impact benchmark

The real world impact benchmark sets up two inference services, one which uses Tensorizer to load the model, and one which does not. Then, with both services sitting idle with `1` GPU, they are each hit with `100` concurrent requests. Metrics on average response time and autoscaling capabilities were extracted for comparison.

This benchmark may be replicated by following [the real world impact benchmark tutorial](../how-to-guides-and-tutorials/examples/tensorizer-benchmarks-and-examples/real-world-impact-benchmark.md).

### Comparison benchmark

The comparison benchmark measures raw model load time from a PVC across vanilla Hugging Face, Safetensors, and Tensorizer, for comparison between all three. This comparison is much like a lab test for performance measuring.

The code for this benchmark may be viewed on CoreWeave's GitHub.

{% embed url="https://github.com/coreweave/tensorizer/tree/main/examples/benchmark" %}

## Learn more

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> View the Tensorizer source code</td><td></td><td></td><td><a href="https://github.com/coreweave/tensorizer/">https://github.com/coreweave/tensorizer/</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f9e0">🧠</span> View Tensorizer code examples</td><td></td><td></td><td><a href="https://github.com/coreweave/tensorizer/tree/main/examples">https://github.com/coreweave/tensorizer/tree/main/examples</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4da">📚</span> Read more about Tensorizer usage</td><td></td><td></td><td><a href="https://github.com/coreweave/tensorizer/#basic-usage">https://github.com/coreweave/tensorizer/#basic-usage</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f389">🎉</span> View available pre-Tensorized models</td><td></td><td></td><td><a href="https://github.com/coreweave/tensorizer/#available-pre-tensorized-models-on-the-coreweave-cloud">https://github.com/coreweave/tensorizer/#available-pre-tensorized-models-on-the-coreweave-cloud</a></td></tr></tbody></table>

## How-to guides and tutorials

For how-to guides and tutorials using Tensorizer including benchmark examples, see [Tensorizer Benchmarks and Examples](../how-to-guides-and-tutorials/examples/tensorizer-benchmarks-and-examples/).
