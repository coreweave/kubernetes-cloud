---
description: Learn about networking options on CoreWeave.
---

# Getting Started with Networking

## Introduction

CoreWeave offers three primary networking solutions, often used in combination.

### [CoreWeave Cloud Native Networking (CCNN)](../coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md)

<mark style="background-color:green;">****</mark>:white\_check\_mark: **Ideal for most use cases.**

CoreWeave's Cloud Native Networking is designed to provide high performance for compute-intensive applications, while moving functionality traditionally found in centralized firewalls and load-balancers directly into the networking fabric.

As many other things in CoreWeave Cloud, the networking fabric is designed around the Kubernetes network design principles. Users with Kubernetes experience will feel right at home, and others will notice that the network stack removes all the need for IP address management, routing, VLAN management, and so on.

These are all handled by the network layer, and concepts such as Services and Network Policies are used to segment access and expose applications to the Internet.

{% hint style="info" %}
**Additional Resources**\
****[Read more in our CoreWeave Cloud Native Networking (CCNN) documentation.](../coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md)
{% endhint %}

### [CoreWeave Layer 2 VPC (L2VPC)](../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/)

****:bulb: **Ideal for:**

* Connecting to an on-premise environment via a [Site-to-Site VPN](getting-started-with-networking.md#site-to-site-vpn) or [Direct Connect](../coreweave-kubernetes/networking/site-to-site-connections/direct-connections.md).
* Deploying Telco applications in the Cloud.
* Other niche networking use cases.

{% hint style="info" %}
**Additional Resources**

Read more in [our L2VPC documentation](../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/).
{% endhint %}

### ****[**HPC Interconnect**](getting-started-with-networking.md#undefined)****

:bulb: **Ideal for:**

* Multi-node distributed Deep Neural Network Training
* Multi-node HPC applications
