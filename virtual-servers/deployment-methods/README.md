---
description: >-
  Learn about the different methods available for deploying Virtual Servers to
  CoreWeave Cloud.
---

# Deployment Methods

{% hint style="success" %}
**What is a Virtual Server?**

See [Getting Started with Virtual Servers](../getting-started.md).

To learn about Virtual Server configuration options, see [Virtual Server Configuration Options](../../docs/virtual-servers/virtual-server-configuration-options/).

To configure **data-disk storage** for your Virtual Server, see [How to provision CoreWeave Cloud Storage](https://docs.coreweave.com/coreweave-kubernetes/storage#how-to-provision-coreweave-cloud-storage).
{% endhint %}

There are multiple ways to deploy and manage Virtual Servers on CoreWeave Cloud, each with their own unique advantages.

Below are descriptions of some of the deployment possibilities CoreWeave offers, as well as some information on each to help you choose which method may be best for your use case.

**To learn about configuration options for Virtual Servers, proceed to** [**Virtual Server Configuration Options**](../../docs/virtual-servers/virtual-server-configuration-options/)**.**

## [The CoreWeave Cloud UI](coreweave-apps.md)

The CoreWeave Cloud UI is an easy-to-use Web interface to deploy, visualize, and manage Virtual Servers, while still providing access to deployment configuration files, server event details, and even a virtual terminal for quick access to your Virtual Servers right from the Cloud UI.

{% hint style="info" %}
**Best if:** You prefer using a graphical interface with toggles and buttons to visualize your configurations, but still want access to lower-level configuration files.
{% endhint %}

![](<../../docs/.gitbook/assets/image (6) (1) (1).png>)

## [Kubernetes CLI](../../docs/virtual-servers/deployment-methods/kubectl.md)\*\*\*\*

![](<../../docs/.gitbook/assets/image (71) (1) (1).png>)

[Virtual Servers are a Kubernetes Custom Defined Resource (CRD)](https://github.com/coreweave/kubernetes-cloud/blob/5632d497da5883be07a1535a67cad69b97ea5050/docs/virtual-servers/deployment-methods/kubectl.md), which may be directly deployed on CoreWeave Cloud using the `kubectl` command line tool.

**This method is best if you are:**

* comfortable with Kubernetes principles
* familiar with using `kubectl` on the command line

{% content-ref url="../../docs/virtual-servers/deployment-methods/kubectl.md" %}
[kubectl.md](../../docs/virtual-servers/deployment-methods/kubectl.md)
{% endcontent-ref %}

## [Terraform](terraform.md)

![](<../../docs/.gitbook/assets/image (4) (2) (1) (2).png>)

CoreWeave offers [an open source Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/5632d497da5883be07a1535a67cad69b97ea5050/virtual-server/examples/terraform) for deploying Virtual Servers, which can also be customized by extending the module yourself.

**This method is best if you are:**

* comfortable using Terraform modules
* comfortable using Terraform on the command line

{% content-ref url="terraform.md" %}
[terraform.md](terraform.md)
{% endcontent-ref %}

## :desktop: [Programmatic API interface options](programmatically/)

CoreWeave offers several methods for interfacing with the Kubernetes REST API programmatically to deploy Virtual Servers into CoreWeave Cloud. Additionally, **any Kubernetes standards-compliant SDK may be used**.

CoreWeave provides interface examples in the following languages:

<table data-card-size="large" data-column-title-hidden data-view="cards"><thead><tr><th>Language</th></tr></thead><tbody><tr><td><a href="../../docs/virtual-servers/deployment-methods/programmatically/bash.md">Bash</a> (using <code>curl</code> and <code>jq</code>)</td></tr><tr><td><a href="programmatically/golang.md">Golang</a></td></tr><tr><td><a href="programmatically/python.md">Python</a></td></tr><tr><td><a href="programmatically/nodejs.md">NodeJS</a></td></tr></tbody></table>

**This method is best if you are:**

* interested in precise customizations and configurations
* are comfortable interacting programmatically with the Kubernetes API

{% content-ref url="programmatically/" %}
[programmatically](programmatically/)
{% endcontent-ref %}
