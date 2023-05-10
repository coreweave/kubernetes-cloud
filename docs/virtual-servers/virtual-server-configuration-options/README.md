---
description: Configure and deploy Virtual Servers using one of four deployment methods
---

# Configuration Options

## Deployment methods

Virtual Servers may be configured and deployed using four distinctive methods. Learn more about how to set up each of the deployment methods covered in this implementation guide by visiting their respective pages under the [Virtual Server Deployment Methods](../../../virtual-servers/deployment-methods/) section.

<table data-card-size="large" data-view="cards"><thead><tr><th>Deployment method</th><th>Description</th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="2601">☁</span> <a href="../../../virtual-servers/deployment-methods/coreweave-apps.md"><strong>CoreWeave Cloud UI</strong></a></h3></td><td>Our in-house, graphical Web-based interface for configuring Virtual Servers. Configuration options are represented either as graphical selection options, or as fields that can be configured in the YAML manifest from the UI.</td><td><a href="../../../virtual-servers/deployment-methods/coreweave-apps.md">coreweave-apps.md</a></td><td><a href="../../../virtual-servers/deployment-methods/coreweave-apps.md">coreweave-apps.md</a></td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="26f5">⛵</span> <a href="../deployment-methods/kubectl.md"><strong>Kubernetes CLI</strong></a></h3></td><td>Deploy Virtual Servers using the standard way of interacting with Kubernetes, via <code>kubectl</code>. Configuration options are implemented as fields in the YAML manifest file.</td><td><a href="../deployment-methods/kubectl.md">kubectl.md</a></td><td><a href="../deployment-methods/kubectl.md">kubectl.md</a></td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f528">🔨</span> <a href="../../../virtual-servers/deployment-methods/terraform.md"><strong>Terraform</strong></a></h3></td><td>HashiCorp's infrastructure-as-code tool can deploy Virtual Servers by leveraging <a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform">CoreWeave's Virtual Server Terraform module</a>. Configuration options are implemented using Terraform module configurations.</td><td><a href="../../../virtual-servers/deployment-methods/terraform.md">terraform.md</a></td><td><a href="../../../virtual-servers/deployment-methods/terraform.md">terraform.md</a></td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> <a href="../../../virtual-servers/deployment-methods/programmatically/"><strong>Programmatic deployment</strong></a></h3></td><td>Interact with the Kubernetes API directly, using any Kubernetes-compliant SDK. Configuration options are language-specific interactions with the Kubernetes API.</td><td><a href="../../../virtual-servers/deployment-methods/programmatically/">programmatically</a></td><td><a href="../../../virtual-servers/deployment-methods/programmatically/">programmatically</a></td></tr></tbody></table>

The following configuration options may be changed while the Virtual Server is running:

* Annotations and labels
* Floating IPs
* Root disk size (storage size can only be **increased** while the Virtual Server is running - it may also take a while before the change is reflected)

## How to use this section

Each page beneath this one contains a tabbed table. Each tab explains how to deploy the configurations to your Virtual Server, respective to the method described.

For example:

<figure><img src="../../.gitbook/assets/image (30).png" alt="Screenshot of a tabbed page for Networking"><figcaption><p>Click the tab for the chosen deployment method to get more information about its config options</p></figcaption></figure>

## Examples

Example deployments can be found on [CoreWeave's GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/):

<table data-card-size="large" data-column-title-hidden data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="2728">✨</span> View all examples</td><td></td><td></td><td><a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples">https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="26f5">⛵</span> Kubernetes CLI</td><td></td><td></td><td><a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl">https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f528">🔨</span> Terraform</td><td></td><td></td><td><a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform">https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> Programmatic (<a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/curl">Bash</a>, <a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/go">Golang</a>, <a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/nodejs">NodeJS</a>, <a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/python">Python</a>)</td><td></td><td></td><td><a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/">https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/</a></td></tr></tbody></table>
