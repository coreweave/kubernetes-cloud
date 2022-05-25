---
description: Feature Updates and Release Notes for CoreWeave Cloud
---

# Release Notes

## May 2022 :sunflower:

The Release Notes for May 2022 are inclusive of many new features launched since January 2022.

### Say Hello to LGA1 :tada:&#x20;

We are pleased to announce the general availability of the CoreWeave LGA1 data center, **providing extremely low latency, high performance cloud compute resources to the broader New York City market**. Richly connected into the global Tier 1 internet backbone, LGA1 is built for low latency compute intensive use cases that require ultimate reliability and security.

Like all CoreWeave data centers, LGA1 is packed with a broad range of state of the art NVIDIA GPU accelerated cloud compute instances, including the **Quadro RTX series, the newest RTX Ampere workstation and A40 data center GPUs**. In addition to GPU compute, LGA1 is packed with CPU only instances, and high performance Block and Shared File System storage.

LGA1 is housed in an ISO 27001 certified, SSAE 18 SOC 2 compliant, Energy Star Certified campus, providing the utmost in security and efficiency for your critical workloads.

**Try it today by launching a** [**Virtual Server**](https://cloud.coreweave.com/virtual-servers) **from the CoreWeave Cloud UI!**

### Increased A100 80GB Capacity :chart\_with\_upwards\_trend:

CoreWeave now offers the **NVIDIA A100 80GB PCIe**, which delivers unprecedented acceleration to power the world’s highest-performing AI, data analytics, and HPC applications. The NVIDIA A100 80GB PCIe accelerator is **now available for Kubernetes deployments in ORD1** using the `gpu.nvidia.com/model` label selector `A100_PCIE_80GB`.

{% hint style="info" %}
_**Coming Soon:**_ CoreWeave is bringing NVIDIA A100 80GB support to the **LAS1** region with a deployment of **NVIDIA HGX A100 80GB NVLINK servers, built with GPUDirect Infiniband RDMA connectivity for blazing fast GPU to GPU communication**.&#x20;

Reach out to [sales@coreweave.com](mailto:sales@coreweave.com) today to reserve space on our newest distributed training infrastructure!
{% endhint %}

### View and Manage Storage Volumes :floppy\_disk:

Managing cloud native storage has never been easier. **CoreWeave Cloud now provides an easy to use UI to manage your** [**Storage Volumes**](https://cloud.coreweave.com/storage). Expand and clone your volumes with the click of a button. [Learn more about CoreWeave Cloud Storage.](coreweave-kubernetes/storage.md)

### Organization Management :people\_with\_bunny\_ears\_partying:

By popular demand, **we’ve added support for multiple users per organization and an** [**Organization Management UI** ](https://cloud.coreweave.com/organization)to invite and manage these users. Keep an eye on this page - we are regularly updating it with additional improvements and functionality.

![](https://lh3.googleusercontent.com/b\_rsG4Tz1ttqERXQGrGFxUSJfr8cU1r6bYPat9fa-m9r\_VWi3-nE17dhBIu\_dlUSLxnjYM71RF1pXcqmrgpE\_6xhjLm-Jr1ImP4aFzxUkT3L1SIHJ8Io39-vbkgm7xm0DwvR7eTr1gFELkXEng)

Since the start of the year, we've added:&#x20;

👫 **Multi-User Support:** Invite and manage users to your Organization.

🔢 **Resource Quotas:** See how many pods, the number of GPUs, and storage capacity allocated at any time.&#x20;

Features coming soon:

:closed\_lock\_with\_key: **RBAC:** Permissions and granular control over user access

:briefcase: **Multiple Namespaces:** Provision multiple namespaces per Organization

### Apps Catalog Additions :clipboard:

🕹️ **Scalable Pixel Streaming:** Stream your Unreal Engine projects to the masses quickly and easily.&#x20;

🌐 **Traefik:** Custom ingresses, for use with your own domains.&#x20;

🚚 **ArgoCD:** Access to a declarative, GitOps continuous delivery tool for Kubernetes.&#x20;

🔥 **Backblaze:** Automate your volume backups to safeguard your data.

Launch any of these new Applications via [apps.coreweave.com](https://apps.coreweave.com)

### Finetune Your ML Models :bar\_chart:

Looking to finetune your own ML model on CoreWeave? [Check out our new reference tools and examples](https://docs.coreweave.com/compass/finetuning-machine-learning-models) for models such as **GPT-Neo, GPT-J-6B, and Fairseq**. Learn how to collect your dataset, which will then be tokenized and finetuned on with the parameters you give it, and even set up an endpoint to test your work with.

### Kubernetes Log Forwarding :fast\_forward:

Logs from all your containers to popular aggregation tools such as **Loki and DataDog**. [Click here to learn more.](coreweave-kubernetes/prometheus/logging.md)

### Better Track API Access Tokens :key2:

Need to organize your access tokens by user or track what they are being used for? You can now label them at creation from the CoreWeave Cloud UI.

### **Virtual Server Enhancements** :computer:****

With CloudInit, you can **choose your preferred settings in advance** and they'll be set up during your instance launch. Plus, we now offer Static MAC Addresses and Serial Number support.

### Upgrades to Global Connectivity :earth\_americas:

We’ve invested heavily in networking to start 2022, with upgrades to **200Gbps+ Tier 1 transit in each region**.&#x20;

Direct connects **up to 100Gbps** are now available at all of our data centers, and we’ve installed a **CoreWeave Cloud On Ramp** in downtown Los Angeles at CoreSite LA2 to accept cross connects back to LAS1.&#x20;

We’ve also joined the **Megaport** network **at LAS1 and LGA1** for direct, quick software defined connectivity to CoreWeave Cloud.
