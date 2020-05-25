# Storage

## Persistent Storage

Fast SSD and cost effective HDD storage is available as both block storage and shared filesystem. All data is replicated for High Availability. Storage is allocated using Kubernetes [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims). Volumes are automatically provisioned when a Volume Claim is created.

#### Block Storage

Block Storage provides the best performance, and is the recommended storage access method whenever possible. Block Storage is exposed via the Kubernetes `ReadWriteOnce` access mode. Block volumes can only be attached to a single physical node at the same time.

{% tabs %}
{% tab title="HDD" %}
{% code title="data-hdd-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: ceph-hdd-2-replica
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}
{% endtab %}

{% tab title="SSD" %}
{% code title="data-ssd-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: ceph-ssd-2-replica
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Shared Filesystem

Unlike block volumes a shared filesystem can be accessed by multiple nodes at the same time. This storage type is useful for ie. reading assets for CGI rendering or loading ML models for parallel inference. A shared filesystem is accessed similarly to block storage. The access mode changes to `ReadWriteMany` and the storage class names are different.

{% tabs %}
{% tab title="HDD" %}
{% code title="shared-data-hdd-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data
spec:
  storageClassName: sharedfs-hdd-replicated
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}
{% endtab %}

{% tab title="SSD" %}
{% code title="shared-data-ssd-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data
spec:
  storageClassName: sharedfs-ssd-replicated
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Billing

Storage is billed per gigabyte of allocated \(requested\) space as average amount requested over the month.

## Ephemeral Storage

All physical nodes are equipped with SSD or NVMe persistent storage. Local storage available ranges between 100GB to 2TB depending on node type. No volume claims are needed to allocate local storage. Simply write anywhere in the container filesystem. If a larger amount \(above 20GB\) of ephemeral storage is used, it is recommended to include this in the workloads resource request.

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

