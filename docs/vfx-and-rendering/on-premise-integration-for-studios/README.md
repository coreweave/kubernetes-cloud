---
description: Connect CoreWeave Cloud to existing on-premise infrastructure with CloudLink
---

# On-Premise Integration for Studios

Connecting CoreWeave Cloud to existing on-premise infrastructure allows customers to leverage powerful and elastic compute in CoreWeave Cloud without migrating their entire production pipeline.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span> <strong>On-Premise Storage</strong></td><td>Let Render Nodes and Virtual Workstations in CoreWeave Cloud seamlessly access storage hosted outside of CoreWeave</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="2728">✨</span> <strong>On-Premise Thinkbox Deadline</strong></td><td>Connect CoreWeave's auto-scaling render nodes to an existing on-premise Thinkbox Deadline installation</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4aa">💪</span> <strong>Local Access to CoreWeave Storage</strong></td><td>Efficiently access CoreWeave storage from local workstations</td><td></td><td></td></tr></tbody></table>

Integration is achieved using one or a combination of technologies:

## Site-to-Site VPN

[Site-to-Site VPN connections](../../coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/) allow CoreWeave Cloud to act as a direct extension of an on-premise network, making it the ideal choice for more complex integrations.

[Storage](../../virtual-servers/virtual-server-configuration-options/storage.md) on CoreWeave can be accessed by on-premise nodes over NFS and SMB, and storage on premise can be accessed directly from CoreWeave Cloud. Transparent Caching can optionally be employed to minimize upstream bandwidth requirement from the on-premise location. Deadline workers can run both on-premise and in the cloud, with the actual deadline installation also residing on either location.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more about Site-to-Site VPN</td><td></td><td></td><td><a href="../../coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/">site-to-site-vpn</a></td></tr></tbody></table>

## **Transparent cache**

A [transparent cache](./#transparent-cache-for-cloudlink) in CoreWeave Cloud also minimizes upstream bandwidth requirements, even when rendering on hundreds of Cloud nodes.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more about transparent cache</td><td></td><td></td><td><a href="transparent-cache.md">transparent-cache.md</a></td></tr></tbody></table>

## **Storage synchronization**

In situations where direct storage access isn't performant, synchronizing all or partial on-premise storage to CoreWeave Cloud is recommended. This is also a common choice when integrating Virtual Workstations over geographically dispersed locations, providing the best user experience to all clients.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> <a href="https://cloud.coreweave.com/contact">Contact support</a> for more information on storage synchronization</td><td></td><td></td></tr></tbody></table>
