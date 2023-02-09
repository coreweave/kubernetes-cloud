# Cloning block volumes

**Objective:** Clone a Virtual Server block volume between storage classes, or regions.\
**Overview:** This guide details using the `clone_block_volume` function from the [Kubernetes Cloud](https://github.com/coreweave/kubernetes-cloud) repository to clone between two example datacenter regions.&#x20;

{% hint style="success" %}
This guide requires `kubectl` and a valid access token. View [Getting Started](../../coreweave-kubernetes/getting-started/) for more details.
{% endhint %}

## Volume Cloning

### Storage Classes

[Storage](../../storage/storage/) on CoreWeave Cloud is delineated by [storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/), in the notation of `<storage type block|shared>`-`<storage medium hdd|nvme>`-`<region ord1|las1|etc>`. For example:

* `block-nvme-ewr1`
* `block-nvme-las1`
* `block-nvme-lga1`
* `block-nvme-ord1`

[CSI Volume Cloning](https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/) allows an existing volume to be duplicated:

### Cloning via CLI within the same Storage Class

Cloning a block volume within the _same_ storage class is easily done using our [PVC cloning script](../../../virtual-server/pvc-clone.sh), or with a simple PVC manifest:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: destination-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: block-nvme-ord1
  volumeMode: Block
  resources:
    requests:
      storage: 1234Gi
  dataSource:
    kind: PersistentVolumeClaim
    name: source-pvc
```

### Cloning via Web UI within the same Storage Class

Cloning within the same storage class can also be accomplished via the [CoreWeave Cloud Storage UI](https://cloud.coreweave.com/storage):&#x20;

![](<../../.gitbook/assets/image (55) (1).png>)

### Cloning via CLI between Storage Classes

Cloning a block volume between storage classes, as done when cloning between regions, requires data within the volume to be manually duplicated, as it cannot be zero-copied.&#x20;

To automate the process of cloning a Virtual Server root disk block volume, we provide a [block volume cloning script](../../../virtual-server/clone\_block\_volume.sh). This script creates a Kubernetes [Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) along with a new volume in the destination region, and uses `dd` to clone between source as destination.

First, we identify the Virtual Server root disk volume we'd like to clone:

{% embed url="https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/clone_block_volume.sh" %}

```bash
$ kubectl get pvc vs-example
NAME         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
vs-example   Bound    pvc-78d4950a-e1ba-476f-815e-b9c32e9c8b27   40Gi       RWO            block-nvme-ewr1   3m11s
```

Ensure it's not running:

```bash
$ kubectl get vs vs-example
NAME         STATUS                 REASON                 STARTED   INTERNAL IP   EXTERNAL IP
vs-example   VirtualServerStopped   VirtualServerStopped   False 
```

Download and source the script:

```
$ curl https://raw.githubusercontent.com/coreweave/kubernetes-cloud/master/virtual-server/clone_block_volume.sh -o ~/clone_block_volume.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4109  100  4109    0     0  27211      0 --:--:-- --:--:-- --:--:-- 27211

$ source ~/clone_block_volume.sh
```

Initiate a clone:

```
$ clone_block_volume  --source vs-example --destination vs-example --region lga1
persistentvolumeclaim/vs-example-lga1 created
job.batch/clone-vs-example-lga1 created
No resources found in namespace.
pod/clone-vs-example-lga1-rn55n condition met
job.batch/clone-vs-example-lga1 condition met
42945478656 bytes (43 GB, 40 GiB) copied, 54 s, 795 MB/s 
40960+0 records in
40960+0 records out
42949672960 bytes (43 GB, 40 GiB) copied, 54.0091 s, 795 MB/s
job.batch "clone-vs-example-lga1" deleted

```

#### Script Workflow

In the clone example above, the following actions were performed:

* A new PVC in the destination namespace was created - `vs-example-lga1`
* A cloning job was created - `clone-vs-example-lga1`
* The script pauses until a worker pod is spun up - `clone-vs-example-lga1-rn55n`
* The script pauses until the job reports a completed status
* Stats from the copy job are printed
* The Job (and its worker pod) are cleaned up and deleted

#### Script Arguments

* `--source`
  * Name of the root disk volume being cloned
* `--destination`
  * Desired name of new volume
  * Region will always be appended as `-region`, e.g `new-vol-lga1`
* `--region`
  * Name of destination region
  * Storage class is automatically derived as `block-nvme-region`
