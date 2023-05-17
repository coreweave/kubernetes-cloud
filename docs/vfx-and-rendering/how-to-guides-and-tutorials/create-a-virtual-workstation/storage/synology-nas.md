---
description: Use Synology NAS as a VFX Studio storage backend
---

# Synology NAS

Synology NAS may be included as a storage backend by configuring [a Site-to-Site VPN](../../../../coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/).

This guide explains how to expose both **Windows File Sharing (SMB/CIFS)** and **NFS** to CoreWeave with Synology NAS. One of the two is most likely already in use; whichever protocol is employed currently will be used.

## Prerequisites

The following assets are required for this process.

* Any [Synology model](https://www.synology.com/en-us/dsm/packages/Docker)
* Admin credentials to the NAS (Credentials are provided to the organization admin by your CoreWeave Support Specialist in the form of a JSON file, titled `coreweave-cloud-link.json`)

## Setup

### Configure the file server

Select the tab that corresponds to your filesystem type.

{% tabs %}
{% tab title="SMB" %}
From the Control Panel, navigate to **File Services**. If you are primarily using **SMB (Windows File Sharing)** to access your data, SMB is likely already enabled. The CoreWeave VPN will then use SMB to connect to your storage.

<figure><img src="../../../../.gitbook/assets/image (26) (1) (1) (1).png" alt=""><figcaption><p>Adjusting shared folder permissions for SMB</p></figcaption></figure>

Ensure that a specific User Account has been created for CoreWeave. Provide the username and password to your CoreWeave Support Specialist. Give this account permissions on all Shared Folders that will be accessible from CoreWeave Cloud. Take note of the share names and provide them to your CoreWeave Support Specialist.
{% endtab %}

{% tab title="NFS (Linux)" %}
If you are primarily using **Linux**, you will want to select **NFS**. Under **Advanced Settings**, make sure `NFSv4.1` is **enabled**, and set **packet sizes** to `32KB`.

<figure><img src="../../../../.gitbook/assets/image (46) (1) (1).png" alt=""><figcaption><p>Example configuration for NFSLinux users</p></figcaption></figure>

Ensure that permissions for all Shared Folders accessible from CoreWeave Cloud are setup as described below. Provide the Mount path of the shares to your CoreWeave Specialist.

| Setting                                     | Value                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------- |
| Client Hostname or IP                       | `127.0.0.1`                                                                     |
| Privilege                                   | `Read/Write` or `Read-Only` if writing render outputs to CoreWeave storage only |
| Squash                                      | Implementation-dependent, start out with `No mapping` if unsure                 |
| Security                                    | `Sys`                                                                           |
| Enable Asynchronous                         | `Yes`                                                                           |
| Allow connections from non-privileged ports | `Yes`                                                                           |
| Allow users to access mounted subfolders    | `Yes`                                                                           |



<figure><img src="../../../../.gitbook/assets/image (31) (2).png" alt=""><figcaption><p>Described NFS settings as shown in the <strong>Edit NFS rules</strong> window</p></figcaption></figure>
{% endtab %}
{% endtabs %}
