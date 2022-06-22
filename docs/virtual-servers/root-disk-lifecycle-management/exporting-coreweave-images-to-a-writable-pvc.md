# Copying CoreWeave Images to a Writable PVC

**Objective:** Clone an existing CoreWeave image to your namespace, digestible by tools like Packer or bootable as a VS.\
**Overview:** This process consists of copying a CoreWeave block PVC from the **vd-images** namespace, into your own namespace.

#### References:

{% file src="../../.gitbook/assets/volume_clone.yaml" %}

{% hint style="success" %}
Be sure to review [Getting Started](../../coreweave-kubernetes/getting-started.md#obtain-access-credentials) and the [kubectl Virtual Server deployment method](../deployment-methods/kubectl.md#deploying-a-virtual-server) before starting this guide.
{% endhint %}

### Identifying source image

We start by identifying an image we wish to export and modify. To browse images from the CoreWeave store:

{% tabs %}
{% tab title="CLI" %}
```
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=windows --sort-by=.spec.storageClassName
```

{% hint style="info" %}
For more information on querying source images, see [Identifying Images](../coreweave-system-images/#identifying-images)
{% endhint %}
{% endtab %}
{% endtabs %}

In this example – we’ll be targeting the latest Windows Server 2019 Standard image presented from region **ORD1**:

{% hint style="info" %}
_Ensure your location is consistent throughout these examples – here we are using **ORD1** - valid locations also include **EWR1** and **LAS1**_
{% endhint %}

![](../../.gitbook/assets/0.png)

### Clone source image into namespace

Now we need to clone the PVC from vd-images into our own namespace so that we can attach it to a worker VM. To do this we deploy **volume\_clone.yaml** with `kubectl create -f volume_clone.yaml`

{% tabs %}
{% tab title="YAML" %}
{% code title="volume_clone.yaml" %}
```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  annotations:
  labels:
  name: winserver2019std-clone-20210701-ord1
  namespace: tenant-<name>
spec:
  pvc:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: 79Gi
    storageClassName: block-nvme-ord1
    volumeMode: Block
  source:
    pvc:
      name: winserver2019std-master-20210722-ord1
      namespace: vd-images
```
{% endcode %}

{% hint style="info" %}
Note here we are referencing the source image from vd-images **winserver2019std-master-20210701-ord1** and re-creating it in our own namespace with the name **winserver2019std-clone-20210701-ord1.**
{% endhint %}

{% hint style="warning" %}
Note storage size needs to be equal to or greater than the source disk capacity.
{% endhint %}
{% endtab %}
{% endtabs %}

With `kubectl get pvc`, we can see our newly cloned image existing in our own namespace:

![](../../.gitbook/assets/2.png)
