# Storage

## CoreWeave Cloud Storage

Fast SSD and cost effective HDD storage are available as both block storage and shared filesystem types. All data is replicated for High Availability. Storage is allocated using Kubernetes [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims). Volumes are automatically provisioned when a Persistent Volume Claim is created.

| Storage Type      | Disk Class | Region | Storage Class Name |
| ----------------- | ---------- | ------ | ------------------ |
| Block Storage     | NVMe       | EWR1   | block-nvme-ewr1    |
| Block Storage     | HDD        | EWR1   | block-hdd-ewr1     |
| Shared Filesystem | NVMe       | EWR1   | shared-nvme-ewr1   |
| Shared Filesystem | HDD        | EWR1   | shared-hdd-ewr1    |
| Block Storage     | NVMe       | ORD1   | block-nvme-ord1    |
| Block Storage     | HDD        | ORD1   | block-hdd-ord1     |
| Shared Filesystem | NVMe       | ORD1   | shared-nvme-ord1   |
| Shared Filesystem | HDD        | ORD1   | shared-hdd-ord1    |
| Block Storage     | NVMe       | LGA1   | block-nvme-lga1    |
| Block Storage     | HDD        | LGA1   | block-hdd-lga1     |
| Shared Filesystem | NVMe       | LGA1   | shared-nvme-lga1   |
| Shared Filesystem | HDD        | LGA1   | shared-hdd-lga1    |
| Block Storage     | NVMe       | LAS1   | block-nvme-las1    |
| Block Storage     | HDD        | LAS1   | block-hdd-las1     |
| Shared Filesystem | NVMe       | LAS1   | shared-nvme-las1   |
| Shared Filesystem | HDD        | LAS1   | shared-hdd-las1    |

### Block Storage

Block Storage provides the best performance, and is the recommended storage access method whenever possible. Block Storage is exposed via the Kubernetes `ReadWriteOnce` access mode. Block volumes can only be attached to a single physical node at any one time.

{% tabs %}
{% tab title="NVMe" %}
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

{% tab title="HDD" %}
{% code title="data-hdd-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: block-hdd-ord1
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```
{% endcode %}
{% endtab %}
{% endtabs %}

### Shared Filesystem

Unlike block volumes a shared filesystem can be accessed by multiple nodes at the same time. This storage type is useful for parallel tasks, I.E. reading assets for CGI rendering or loading ML models for parallel inference. A shared filesystem is accessed similarly to block storage. The access mode changes to `ReadWriteMany` and the storage class names are different.

{% tabs %}
{% tab title="NVMe" %}
{% code title="shared-data-nvme-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data
spec:
  storageClassName: shared-nvme-ord1
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}
{% endtab %}

{% tab title="HDD" %}
{% code title="shared-data-hdd-pvc.yaml" %}
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
      storage: 100Gi
```
{% endcode %}
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
For the vast majority of use cases, workloads should run in the same region as the storage they are accessing. Use the [region label affinity](label-selectors.md) to limit scheduling of the workload to a single region. There are certain exceptions:

\
\- Batch workloads where IOPS are not a concern but accessing compute capacity from multiple regions might give scaling benefits\
\- When data is strictly read during startup of a process, such as when reading a ML model from storage into system and GPU memory for inference\
\
As a rule of thumb, Block volumes should always be used in the same region they are allocated. Shared volumes are where the above noted exceptions might be relevant.
{% endhint %}

### Billing

Storage is billed per gigabyte of allocated (requested) space as an average over a billing cycle.

### **Resizing**

Volumes can be expanded by simply increasing the `storage` request and reapplying the manifest. `ReadWriteMany` volumes are resized online without disruption the workload. For `ReadWriteOnce` volumes you will need to stop or restart all workloads that are attaching the volume for the resize to take effect. Please note that volumes cannot be shrunk after they are expanded. One-line example to grow a storage volume: `kubectl patch pvc myvolume -p '{"spec":{"resources":{"requests":{"storage": "500Gi"}}}}'`

## Ephemeral Storage

All physical nodes are equipped with SSD or NVMe ephemeral (local) storage. Ephemeral storage available ranges between 100GB to 2TB depending upon node type. No volume claims are needed to allocate ephemeral storage, simply write anywhere in the container filesystem. If a larger amount (above 20GB) of ephemeral storage is used, it is recommended to include this in the workloads resource request.

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
