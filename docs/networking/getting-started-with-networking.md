---
description: Learn about networking options on CoreWeave.
---

# Getting Started with Networking

## Exposing applications

[Kubernetes Workloads](https://kubernetes.io/docs/concepts/workloads/) can be exposed to each other, but they can also be publicly exposed to the Internet using [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/) and [Ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/).

A Service allocates a dedicated IP address for the exposed application, whereas an Ingress works for HTTP-based protocols to alleviate the need for a separate IP at each endpoint.

{% hint style="info" %}
**Additional Resources**

Learn more about how to expose your applications using Kubernetes Ingresses and Services in [our Exposing Applications guide](layer-2-vpc-l2vpc/exposing-applications.md).
{% endhint %}

## Networking solutions

CoreWeave offers three primary networking solutions, which are often used in combination:

### [CCNN: CoreWeave Cloud Native Networking](../coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md)

:white\_check\_mark: **Ideal for most use cases.**

CoreWeave's Cloud Native Networking is designed to provide high performance for compute-intensive applications, while moving functionality traditionally found in centralized firewalls and load-balancers directly into the networking fabric.

As many other things in CoreWeave Cloud, the networking fabric is designed around the Kubernetes network design principles. Users with Kubernetes experience will feel right at home, and others will notice that the network stack removes all the need for IP address management, routing, VLAN management, and so on.

These are all handled by the network layer, and concepts such as Services and Network Policies are used to segment access and expose applications to the Internet.

{% hint style="info" %}
**Additional Resources**\
****[Read more in our CoreWeave Cloud Native Networking (CCNN) documentation.](../coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md)
{% endhint %}

### [L2VPC: CoreWeave Layer 2 VPC](../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/)

:white\_check\_mark: **Ideal for the following use cases:**

* Connecting to an on-premise environment via a [Site-to-Site VPN](../coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/) or [Direct Connect](../coreweave-kubernetes/networking/site-to-site-connections/direct-connections.md)
* Deploying Telco applications in the Cloud
* Other niche networking use cases

**CoreWeave's Layer 2 VPC (L2VPC)** is vastly different from the [CoreWeave Cloud Native Networking (CCNN)](../coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md) fabric. Most notably, many of the extended networking features built in to CCNN - such as network policies and Kubernetes loadbalancing - are not present in an L2VPC, in order to provide more control to the user.

The L2VPC is enabled on a workload by workload basis. A workload (a Pod or Virtual Server) can have multiple interfaces - it can maintain a CCNN interface as well as one or multiple VPC interfaces, or it can attach to L2VPC exclusively.

{% hint style="info" %}
**Additional Resources**

Read more in [our L2VPC documentation](../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/).
{% endhint %}

### [**HPC Interconnect**](../coreweave-kubernetes/networking/hpc-interconnect.md)****

****:white\_check\_mark: **Ideal for the following use cases:**

* Multi-node distributed Deep Neural Network Training
* Multi-node HPC applications

**HPC Workloads** are first-class tenants on CoreWeave Cloud. Customers leverage the wide range of GPU availability and seamless access to scale to run parallel jobs, with thousands to tens of thousands of GPUs working together in areas such as Neural Net Training, Rendering and Simulation.

In these applications, connectivity between compute hardware as well as storage play a major role in overall system performance. CoreWeave provides highly optimized IP-over-Ethernet connectivity across all GPUs and an industry-leading, non-blocking InfiniBand fabric for our top-of-the-line A100 NVLINK GPU fleet.

{% hint style="info" %}
**Additional Resources**

Read more in our [HPC Interconnect documentation](../coreweave-kubernetes/networking/hpc-interconnect.md).
{% endhint %}
