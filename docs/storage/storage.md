---
description: Learn about CoreWeave Storage options
---

# Getting Started with Storage

**High-performance, network-attached storage volumes** for both containerized workloads and [Virtual Servers](broken-reference) are easy to provision and manage on CoreWeave Cloud.

Available in both [all-NVMe](storage.md#all-nvme-volumes) and [HDD tiers](storage.md#hdd-storage-volumes), Storage Volumes can be created as [Block Volumes](storage.md#block-storage-volumes) or [Shared File System Volumes](storage.md#block-storage-volumes-1), and can be resized at any time. Storage is managed separately from compute, and can be moved between instances and hardware types.

CoreWeave Cloud Storage Volumes are built on top of [Ceph](https://docs.ceph.com/), a software defined scale-out enterprise grade storage platform. Built with triple replication, the CoreWeave Cloud Storage platform is built to provide high-availability, performant storage for your most demanding Cloud-native workloads.

#### Object Storage

In addition to traditional storage volumes, CoreWeave also offers [S3-compliant Object Storage](object-storage.md).

## Storage Volume Features

:handshake: Storage Volumes are accessible by both containerized and hypervisor workloads&#x20;

:chart\_with\_upwards\_trend: Easily resized to add more capacity at any time&#x20;

:exploding\_head: Single Storage Volumes can be scaled to the multiple Petabyte level

:white\_check\_mark: Create and manage your Cloud Storage Volumes from the Storage Volumes UI, or via `kubectl`

:checkered\_flag: Clone your Block Storage Volumes to instantiate Virtual Servers from a template&#x20;

:fire: Run automated backups of your Shared File System Volumes to BackBlaze via [CoreWeave Apps](https://apps.coreweave.com)

## Volume Types

### Block Storage Volumes

**Block Storage Volumes** are attached to containerized workloads and Virtual Server instances as high-performance virtual disks.

When served from our all-NVMe storage tier, these virtual disks readily outperform local workstation SSDs, and are scalable to the Petabyte scale. These volumes are presented as generic block devices, so they are treated by the operating system like a typical physically connected storage device.

### Shared File System Volumes

**POSIX compliant Shared File System Volumes** can be attached to both containerized and Virtual Server workloads to provide native shared file systems.

It is possible to attach these Volumes to many instances at the same time. They are great for centralized asset storage, whether for sharing with co-workers in the cloud or as a data source for massively parallel computation.

### :fast\_forward: All-NVMe

The **All-NVMe CoreWeave Cloud storage tier** offers the highest performance in both throughput and IOPS. Great for hosting the root disk of a Virtual Server, or as the backing store for a transactional database, the All-NVMe tier can provide up to 10 million IOPS per Volume and peak storage throughput into the Tbps range.

All-NVMe Cloud Storage Volumes can be provisioned using the following storage class convention:

**Block Volumes:** `block-nvme-<region>`\
**Shared File System:** `shared-nvme-<region>`

### :arrow\_forward: HDD

The **HDD CoreWeave Cloud storage tier** offers excellent throughput optimized performance at a lower cost. Great for large file storage with sequential IOPS access patterns, the HDD tier is backed by an NVMe caching layer to improve performance and scale throughput capacity.

All HDD Cloud Storage Volumes can be provisioned using the following storage class convention:\
\
**Block Volumes:** `block-hdd-<region>`\
**Shared File System:** `shared-hdd-<region>`

## Billing&#x20;

Storage is billed per gigabyte of allocated (requested) space as an average over a billing month.

## Deploying Storage Volumes

Storage Volumes can be configured and deployed using either the [CoreWeave Cloud UI](storage.md#cloud-ui) or using [the Kubernetes command line](storage.md#cli) (`kubectl`).

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

[The CoreWeave Cloud UI](../../virtual-servers/deployment-methods/coreweave-apps.md) provides an easy-to-use storage configuration page.

To access it, first log in to your CoreWeave Cloud account. Then, from the left-hand menu, navigate to **Storage Volumes**.



![The storage volumes link on the left-hand menu of the Cloud UI](<../.gitbook/assets/image (1) (1).png>)



From the upper right-hand corner, click the **New Volume** button. This will launch the volume configuration modal.



![The New Volume button](<../.gitbook/assets/image (16).png>)



![The volume configuration modal](<../.gitbook/assets/image (53) (1).png>)

On this modal, configure your desired Volume settings. Finally, click **Create** to deploy the storage volume.
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Storage can also be managed via the Kubernetes API natively using `kubectl`. Below are some example manifests to do this, as well as descriptions of the fields used.



| Field name         | Field type | Description                                                                                                         |
| ------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| `storageClassName` | string     | Sets the storage class name for the volume's PVC; determines which kind of storage class the volume will be         |
| `accessModes`      | list       | Sets the [access mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) for the volume |
| `resources`        | array      | Defines which resources with which to provision the Volume                                                          |
| `requests`         | array      | Defines the resource requests to create the volume                                                                  |
| `storage`          | string     | Determines the size of the volume, in Gi                                                                            |



### **All-NVMe volumes**

**All-NVMe** Cloud Storage Volumes can be provisioned using the following storage class convention:

**Block Volumes:** `block-nvme-<region>`\
**Shared File System:** `shared-nvme-<region>`

For example:

{% code title="" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: block-nvme-ord1
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}



### HDD storage volumes

All HDD Cloud Storage Volumes can be provisioned using the following storage class convention:

**Block Volumes:** `block-hdd-<region>`\
**Shared File System:** `shared-hdd-<region>`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data
spec:
  storageClassName: shared-hdd-ord1
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```
{% endtab %}
{% endtabs %}

## **Using Storage**

The steps below describe how to attach storage for usage on both Virtual Servers and Pods according to deployment method.

{% hint style="info" %}
**Note**

The volumes must first be created and provisioned **before** they can be attached to a Pod or Virtual Server.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

### Filesystem attachments

Filesystem attachments are specified under the **Attach Filesystems** menu while [creating a Virtual Server](../../virtual-servers/deployment-methods/). To attach a filesystem, select the volume you wish to attach from the **Available Volumes** menu. The selected volumes will appear under the **Attach Volume** column. Finally, configure the mount point under the **Mount As** column.

**Example**

![The Attach Filesystems menu during Virtual Server creation](../.gitbook/assets/image.png)

****

### **Block device attachments**

{% hint style="info" %}
**Note**

Attaching block device storage is not currently achievable via the Cloud UI. [Please see CLI options to attach block storage devices to Virtual Servers](storage.md#virtual-servers).
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>



Select instructions for Pods or Virtual Servers below.

| Attach to:                          |
| ----------------------------------- |
| [Pods](storage.md#pods)             |
| [Virtual Servers](broken-reference) |

## **Pods**

### **Filesystem attachments**

To attach filesystem storage to a Pod, specify the  `mountPath` and `name` under the `volumeMounts` stanza.

Then, specify the `volumes.name` and the `persistentVolumeClaim.claimName`.



**Example**

<pre class="language-yaml"><code class="lang-yaml">apiVersion: v1
kind: Pod
metadata:
  name: filesystem-storage-example
spec:
  containers:
  - image: nginx:1.14.2
    name: nginx
<strong>    volumeMounts:
</strong>    - mountPath: /storage
      name: filesystem-storage
  volumes:
  - name: filesystem-storage
    persistentVolumeClaim:
      claimName: filesystem-storage-pvc</code></pre>

****

### **Block storage attachments**

As a kind of device, block storage is attached to a Pod by providing the `devicePath` under `volumeDevices`, in addition to the `volumes.name` and `persistentVolumeClaim.claimName` values.



**Example**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: block-storage-example
spec:
  containers:
  - image: nginx:1.14.2
    name: nginx
    volumeDevices:
    - devicePath: /dev/vda1
      name: block-storage
  volumes:
  - name: block-storage
    persistentVolumeClaim:
      claimName: block-storage-pvc
```



## Virtual Servers

### Filesystem attachments

The filesystem attachment information for Virtual Servers is provided in the `storage.filesystems` stanza of the spec. Here, specifying values for `filesystems.name`, `filesystems.mountPoint`,  and `persistentVolumeClaim.name`.

****

**Example**

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: filesystem-storage-example
spec:
  [...]
  storage:
    filesystems:
    - name: filesystem-storage
      mountPoint: /mnt/storage
      spec:
        persistentVolumeClaim:
          name: filesystem-storage-pvc
```

###

### Block storage attachments

To attach a block storage device to a Virtual Server, specify the block device's values in the `storage.additionalDisks` stanza.

****

**Example**

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: block-storage-example
spec:
  ...
  storage:
    additionalDisks:
    - name: block-storage
      spec:
        persistentVolumeClaim:
          name: block-storage-pvc
```
{% endtab %}
{% endtabs %}

## **Resizing Volumes**

Volumes can be expanded by simply increasing the `storage` request, then reapplying the manifest.  Storage Volumes can be resized in the CoreWeave Cloud UI, or via kubectl.

{% hint style="warning" %}
**Important**

**Shared File System Volumes** are resized online without disruption the workload.&#x20;

Resizing **Block Volumes** requires stopping or restarting all workloads that are attaching the volume for the resize to take effect.

**Volumes cannot be downsized again once they are expanded.**
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the Storage Volumes page in the Cloud UI, click the pencil associated with the listed storage volume you'd like to resize. This will open the Persistent Volume Claim modal.



![The storage volume list, featuring the pencil icon to the right](<../.gitbook/assets/image (2) (1).png>)



From this modal, make the desired changes, then click **Save** to apply the changes.



![The volume edit modal](<../.gitbook/assets/image (10).png>)
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Expanding storage volumes via `kubectl` is as simple as a single-line command:

```bash
kubectl patch pvc <myvolume> -p \
'{"spec":{"resources":{"requests":{"storage": "500Gi"}}}}'
```
{% endtab %}
{% endtabs %}

## Ephemeral Storage

**All physical nodes are equipped with SSD or NVMe ephemeral (local) storage.** Ephemeral storage available ranges between 512GB to 2TB, depending upon node type.

No volume claims are needed to allocate ephemeral storage - simply write anywhere in the container file system.

If a larger amount (above 20GB) of ephemeral storage is used, it is recommended to include ephemeral storage in the workloads resource request:

```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 3
        memory: 16Gi
        nvidia.com/gpu: 1
        ephemeral-storage: 20Gi
```

{% hint style="warning" %}
**Important**

For the vast majority of use cases, workloads should run in the same region as the storage **** block they are accessing. Use the [region label affinity](../../coreweave-kubernetes/label-selectors.md) to limit scheduling workloads to a single region.

There are certain exceptions to this rule of thumb, which are mainly relevant for shared volumes, such as:

* Batch workloads where IOPS are not a concern but accessing compute capacity from multiple regions might give scaling benefits
* When data is strictly read during startup of a process, such as when reading a ML model from storage into system and GPU memory for inference

In general, **block volumes** should always be **used in the same region in which they are allocated**.&#x20;
{% endhint %}
