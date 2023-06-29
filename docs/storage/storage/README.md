---
description: Learn about CoreWeave Storage options
---

# Get Started with Storage

**High-performance, network-attached storage volumes** for both containerized workloads and [Virtual Servers](../../../virtual-servers/getting-started.md) are easy to provision and manage on CoreWeave Cloud.

Available in both [all-NVMe](./#storage-tiers) and [HDD tiers](./#storage-tiers), Storage Volumes can be created as [Block Volumes](./#block-storage-volumes) or [Shared File System Volumes](./#shared-file-system-volumes), and can be resized at any time. Storage is managed separately from compute, and can be moved between instances and hardware types.

CoreWeave Cloud Storage Volumes are built on top of [Ceph](https://docs.ceph.com/), a software defined scale-out enterprise grade storage platform. Built with triple replication, the CoreWeave Cloud Storage platform is built to provide high-availability, performant storage for your most demanding Cloud-native workloads.

## Storage Volumes

### Features

:handshake: Accessible by both containerized and hypervisor Workloads

:chart\_with\_upwards\_trend: Easily resized to add more capacity at any time

:exploding\_head: Single Storage Volumes can be scaled to the multiple Petabyte level

:white\_check\_mark: Easily managed from the CoreWeave Cloud UI or via `kubectl`

:checkered\_flag: May be cloned to instantiate new Virtual Servers from a template

:fire: Automatic backups are supported using BackBlaze via [CoreWeave Apps](../../welcome-to-coreweave/coreweave-cloud-ui/applications-catalog.md)

### Creating and using Storage Volumes

{% hint style="warning" %}
**Important**

For the vast majority of use cases, Workloads should run in the same region as the storage block they are accessing. Use the [region label affinity](../../../coreweave-kubernetes/label-selectors.md) to limit scheduling workloads to a single region.

There are certain exceptions to this rule of thumb, which are mainly relevant for shared volumes, such as:

* Batch Workloads where IOPS are not a concern but accessing compute capacity from multiple regions might give scaling benefits
* When data is strictly read during startup of a process, such as when reading a ML model from storage into system and GPU memory for inference

In general, **block volumes** should always be **used in the same region in which they are allocated**.
{% endhint %}

Storage Volumes can be configured, deployed, and managed using either the [CoreWeave Cloud UI](using-storage-cloud-ui.md) or using [the Kubernetes command line](using-storage-kubectl.md) (`kubectl`).

Select your preferred method to learn more:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h4><span data-gb-custom-inline data-tag="emoji" data-code="2601">☁</span> <strong>Use Storage Volumes via Cloud UI</strong></h4></td><td>The Cloud UI offers an easy-to-use visual interface for interacting with Storage Volumes.</td><td></td><td><a href="using-storage-cloud-ui.md">using-storage-cloud-ui.md</a></td></tr><tr><td><h4><span data-gb-custom-inline data-tag="emoji" data-code="1f469-1f4bb">👩💻</span> <strong>Use Storage Volumes via Kubectl</strong></h4></td><td>The Kubernetes command line offers more fine-grained, programmable configuration options.</td><td></td><td><a href="using-storage-kubectl.md">using-storage-kubectl.md</a></td></tr></tbody></table>

## Volume Types and Tiers

### Block Storage Volumes

Block Storage Volumes are attached to containerized workloads and Virtual Server instances as high-performance virtual disks.

When served from our all-NVMe storage tier, these virtual disks readily outperform local workstation SSDs, and are scalable to the Petabyte scale. These volumes are presented as generic block devices, so they are treated by the operating system like a typical physically connected storage device.

### Shared File System Volumes

POSIX-compliant Shared File System Volumes can be attached to both containerized and Virtual Server workloads to provide native shared file systems.

It is possible to attach these Volumes to many instances at the same time. They are great for centralized asset storage, whether for sharing with co-workers in the cloud or as a data source for massively parallel computation.

### Storage tiers

<table data-card-size="large" data-view="cards"><thead><tr><th></th></tr></thead><tbody><tr><td><p><span data-gb-custom-inline data-tag="emoji" data-code="23e9">⏩</span> <strong>All-NVMe</strong></p><p></p><p>The <strong>All-NVMe CoreWeave Cloud storage tier</strong> offers the highest performance in both throughput and IOPS.</p><p></p><p>Great for hosting the root disk of a Virtual Server, or as the backing store for a transactional database, the All-NVMe tier can provide up to 10 million IOPS per Volume and peak storage throughput into the Tbps range.</p><p></p><p>Provision <a href="using-storage-kubectl.md#all-nvme-volumes">All-NVMe</a> Block and Shared Storage Volumes with <a href="using-storage-kubectl.md#all-nvme-volumes">kubectl</a> or <a href="using-storage-cloud-ui.md">Cloud UI</a>. </p></td></tr><tr><td><p><span data-gb-custom-inline data-tag="emoji" data-code="25b6">▶</span> <strong>HDD</strong></p><p></p><p>The <strong>HDD CoreWeave Cloud storage tier</strong> offers excellent throughput optimized performance at a lower cost.</p><p></p><p>Great for large file storage with sequential IOPS access patterns, the HDD tier is backed by an NVMe caching layer to improve performance and scale throughput capacity.</p><p></p><p>Provision <a href="using-storage-kubectl.md#hdd-storage-volumes">HDD</a> Block and Shared Storage Volumes with <a href="using-storage-kubectl.md#hdd-storage-volumes">kubectl</a> or <a href="using-storage-cloud-ui.md">Cloud UI</a>. </p></td></tr></tbody></table>

## Ephemeral storage

**All physical nodes are equipped with SSD or NVMe ephemeral (local) storage.** Ephemeral storage available ranges between `512GB` to `2TB`, depending on the node type. No [Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) are needed to allocate ephemeral storage - simply write anywhere in the container file system.

{% hint style="info" %}
**Tip**

If a larger amount (above `20Gi`) of ephemeral storage is needed, include it in the workloads resource request. See [Using Storage - Kubectl ](using-storage-kubectl.md#ephemeral-storage)for details.
{% endhint %}

## **CoreWeave Object Storage**

In addition to traditional Storage Volumes, CoreWeave also offers S3-compliant Object Storage. [See the Object Storage page to learn more](../object-storage.md).

## Billing

Storage is billed per gigabyte of allocated (requested) space as an average over a billing month.
