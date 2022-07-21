---
description: Configuration guide for the CoreWeave end of a VPN tunnel.
---

# Getting Started

## IPSec VPN setup

Site-to-Site VPNs are configured through the [CoreWeave Cloud UI](../../../../virtual-servers/deployment-methods/coreweave-apps.md). The IPSec VPN gateway is provided through our application Catalog. To set up the IPSec VPN gateway, first navigate to the **Catalog** page from the CoreWeave Cloud UI main menu.

### Installation

Find and select the **vpn-ipsec-server** in the catalog.

![The applications page on CoreWeave Cloud, with a search filter for "vpn."](<../../../.gitbook/assets/image (2) (1).png>)

### Configuration

Selecting the VPN application from the catalog exposes its configuration options, shown and detailed below.

![VPN Server configuration example.](<../../../.gitbook/assets/image (1) (1).png>)

#### Configuration Options

| **Proposals**      | First, select [a proposal](getting-started.md#proposals) that best suits your implementation. Broadly, `aes256gcm16-sha256-modp2048` is recommended for the highest performance.                                                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pre Shared Key** | 32-64 alphanumeric random string                                                                                                                                                                                                                                                          |
| **Peer IP**        | The remote VPN device IP or hostname                                                                                                                                                                                                                                                      |
| **Peer network**   | <p>The remote network(s) that you need to reach from your VPC network.<br><br>This can be a single network, specified as a single address, e.g.: <code>10.0.0.0/16</code>, or multiple networks, specified as a comma separated list, e.g.: <code>10.0.0.0/16, 192.168.0.0/24</code>.</p> |
| **Tunnel IP**      | The local-side IP address of the VPN tunnel                                                                                                                                                                                                                                               |
| **IKE version**    | :warning:**Non-configurable** - **** CoreWeave only supports IKE Version 2                                                                                                                                                                                                                |

### VPC configuration

Under the **Network Settings** portion of the IPSec VPN setup page are the configuration fields for your VPC.

![VPC configuration example.](<../../../.gitbook/assets/image (2).png>)

The fields provided are:

| **VPC Name**          | The name of your VPC. This has to be created before the VPN gateway                        |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **Static IP for VPC** | If there is no VPC DHCP service available, a static IP in the VPC network can be specified |

#### Proposals

CoreWeave currently supports four different Proposals for **Phase 1** and **Phase 2**:

**Phase 1**

| Proposal                       | Encryption  | Integrity | DH-Group |
| ------------------------------ | ----------- | --------- | -------- |
| `aes128gcm16-sha256-modp2048​` | aes128gcm16 | sha2-256  | 14       |
| `aes256gcm16-sha256-modp2048`  | aes256gcm16 | sha2-256  | 14       |
| `aes128gcm16-sha256-ecp256`    | aes128gcm16 | sha2-256  | 19       |
| `aes256gcm16-sha256-ecp256`    | aes256gcm16 | sha2-256  | 19       |

**Phase 2**

| Proposal                       | Encryption  | Integrity | DH-Group |
| ------------------------------ | ----------- | --------- | -------- |
| `aes128gcm16-sha256-modp2048​` | aes128gcm16 | sha2-256  | 14       |
| `aes256gcm16-sha256-modp2048`  | aes256gcm16 | sha2-256  | 14       |
| `aes128gcm16-sha256-ecp256`    | aes128gcm16 | sha2-256  | 19       |
| `aes256gcm16-sha256-ecp256`    | aes256gcm16 | sha2-256  | 19       |

## Launching the VPN

The final configuration option is for creating a user account on the VPN Gateway Virtual Server.

Once your configurations have been set, select the **Deploy** button at the bottom of the screen to deploy the VPN server to your cluster!
