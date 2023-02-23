---
description: Configuration guide for the CoreWeave end of the VPN tunnel.
---

# VPN Setup

## IPSec VPN setup

Site-to-Site VPNs are configured through the [CoreWeave Cloud UI](../../../../../virtual-servers/deployment-methods/coreweave-apps.md). The IPSec VPN Server is provided through our application catalogue. To set up the IPSec VPN server, first navigate to the **Catalog** page from the CoreWeave Cloud UI main menu.

{% hint style="warning" %}
**Important**

The VPC **must be created** before the VPN is deployed.
{% endhint %}

### Installation

Find and select the **vpn-ipsec-server** in the applications Catalog:

![The applications page on CoreWeave Cloud, with a search filter for "vpn"](<../../../../.gitbook/assets/image (2) (1) (2).png>)

### Configuration

Selecting the VPN application from the catalog exposes its configuration options, shown and detailed below.

![VPN Server configuration example](<../../../../.gitbook/assets/image (1) (1) (1) (1).png>)

#### Configuration Options

| **Proposals**      | First, select [a proposal](vpn-setup.md#proposals) that best suits your implementation. Broadly, `aes256gcm16-sha256-modp2048` is recommended for the highest performance.                                                                                                                |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pre Shared Key** | 32-64 alphanumeric random string                                                                                                                                                                                                                                                          |
| **Peer IP**        | The remote VPN device IP or hostname                                                                                                                                                                                                                                                      |
| **Peer network**   | <p>The remote network(s) that you need to reach from your VPC network.<br><br>This can be a single network, specified as a single address, e.g.: <code>10.0.0.0/16</code>, or multiple networks, specified as a comma separated list, e.g.: <code>10.0.0.0/16, 192.168.0.0/24</code>.</p> |
| **Tunnel IP**      | The local-side IP address of the VPN tunnel                                                                                                                                                                                                                                               |
| **IKE version**    | :warning:**Non-configurable** - \*\*\*\* CoreWeave only supports IKE Version 2                                                                                                                                                                                                            |

### VPC configuration

Under the **Network Settings** portion of the IPSec VPN setup page are the configuration fields for your VPC.

![VPC configuration example](<../../../../.gitbook/assets/image (105).png>)

The fields provided are:

| **VPC Name**          | The name of your VPC. This has to be created before the VPN gateway                        |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **Static IP for VPC** | If there is no VPC DHCP service available, a static IP in the VPC network can be specified |

#### Proposals

CoreWeave currently supports four different Proposals for **Phase 1** and **Phase 2**:

**Phase 1**

| Proposal                       | Encryption  | Integrity      | DH-Group |
| ------------------------------ | ----------- | -------------- | -------- |
| `aes128gcm16-sha256-modp2048​` | aes128gcm16 | sha2-256 (prf) | 14       |
| `aes256gcm16-sha256-modp2048`  | aes256gcm16 | sha2-256 (prf) | 14       |
| `aes128gcm16-sha256-ecp256`    | aes128gcm16 | sha2-256 (prf) | 19       |
| `aes256gcm16-sha256-ecp256`    | aes256gcm16 | sha2-256 (prf) | 19       |
| `aes256gcm16-sha384-ecp384`    | aes256gcm16 | sha2-384 (prf) | 20       |
| `aes128-sha256-modp2048`       | aes128      | sha2-256       | 14       |
| `aes256-sha256-modp2048`       | aes256      | sha2-256       | 14       |

**Phase 2**

| Proposal                       | Encryption  | Integrity | DH-Group |
| ------------------------------ | ----------- | --------- | -------- |
| `aes128gcm16-sha256-modp2048​` | aes128gcm16 | -         | 14       |
| `aes256gcm16-sha256-modp2048`  | aes256gcm16 | -         | 14       |
| `aes128gcm16-sha256-ecp256`    | aes128gcm16 | -         | 19       |
| `aes256gcm16-sha256-ecp256`    | aes256gcm16 | -         | 19       |
| `aes256gcm16-sha384-ecp384`    | aes256gcm16 | -         | 20       |
| `aes128-sha256-modp2048`       | aes128      | sha2-256  | 14       |
| `aes256-sha256-modp2048`       | aes256      | sha2-256  | 14       |

{% hint style="success" %}
**Tip**

The most performant proposal has been benchmarked to be`aes128gcm16-sha256-modp2048`.
{% endhint %}

Finally, create a user account on the VPN Gateway Virtual Server in the final fields of the configuration screen.

## Launching the VPN

Once the settings for your VPN have been configured, click the **Deploy** button at the bottom of the screen to deploy the VPN server to your cluster!

## Configure routes

After the VPN is set up, you will need to configure routing for the subnet that you want to reach on the other end of the tunnel. The easiest way to configure this is to use the [DHCP on L2VPC](../../layer-2-vpc-l2vpc/dhcp-on-l2vpc.md), available in the Application Catalog.

{% hint style="info" %}
**Note**

If you are running your own DHCP server you will need to implement [RFC3442](https://datatracker.ietf.org/doc/html/rfc3442) (classless static routes) in your DHCP server's configuration.
{% endhint %}
