---
description: Feature Updates and Release Notes for CoreWeave Cloud
---

# Release Notes

## December 2022 :snowflake:

New on CoreWeave Cloud this month:

### Welcome NVIDIA HGX H100s to the CoreWeave fleet! :muscle:

CoreWeave's infrastructure has always been purpose-built for large-scale GPU-accelerated workloads. Since the beginning, CoreWeave Cloud has been specialized to serve the most demanding AI and machine learning applications. So it only makes sense that CoreWeave will soon be **one of the only Cloud platforms in the world offering** [**NVIDIA's most powerful end-to-end AI supercomputing platform**](https://www.nvidia.com/en-us/data-center/hgx/)**.**

**NVIDIA HGX H100s** enable...

* **seven times more efficient** high-performance computing (HPC) applications,
* up to **nine times faster AI training** on large models,
* and up to **thirty times faster** [**AI inference**](broken-reference) than the [NVIDIA HGX A100](../coreweave-kubernetes/node-types.md)!

This speed, combined with the lowest NVIDIA GPUDirect network latency in the market with [the NVIDIA Quantum-2 InfiniBand platform](coreweave-kubernetes/networking/hpc-interconnect.md), reduces the training time of AI models to ["days or hours, instead of months."](https://cts.businesswire.com/ct/CT?id=smartlink\&url=https%3A%2F%2Fwww.forbes.com%2Fsites%2Fmoorinsights%2F2022%2F09%2F14%2Fnvidias-new-h100-gpu-smashes-artificial-intelligence-benchmarking-records%2F%3Fsh%3D14bccacae728\&esheet=52960519\&newsitemid=20221107005057\&lan=en-US\&anchor=%26%238220%3Bdays+or+hours+instead+of+months.%26%238221%3B\&index=4\&md5=1aca6283a20b6bb79597814bc4574be4)

**HGX H100s will be available in Q1 of 2023!**

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>➡️ <strong>Learn more and make a reservation for an HGX H100!</strong></td><td><a href="compass/nvidia-hgx-h100.md">nvidia-hgx-h100.md</a></td></tr></tbody></table>

### Launch GPT DeepSpeed Models using DeterminedAI :brain:

DeepSpeed is an [open source](https://en.wikipedia.org/wiki/Open\_source) [deep learning](https://en.wikipedia.org/wiki/Deep\_learning) optimization library for [PyTorch](https://en.wikipedia.org/wiki/PyTorch), designed for low latency and high throughput training while reducing compute power and memory use for the purpose of training large distributed models.

In our new walkthrough, a minimal GPT-NeoX DeepSpeed distributed training job is launched without the additional features such as tracking, metrics, and visualization that DeterminedAI offers.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td> ➡️ <strong>Launch GPT DeepSpeed models using DeterminedAI now!</strong></td><td><a href="compass/determined-ai/launch-gpt-deepspeed-models-using-determinedai.md">launch-gpt-deepspeed-models-using-determinedai.md</a></td></tr></tbody></table>

### Multi-namespace support :ferris\_wheel:

CoreWeave Cloud now **supports multiple namespaces for organizations!**

[Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) provide logical separations of resources within a [Kubernetes cluster](https://kubernetes.io/docs/concepts/architecture/). While it is typical for CoreWeave client resources to be run inside a single namespace, there are sometimes cases in which more than one namespace within the same organization is required.

CoreWeave Cloud now supports multiple namespaces for organizations, **enabled by default!**

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>➡️ Learn more about multi-namespace support!</strong></td><td><a href="cloud-account-management/namespace-management.md">namespace-management.md</a></td></tr></tbody></table>

### Accelerated Object Storage:zap:

**Accelerated Object Storage** provides local caching for frequently accessed objects across all CoreWeave data centers. Accelerated Object Storage is especially useful for large scale, multi-region rendering, or for inference auto-scaling where the same data needs to be loaded by hundreds or even thousands of compute nodes.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>➡️ Learn more about accelerated Object Storage!</strong></td><td><a href="storage/object-storage.md#accelerated-object-storage">#accelerated-object-storage</a></td></tr></tbody></table>

{% hint style="success" %}
**Import Disk Images from CoreWeave Object Storage**

Did you know you can import your own Virtual Disk Images for Virtual Servers right from CoreWeave Object Storage? With the help of [our new guide](virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md#using-coreweave-object-storage), you can learn how to do just that!
{% endhint %}

### Introducing CoreWeave CoSchedulers :stopwatch:

In Machine Learning, it is often necessary for all pieces of a project to begin at the same time. In the context of Kubernetes, this means that all Pods must be deployed at the same time.

With **CoreWeave CoSchedulers**, you can ensure that your Pods are all deployed at once, and that deployments only occur if required resources are already available, thereby eliminating the possibility of partial deployments!

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>➡️ Learn more about the CoreWeave CoSchedulers!</strong></td><td><a href="coreweave-kubernetes/coschedulers.md">coschedulers.md</a></td></tr></tbody></table>

##

## September 2022 :maple\_leaf:

New on CoreWeave Cloud this month:

### Self-serve signup for CoreWeave Cloud :writing\_hand:

[Signing up for an account on CoreWeave Cloud](https://cloud.coreweave.com/signup) is now easier than ever! With self-serve signup, you can create your own account without additional approval.

{% hint style="info" %}
**Note**

Some features are only available through an upgrade request. To increase your quota, or access Kubernetes, log in to your CoreWeave account and navigate to **Upgrade Quotas.**
{% endhint %}

### NVIDIA A100 80GB NVLINK with InfiniBand and SHARP:zap:

<figure><img src=".gitbook/assets/image (3) (1).png" alt="NVIDIA Mellanox Quantum leaf switches in the CoreWeave LAS1 datacenter"><figcaption><p>NVIDIA Mellanox Quantum leaf switches in the CoreWeave LAS1 datacenter</p></figcaption></figure>

**A100 80GB NVLINK SXM4** GPUs are now available in the **LAS1** region. These GPUs are provisioned in large clusters, intended for distributed training and inference of LLMs such as [BLOOM 176B](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1.md#what-is-bloom).

Connectivity between compute hardware, as well as storage, plays a major role in overall system performance for applications of Neural Net Training, Rendering, and Simulation. Certain workloads, such as those used for training massive language models of over 100 billion parameters over hundreds or thousands of GPUs, require the fastest, lowest-latency interconnect.

CoreWeave provides highly optimized IP-over-Ethernet connectivity across all GPUs, and an industry-leading, non-blocking [InfiniBand fabric](https://docs.coreweave.com/networking/hpc-interconnect#hpc-over-rdma-infiniband) for our top-of-the-line A100 NVLINK GPU fleet. CoreWeave has partnered with NVIDIA in its design of interconnect for A100 HGX training clusters. All CoreWeave A100 NVLINK GPUs offer [GPUDirect RDMA](https://developer.nvidia.com/gpudirect) over InfiniBand, in addition to standard IP/Ethernet networking.

CoreWeave's InfiniBand topology is fully [SHARP compliant](https://docs.nvidia.com/networking/display/sharpv270), and all components to leverage SHARP are implemented in the network control-plane, such as Adaptive Routing and Aggregation Managers, effectively doubling the performance of a compliant InfiniBand network as compared to a network with similar specifications without in-network computing such as RDMA over Converged Ethernet (RoCE).

**A100 NVLINK 80GB GPUs with InfiniBand are now available in the** [**LAS1 (Las Vegas) data center region**](https://docs.coreweave.com/data-center-regions#las1-las-vegas-nv-us-west)**. A100 NVLINK 40GB GPUs with InfiniBand are available in the** [**ORD1 (Chicago) data center region**](data-center-regions.md#ord1-chicago-il-us-central)**!**

> **Read more about** [**HPC Interconnect and SHARP**](coreweave-kubernetes/networking/hpc-interconnect.md) **on CoreWeave Cloud!**

### CoreWeave's Private Docker Registry 📦

Customers can now deploy their own private Docker registry from [the application Catalog](https://apps.coreweave.com)!

Images being hosted inside CoreWeave means no requirement for any subscriptions to external services such as Docker Hub, GitHub or GitLab. Additionally, credentials to pull images are automatically provisioned to a customer's namespace, alleviating the need to fiddle with “image pull secrets” that trip up many first-timers.

As usual with CoreWeave services, there is no charge except for the storage used for images and the minimal compute resources needed to run the registry server.

> **Head over to** [**the Cloud applications Catalog**](https://apps.coreweave.com/) **to deploy a private Docker registry to your namespace!**

### Rocky Linux is now supported on CoreWeave Cloud :mountain:

[**Rocky Linux**](https://rockylinux.org/) is a premiere, open-source enterprise Operating System, designed to be completely compatible with Red Hat Enterprise Linux®. Tipped to replace CentOS 7 as the leading VFX workstation of choice by [the Visual Effects Society survey](https://www.vesglobal.org/technology-committee-activities/#61e6987e16a546a91), Rocky Linux provides a stable platform with a 10-year upstream support lifecycle.

### Determined AI is now available in the Applications Catalog :brain:

<figure><img src=".gitbook/assets/determined-logo.png" alt="The Determined AI logo"><figcaption></figcaption></figure>

[Determined AI](https://www.determined.ai/) is an open-source deep learning training platform that makes building models fast and easy. Determined AI can now be deployed directly onto CoreWeave Cloud by deploying the application from [the application Catalog](https://apps.coreweave.com). With Determined AI, you can launch Jupyter notebooks, interactive shells with VSCode support, and distributed training experiments right from the Web UI and CLI tools. Deploying Determined AI from the CoreWeave applications Catalog makes spinning up an instance fast and easy, and when running, the platform consumes minimal resources and incurs minimal cost.

> [**Find Determined AI in the apps Catalog**](https://apps.coreweave.com) **to learn more about it or deploy an instance to your namespace!**

### vCluster is now available in the Applications Catalog :sailboat:

<figure><img src=".gitbook/assets/vcluster_horizontal_black.svg" alt=""><figcaption></figcaption></figure>

For those of you who require or desire more custom control over your Kubernetes Control Plane, the [vCluster](https://www.vcluster.com/) application is a great solution. With vCluster, you can install your own custom cluster-wide controllers, manage your own custom resource definitions, all without sacrificing the benefits of running on CoreWeave Cloud's bare metal environment.

> [**Find vCluster in the apps Catalog**](https://apps.coreweave.com) **to learn more about it or deploy an instance to your namespace!**

### New machine learning walkthroughs on CoreWeave Cloud :test\_tube:

It's never been easier to deploy, train, and finetune machine learning models on the Cloud for some incredible results, and with our [new walkthroughs and examples](broken-reference/) demonstrating just some of the ways CoreWeave's state-of-the-art compute power can be leveraged for model training, you can start today!:

* [**PyTorch Hugging Face Diffusers - Stable Diffusion Text to Image**](compass/examples/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md)**:** Generating high-quality images with photorealistic qualities from nothing but a text prompt used to be the stuff of science fiction. But now, using the open source model built by our friends at [Stability.AI](https://stability.ai/), you can leverage CoreWeave Cloud's compute power to do precisely that with just a few clicks and commands in [our latest walkthrough of this cutting-edge AI technology](https://docs.coreweave.com/compass/examples/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image).
* [**PyTorch Hugging Face Transformers BigScience BLOOM:** ](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom.md)In the[ PyTorch Hugging Face Transformers BigScience BLOOM](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1.md) walkthrough, you'll learn how to use the autoregressive Large Language Model (LLM) trained to continue text from a prompt on vast amounts of text data using industrial-scale computational resources. BLOOM is able to output coherent text in 46 languages - and 13 programming languages - whose structure is hardly distinguishable from text written by humans. BLOOM can even be instructed to perform text tasks it hasn't been explicitly trained for by casting them as text generation tasks.
* [**Triton Inference Server for GPT-J with FasterTransformer:**](compass/examples/triton-inference-server-fastertransformer.md) GPT-J is one of the most popular Open Source NLP model. It's size and performance makes it a perfect fit for cost sensitive NLP use cases. In our [Triton Inference Server for GPT-J FasterTransformer walkthrough](https://huggingface.co/EleutherAI/gpt-j-6B), you'll learn how to leverage [FasterTransformer ](https://github.com/NVIDIA/FasterTransformer)for up to 40% faster GPT-J inference over a vanilla Hugging Face Transformers based implementation.
* [**Triton Inference Server for GPT-NeoX 20B with FasterTransformer**](compass/examples/triton-inference-server-fastertransformer.md)**:** Together with EleutherAI, CoreWeave trained and released the Open Source GPT-NeoX 20B model in January. We are now taking self-hosted inference of this Large Language Model to the next level by offering a NVIDIA FasterTransformer-based inference option. In our [Triton Inference Server for GPT-NeoX 20B walkthrough](https://huggingface.co/EleutherAI/gpt-j-6B), you'll learn how to leverage [FasterTransformer ](https://github.com/NVIDIA/FasterTransformer)for up to 40% faster GPT-NeoX inference over a vanilla Hugging Face Transformers based implementation.
* [**GPT-NeoX finetuning**](compass/determined-ai/gpt-neox.md)**:** In our new [GPT-NeoX finetuning walkthrough](compass/determined-ai/gpt-neox.md), using [the DeterminedAI MLOps platform](https://www.determined.ai/blog/determined-algorithmia-integration) to run distributed finetuning jobs, you'll learn how to finetune a 20B parameter autoregressive model trained on [the Pile dataset](https://arxiv.org/abs/2101.00027) to generate text based on context or unconditionally for use cases such as story generation, chat bots, summarization, and more.

### Introducing Layer 2 VPC :cloud:

[CoreWeave Cloud Networking](networking/coreweave-cloud-native-networking-ccnn.md) (CCNN) is built to handle workloads requiring up to 100Gbps of network connectivity at scale, and it also handles firewalls and Load Balancing via Network Policies. Certain use cases, however, require a deeper level of network control than what is offered by a traditional Cloud network stack. For these users, we are now introducing the CoreWeave Cloud [Layer 2 VPC](coreweave-kubernetes/networking/layer-2-vpc-l2vpc/) (L2VPC).

L2VPC provides fine-grained customization by relinquishing all control over [DHCP servers](coreweave-kubernetes/networking/layer-2-vpc-l2vpc/dhcp-on-l2vpc.md), and [VPN gateways](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/) to the user. [Virtual Firewalls](networking/layer-2-vpc-l2vpc/virtual-firewalls/) are also supported and configured by the user - most KVM-compatible firewall images are compatible, allowing you to install your own firewall from the ground up. Installation guides for some of the most popular third-party choices, such as [Fortinet's FortiGate](networking/layer-2-vpc-l2vpc/virtual-firewalls/fortinet.md), are also provided.

L2VPC is built on top of SR-IOV hardware virtualization technology, retaining the high performance and low latency customers have come to expect from CoreWeave Cloud.

> [**Learn more about Layer 2 VPC on CoreWeave Cloud**](coreweave-kubernetes/networking/layer-2-vpc-l2vpc/)**!**

### CoreWeave Object Storage is now in beta :sparkles:

[Object Storage](storage/object-storage.md) is coming to CoreWeave! CoreWeave's S3-compatible Object Storage allows for an easy place to store and reference things like Docker images, machine learning models, and any other kinds of objects right within CoreWeave Cloud, streamlining your project workflows! Object storage is priced at only $0.03/GB/mo with no access and egress fees!

Accelerated object storage provides local caching for frequently accessed objects across all CoreWeave datacenters. Accelerated object storage is especially useful for large scale multi region rendering or inference auto-scaling where the same data needs to be loaded by hundreds or thousands of compute-nodes.

> **This feature is currently in beta, but you can** [**learn more now**](storage/object-storage.md)**, and contact your CoreWeave Support Specialist to try it out!**

### **Introducing The Workload Activity Tracker dashboard** :chart\_with\_upwards\_trend:

<figure><img src=".gitbook/assets/image (2) (3) (1).png" alt="Screenshot of the Workload Activity Tracker in action - vertical columns displaying information on Pods, such as their CPU usage and idle status"><figcaption><p>The Workload Activity Tracker in action</p></figcaption></figure>

It's an all too common experience to let idle research shells or experiments idle in your namespace after you're done working with them, only to later come back and realize you've been eating resources unnecessarily. Now, with the Workload Activity Tracker dashboard for Grafana, answering "is everything deployed in my namespace doing something?" is never a question you have to worry about.

The Workload Activity Tracker displays which of your Workloads have had activity in the past 24 hours, which are inactive, how many resources they are consuming, and how much cost they're incurring, all in a convenient and concise overview format.

> **Check out** [**the Workload Activity Tracker dashboard**](http://grafana.coreweave.com/) **now!**

##

## May 2022 :sunflower:

The Release Notes for May 2022 are inclusive of many new features launched since January 2022.

### Say Hello to LGA1 :tada:

We are pleased to announce the general availability of the CoreWeave LGA1 data center, **providing extremely low latency, high performance cloud compute resources to the broader New York City market**. Richly connected into the global Tier 1 internet backbone, LGA1 is built for low latency compute intensive use cases that require ultimate reliability and security.

Like all CoreWeave data centers, LGA1 is packed with a broad range of state of the art NVIDIA GPU accelerated cloud compute instances, including the **Quadro RTX series, the newest RTX Ampere workstation and A40 data center GPUs**. In addition to GPU compute, LGA1 is packed with CPU only instances, and high performance Block and Shared File System storage.

LGA1 is housed in an ISO 27001 certified, SSAE 18 SOC 2 compliant, Energy Star Certified campus, providing the utmost in security and efficiency for your critical workloads.

**Try it today by launching a** [**Virtual Server**](https://cloud.coreweave.com/virtual-servers) **from the CoreWeave Cloud UI!**

### Increased A100 80GB Capacity :chart\_with\_upwards\_trend:

CoreWeave now offers the **NVIDIA A100 80GB PCIe**, which delivers unprecedented acceleration to power the world’s highest-performing AI, data analytics, and HPC applications. The NVIDIA A100 80GB PCIe accelerator is **now available for Kubernetes deployments in ORD1** using the `gpu.nvidia.com/model` label selector `A100_PCIE_80GB`.

{% hint style="info" %}
_**Coming Soon:**_ CoreWeave is bringing NVIDIA A100 80GB support to the **LAS1** region with a deployment of **NVIDIA HGX A100 80GB NVLINK servers, built with GPUDirect Infiniband RDMA connectivity for blazing fast GPU to GPU communication**.

Reach out to [sales@coreweave.com](mailto:sales@coreweave.com) today to reserve space on our newest distributed training infrastructure!
{% endhint %}

### View and Manage Storage Volumes :floppy\_disk:

Managing cloud native storage has never been easier. **CoreWeave Cloud now provides an easy to use UI to manage your** [**Storage Volumes**](https://cloud.coreweave.com/storage). Expand and clone your volumes with the click of a button. [Learn more about CoreWeave Cloud Storage.](storage/storage/)

### Organization Management :people\_with\_bunny\_ears\_partying:

By popular demand, **we’ve added support for multiple users per organization and an** [**Organization Management UI** ](https://cloud.coreweave.com/organization)to invite and manage these users. Keep an eye on this page - we are regularly updating it with additional improvements and functionality.

![](https://lh3.googleusercontent.com/b\_rsG4Tz1ttqERXQGrGFxUSJfr8cU1r6bYPat9fa-m9r\_VWi3-nE17dhBIu\_dlUSLxnjYM71RF1pXcqmrgpE\_6xhjLm-Jr1ImP4aFzxUkT3L1SIHJ8Io39-vbkgm7xm0DwvR7eTr1gFELkXEng)

Since the start of the year, we've added:

👫 **Multi-User Support:** Invite and manage users to your Organization.

🔢 **Resource Quotas:** See how many pods, the number of GPUs, and storage capacity allocated at any time.

Features coming soon:

:closed\_lock\_with\_key: **RBAC:** Permissions and granular control over user access

:briefcase: **Multiple Namespaces:** Provision multiple namespaces per Organization

### Apps Catalog Additions :clipboard:

🕹️ **Scalable Pixel Streaming:** Stream your Unreal Engine projects to the masses quickly and easily.

🌐 **Traefik:** Custom ingresses, for use with your own domains.

🚚 **ArgoCD:** Access to a declarative, GitOps continuous delivery tool for Kubernetes.

🔥 **Backblaze:** Automate your volume backups to safeguard your data.

Launch any of these new Applications via [apps.coreweave.com](https://apps.coreweave.com)

### Finetune Your ML Models :bar\_chart:

Looking to finetune your own ML model on CoreWeave? [Check out our new reference tools and examples](https://docs.coreweave.com/compass/finetuning-machine-learning-models) for models such as **GPT-Neo, GPT-J-6B, and Fairseq**. Learn how to collect your dataset, which will then be tokenized and finetuned on with the parameters you give it, and even set up an endpoint to test your work with.

### Kubernetes Log Forwarding :fast\_forward:

Logs from all your containers to popular aggregation tools such as **Loki and DataDog**. [Click here to learn more.](coreweave-kubernetes/prometheus/logging.md)

### Better Track API Access Tokens :key2:

Need to organize your access tokens by user or track what they are being used for? You can now label them at creation from the CoreWeave Cloud UI.

### **Virtual Server Enhancements** :computer:

With CloudInit, you can **choose your preferred settings in advance** and they'll be set up during your instance launch. Plus, we now offer Static MAC Addresses and Serial Number support.

### Upgrades to Global Connectivity :earth\_americas:

We’ve invested heavily in networking to start 2022, with upgrades to **200Gbps+ Tier 1 transit in each region**.

Direct connects **up to 100Gbps** are now available at all of our data centers, and we’ve installed a **CoreWeave Cloud On Ramp** in downtown Los Angeles at CoreSite LA2 to accept cross connects back to LAS1.

We’ve also joined the **Megaport** network **at LAS1 and LGA1** for direct, quick software defined connectivity to CoreWeave Cloud.
