---
description: Manage Storage Volumes from the CoreWeave Cloud UI
---

# Using Storage - Cloud UI

## Creating Storage Volumes

[The CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) provides an easy-to-use storage configuration page. To access it, first log in to your CoreWeave Cloud account. Then, from the left-hand menu, navigate to **Storage Volumes**.

![The storage volumes link on the left-hand menu of the Cloud UI](<../../.gitbook/assets/image (1) (6).png>)

From the upper right-hand corner, click the **New Volume** button. This will launch the volume configuration modal.

![The New Volume button](<../../.gitbook/assets/image (3).png>)

![The volume configuration modal](<../../.gitbook/assets/image (53) (1).png>)

Within this modal, configure your desired Volume settings.

Finally, click **Create** to deploy the storage volume.

## Attaching Storage Volumes

{% hint style="warning" %}
**Important**

The volumes must first be created and provisioned **before** they can be attached to a Pod or Virtual Server.
{% endhint %}

### Filesystem attachments

Filesystem attachments are specified under the **Attach Filesystems** menu while [creating a Virtual Server](../../../virtual-servers/deployment-methods/). To attach a filesystem, first select the Volume you wish to attach from the **Available Volumes** menu. The selected Volumes will appear under the **Attach Volume** column. Finally, configure the mount point under the **Mount As** column.

**Example**

![The Attach Filesystems menu during Virtual Server creation](<../../.gitbook/assets/image (13).png>)

### **Block device attachments**

{% hint style="info" %}
**Note**

Attaching block device storage is not currently achievable via the Cloud UI. [Please see CLI options to attach block storage devices to Virtual Servers](using-storage-cloud-ui.md#virtual-servers).
{% endhint %}

## **Resizing Volumes**

{% hint style="warning" %}
**Important**

**Shared File System Volumes** are resized online **without disruption** the workload.

Resizing **Block Volumes** requires **stopping or restarting all workloads** that are attached the Volume in order for the resize to take effect.

_**Volumes cannot be downsized again once they are expanded.**_
{% endhint %}

From **the Storage Volumes page** in the Cloud UI, click the pencil icon beside the listed storage volume that you'd like to resize. This will open the Persistent Volume Claim modal.

![The storage volume list, featuring the pencil icon to the right](<../../.gitbook/assets/image (2) (6).png>)

From this modal, make the desired changes, then click **Save** to apply the changes.
