---
description: Learn about configuring a DHCP server in a VPC on CoreWeave.
---

# DHCP

## Introduction

For IP address assignment in a VPC a DHCP server needs to be deployed. CoreWeave provides a DHCP Server application that supports IP allocation, static assignment and distribution of routes. This is the recommended method for distributing IP addresses inside a VPC unless a dedicated virtual firewall is used. In some deployments, users also chose do distribute VPC IPs from a Windows Domain Controller.

{% hint style="warning" %}
The VPC **must be created** before the DHCP server is deployed
{% endhint %}

## Installation

To install the dhcp server, navigate to the Applications catalogue from the CoreWeave Cloud UI homepage, then find and select the dhcp-server **** application.

![Screenshot of the dhcpd-server application in the CoreWeave application catalog.](<../../../.gitbook/assets/image (9).png>)

### Configuration

Selecting the application will expose the configuration options for the DHCP server, shown and detailed below.

![DHCP configuration settings, exposed by clicking the DHCP server application.](<../../../.gitbook/assets/image (15).png>)

#### Configuration options

| **Subnet**                                  | <p>The VPC subnet where dynamic IP addresses will be assigned<br><br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong>Note:</strong> This should be the netidentifier of the subnet (e.g., for a <code>/24</code> network, the address would be <code>192.168.0.0</code>. For a <code>/25</code> network, either <code>192.168.0.0</code> or <code>192.168.0.128</code>).</p>                                |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Subnet Mask**                             | The netmask of the VPC subnet                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Range**                                   | <p>The range in the subnet to use dynamic IP assignment<br><br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong>Note:</strong> This should be formatted as:<br><code>&#x3C;first usable address> &#x3C;space> &#x3C;last usable address></code>.</p>                                                                                                                                                         |
| **Fixed IP assignment via DHCP**            | A comma-separated list of fixed IP addresses that will bind to the client ID of a Pod                                                                                                                                                                                                                                                                                                                                                     |
| **Routes**                                  | <p>Allows Virtual Servers to receive </p><p>specific routes, such as in the case where there is a VPN setup to another cloud provider</p><p><br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong>Note:</strong> Should be formatted as <code>&#x3C;remotenetwork>/&#x3C;cidr>=&#x3C;gateway>.</code> </p><p><strong></strong><br><strong>Example:</strong></p><p><code>10.0.0.0/16=192.168.0.254</code>.</p> |
| **Default gateway to be assigned via DHCP** | This will set a default gateway address via DHCP. Please note that this should not be used if your Virtual Servers are connected to the regular pod network                                                                                                                                                                                                                                                                               |

### VPC and Network settings

At the bottom of the application's configuration screen are the **Network settings** for the DHCP server, in which you can adjust the settings for the server's VPC and network.

![Network settings for DHCP server application.](<../../../.gitbook/assets/image (14).png>)

#### Configuration options

| **VPC Name**          | The name of your VPC. **The VPC must be created before the DHCP service.** |
| --------------------- | -------------------------------------------------------------------------- |
| **Static IP for VPC** | The static IP address of the DHCP server (e.g., `192.168.0.250/24`)        |

