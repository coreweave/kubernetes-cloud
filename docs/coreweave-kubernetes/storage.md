# Storage

High-performance network attached storage for both containerized workloads and Virtual Servers are easy to provision and manage on CoreWeave Cloud. Available in both all-NVMe and HDD tiers, Storage Volumes can be created as Block Volumes or Shared File System Volumes and can be resized at any time. Storage is managed separately from compute and can be moved between instances and hardware types.

CoreWeave Cloud Storage Volumes are built on top of Ceph, a software defined scale-out enterprise grade storage platform. Built with triple replication, the CoreWeave Cloud Storage platform is built to provide high-availability, performant storage for your most demanding cloud native workloads.

### Block Storage Volumes&#x20;

Block Storage Volumes are attached to containerized workloads and Virtual Server instances as high-performance virtual disks. When served from our all-NVMe storage tier, these virtual disks readily outperform local workstation SSDs and are scalable to the Petabyte scale. These volumes are presented as generic block devices, so they are treated by the operating system like a typical physically connected storage device.

### Shared File System Volumes&#x20;

POSIX compliant Shared File System Volumes can be attached to both containerized and Virtual Server workloads to provide native shared file systems. Attachable to many instances at the same time, these Volumes are great for centralized asset storage, whether for sharing with co-workers in the cloud or as a data source for massively parallel computation.

### Available Storage Types

#### :fast\_forward: All-NVMe

The All-NVMe CoreWeave Cloud storage tier offers the highest performance in both throughput and IOPS. Great for hosting the root disk of a Virtual Server, or as the backing store for a transactional database, the All-NVMe tier can provide up to 10 million IOPS per Volume and peak storage throughput into the Tbps range.

All-NVMe Cloud Storage Volumes can be provisioned using the storage class convention:

```
Block Volumes: block-nvme-<region>
Shared File System: shared-nvme-<region>
```

#### :arrow\_forward: HDD

The HDD CoreWeave Cloud storage tier offers excellent throughput optimized performance at a lower cost. Great for large file storage with sequential IOPS access patterns, the HDD tier is backed by an NVMe caching layer to improve performance and scale throughput capacity.

All HDD Cloud Storage Volumes can be provisioned using the storage class convention:

```
Block Volumes: block-hdd-<region>
Shared File System: shared-hdd-<region>
```

### Features

:handshake: Storage Volumes are accessible by both containerized and hypervisor workloads&#x20;

:chart\_with\_upwards\_trend: Easily resized to add more capacity at any time&#x20;

:exploding\_head: Single Storage Volumes can be scaled to the multiple Petabyte level&#x20;

:white\_check\_mark: Create and manage your Cloud Storage Volumes from the Storage Volumes UI, or via kubectl

:checkered\_flag: Clone your Block Storage Volumes to instantiate Virtual Servers from a template&#x20;

:fire: Run automated backups of your Shared File System Volumes to BackBlaze via [CoreWeave Apps](https://apps.coreweave.com)

### How to provision CoreWeave Cloud Storage

The CoreWeave Cloud UI has an easy to use Storage Volume management page:

![](<../.gitbook/assets/image (66).png>)

Storage can also be managed via the Kubernetes API natively via kubectl. Below are example resource manifests.

{% tabs %}
{% tab title="Block Volume - All-NVMe" %}
{% code title="data-ssd-nvme.yaml" %}
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
{% endtab %}

{% tab title="Shared File System - HDD" %}
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

{% hint style="warning" %}
For the vast majority of use cases, workloads should run in the same region as the storage they are accessing. Use the [region label affinity](label-selectors.md) to limit scheduling of the workload to a single region. There are certain exceptions:

\
:notes:  Batch workloads where IOPS are not a concern but accessing compute capacity from multiple regions might give scaling benefits\
:gear:  When data is strictly read during startup of a process, such as when reading a ML model from storage into system and GPU memory for inference\
\
As a rule of thumb, Block volumes should always be used in the same region they are allocated. Shared volumes are where the above noted exceptions might be relevant.
{% endhint %}

### Billing&#x20;

Storage is billed per gigabyte of allocated (requested) space as an average over a billing month.

### **Resizing** :dart:****

Volumes can be expanded by simply increasing the `storage` request and reapplying the manifest. Shared File System Volumes are resized online without disruption the workload. For Block Volumes you will need to stop or restart all workloads that are attaching the volume for the resize to take effect. **Please note that volumes cannot be shrunk after they are expanded.** Storage volumes can be resized in the[ CoreWeave Cloud UI](https://cloud.coreweave.com) or via kubectl.

![](<../.gitbook/assets/Screen Shot 2022-05-25 at 4.33.13 PM (1).png>)

One-line example to grow a storage volume: `kubectl patch pvc <myvolume> -p '{"spec":{"resources":{"requests":{"storage": "500Gi"}}}}'`

## Ephemeral Storage

All physical nodes are equipped with SSD or NVMe ephemeral (local) storage. Ephemeral storage available ranges between 512GB to 2TB depending upon node type. No volume claims are needed to allocate ephemeral storage, simply write anywhere in the container file system. If a larger amount (above 20GB) of ephemeral storage is used, it is recommended to include this in the workloads resource request.

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
