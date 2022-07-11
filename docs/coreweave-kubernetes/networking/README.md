# Networking

CoreWeave's Cloud Native Networking is designed to provide high performance for compute intensive applications, while moving functionality traditionally found in centralized firewalls and load-balancers into the networking fabric. As many other things in CoreWeave Cloud, the networking fabric is designed around the Kubernetes network design principles, users with Kubernetes experience will feel right at home, and others will notice that the network stack removes all the need for IP address management, routing, VLAN management etc. These are all handled by the network layer, and concepts such as Services and Network Policies are used to segment access and expose applications to the Internet. For certain use-cases, i.e. when connecting to an on-premise environment via a VPN or direct-connect, or when deploying Telco applications in the cloud, a flat Layer 2 network is still preferred. This option is available as CoreWeave Layer 2 VPC.

### CoreWeave Cloud Native Networking (CCNN)

CCNN has routing, switching, firewalling and load-balancing built into the network fabric. It is designed to scale to 100Gbps+ with a completely decentralized design. All decisions happen intelligently in the network fabric allowing endless horizontal scaling of users' workloads. Network connectivity is equally efficient locally, as it is egressing to the Internet.

#### Workload Networking (Pod Networking)

This building block handles connectivity to each individual workload. Be it a Kubernetes Pod or a Virtual Machine (Virtual Server in CoreWeave terminology). This component automatically handles assigning ephemeral IP addresses to each workload. These IP addresses are private, and cannot be directly accessed from the internet. Workloads can also attach a static IP directly, as discussed further down. Workloads can reach the internet from their private ephemeral IPs, they reach the internet through Network Address Translation (NAT) built into the networking fabric. Servers on the internet will see connections initiated from the workload as originating from a pool of NAT IP addresses specific for the local datacenter.

#### Load Balancing (Service)

The Load Balancing Service exposes one or multiple workloads behind a static public or private IP. This is the primary method of exposing services to the world, alongside Ingresses that are specifically used for HTTP based applications. Services load-balance and forward a specific set of ports to all instances of the workload curently running and in a healthy status. The workloads maintain their ephemeral private IPs. If unfamiliar with load balancing concepts, the traffic is forwarded similar to a "port forward" in a traditional NAT firewall.

{% hint style="info" %}
[How to create Load Balancer Services ->](exposing-applications.md#public-services)
{% endhint %}

#### Direct Attach (Service)

A special condition where a static public or private IP from a Service is attached directly to a Workload. This setup is useful in cases where a wide range of ports would otherwise have to be load-balanced, or it is important for the Workload to see it's public IP as the IP on its virtual NIC. By nature of the direct attach, load balancing is no longer possible and it becomes a simple 1:1 mapping of workload to public IP. Unlike regular Workload Networking, servers on the internet will see connections initiated from the workload as originating from the Direct Attach IP.

{% hint style="info" %}
[How to Direct Attach an IP Address to Workloads ->](exposing-applications.md#attaching-service-ip-directly-to-pod)
{% endhint %}

#### Ingress Controller

[Ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/) provide an attractive option for HTTP(S) based applications where one or multiple application can be placed behind a hostname without needing to allocate individual public IPs. Ingresses support routing, and can be used to route different query paths to different backing microservices. They also provide automatic TLS, alleviating the need to configure TLS and certificates in the backend applications. CoreWeave provides a shared ingress with automatic certificate generation to quickly deploy secure HTTP endpoints.

{% hint style="info" %}
[How to create Ingresses ->](https://docs.coreweave.com/coreweave-kubernetes/networking/exposing-applications#ingress)
{% endhint %}

#### Service Discovery

All services are registered in CoreWeave internal DNS, and also optionally in public DNS records. A proper cloud-native application design never relies on hard-coded IPs, but instead uses the name of a Service to reach different applications. By using DNS names only, the same application can easily be deployed multiple times in different environments (namespaces) without updating statically configured IP addresses. External DNS is also available for generation of DNS names that are accessible from all over the internet.

{% hint style="info" %}
[How to create an External DNS record ->](https://docs.coreweave.com/coreweave-kubernetes/networking/exposing-applications#external-dns)
{% endhint %}

#### Network Policies (Firewalling)

Firewalling is built in to the network fabric. Each instance, be it a VM or a Pod has a firewall attached to it. This allows for granular control at a level not possible with traditional centralized firewalls. Traditionally, an administrator is forced to group workloads into different groups (ie. VLANs) and take action on only traffic between the groups, but without any control of traffic inside the group. With cloud native firewalling, users are encouraged to apply a zero-trust philosophy, where access is locked down between every instance by default, and only opened up as needed. The firewalling is configured using Kubernetes NetworkPolicies. These are stateful Layer 4 rules, which acts upon who or what initiated a connection. To describe what workloads to target with a rule, a label system is used. Much like with service discovery, staying away from hardcoded IPs is the goal and instead matching on workload names or label combinations decided by the user.

#### Multi-Region

CoreWeave's network fabric is multi-region, connectivity works the same way if all your workloads are in a single region or span multiple regions. Powerful technologies such as anycast (contact support for more info) can be used to route applications spanning multiple regions optimally.

### CoreWeave Layer 2 VPC (L2VPC)

{% hint style="danger" %}
Layer 2 VPC networks are coming soon to CoreWeave Cloud. Please contact your account manager or sales@coreweave.com for more information and timing
{% endhint %}

CoreWeave's Layer 2 VPC is vastly different from the CoreWeave Cloud Native Networking fabric. It removes many of the features in order to provide more control to the user, which might be preferred in specific use cases. Layer 2 VPC can be enabled on a workload by workload basis. A workload (Pod or VM) can have multiple interfaces, it can keep the regular CCNN interface as well as add on one or multiple VPC interfaces, or it can attach to L2VPC only.

#### Multi-Region vs. Single-Region

Layer 2 VPCs can be either Multi-Region, spanning all CoreWeave data centers, or Single-Region, local to a single data center. A Single-Region VPC can be converted to a Multi-Region and vice versa, however this does require a restart of all workloads. A single workload can attach up to 10 L2VPCs at the same time, in addition to the regular CCNN network.

#### IP Addressing

In Layer 2 VPC, IP addressing happens using traditional Static IP or DHCP. CoreWeave provides an out-of-the-box DHCP server managed via CoreWeave Apps that allows static reservations via Workflow labels. The user can also choose to fully control IP addressing without any CoreWeave tools.

#### Routing

Each Layer 2 VPC is a flat non-blocking Layer 2 network. There is no routing built in. If the user desires to have routing between Layer 2 VPCs, or routing between Layer 2 VPCs and the Internet / CCNN, a virtual router/firewall will need to be deployed by the user. Please note that this virtual router/firewall will act as a choke point and add an extra hop to the path. When possible, it is recommended to keep a CCNN interface on the workload to use for Internet access instead of routing via a virtual router / firewall. This ensures lowest possible latency and highest Internet throughput.

#### Network Policies (Firewalling)

The fabric based firewall that exists around every workload in the regular Coreweave Cloud Native Networking is bypassed in Layer 2 VPC. Users are encouraged to setup firewalling inside Virtual Machines (Virtual Servers) to follow the zero-trust philosophy. Virtual routers / firewalls can be leveraged to provide firewalling between L2VPCs, and L2VPCs and the Internet if the L2VPC is used as the only egress.

#### Performance

The Layer 2 VPC is implemented using SR-IOV inside Virtual Machines and Kubernetes Pods. This provides full bare-metal performance with no additional software layers in the path. The L2VPC supports a MTU up to 9000, which can be beneficial for storage intensive applications.

#### When should I use Layer 2 VPC?

CoreWeave Cloud Native Networking is designed to be the preferred choice for most use-cases. Layer 2 VPC should only be considered if one or multiple of the following criteria is fulfilled:

* A Site to Site connection is needed to an on-premise environment, and that on-premise environment is a private network with custom private IP addressing.
* Specific firewall or routing requirements that can not be achieved in any other way, i.e. via a web-filtering proxy and Network Policies.
* Specific high-performance storage or communication requirements inside Virtual Machines (Virtual Servers) where a high MTU hardware NIC will provide concrete benefits.

### Site to Site Connectivity

It is a common desire to connect private on-premise networks with CoreWeave Cloud. For production applications, especially where latency and bandwidth is a concern, we always recommend a physical direct-connect. CoreWeave's data centers and cloud on-ramps are centrally located and well connected, making it easy to establish direct connections to on-premise environments.

#### Site to Site VPN

Site to Site VPNs are provided by instantiating a virtual firewall in a Layer 2 VPC. Each workload needing access to the Site to Site VPN should be placed into the VPC in addition to the regular CoreWeave networking. The IPSEC VPN has been benchmarked to over 5Gbps. Please note that most on-premise firewalls and cloud firewalls on other cloud-providers are rarely rated for over 1Gbps of IPSEC performance.

#### [Direct Connect](./#direct-connect)

Direct Connect is available by working with your connectivity provider to bring a physical connection to one of our data centers or cloud on-ramps. A direct connect can also be established instantly via Megaport. Please contact support for more information. We support Direct Connects with bandwidth between 1Gbps and 100Gbps. The default configuration for a Direct Connect is a Layer 3 connection into a Layer 2 VPC, however the Layer 2 VPC can be extended over the Direct Connect to create a flat Layer 2 connection all the way to the customer premises.
