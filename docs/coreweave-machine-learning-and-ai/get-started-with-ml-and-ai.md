---
description: Learn what makes CoreWeave special for machine learning and AI applications
---

# Get Started with ML and AI

**Machine learning** is one of the most popular applications of CoreWeave Cloud's state-of-the-art, purpose-built infrastructure. Models are easily hosted on CoreWeave, and can be sourced from a range of storage backends including [S3-compatible object storage](../storage/object-storage.md), HTTP, or persistent [Storage Volumes](../storage/storage/#storage-volumes).

## CoreWeave infrastructure for ML and AI

### :desktop: [**Virtual Servers**](../../virtual-servers/getting-started.md)

Virtual Servers are the most "vanilla" of CoreWeave's compute offerings. Virtual Servers are great for experimentation using few GPUs from a familiar environment, however administrative and performance overheads make them less desirable for distributed tasks.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

### :sailboat: [**Kubernetes**](../coreweave-kubernetes/getting-started.md)

Our Kubernetes offering differs from most of the other leading cloud providers by offering a **fully managed cluster** with thousands of GPUs pre-populated. Kubernetes access gives experienced MLOps teams the power to deploy their own stacks in a bare metal container environment. The Kubernetes environment fully supports massive distributed training on our NVIDIA A100 HGX clusters with RDMA GPUDirect InfiniBand. Plus, there's no need to worry about cluster scaling or idle virtual machines incurring costs - charges are incurred only for what is actually used.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../coreweave-kubernetes/getting-started.md">getting-started.md</a></td></tr></tbody></table>

### :muscle: NVIDIA HGX H100

The **NVIDIA HGX H100** enables up to seven times more efficient high-performance computing (HPC) applications, up to nine times faster AI training on large models, and up to thirty times faster [AI inference](broken-reference) than the [NVIDIA HGX A100](../../coreweave-kubernetes/node-types.md).

This speed, combined with the lowest NVIDIA GPUDirect network latency in the market with [the NVIDIA Quantum-2 InfiniBand platform](../coreweave-kubernetes/networking/hpc-interconnect.md), reduces the training time of AI models to ["days or hours, instead of months."](https://cts.businesswire.com/ct/CT?id=smartlink\&url=https%3A%2F%2Fwww.forbes.com%2Fsites%2Fmoorinsights%2F2022%2F09%2F14%2Fnvidias-new-h100-gpu-smashes-artificial-intelligence-benchmarking-records%2F%3Fsh%3D14bccacae728\&esheet=52960519\&newsitemid=20221107005057\&lan=en-US\&anchor=%26%238220%3Bdays+or+hours+instead+of+months.%26%238221%3B\&index=4\&md5=1aca6283a20b6bb79597814bc4574be4) With AI permeating nearly every industry today, this speed and efficiency has never been more vital for HPC applications.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="nvidia-hgx-h100.md">nvidia-hgx-h100.md</a></td></tr></tbody></table>

### :anchor: **Sunk: SLURM on Kubernetes**

SLURM is the incumbent job scheduler of the HPC world. Sunk, CoreWeave's implementation of SLURM on Kubernetes, allows you to leverage the resource management of SLURM on Kubernetes.

{% hint style="info" %}
**Note**

SLURM support is currently available for reserved instance customers only. Please [contact support](https://cloud.coreweave.com/contact) for more information.
{% endhint %}

## Model training on CoreWeave

Training [Machine Learning](broken-reference) models, especially models of modern Deep Neural Networks, is at the center of CoreWeave Cloud's architecture. The entire CoreWeave Cloud stack is purpose-built to enable highly scalable, cost-efficient model training.

In addition to its core tech stack, CoreWeave has a history of supporting our customers with cutting-edge Machine Learning research through in-house expertise, industry partnerships, and contributions to research organizations. Our team has extensive experience in training large transformer architectures, optimizing [Hugging Face code](https://huggingface.co/), and selecting the right hardware for any given job.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="training/">training</a></td></tr></tbody></table>

## Inference on CoreWeave

**CoreWeave Cloud's inference engine** autoscales containers based on demand in order to to swiftly fulfill user requests, then scales down according to load so as to preserve GPU resources. Allocating new resources and scaling up new containers can be as fast as 15 seconds for the 6B GPT-J model.

Allocating new resources and scaling up a container can be **as fast as fifteen seconds** for the 6B GPT-J model. This quick autoscale allows for a significantly more responsive service than that of other Cloud providers.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="inference/">inference</a></td></tr></tbody></table>
