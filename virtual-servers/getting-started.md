---
description: >-
  What Virtual Servers are, what makes them unique, and how to deploy them onto
  CoreWeave Cloud
---

# Get Started with Virtual Servers

**CoreWeave Cloud's** **Virtual Servers** are highly configurable virtual machines, deployed and managed on CoreWeave Cloud via the easy-to-use [Cloud UI](deployment-methods/coreweave-apps.md) or programmatically via the Kubernetes API, enabling anyone to deploy and host applications at scale with high availability.

### Virtual Servers feature...

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="26a1">⚡</span> <strong>Powerful computation</strong></td><td>With powerful CPU- and <a href="https://www.coreweave.com/gpu-cloud-pricing">high-performance NVIDIA GPU-accelerated Virtual Servers</a> featuring unlimited resource configurability, and Virtual Servers are deployed and ready to use in seconds.</td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f30e">🌎</span> <strong>High availability</strong></td><td>Virtual Servers can be deployed in all of CoreWeave's <a href="../docs/data-center-regions.md">Data Center Regions</a>, allowing for geographic diversity.</td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="2699">⚙</span> <strong>Bare-metal performance</strong></td><td>With GPU PCI pass-through, there's no GPU virtualization or shared resources.</td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4bd">💽</span> <strong>Versatile</strong></td><td>Virtual Servers come with pre-built <a href="../docs/virtual-servers/coreweave-system-images/linux-images.md">Linux distributions</a>, <a href="../docs/virtual-servers/coreweave-system-images/windows-images.md">Windows versions</a>, or <a href="../docs/virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md">bring your own image</a>! Use <a href="../docs/virtual-servers/coreweave-system-images/linux-images.md#cloud-init">cloud-init</a> at startup for even more customization and control.</td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4be">💾</span> <strong>High-performance storage</strong></td><td>Leverage the high performance of <a href="../docs/virtual-servers/virtual-server-configuration-options/storage.md">CoreWeave Cloud Storage</a> for both the Virtual Server root disk and any shared file system volumes to connect to centralized asset storage.</td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f680">🚀</span> <strong>Blazing fast, flexible networking</strong></td><td>Up to 100Gbps internal and external networking speed per instance, for blazing fast data transfers.</td><td>Directly <a href="../docs/virtual-servers/virtual-server-configuration-options/networking.md#attach-public-ip">attach IP addresses</a> to a Virtual Server network interface, or leverage <a href="https://docs.coreweave.com/coreweave-kubernetes/networking">Load Balancer IPs</a> to control internal and external service access.</td></tr></tbody></table>

### What can I do with Virtual Servers?

While not every use case is appropriately solved using Virtual Servers, there are some things that aren't possible without them!

CoreWeave Virtual Servers run under the same API control plane and use the same storage and networking as your Kubernetes workloads. This provides a single, powerful platform for both stateful and stateless resource management.

Common use cases for CoreWeave Virtual Servers include:

<details>

<summary><strong>Leverage the performance of CoreWeave's bare metal Cloud, even when running containerized Virtual Machines</strong></summary>

CoreWeave Virtual Servers provide all the isolation and control benefits that come with running a workload on a real server. Leveraging GPU PCI pass-through means no GPU virtualization or shared resources on Virtual Servers.

</details>

<details>

<summary>Create virtual desktops and developer workstations accessible from anywhere</summary>

Virtual Servers can be deployed with virtual desktop environments, also known as **virtual desktop infrastructures** or VDIs, which provide developer workstations running either Linux or Windows. By using applications like [Parsec](https://parsec.app/) (for Windows machines) and [Teradici](https://www.teradici.com/) (for Linux), developers can log in to their workstations to access their work from anywhere!

</details>

{% hint style="success" %}
**Don't need a Virtual Server?**

If you've determined you don't need a Virtual Server, but want to leverage the performance benefits of running containerized workloads on CoreWeave Cloud, check out our documentation [on CoreWeave Kubernetes](broken-reference).
{% endhint %}
