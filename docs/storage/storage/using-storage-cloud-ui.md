---
description: Manage Storage Volumes using the CoreWeave Cloud UI
---

# Using Storage - Cloud UI

[The CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) provides an easy-to-use storage configuration page. To access it, first log in to your CoreWeave Cloud account. Then, from the left-hand menu, navigate to **Storage Volumes**. To create a new Storage Volume, click the **New Volume** button in the upper right-hand corner or center of the page.

<figure><img src="../../.gitbook/assets/image (5) (2).png" alt="Screenshot: The Storage Volumes management page"><figcaption><p>The Storage Volumes management page</p></figcaption></figure>

## Create a new Storage Volume

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

The **storage type** field determines whether the new storage volume will be a [shared filesystem](./#shared-file-system-volumes) or a [block storage](./#block-storage-volumes) device.

{% hint style="info" %}
**Additional Resources**

For more information on these disk classes, refer to [the "Volume types" portion of the Storage section](./#volume-types).
{% endhint %}

### Size

The desired **size** of the disk is specified in `Gi`_._ The maximum allotable size for a single storage volume is `30720Gi`.

### Labels

While optional, if it is desired to schedule specific workloads onto certain storage volumes, **labels** can be very helpful. Kubernetes affinities may be used to select these labels for scheduling workloads appropriately. See [the Custom Container guide](../../coreweave-kubernetes/custom-containers.md) for examples.

## View and edit Storage Volumes

Navigate to **Storage** to view a list of all available storage volumes. To see more details about a volume, click to expand the volume's detail window.

<figure><img src="../../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>

The detailed view of the storage volume will include its age, its size, how much of it is being used, as well as some important metadata such as all labels associated with the drive, the cost it is currently incurring, its creation date, and its access modes. The volume may also be edited, cloned to create an exact copy of it, or completely deleted from this menu.

Edit the volume to add or remove labels or to expand the volume's capacity.

{% hint style="danger" %}
**Warning**

Shared File System Volumes are resized online, without disruption to workloads.

**Resizing** **Block Volumes** requires **stopping or restarting all workloads** that are attached the Volume in order for the resize to take effect.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (55) (2).png" alt=""><figcaption></figcaption></figure>

## Attach a Storage Volume using the Cloud UI

{% hint style="warning" %}
**Important**

Storage Volumes must be created and provisioned **before** they can be attached to a Pod or Virtual Server.
{% endhint %}

When [creating a Virtual Server](../../../virtual-servers/getting-started.md), the option to attach a volume is found under the **Attach Volumes** section of the Virtual Server creation screen.

To attach a filesystem or block volume, locate the volume in the list provided under the **Available volume** column. To attach it, click the toggle until it is in the "on" position and says "Attached."

<figure><img src="../../.gitbook/assets/image (44).png" alt="Screenshot of a volume being attached to a Virtual Server using sliders"><figcaption></figcaption></figure>

The storage block volume information will be reflected in the YAML editor under the `.filesystems` block.

<figure><img src="../../.gitbook/assets/image (34) (1).png" alt=""><figcaption><p>An example of a mounted filesystem volume reflected </p></figcaption></figure>

Example in plain text:

```yaml
 filesystems:
   - name: test-docker-registry
     spec:
       persistentVolumeClaim:
         claimName: test-docker-registry
     mountPoint: /mnt/
```
