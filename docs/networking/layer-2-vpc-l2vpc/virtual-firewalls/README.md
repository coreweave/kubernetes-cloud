---
description: Introduction to using Virtual Firewalls on CoreWeave Cloud
---

# Virtual Firewalls

The recommended method for accessing resources hosted outside of a VPC is to attach a regular CoreWeave Cloud Native NIC to a Pod or to a [Virtual Server](broken-reference).

However, certain users may want to deploy and manage their own Virtual Firewalls to bridge a VPC to the outside world instead.

{% hint style="info" %}
**Note**

Virtual Firewalls come with additional cost and scaling considerations, as all traffic will be routed through a single point instead of being handled by the CoreWeave Network Fabric.
{% endhint %}

If you would like to use your own firewall or virtual appliance, it must adhere to the following criteria:

* must be able to run on the KVM hypervisor
* appliances providing images in QCOW2 or RAW format must require no conversion to install
* must support SR-IOV NICs from Intel and Mellanox\
  **Note:** _Most Linux- and BSD-based firewalls support these. CoreWeave does not support software virtualized NIC drivers such as virtio-net or VMXNET for Layer 2 VPC interfaces, out of concerns for performance._

If these criteria are satisfied, the firewall or virtual appliance can be deployed on CoreWeave Cloud.

## Setup guides

For your convenience, CoreWeave provides the following setup guides for popular Virtual Firewalls:

| Virtual Firewalls       |
| ----------------------- |
| [Fortinet](fortinet.md) |
