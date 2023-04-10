---
description: Learn about CoreWeave Cloud Native Networking (CCNN).
---

# CoreWeave Cloud Native Networking (CCNN)

## Introduction

With CoreWeave Cloud Native Networking (CCNN), routes, switches, firewalls, and load-balancing are built right into the network fabric.

CCNN is designed to scale to **100Gbps+** with a completely decentralized design. All decisions happen intelligently in the network fabric, allowing for endless horizontal scaling of users' workloads. Network connectivity is equally as efficient locally as it is egressing to the Internet.

### Use cases

CCNN is designed to be the **preferred choice** for **most use-cases**. Only specific use cases requiring greater control may require a a [Layer 2 VPC (L2VPC)](../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/).

## CCNN Features

### Workload Networking (Pod Networking)

This component handles network connectivity to each individual workload. Whether it's a Kubernetes Pod or a Virtual Machine, this component automatically handles assigning ephemeral IP addresses to each workload.

Assigned IP addresses are private, and cannot be directly accessed from the Internet without some manner of ingress. However, Network Address Translation (NAT) built into the networking fabric allows workloads to reach the Internet one-directionally.

{% hint style="info" %}
**Note**

Workload connections will appear to originate from a pool of NAT IP addresses, which are specific to the host datacenter.
{% endhint %}

### Load Balancing (Service)

{% hint style="info" %}
**Additional Resources**

Learn how to create a Load Balancing Service in [Exposing Applications: Public Services](../coreweave-kubernetes/exposing-applications.md#public-services).
{% endhint %}

The **Load Balancing Service** exposes one or multiple Workloads behind a static IP, either public or private. At the same time, workloads maintain their ephemeral private IPs.

This is the primary method of exposing services to the world, alongside Ingresses, which are specifically used for HTTP-based applications. Services are used to load-balance traffic and forward a specific set of ports to all instances of the Workload that are currently running with a healthy status.

{% hint style="info" %}
**Note**

If you are unfamiliar with load balancing concepts, it may help to understand that the traffic is forwarded, similar to the kind of port forwarding found in a traditional NAT firewall.
{% endhint %}

### Direct Attach (Service)

{% hint style="info" %}
**Additional Resources**

Learn how to create a load balancing service in [Attaching a Service IP directly to a Pod](https://docs.coreweave.com/coreweave-kubernetes/networking/exposing-applications#attaching-service-ip-directly-to-pod).
{% endhint %}

When a Service is attached to a pod through the **Direct Attach** method, a public or private IP from [a Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services) is attached directly to a Workload.

This choice is useful in cases where a wide range of ports would otherwise have to be load-balanced, or in cases where it is important for the Workload to see its public IP as the IP on its virtual NIC.

In a Direct Attach scenario, load-balancing is no longer possible. Connections are made using a 1:1 mapping of Workload to static public IP. Unlike regular Workload Networking, servers on the internet will see connections initiated from the workload as originating from the Direct Attach IP.

### Ingress Controller

[Ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/) provide an attractive option for HTTP(S) based applications where one or multiple application can be placed behind a hostname without needing to allocate individual public IPs. Ingresses support routing, and can be used to route different query paths to different backing microservices.

Ingresses also provide automatic TLS, alleviating the need to configure TLS certificates in backend applications. CoreWeave provides a shared Ingress with automatic certificate generation to quickly deploy secure HTTP(S) endpoints.

{% hint style="info" %}
**Additional Resources**\
Learn more in [How to create Ingresses](https://docs.coreweave.com/coreweave-kubernetes/networking/exposing-applications#ingress).
{% endhint %}

### Service Discovery

All services are registered in the CoreWeave internal DNS, and also optionally in public DNS records. A proper Cloud-native application design never relies on hard-coded IPs, but instead uses the name of a Service to reach different applications. By using DNS names only, the same application can easily be deployed multiple times in different environments (namespaces) without updating statically configured IP addresses. External DNS is also available for generation of DNS names that are accessible from all over the internet.

{% hint style="info" %}
**Additional Resources**\
Learn more in [How to create an External DNS record](https://docs.coreweave.com/coreweave-kubernetes/networking/exposing-applications#external-dns).
{% endhint %}

### Network Policies (Firewalls)

Network policies are built into the network fabric. Each instance, be it a VM or a Pod, has a firewall attached to it. This allows for granular control at a level not possible with traditional centralized firewalls. Traditionally, an administrator is forced to group workloads into different groups (i.e., VLANs) and take action only on traffic _between_ the groups, but without any control of traffic _inside_ the group.

With Cloud native firewalls, users are encouraged to apply a zero-trust philosophy, where access is locked down between every instance by default, and only allowed as needed. Firewalls are configured using [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/). These are stateful, Layer 4 rules, which act upon whoever or whatever initiated a connection.

To describe what workloads to target with a rule, a label system is used. Much like with service discovery, staying away from hardcoded IPs is the goal and instead matching on workload names or label combinations decided by the user.

### Multi-Region

CoreWeave's network fabric is **multi-region**. This means that connectivity works the same way if all your workloads are in a single region or span multiple regions. Powerful technologies such as [anycast](https://en.wikipedia.org/wiki/Anycast) can be used to optimally route applications spanning multiple regions.
