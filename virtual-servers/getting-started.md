---
description: >-
  What Virtual Servers are, what makes them unique, and how to deploy them onto
  CoreWeave Cloud.
---

# Getting Started

## Introduction

**CoreWeave Cloud's** **Virtual Servers** are highly configurable virtual machines managed in CoreWeave Cloud by Kubernetes, enabling anyone to deploy and host applications at scale with high availability.

Hosted across [three datacenter regions](https://docs.coreweave.com/data-center-regions#las1-las-vegas-nv-us-west), Virtual Servers can be deployed running [a variety of Linux distributions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/linux-images) or [Windows versions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/windows-images) as their operating systems, and can be configured either as CPU-only machines, or with [high-performance NVIDIA GPUs](https://www.coreweave.com/pricing) enabled - ideal for applications that require intensive compute power.

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

If you've determined you don't need a Virtual Server, but still but want to leverage the bare-metal performance benefits of running containerized workloads on CoreWeave Cloud, check out our documentation [on CoreWeave Kubernetes](broken-reference).
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
