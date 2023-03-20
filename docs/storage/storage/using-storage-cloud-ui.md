---
description: Manage Storage Volumes using the CoreWeave Cloud UI
---

# Using Storage - Cloud UI

[The CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) provides an easy-to-use storage configuration page. To access it, first log in to your CoreWeave Cloud account. Then, from the left-hand menu, navigate to **Storage Volumes**. To create a new Storage Volume, click the **New Volume** button in the upper right-hand corner or center of the page.

<figure><img src="../../.gitbook/assets/image (9).png" alt="Screenshot: The Storage Volumes management page"><figcaption><p>The Storage Volumes management page</p></figcaption></figure>

## Create a new Storage Volume

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption><p>The Storage Volume modal opens when the <strong>New Volume</strong> button is clicked</p></figcaption></figure>

### Volume name

The **volume name** will be used to refer to and identify the Storage Volume across the Cloud platform. If the new volume is being used for a specific application, it is recommended to create a name that clearly identifies it for that use for the sake of easy association.

### Namespace

The **namespace** field will be prepopulated with your current tenant namespace name. This cannot be changed from this modal.

### Region

The **region** field specifies in which [data center region](../../data-center-regions.md) you'd like the new storage volume to be hosted.

{% hint style="warning" %}
**Important**

It is strongly recommended that application workloads requiring storage volumes be placed in the same data center region as their associated storage volumes. See Custom Containers for examples, or refer to the [Advanced Label Selectors page](../../../coreweave-kubernetes/label-selectors.md) for more information on scheduling workloads to the same data center region as their storage volumes.
{% endhint %}

### Disk class

Once a **region** has been selected, a **disk class** may be chosen. There are [two disk storage classes](./#volume-types) from which to choose, NVMe and HDD.

{% hint style="info" %}
**Additional Resources**

For more information on these disk classes, refer to [the Storage section](../../virtual-servers/virtual-server-configuration-options/storage.md).
{% endhint %}

### Storage type

The **storage type** field determines whether the new storage volume will be a [shared filesystem](./#shared-file-system-volumes) or a [block storage](./#block-storage-volumes) **** device.

{% hint style="info" %}
**Additional Resources**

For more information on these disk classes, refer to [the "Volume types" portion of the Storage section](./#volume-types).
{% endhint %}

### Size

The desired **size** of the disk is specified in `Gi`_._ The maximum allotable size for a single storage volume is `30720Gi`.

### Labels

While optional, if it is desired to schedule specific workloads onto certain storage volumes, **labels** can be very helpful. Kubernetes affinities may be used to select these labels for scheduling workloads appropriately. See [the Custom Container guide](../../coreweave-kubernetes/custom-containers.md) for examples.

## Attach a Storage Volume using the Cloud UI

{% hint style="warning" %}
**Important**

Storage Volumes must be created and provisioned **before** they can be attached to a Pod or Virtual Server.
{% endhint %}

### Filesystem attachments

When [creating a Virtual Server](../../../virtual-servers/getting-started.md), the option to attach a filesystem volume is presented under the **Attach Filesystems** section of the Virtual Server creation screen.

To attach a filesystem, first select the Volume you wish to attach from the **Available Volumes** column by clicking the blue plus sign beside its name. The selected Volumes will then appear under the **Attach Volume** column.

Finally, the mount point for the Volume is specified under the **Mount As** column.

<figure><img src="../../.gitbook/assets/image (4).png" alt="Screenshot showing a filesystem volume being attached to a Virtual Server"><figcaption><p>Attach a filesystem Volume to a Virtual Server</p></figcaption></figure>

### **Block device attachments**

{% hint style="warning" %}
**Important**

Attaching block device storage is not currently possible via the Cloud UI. [Refer to CLI options to attach block storage devices to Virtual Servers](using-storage-kubectl.md).
{% endhint %}

## **Resize a Volume**

{% hint style="danger" %}
**Warning**

**Shared File System Volumes** are resized online, **without disruption** to workloads.

Resizing **Block Volumes**, on the other hand, requires **stopping or restarting all workloads** that are attached the Volume in order for the resize to take effect.
{% endhint %}

To resize a Volume, first navigate to the Storage Volumes page. Click the pencil icon that appears beside the listed Storage Volume that you'd like to resize to open the Persistent Volume Claim modal.

<figure><img src="../../.gitbook/assets/image.png" alt="Screenshot: Click the pencil icon to the right of the Storage Volume name to edit it"><figcaption><p>Click the pencil icon to the right of the Storage Volume name to edit it</p></figcaption></figure>

From this modal, it is possible to adjust the size and labels of the Volume. Adjust the size under the **size** field, then click the **Save** button to apply your changes.

<figure><img src="../../.gitbook/assets/image (2).png" alt="Screenshot of the storage volume edit module"><figcaption><p>Adjust the volume size</p></figcaption></figure>
