---
description: >-
  Deploy and interact with Virtual Servers programmatically by using the
  Kubernetes REST API
---

# Programmatic Deployment

Virtual Servers can be deployed onto CoreWeave Cloud programmatically by using the [Kubernetes REST API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/). Any Kubernetes-compliant SDK can be used to deploy Virtual Servers.

This approach is an alternative to using the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) command line tool, the standard tool for engaging with Kubernetes, [which can also be used to deploy Virtual Servers onto CoreWeave Cloud](../../../docs/virtual-servers/deployment-methods/kubectl.md).

## Prerequisites

**Before you can access CoreWeave Cloud, you must first** [**request an account**](https://cloud.coreweave.com/signup)**.**

To use programmatic deployment as your deployment method, you will first need to obtain valid access credentials in the form of a `kubeconfig` file. See [Obtain Access Credentials](../../../docs/welcome-to-coreweave/getting-started.md#obtain-access-credentials) for more information.

## Examples

Here are some examples of popular languages being used to deploy Virtual Servers with the Kubernetes REST API.

<table data-card-size="large" data-view="cards"><thead><tr><th>Language</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h2><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> <a href="../../../docs/virtual-servers/deployment-methods/programmatically/bash.md">Bash</a></h2></td><td><a href="../../../docs/virtual-servers/deployment-methods/programmatically/bash.md">bash.md</a></td></tr><tr><td><h2><span data-gb-custom-inline data-tag="emoji" data-code="1f40d">🐍</span> <a href="python.md">Python</a></h2></td><td><a href="python.md">python.md</a></td></tr><tr><td><h2><span data-gb-custom-inline data-tag="emoji" data-code="1f4d7">📗</span> <a href="nodejs.md">NodeJS</a></h2></td><td><a href="nodejs.md">nodejs.md</a></td></tr><tr><td><h2><span data-gb-custom-inline data-tag="emoji" data-code="1f4d8">📘</span><a href="golang.md">Golang</a></h2></td><td><a href="golang.md">golang.md</a></td></tr></tbody></table>
