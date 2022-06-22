---
description: >-
  Learn about the different methods available for deploying Virtual Servers to
  CoreWeave Cloud.
---

# Virtual Server Deployment Methods

{% hint style="success" %}
**What is a Virtual Server?**

[See "Getting Started" to learn more.](../getting-started.md)
{% endhint %}

## Introduction

There are multiple ways to deploy and manage Virtual Servers on CoreWeave Cloud, each with their own unique advantages. Below are descriptions of some of the deployment possibilities CoreWeave offers, as well as some information on each to help you choose which to use.

### Graphical deployment methods

#### [Using The CoreWeave Cloud UI](coreweave-apps.md)****

The **CoreWeave Cloud UI** is an easy-to-use Web interface to deploy, visualize, and manage Virtual Servers, while still providing access to deployment configuration files, server event details, and even a virtual terminal for quick access to your Virtual Servers right from the Cloud UI.

{% hint style="info" %}
**Best if:** You prefer using a graphical interface with toggles and buttons to visualize your configurations, but still want access to lower-level configuration files.
{% endhint %}

![The Virtual Server deployment page on CoreWeave Cloud UI.](<../../.gitbook/assets/image (89).png>)

### Command line deployment options

Virtual Servers can be deployed via the command line onto CoreWeave Cloud a few different ways. CoreWeave supports the following methods for command line deployment options:

#### [Using Kubernetes CLI](kubectl.md)****

![](<../../.gitbook/assets/image (108).png>)

{% hint style="info" %}
**Best if:** You are comfortable with Kubernetes principles and using `kubectl` on the command line.
{% endhint %}

#### [Using Terraform](terraform.md)

![](<../../.gitbook/assets/image (63).png>)

{% hint style="info" %}
**Best if:** You are comfortable with Terraform modules, and with using Terraform on the command line.
{% endhint %}

### [Programmatic API interface options](programmatically/)

{% hint style="info" %}
**Best if:** You are interested in precise customizations and configurations, and are comfortable interacting programmatically with the Kubernetes API.
{% endhint %}

CoreWeave offers several methods for interfacing with the Kubernetes REST API programmatically to deploy Virtual Servers into CoreWeave Cloud. Additionally, any Kubernetes standards-compliant SDK may be used.

CoreWeave supports API interfaces in the following languages:

* [Bash](https://app.gitbook.com/o/-M8EEYiNkaJsT8ISX0kX/s/-M83TghsCfsi8FCYs2DZ/\~/changes/FZAhwuANE9ksdqEBqsD6/virtual-servers/deployment-methods/programmatically/bash) (using `curl` and `jq`)
* [Golang](programmatically/golang.md)
* [Python](programmatically/python.md)
* [NodeJS](programmatically/nodejs.md)
