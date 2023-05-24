---
description: Manage Storage Volumes using Kubectl
---

# Using Storage - Kubectl

## Creating Storage Volumes

Storage can be managed via the Kubernetes API natively using `kubectl`. Below are some example manifests to do this, as well as descriptions of the fields used.

<table><thead><tr><th width="247.33333333333331">Field name</th><th width="110">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>storageClassName</code></td><td>string</td><td>Sets the storage class name for the volume's PVC; determines which kind of storage class the volume will be</td></tr><tr><td><code>accessModes</code></td><td>list</td><td>Sets the <a href="https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes">access mode</a> for the volume</td></tr><tr><td><code>resources</code></td><td>array</td><td>Defines which resources with which to provision the Volume</td></tr><tr><td><code>requests</code></td><td>array</td><td>Defines the resource requests to create the volume</td></tr><tr><td><code>storage</code></td><td>string</td><td>Determines the size of the volume, in Gi</td></tr><tr><td><code>storage.root.serial</code></td><td>bool</td><td>The root disk serial number. When not specified, a new serial number is generated, which is preserved between restarts.</td></tr></tbody></table>

### **All-NVMe volumes**

**All-NVMe** Cloud Storage Volumes can be provisioned using the following storage class convention:

**Block Volumes:** `block-nvme-<region>`\
**Shared File System:** `shared-nvme-<region>`

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

## Attaching Storage Volumes

{% hint style="warning" %}
**Important**

The volumes must first be created and provisioned **before** they can be attached to a Pod or Virtual Server.
{% endhint %}

Attaching Storage Volumes using the Kubectl command line varies depending on whether you are attaching [to Pods](using-storage-kubectl.md#to-pods) or [to Virtual Servers](using-storage-kubectl.md#to-virtual-servers).

### **To Pods**

**Filesystem attachments**

To attach filesystem storage to a Pod, specify the `mountPath` and `name` under the `volumeMounts` stanza. Then, specify the `volumes.name` and the `persistentVolumeClaim.claimName` as shown in the following example.

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
      claimName: filesystem-storage-pvc
</code></pre>

**Block storage attachments**

As a kind of device, block storage is attached to a Pod by providing the `devicePath` under `volumeDevices`, in addition to the `volumes.name` and `persistentVolumeClaim.claimName` values, as demonstrated in the example below.

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

### To Virtual Servers

#### Filesystem attachments

The filesystem attachment information for Virtual Servers is provided in the `storage.filesystems` stanza of the spec. The following example demonstrates specifying values for `filesystems.name`, `filesystems.mountPoint`, and `persistentVolumeClaim.name`:

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

#### Block storage attachments

To attach a block storage device to a Virtual Server, specify the block device's values in the `storage.additionalDisks` stanza, as demonstrated in the following example.

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

#### **Read-only additional disks**

`VirtualServer.spec.storage.additionalDisks[]` allows attaching disks as read-only.

<table><thead><tr><th width="275.66666666666663">Field</th><th width="93">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>storage.additionalDisks[ ].readOnly</code></td><td>bool</td><td>The additional disk is attached as a read-only device. Default set to <code>false</code>.</td></tr></tbody></table>

If you are using a PVC, and the value of `persistentVolumeClaim.readOnly` on the PVC disk is set to `true`, the value of `VirtualServer.spec.storage.additionalDisks[].readOnly` **must also be set to `true`**.

If it is not, the Virtual Server will report an error.

<table data-header-hidden><thead><tr><th width="293.3333333333333">Disk type</th><th>Action</th></tr></thead><tbody><tr><td><code>readOnly</code> disk</td><td>Set the <code>vs.storage.additionalDisks.readOnly: true</code>.</td></tr><tr><td><code>readOnly</code> disk with a <code>readOnly</code> PVC</td><td>Set both the value for the storage disk to (<code>vs.storage.additionalDisks.readOnly</code>) to <code>true</code>, as well as the PVC claim (<code>additionalDisk.spec.persistentVolumeClaim.readOnly</code>) to <code>true</code>.</td></tr></tbody></table>

## **Resizing Volumes**

**Shared File System Volumes** are resized online without disruption the workload, but resizing **Block Volumes** requires stopping or restarting all workloads that are attached the Volume in order for the resize to take effect.

{% hint style="warning" %}
**Important**

Volumes cannot be downsized again once they are expanded.
{% endhint %}

Expanding storage volumes via `kubectl` is as simple as a single-line command:

```bash
kubectl patch pvc <myvolume> -p \
'{"spec":{"resources":{"requests":{"storage": "500Gi"}}}}'
```
