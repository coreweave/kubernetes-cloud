---
description: Learn about CoreWeave's Layer 2 VPC (L2VPC).
---

# Layer 2 VPC (L2VPC)

## Introduction

**CoreWeave's Layer 2 VPC (L2VPC)** is vastly different from the [CoreWeave Cloud Native Networking (CCNN)](../coreweave-cloud-native-networking-ccnn.md) fabric. Most notably, many of the extended networking features built in to CCNN - such as network policies and Kubernetes loadbalancing - are not present in an L2VPC, in order to provide more control to the user.

The L2VPC is enabled on a workload by workload basis. A workload (a Pod or Virtual Server) can have multiple interfaces - it can keep the regular CCNN interface, as well as add on one or multiple VPC interfaces, or it can attach to L2VPC only.

Multiple VPCs can also be allocated to simulate the multiple VLANs (network segments) found in a traditional on-premise network.

### Use cases

[CoreWeave Cloud Native Networking (CCNN)](../coreweave-cloud-native-networking-ccnn.md) is designed to be **the preferred choice for most use-cases**. L2VPC should **only** be considered if one or multiple of the following criteria is fulfilled:

* A Site to Site connection is needed to an on-premise environment, and that on-premise environment is a private network with custom private IP addressing.
* There are specific firewall or routing requirements that can not be achieved any other way, such as via a Web-filtering proxy or Network Policies.&#x20;
* There are specific high-performance storage or communication requirements inside the Virtual Servers where a high MTU hardware NIC will provide concrete benefits.

## L2VPC Features

### :globe\_with\_meridians: Multi-Region or Single-Region

L2VPCs can be either **Multi-Region** - spanning all CoreWeave data centers - or **Single-Region**, **** local to a single data center.

A Single-Region VPC can be converted to a Multi-Region and vice versa, however this does require a restart of all workloads.

A single workload can attach up to ten (10) L2VPCs at the same time, in addition to the regular CCNN network.

### :round\_pushpin:IP Addressing

In L2VPC, IP addressing happens either by using traditional Static IPs, or by using DHCP.

CoreWeave provides an out-of-the-box DHCP server managed via CoreWeave Apps (**dhcp-server**) that allows for dynamic and static IP allocation via Workflow labels. Alternatively, IP addressing can be controlled without any CoreWeave tools and provided by a customer managed virtual firewall.

{% hint style="info" %}
**Additional Resources**

Review our documentation on [DHCP in VPCs](dhcp-on-l2vpc.md) for more information.
{% endhint %}

### :map: Routing

Each L2VPC is a flat, non-blocking Layer 2 network. There is no built-in routing capability. If the user desires to have routing between Layer 2 VPCs, or routing between Layer 2 VPCs and the Internet or CCNN, a virtual router (firewall) will need to be deployed by the user.

{% hint style="warning" %}
**Important**

A virtual router (firewall) will act as a choke point by adding an extra hop to the networking path. When possible, it is recommended to keep a CCNN interface on the workload to use for Internet access instead of routing via a virtual router. This ensures the lowest possible latency and highest Internet throughput.
{% endhint %}

### :fire: Network Policies (Firewalls)

In L2VPC, the fabric-based firewall that exists around every workload in CCNN is **bypassed**.

Users are encouraged to setup firewall rules inside Virtual Servers so as to adhere to a zero-trust security policy. Virtual routers (firewalls) can be leveraged to provide firewalls between L2VPCs, and between L2VPCs and the Internet **if the L2VPC is used as the only egress.**

### :muscle: Performance

L2VPC is implemented using SR-IOV inside Virtual Machines and Kubernetes Pods. This provides full bare-metal performance with no additional software layers in the path. The L2VPC supports a MTU up to 9000, which can be beneficial for storage intensive applications.

### :electric\_plug:Site-to-Site Connectivity

A common use case involves connecting between a private on-premise network and CoreWeave Cloud. CoreWeave offers two primary methods to achieve this goal.

{% hint style="info" %}
**Note**

For production applications, especially where latency and bandwidth is a concern, we always recommend a [**physical Direct Connect**](../site-to-site-connections/direct-connections.md). CoreWeave's data centers and Cloud on-ramps are centrally located and well connected, making it easy to establish direct connections to on-premise environments.
{% endhint %}

#### [Site-to-Site VPN](./#site-to-site-vpn)

**Site-to-Site VPNs** are provided by instantiating a **Virtual VPN** in an L2VPC.

{% hint style="info" %}
**Additional Resources**

Learn more about Site-to-Site VPNs in our [Site-to-Site VPN guide](./#site-to-site-vpn).
{% endhint %}

#### [Direct Connect](./#direct-connect)

**Direct Connect** is available by working with your connectivity provider to bring a physical connection to one of our data centers or Cloud on-ramps.

A direct connection can also be established instantly via Megaport. We support Direct Connects with bandwidth between 1Gbps and 100Gbps.

The default configuration for a Direct Connect is a Layer 3 connection into a Layer 2 VPC, however the Layer 2 VPC can be extended over the Direct Connect to create a flat Layer 2 connection all the way to the customer premises.

{% hint style="success" %}
**Tip**

&#x20;Please [contact support](https://cloud.coreweave.com/contact) for more information and to enable L2VPC in your namespace.
{% endhint %}
