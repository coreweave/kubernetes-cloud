---
description: >-
  Learn how to deploy and interact with Virtual Servers programmatically
  interacting with the Kubernetes REST API.
---

# Programmatic Deployment

Virtual Servers can be deployed onto CoreWeave Cloud by directly programmatically interfacing with the [Kubernetes REST API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/). This approach is an alternative to using the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) command line tool, the standard tool for engaging with Kubernetes, [which can also be used to deploy Virtual Servers onto CoreWeave Cloud](../../../docs/virtual-servers/deployment-methods/kubectl.md).

Any Kubernetes-compliant SDK can be used to deploy Virtual Servers. CoreWeave provides examples of some of the most popular languages used to interact with the Kubernetes REST API to deploy and manage Virtual Servers on CoreWeave Cloud.

## Getting Started

**Before you can access CoreWeave Cloud, you must first** [**request an account**](https://cloud.coreweave.com/request-account)**.**

To use programmatic deployment as your deployment method, you will first need to obtain valid access credentials in the form of a `kubeconfig` file.

{% hint style="info" %}
**Note**

See [Obtain Access Credentials](../../../docs/coreweave-kubernetes/getting-started/#obtain-access-credentials) for more information.
{% endhint %}

## Examples

| Language                                                                          |
| --------------------------------------------------------------------------------- |
| [Bash](../../../docs/virtual-servers/deployment-methods/programmatically/bash.md) |
| [Python](python.md)                                                               |
| [NodeJS](nodejs.md)                                                               |
| [Golang](golang.md)                                                               |
