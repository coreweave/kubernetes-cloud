---
description: View some examples of Virtual Server deployments
---

# Examples

Here are some examples demonstrating use cases for Virtual Servers. See also [Virtual Workstations](../../docs/cloud-studio-reference-guide/virtual-workstations.md).

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f9d1">🧑</span> <strong>Active Directory Environment</strong></td><td><p>A Virtual Server running Windows Server 2022 is deployed to host an Active Directory Domain.</p><p></p><p>This example also demonstrates how to create a domain with appropriate DNS configurations, as well as the attributes needed to join other Virtual Servers in your namespace to your Active Directory domain.</p></td><td></td><td><a href="../../docs/virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/">active-directory-environment-hosted-on-coreweave-cloud</a></td></tr><tr><td> <span data-gb-custom-inline data-tag="emoji" data-code="1f510">🔐</span> <strong>CentOS 7 with LUKS Encryption</strong></td><td><p>A Virtual Server running CentOS 7 is deployed with an encrypted partition on the root disk.</p><p></p><p>The manifest used to deploy this Virtual Server includes <a href="./#cloud-init">cloud-init directives</a>, which are used to encrypt unallocated space on the root disk. </p></td><td></td><td><a href="../../docs/virtual-servers/examples/centos-7-virtual-server-with-luks-encryption.md">centos-7-virtual-server-with-luks-encryption.md</a></td></tr></tbody></table>
