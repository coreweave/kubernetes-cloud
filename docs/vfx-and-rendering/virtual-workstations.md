---
description: Create Virtual Workstations on CoreWeave Cloud
---

# Virtual Workstations

## Get started with Virtual Workstations

Virtual Workstations reduce the burden of maintaining on-premise infrastructure and improve artist workflows, resulting in greater productivity, less strain on your team, and a better end-product for your clients. Virtual Workstations allow artists across the world to easily access applications that require high-powered CPU and GPU acceleration.

Virtual Workstations are deployed on top of the open source project [Kubevirt](https://kubevirt.io/). The `virtctl` tool may be used for fine-grained control over Virtual Servers.

{% hint style="success" %}
**Tip**

Virtual Workstations are specialized [Virtual Servers](broken-reference). Before continuing, it may be helpful to [learn a bit more about Virtual Servers](broken-reference), or a bit more about how to leverage `virtctl` for fine-grained control over Virtual Workstations.
{% endhint %}

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-card-cover data-type="files"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Get Started with Virtual Servers</strong></td><td>Virtual Workstations are specialized Virtual Servers. It may be useful to learn more about Virtual Servers – what they are, how they work, and how to create them.</td><td></td><td><a href="../.gitbook/assets/virtualservers.jpeg">virtualservers.jpeg</a></td><td><a href="../../virtual-servers/getting-started.md">getting-started.md</a></td></tr><tr><td><strong>Manage Virtual Workstations using <code>virtctl</code></strong></td><td>The <a href="https://kubevirt.io/user-guide/operations/virtctl_client_tool/"><code>virtctl</code> tool</a> may be used to remotely manage Virtual Workstations. If you require more fine-grained control over your Virtual Workstations, refer to the <a href="../../virtual-servers/remote-access-and-control.md">Remote Access and Control guide</a>.</td><td></td><td><a href="../.gitbook/assets/kubevirt.png">kubevirt.png</a></td><td><a href="../../virtual-servers/remote-access-and-control.md">remote-access-and-control.md</a></td></tr></tbody></table>

### Operating Systems

Virtual Workstations may be configured to run a variety of [Operating Systems and OS add-ons](../virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md) for virtual desktop environments. Workstations can be provisioned with GPUs or may be provisioned as CPU-only instances.

CoreWeave offers a variety of CPUs, including AMD EPYC and Intel Xeon solutions. You can learn more about pricing and configuration in [our CPU-Only Instance Pricing guide](../../resources/resource-based-pricing.md#cpu-only-instance-resource-pricing).

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Create a Virtual Workstation</td><td></td><td></td><td><a href="how-to-guides-and-tutorials/create-a-virtual-workstation/">create-a-virtual-workstation</a></td></tr></tbody></table>

## Thinkbox Deadline

CoreWeave Cloud Workstations support running managed instances of [Thinkbox Deadline](https://www.awsthinkbox.com/deadline), the most responsive modern render management solution for accessing render nodes and automatic workload scaling.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Deploy a Thinkbox Deadline instance</td><td></td><td></td><td><a href="how-to-guides-and-tutorials/vfx-studio-components-guide/deadline.md">deadline.md</a></td></tr></tbody></table>
