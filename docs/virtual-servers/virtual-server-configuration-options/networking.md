---
description: Learn more about network options for Virtual Servers.
---

# Networking

Networking for Virtual Servers can be as simplistic or as fine-grained as your use case dictates. If you'd like to attach a Public IP or LoadBalancer IP to your Virtual Server, this is the section to do it.

{% hint style="info" %}
**Additional Resources**

To learn more about networking on CoreWeave cloud, see [Networking](broken-reference).
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, click the **Network** expandable.

<figure><img src="../../.gitbook/assets/network.png" alt=""><figcaption></figcaption></figure>

### Attaching IPs

More advanced networking options for Virtual Servers are configured by interacting directly with the YAML editor, but **Public IP** and **LoadBalancer IP** configuration options are also exposed via graphical toggles in this expandable. These toggles are switched on and off according to whether or not you want the Virtual Server to have either kind of IP address provisioned to it.

Attaching a **Public IP** to the Virtual Server will allow it to be accessible through the Internet via an assigned IPv4 address by a created Kubernetes service. When `network.directAttachLoadBalancerIP` is turned on (`true`) a new Service will be created, and its LoadBalancer IP will be directly attached to the Virtual Server.

The graphical toggles affect the `network.directAttachLoadBalancerIP` and `.network.public` options in the CRD manifest respectively, toggling their values between `true` and `false`.\
\
When both options are set to `true`, public networking is provided via an automatically-provisioned public IP address. When both are `false`, public networking is disabled, and no public IP will be provisioned.

<figure><img src="../../.gitbook/assets/image (24) (2).png" alt=""><figcaption></figcaption></figure>

Example in plain text:

```yaml
  network:
    public: true
    directAttachLoadBalancerIP: true
```

{% hint style="info" %}
**Note**

When both `network.directAttachLoadBalancerIP` and `network.public` are set to `false`, the Virtual Server Operator (VSO) creates a "[Headless Service](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)," in order to resolve internal DNS using cluster DNS.

When `network.directAttachLoadBalancerIP` is set to `true`, custom UDP and TCP ports may **not** be set.
{% endhint %}

### Additional networking options

All other networking options for Virtual Servers provisioned through the CoreWeave Cloud UI must be configured through the YAML manifest.

#### Custom MAC addresses

By default, a persistent MAC address, derived from the Virtual Server's name, is assigned to the Virtual Server. To override this, you may include MAC address configurations in the `.network.macAddress` field.

Custom MAC addresses for Virtual Servers are configured with dashes separating each octet:

```yaml
macAddress: A2-1F-EE-09-06-5D
```

#### DNS policy

DNS policies for Virtual Servers refer to the [Kubernetes Pod DNS policies](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy). By default, Virtual Servers have a DNS policy of `ClusterFirst`.

#### TCP and UDP ports

The TCP and UDP ports to expose on the Virtual Server are configured using the `tcp.ports` and `udp.ports` lists in the YAML manifest respectively.

{% hint style="info" %}
**Note**

When `network.directAttachLoadBalancerIP` is set to `true`, custom UDP and TCP ports may not be set.
{% endhint %}

Desired ports may be configured in their respective lists, as seen in this example:

<figure><img src="../../.gitbook/assets/image (56) (4).png" alt=""><figcaption></figcaption></figure>

Example in plain text:

```yaml
  network:
    public: true
    directAttachLoadBalancerIP: false
    tcp:
      ports:
        - 22
        - 443
        - 3389
    udp:
      ports:
        - 3389
        - 4172
```

#### Floating IPs

Floating IPs allow stable IP addresses to be assigned from the load balancer IP of each Service. These allow for custom DNS configurations, and predictable addressing.

Floating IPs can be specified in the YAML manifest using a YAML list:

```yaml
floatingIPs: [240.141.77.141, 82.110.59.244]
```

{% hint style="info" %}
**Additional Resources**

Learn more about [Floating Services](additional-features.md#floating-services).
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

To configure networking options for Virtual Servers deployed using the Kubernetes CLI, configure the options under the `network` stanza of the `spec`:

```yaml
  network:
    public: true
    tcp:
      ports:
        - 22
```

The table below describes all available configuration options for user accounts on Virtual Servers:

<table><thead><tr><th width="275.66666666666663">Field name</th><th width="150">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>network.floatingIPs</code></td><td>[]</td><td>A list of service references to be added as floating IPs. <a href="additional-features.md#floating-services"><em>Learn more about Floating IPs</em></a><em>.</em></td></tr><tr><td><code>network.floatingIPs[ ].serviceName</code></td><td>String</td><td>Name of the service</td></tr><tr><td><code>network.tcp</code></td><td>{}</td><td>Defines the TCP network configuration</td></tr><tr><td><code>network.tcp.ports</code></td><td>[]</td><td>List of TCP ports to expose</td></tr><tr><td><code>network.udp</code></td><td>{}</td><td>Defines the UDP network configuration</td></tr><tr><td><code>network.udp.ports</code></td><td>[]</td><td>List of UDP ports to expose</td></tr><tr><td><code>network.public</code></td><td>Boolean</td><td>Whether a public IP will be assigned</td></tr><tr><td><code>network.macAddress</code></td><td>String</td><td>Set MAC address for VS. If not provided, Virtual Server generates a unicast/local type MAC address</td></tr><tr><td><code>network.dnsConfig</code></td><td><a href="https://pkg.go.dev/k8s.io/api/core/v1#PodDNSConfig">PodDNSConfig</a></td><td>Defines the DNS parameters of the VS. Defult value is <a href="https://pkg.go.dev/k8s.io/kubernetes/pkg/apis/core#DNSPolicy">DNSClusterFirst</a>.</td></tr><tr><td><code>network.dnsPolicy</code></td><td><a href="https://pkg.go.dev/k8s.io/api/core/v1#DNSPolicy">DNSPolicy</a></td><td>Set the DNS policy for VS. The default value is <code>ClustrFirst</code></td></tr></tbody></table>

### Floating IPs

Floating IPs allow the provisioning of stable IP addresses, assigned from the load balancer IP of each Service. These allow for custom DNS configurations and predictable addressing.

Floating IPs can be specified in the YAML manifest as an array:

```yaml
network: 
  floatingIPs: [240.141.77.141, 82.110.59.244]
```

{% hint style="info" %}
**Additional Resources**

Learn more about [Floating IPs](additional-features.md#floating-ips).
{% endhint %}
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

The Virtual Server's networking options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).

The table below describes all available configuration options for user accounts on Virtual Servers.

<table><thead><tr><th width="301.42613833223936">Variable name</th><th width="150">Variable type</th><th width="260.5496313102666">Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>vs_public_networking</code></td><td>Boolean</td><td>Whether or not to allow the Virtual Server to be publicly accessible to the Internet.</td><td><code>true</code></td></tr><tr><td><code>vs_attach_loadbalancer</code></td><td>Boolean</td><td> Whether or not to attach a Service LoadBalancer IP directly to the Virtual Server.<br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong><code>vs_tcp_ports</code> and <code>vs_udp_ports</code> must be empty.</strong></td><td><code>false</code></td></tr><tr><td><code>vs_tcp_ports</code></td><td>List</td><td>Which TCP ports to expose on the Virtual Server.</td><td><code>[22, 443, 60443, 4172, 3389]</code></td></tr><tr><td><code>vs_udp_ports</code></td><td>List</td><td>Which UDP ports to expose on the Virtual Server.</td><td><code>[4172, 3389]</code></td></tr></tbody></table>

Terraform example:

```json
variable "vs_public_networking" {
  default = true
}

variable "vs_attach_loadbalancer" {
  description = "Attach Service LoadBalancer IP directly to VS (vs_tcp_ports and vs_udp_ports must be empty)."
  default     = false
}

variable "vs_tcp_ports" {
  type    = list(any)
  default = [22, 443, 60443, 4172, 3389]
}

variable "vs_udp_ports" {
  type    = list(any)
  default = [4172, 3389]
}
```
{% endtab %}
{% endtabs %}

## Attaching a Layer 2 VPC

A Virtual Server may be attached to one or multiple VPCs, as well as to the regular [CoreWeave Cloud Native Kubernetes](../../networking/coreweave-cloud-native-networking-ccnn.md) (CCNN) network.

Each VPC will be represented as a separate Network Interface Card (NIC) inside the Virtual Server, in addition to the CoreWeave network (CCNN). The NICs inside a Virtual Server will be in the same order as the VPCs are specified - the order is deterministic to ensure that a NIC inside the Virtual Server always connects to the same VPC, even through reboots and migrations.

{% hint style="info" %}
**Additional Resources**

Learn more about[ CoreWeave Layer 2 VPCs](../../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/).
{% endhint %}

By default, [CoreWeave Cloud Native Networking](../../networking/coreweave-cloud-native-networking-ccnn.md) is **enabled**. To disable CoreWeave networking, set `disableK8sNetworking` to `true`.

{% hint style="danger" %}
**Warning**

CoreWeave Cloud Native Networking is designed with low latency and high isolation in mind. Even when a VPC is in use, it is recommended to leave the regular networking attached for Internet access while leveraging the VPC interface for things like on-premise connectivity.

Additionally, disabling CoreWeave Cloud Native Networking means loss of all regular Kubernetes networking functionality, such as Services, Load Balancers and internet access. The Pod will only be able to communicate on the specified VPCs. For internet access, a virtual firewall can be deployed bridging a VPC and a regular CCNN interface. For most Kubernetes use cases, it is not recommended to disable the standard network.

Also note that if disableK8sNetworking is set to `true` and a VPC is designated, no k8s (paravirtual) NIC will be attached - only the VPC will be attached.

[**CoreWeave support**](https://cloud.coreweave.com/contact) **is available to help with any network design questions.**
{% endhint %}

[Layer 2 VPCs](../../coreweave-kubernetes/networking/layer-2-vpc-l2vpc/) may be attached to Virtual Servers using the following methods:

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

VPCs that are deployed in the client namespace are associated with Virtual Servers by configuring their addresses within the YAML spec of the Virtual Server to be associated.

VPC names are configured inside the `.network.vpcs` stanza in the YAML manifest:

```yaml
network:
  vpcs: []
    - name: vpc0
    - name: vpc1
  # If disableK8sNetworking is set to `true` and a VPC is defined, no k8s (paravirtual) NIC will be attatched
  disableK8sNetworking: false
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Using Kubernetes, Virtual Server Layer 2 VPC connections are configured inside the `spec.network.vpcs` stanza in the Virtual Server spec.

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
{% endtab %}
{% endtabs %}
