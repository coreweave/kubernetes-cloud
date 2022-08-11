---
description: >-
  Learn how to attach Layer 2 VPCs to Kubernetes Pods and Virtual Servers on
  CoreWeave Cloud.
---

# L2VPC Usage

## Usage with Pods

To connect a Pod to a Layer 2 VPC, a Kubernetes annotation is used. A Pod can be attached to one or multiple VPC as well as the regular CoreWeave Cloud Native Kubernetes network. Each VPC will be represented as a separate network interface inside the Pod, in addition to the regular pod network. The VPCs are listed in the annotation separated by commas.

<pre class="language-yaml"><code class="lang-yaml"><strong>annotations:
</strong><strong>    vpc.coreweave.cloud/name: &#x3C;your-vpc-name>,&#x3C;optional-second-vpc></strong></code></pre>

By default, CoreWeave Cloud Native Kubernetes Pod networking is enabled. To disable Kubernetes Pod networking, add the following annotation:

```yaml
annotations:
    vpc.coreweave.cloud/kubernetes-networking: false
```

{% hint style="danger" %}
**Warning**

CoreWeave Cloud Native Networking is designed with low latency and high isolation in mind. Even when a VPC is in use, it is recommended to leave the regular networking attached for Internet access while leveraging the VPC interface for things like on-premise connectivity.

Additionally, disabling CoreWeave Cloud Native Networking means loss of all regular Kubernetes networking functionality, such as Services, Load Balancers and internet access. The Pod will only be able to communicate on the specified VPCs. For internet access, a virtual firewall can be deployed bridging a VPC and a regular CCNN interface. For most Kubernetes use cases, it is not recommended to disable the standard network.

****[**CoreWeave support**](https://cloud.coreweave.com/contact) **is available to help with any network design questions.**
{% endhint %}

## Usage with Virtual Servers

Virtual Server Layer 2 VPC connections are configured inside the `network` stanza in the Virtual Server spec, as shown below.

A Virtual Server can be attached to one or multiple VPCs, as well as the regular CoreWeave Cloud Native Kubernetes network. Each VPC will be represented as a separate Network Interface Card (NIC) inside the Virtual Server in addition to the regular CoreWeave network. The NICs inside a Virtual Server will be in the same order as the VPCs specified - ordering is deterministic to ensure that a NIC inside the Virtual Server always connects to the same VPC, even through reboots and migrations.

**Example**

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: my-vs-in-a-vpc
  namespace: tenant-coreweave-example
spec:
  network:
    disableK8sNetworking: false
    vpcs:
    - name: your-vpc-name
    - name: optional-second-vc
```

{% hint style="success" %}
**Tip**

The VPC NICs inside a Virtual Server are based on SR-IOV technology. SR-IOV allows secure hardware passthrough of a hardware NIC into a Virtual Machine. CoreWeave implements VPC with SR-IOV to provide bare-metal networking performance inside Virtual Machines.
{% endhint %}

By default, CoreWeave Cloud Native Networking is **enabled**. To disable CoreWeave networking, set `disableK8sNetworking` to `true`. Please see the warning above about the functionality that is lost when regular networking is disabled.

**Example**

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: my-vs-in-a-vpc
  namespace: tenant-coreweave-example
spec:
  network:
    disableK8sNetworking: true
    vpcs:
    - name: your-vpc-name
    - name: optional-second-vc
```
