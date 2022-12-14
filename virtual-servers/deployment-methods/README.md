---
description: >-
  Learn about the different methods available for deploying Virtual Servers to
  CoreWeave Cloud.
---

# Deployment Methods

{% hint style="success" %}
**What is a Virtual Server?**

See [Getting Started with Virtual Servers](../getting-started.md).
{% endhint %}

## Recommended Reading

The following articles provide additional materials for learning about Virtual Servers:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Get Started with Virtual Servers</strong></td><td>Learn about what Virtual Servers are, what they're used for, and how they work</td><td></td><td><a href="../getting-started.md">getting-started.md</a></td></tr><tr><td><strong>Virtual Server Configuration Options</strong></td><td>Learn how to configure a Virtual Server to your specifications using three different methods</td><td></td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/">virtual-server-configuration-options</a></td></tr><tr><td><strong>Provision CoreWeave Cloud Storage</strong></td><td>Learn how storage works on CoreWeave Cloud, how to provision storage, and how to connect a Virtual Server to storage</td><td></td><td><a href="../../docs/storage/storage.md">storage.md</a></td></tr></tbody></table>

## Deployment Methods

There are multiple ways to deploy and manage Virtual Servers on CoreWeave Cloud, each with their own unique advantages.

Below are descriptions of some of the deployment possibilities CoreWeave offers, as well as some information on each to help you choose which method may be best for your use case.

**To learn about configuration options for Virtual Servers, proceed to** [**Virtual Server Configuration Options**](../../docs/virtual-servers/virtual-server-configuration-options/)**.**

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th></th><th data-hidden data-card-cover data-type="files"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>CoreWeave Cloud UI</strong></td><td>The CoreWeave Cloud UI is an easy-to-use Web interface to deploy, visualize, and manage Virtual Servers, while still providing access to deployment configuration files, server event details, and even a virtual terminal for quick access to your Virtual Servers right from the Cloud UI.</td><td>Best for those <strong></strong> who prefer to use a graphical interface with toggles and buttons to visualize configurations, but still want access to lower-level configuration files and options.</td><td></td><td><a href="../../docs/.gitbook/assets/image.png">image.png</a></td><td><a href="coreweave-apps.md">coreweave-apps.md</a></td></tr><tr><td><strong>Kubernetes</strong></td><td><a href="../../docs/virtual-servers/deployment-methods/kubectl.md">Virtual Servers are a Kubernetes Custom Defined Resource (CRD)</a>, which may be directly deployed on CoreWeave Cloud using the <code>kubectl</code> command line tool.</td><td>Best for those who <strong></strong> are comfortable with Kubernetes principles, and are familiar with using <code>kubectl</code> on the command line.</td><td></td><td><a href="../../docs/.gitbook/assets/Kubernetes_logo_without_workmark.svg">Kubernetes_logo_without_workmark.svg</a></td><td><a href="../../docs/virtual-servers/deployment-methods/kubectl.md">kubectl.md</a></td></tr><tr><td><strong>Terraform</strong></td><td><p>CoreWeave offers <a href="https://github.com/coreweave/kubernetes-cloud/tree/5632d497da5883be07a1535a67cad69b97ea5050/virtual-server/examples/terraform">an open source Terraform module</a> for deploying Virtual Servers, which can also be customized by extending the module yourself.</p><p></p><p>Best for those who are comfortable using Terraform modules, and comfortable using Terraform on the command line.</p></td><td></td><td></td><td><a href="../../docs/.gitbook/assets/og-image-8b3e4f7d-blog-aspect-ratio.png">og-image-8b3e4f7d-blog-aspect-ratio.png</a></td><td><a href="terraform.md">terraform.md</a></td></tr><tr><td><strong>API</strong></td><td>CoreWeave offers several methods for interfacing with the Kubernetes REST API programmatically to deploy Virtual Servers into CoreWeave Cloud. Additionally, any Kubernetes standards-compliant SDK may be used.</td><td><p>Best for those interested in precise customizations and configurations, and who are comfortable interacting programmatically with the Kubernetes API. </p><p></p><p>We provide language-specific examples of API deployment in these languages:</p></td><td><ul><li><a href="../../docs/virtual-servers/deployment-methods/programmatically/bash.md">Bash</a></li><li><a href="programmatically/golang.md">Golang</a></li><li><a href="programmatically/python.md">Python</a></li><li><a href="programmatically/nodejs.md">NodeJS</a></li></ul></td><td><a href="../../docs/.gitbook/assets/k8s (2).png">k8s (2).png</a></td><td><a href="programmatically/">programmatically</a></td></tr></tbody></table>
