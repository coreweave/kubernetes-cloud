---
description: Learn about the CoreWeave Site-to-Site VPN Server.
---

# Site-to-Site VPN

## Introduction

In cases where infrastructure is hosted across different Cloud platforms or on a mix of on-premise infrastructure and Cloud platform infrastructure, but both need to be able to communicate with one another, **Site-to-Site VPNs** are leveraged for networking across platforms.

{% hint style="info" %}
**Note**

On CoreWeave Cloud, Site-to-Site VPNs are provided by instantiating a Virtual VPN in a [**Layer 2 VPC (L2VPC)**](../layer-2-vpc/). Each workload that requires access to the Site-to-Site VPN should be placed in the VPC in addition to the regular CoreWeave network.
{% endhint %}

CoreWeave provides guides for setup and usage both on **CoreWeave Cloud** as well as other Cloud platforms and firewalls.

**Configurations must be completed for both sides of the Site-to-Site VPN.**

Learn more in our Cloud-specific endpoint configuration examples:

| Cloud                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [AWS](https://app.gitbook.com/o/-M8EEYiNkaJsT8ISX0kX/s/-M83TghsCfsi8FCYs2DZ/\~/changes/Uy7xH1nABFQP3H059xgP/coreweave-kubernetes/networking/site-to-site-vpn/examples/aws) |

{% hint style="success" %}
**Tip**

The IPSec VPN that CoreWeave uses has been benchmarked to over 4Gbps (with proposal `aes128gcm16-sha256-modp2048`). Most enterprise on-premise firewalls and Cloud firewalls on other Cloud providers are rarely rated over 1Gbps of IPSec performance!
{% endhint %}

## **Basic IPSec VPN u**sage

After initial installation, VPN status and troubleshooting can be conducting by accessing the VPN Gateway directly.

To get the current status of your VPN tunnel, you will need to SSH into the VPN server on its VPC IP, or attach to the console.

| Commands               |                                           |
| ---------------------- | ----------------------------------------- |
| `sudo ipsec statusall` | Display information about your tunnel(s). |
| `sudo ipsec restart`   | Restart the IPSec service.                |

#### Updating VPN configuration

After changes have been made to your VPN configuration via the CoreWeave Cloud UI, the VPN server must be restarted for the new configuration to take effect.

```
virtctl restart vpn02
```

### Troubleshooting

To troubleshoot your connection, first issue `sudo ipsec status`.&#x20;

The output should be similar to:

```bash
vpn02[1]: CONNECTING, 216.153.60.182[%any]...123.123.123.123[%any]
```

{% hint style="info" %}
**Additional Resources**

Additional information can be found in [the strongSwan documentation](https://docs.strongswan.org/docs/5.9/index.html).
{% endhint %}
