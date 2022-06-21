---
description: >-
  What Virtual Servers are, what makes them unique, and how to deploy them onto
  CoreWeave Cloud.
---

# Getting Started

## Introduction

**CoreWeave Cloud's** **Virtual Servers** are highly configurable virtual machines deployed and managed on CoreWeave Cloud via an easy-to-use UI or programmatically via the Kubernetes API, enabling anyone to deploy and host applications at scale with high availability.

### Virtual Server Features

* :zap: Powerful **CPU and** [**high-performance NVIDIA GPU**](https://www.coreweave.com/pricing)**-accelerated** Virtual Servers with unlimited resource configurability.
* :earth\_americas: Available in all of CoreWeave's [**Data Center Regions**](../docs/data-center-regions.md) for geographic diversity.
* ****:gear: **Bare-metal performance via GPU PCI pass-through.** No GPU virtualization or shared resources.
* :minidisc: Available with pre-built [**Linux distributions**](https://docs.coreweave.com/virtual-servers/coreweave-system-images/linux-images)**,** [**Windows versions**](https://docs.coreweave.com/virtual-servers/coreweave-system-images/windows-images)**, or** [**bring your own image**](../docs/virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md)**.** Need additional control? [Use cloud-init for customization at startup.](https://docs.coreweave.com/virtual-servers/coreweave-system-images/linux-images)
* :floppy\_disk: Leverage **high-performance** [**CoreWeave Cloud Storage**](../coreweave-kubernetes/storage.md) for both the Virtual Server root disk and any shared file system volumes to connect to centralized asset storage.
* :rocket: Up to **100Gbps internal and external networking speed** per instance, for blazing fast data transfers.
* ****:bulb: **** [**Directly attach public IP addresses**](https://docs.coreweave.com/coreweave-kubernetes/networking) to a Virtual Server network interface, or leverage [Load Balancer IPs](https://docs.coreweave.com/coreweave-kubernetes/networking) to control internal and external service access.

### What can I do with Virtual Servers?

While not every use case is appropriately solved using Virtual Servers, there are some things that aren't possible without them!

CoreWeave Virtual Servers run under the same API control plane and use the same storage and networking as your Kubernetes workloads. This provides a single, powerful platform for both stateful and stateless resource management.

Common use cases for CoreWeave Virtual Servers include:

<details>

<summary>Running applications in a bare-metal environment.</summary>

CoreWeave Virtual Servers provide all the isolation and control benefits that come with running a workload on a real server.

</details>

<details>

<summary>Create virtual desktops and developer workstations accessible from anywhere.</summary>

Virtual Servers can be deployed with **virtual desktop environments**, providing developer workstations running Linux or Windows. Using applications like [Parsec](https://parsec.app/) for Windows machines and [Teradici](https://www.teradici.com/) for Linux, developers can log in to their workstations to access their work from anywhere!

</details>

{% hint style="success" %}
**Don't need a Virtual Server?**

If you've determined you don't need a Virtual Server, but want to leverage the bare-metal performance benefits of running containerized workloads on CoreWeave Cloud, check out our documentation [on CoreWeave Kubernetes](broken-reference).
{% endhint %}

## Deploying Virtual Servers

There are multiple ways to deploy and manage Virtual Servers on CoreWeave Cloud, each with their own unique advantages. Below are descriptions of some of the deployment possibilities CoreWeave offers, as well as some information on each to help you choose which to use.

### Graphical deployment methods

#### [Using The CoreWeave Cloud UI](deployment-methods/coreweave-apps.md)****

The **CoreWeave Cloud UI** is an easy-to-use Web interface to deploy, visualize, and manage Virtual Servers, while still providing access to deployment configuration files, server event details, and even a virtual terminal for quick access to your Virtual Servers right from the Cloud UI.

{% hint style="info" %}
**Best if:** You prefer using a graphical interface with toggles and buttons to visualize your configurations, but still want access to lower-level configuration files.
{% endhint %}

![The Virtual Server deployment page on CoreWeave Cloud UI.](<../docs/.gitbook/assets/image (66).png>)

### Command line deployment options

Virtual Servers can be deployed via the command line onto CoreWeave Cloud a few different ways. CoreWeave supports the following methods for command line deployment options:

#### [Using Kubernetes CLI](../docs/virtual-servers/deployment-methods/kubectl.md)****

![](<../docs/.gitbook/assets/image (71).png>)

{% hint style="info" %}
**Best if:** You are comfortable with Kubernetes principles and using `kubectl` on the command line.
{% endhint %}

#### [Using Terraform](deployment-methods/terraform.md)

![](<../docs/.gitbook/assets/image (54).png>)

{% hint style="info" %}
**Best if:** You are comfortable with Terraform modules, and with using Terraform on the command line.
{% endhint %}

### [Programmatic API interface options](deployment-methods/programmatically/)

{% hint style="info" %}
**Best if:** You are interested in precise customizations and configurations, and are comfortable interacting programmatically with the Kubernetes API.
{% endhint %}

CoreWeave offers several methods for interfacing with the Kubernetes API programmatically to deploy Virtual Servers into CoreWeave Cloud. Additionally, any Kubernetes standards-compliant SDK may be used.

CoreWeave supports API interfaces in the following languages:

* [Golang](deployment-methods/programmatically/golang.md)
* [Python](deployment-methods/programmatically/python.md)
* [NodeJS](deployment-methods/programmatically/nodejs.md)
