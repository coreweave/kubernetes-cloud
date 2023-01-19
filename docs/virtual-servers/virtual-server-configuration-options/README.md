---
description: >-
  Explore all of the Virtual Server configuration options and how to implement
  them.
---

# Configuration Options

Virtual Servers are highly customizable, and can be configured for deployment a few different ways.

Each page beneath this one contains a tabbed table. Each tab explains how to deploy the configurations to your Virtual Server, respective to the method described.

{% hint style="info" %}
**Additional Resources**

You can find examples of [Kubernetes CLI deployments](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl), [Terraform deployments](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform), and Programmatic deployments in [the `examples` directory on our GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples).
{% endhint %}

You can learn more about how to set up each of the **deployment methods** covered in this implementation guide by visiting their respective pages under the [Virtual Server Deployment Methods](../../../virtual-servers/deployment-methods/) section:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="2601">☁</span> <a href="../../../virtual-servers/deployment-methods/coreweave-apps.md"><strong>CoreWeave Cloud UI</strong></a></td><td>Our in-house, graphical Web-based interface for configuring Virtual Servers. Configuration options are represented either as graphical selection options, or as fields that can be configured in the YAML manifest from the UI.</td><td></td><td><a href="../../../virtual-servers/deployment-methods/coreweave-apps.md">coreweave-apps.md</a></td></tr><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="2638">☸</span> <strong></strong> <a href="../deployment-methods/kubectl.md"><strong>Kubernetes CLI</strong></a><strong></strong></td><td>Deploy Virtual Servers using the standard way of interacting with Kubernetes, via <code>kubectl</code>. Configuration options are implemented as fields in the YAML manifest file.</td><td></td><td><a href="../deployment-methods/kubectl.md">kubectl.md</a></td></tr><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="1f528">🔨</span> <strong></strong> <a href="../../../virtual-servers/deployment-methods/terraform.md"><strong>Terraform</strong></a></td><td>HashiCorp's infrastructure-as-code tool can deploy Virtual Servers by leveraging <a href="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform">CoreWeave's Virtual Server Terraform module</a>. Configuration options are implemented using Terraform module configurations.</td><td></td><td><a href="../../../virtual-servers/deployment-methods/terraform.md">terraform.md</a></td></tr><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> <strong></strong> <a href="../../../virtual-servers/deployment-methods/programmatically/"><strong>Programmatic deployment</strong></a></td><td>Interact with the Kubernetes API directly, using any Kubernetes-compliant SDK. Configuration options are language-specific interactions with the Kubernetes API.</td><td></td><td><a href="../../../virtual-servers/deployment-methods/programmatically/">programmatically</a></td></tr></tbody></table>

{% hint style="warning" %}
**Important**

If you're using the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) as your deployment method, be aware that not _every_ Virtual Server configuration option is exposed through the options displayed graphically on the Cloud UI configuration screen.

If you are using the Cloud UI to deploy your Virtual Servers but require more fine-tuned control, or, you wish to save your Virtual Server configuration in order to replicate it for additional Virtual Servers, you can interact with the server's corresponding YAML configuration chart under the **YAML** tab, as shown below.

**All options exposed through the Graphical UI are also available to interact with on the YAML tab.**
{% endhint %}

![YAML manifest, selectable from the Virtual Server configuration screen.
](<../../.gitbook/assets/image (108).png>)

{% hint style="success" %}
**Tip**

The following configuration options can be changed **while the Virtual Server is running:**

* Annotations and labels
* [Floating IPs](additional-features.md#floating-ips)
* Root disk size (The storage size can only be **increased** while the Virtual Server is running - it may also take a while before the change is reflected)
{% endhint %}
