---
description: >-
  Learn how to deploy and interact with Virtual Servers programmatically
  interacting with the Kubernetes REST API.
---

# Programmatic deployment

{% hint style="success" %}
**What is a Virtual Server?**

[See "Getting Started" to learn more.](../../../coreweave-kubernetes/getting-started.md)
{% endhint %}

## Introduction

One method for deploying and manipulating CoreWeave Virtual Servers is by directly, programmatically interfacing with the [Kubernetes REST API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/).

This is an alternative method to using [`kubectl`](https://kubernetes.io/docs/reference/kubectl/), the standard tool for engaging with Kubernetes, [which can also be used to deploy Virtual Servers onto CoreWeave Cloud](../../../docs/virtual-servers/deployment-methods/kubectl.md).

{% hint style="warning" %}
**Important**

Before you can interact with the CoreWeave Kubernetes API server, you must first have valid credentials in the form of an **API token** and correctly configured **`kubeconfig` file**.

****[**Learn more about gaining access credentials and generating the `kubeconfig` file.**](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials)****
{% endhint %}

### Language examples

Below are some language-specific examples of interacting with the Kubernetes REST API to deploy and manage Virtual Servers on CoreWeave Cloud.

* [Bash](https://docs.coreweave.com/virtual-servers/deployment-methods/programmatically/bash) (using `curl` and `jq`)
* [Python](python.md)
* [NodeJS](nodejs.md)
* [Golang](golang.md)
