---
description: >-
  Learn how to attach Layer 2 VPCs to Kubernetes Pods and Virtual Servers on
  CoreWeave Cloud.
---

# L2VPC Usage

## Usage with Pods

To connect a Pod to a Layer 2 VPC an annotation is used. A Pod can be attached to one or multiple VPC as well as the regular CoreWeave Cloud Native Kubernetes network. Each VPC will be represented as a separate network interface inside the Pod in addition to the regular pod network. The VPCs are listed in the annotation separated by commas.

<pre class="language-yaml"><code class="lang-yaml"><strong>annotations:
</strong><strong>    vpc.coreweave.cloud/name: &#x3C;your-vpc-name>,&#x3C;optional-second-vpc></strong></code></pre>

By default, CoreWeave Cloud Native Kubernetes Pod networking is enabled. To disable Kubernetes Pod networking, add the following annotation:

```yaml
annotations:
    vpc.coreweave.cloud/kubernetes-networking: false
```

{% hint style="info" %}
**Note**

Kubernetes Pod networking can be used together with Layer 2 VPC networking - they are not mutually exclusive.
{% endhint %}

{% hint style="warning" %}
**Warning**

Disabling CoreWeave Cloud Native Networking means loss of all regular Kubernetes networking functionality, such as Services, Load Balancers and internet access. The Pod will only be able to communicate on the specified VPCs. For internet access, a virtual firewall can be deployed bridging a VPC and a regular CCNN interface. For most Kubernetes use cases, it is not recommended to disable the standard network.

CoreWeave support is available to help with any network design questions.
{% endhint %}

## Usage with Virtual Servers

To connect a Virtual Server to a Layer 2 VPC, a section under `networking` in the Virtual Server spec is used.

A Virtual Server can be attached to one or multiple VPC as well as the regular CoreWeave Cloud Native Kubernetes network. Each VPC will be represented as a separate Network Interface Card (NIC) inside the Virtual Server in addition to the regular CoreWeave network. The NICs inside a Virtual Server will be in the same order as VPCs specified. The ordering is deterministic to ensure that a NIC inside the VS always connects to the same VPC, even over reboots and migrations.

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
The VPC NICs inside a Virtual Server are based on SR-IOV technology. SR-IOV allows secure hardware passthrough of a hardware NIC into a Virtual Machine. CoreWeave implements VPC with SR-IOV to provide bare-metal networking performance inside Virtual Machines.
{% endhint %}

By default, CoreWeave Cloud Native Networking is enabled. To disable CoreWeave networking, set `disableK8sNetworking` to `true`. Please see warning above about functionality that is lost when regular networking is disabled.

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

{% hint style="warning" %}
**Warning**

CoreWeave Cloud Native Networking is designed with low latency and high isolation in mind. Even when VPC is in use, it is recommended to leave the regular networking attached for internet access while leveraging the VPC interface for things line on-premise connectivity.
{% endhint %}
