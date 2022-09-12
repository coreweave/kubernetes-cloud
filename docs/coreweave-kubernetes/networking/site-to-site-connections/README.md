# Site-to-Site Connections

## Introduction

In cases where infrastructure hosted on another Cloud provider or an on-premise site needs to be able to communicate with infrastructure hosted on CoreWeave Cloud, Site-to-Site connections can offer a solution.

{% hint style="warning" %}
**Important**\
All Site-to-Site connections are **only possible when using** [**an L2VPC**](../layer-2-vpc-l2vpc/). They cannot be created using [CCNN](../coreweave-cloud-native-networking-ccnn.md) alone.
{% endhint %}

## Options

CoreWeave offers two Site-to-Site connection options:

### [**Site-to-Site VPN**](site-to-site-vpn/)

Create a Virtual Private Network (VPN) between CoreWeave and the other site. CoreWeave provides examples for setting up VPN endpoints on other Cloud providers:

| Examples                                |
| --------------------------------------- |
| [AWS](site-to-site-vpn/examples/aws.md) |

### ****[**Direct Connect**](direct-connections.md)

Connect directly between a CoreWeave data center and an on-premise site.
