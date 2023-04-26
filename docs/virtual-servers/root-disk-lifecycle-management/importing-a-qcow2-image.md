---
description: Import a disk image from an external source
---

# Importing Disk Images

Disk images can be imported from external URLs to be used as source images for root or additional disks for Virtual Servers. In addition to `qcow2`, `raw` and `iso` formatted images are also supported, and may be compressed with either `gz` or `xz`.

Most Operating Systems and virtual appliances provide a Cloud image in `qcow2` or `raw` format. These are all compatible, and may be used while following this guide.

{% hint style="info" %}
**Note**

Using a `.iso` installation media (ie., a virtual DVD) requires additional parameters not covered in this document. For assistance, please [contact your CoreWeave Support Specialist](https://cloud.coreweave.com/contact).
{% endhint %}

There are three ways to import disk images from external sources:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Import a disk image using HTTP/HTTPS</strong></td><td><a href="importing-a-qcow2-image.md#using-http-https">#using-http-https</a></td></tr><tr><td><strong>Import a disk image via an external object store</strong></td><td><a href="importing-a-qcow2-image.md#using-an-external-object-store">#using-an-external-object-store</a></td></tr><tr><td><strong>Import a disk image via CoreWeave Object Storage</strong></td><td><a href="importing-a-qcow2-image.md#using-coreweave-object-storage">#using-coreweave-object-storage</a></td></tr></tbody></table>

## Using HTTP/HTTPS

A `DataVolume` is used to both do the import and store the imported image.

Use the following manifest to import a disk image already hosted on a publicly accessible HTTP/HTTPS Web server:

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: debian-import
spec:
  source:
      http:
         url: "http://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img"
  pvc:
    accessModes:
      - ReadWriteOnce
    volumeMode: Block
    storageClassName: block-nvme-ord1 # Update to region where your VS will run
    resources:
      requests:
        storage: 64Mi # Update to size of imported image
```

## Using an external object store

A `DataVolume` can also import a disk image from an S3-compatible object store. To import an image from an existing object store, create a `Secret` with your `accessKey` and `secretKey`:

```yaml
kind: Secret
metadata:
  name: object-import-secret
type: Opaque
apiVersion: v1
data:
  accessKeyId: EBMAq2KEBQyxLBi2ZipHQE1b
  secretKey: YeXoB0QmpdS4zYFDGn7UYaPu6EglSHI5MkIMfMcv2Z6n7GBLCNAA4gH13NMU
```

Apply the manifest:

```shell
$ kubectl apply -f object-import-secret.yaml

secret/object-import-secret created
```

The `Secret` - along with your object store URL - will be referenced in your manifest:

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: debian-import
spec:
  source:
      s3:
         url: https://object-store-tld/bucket-name/cirros-0.5.2-x86_64-disk.img
         secretRef: object-import-secret
  pvc:
    accessModes:
      - ReadWriteOnce
    volumeMode: Block
    storageClassName: block-nvme-ord1 # Update to region where your VS will run
    resources:
      requests:
        storage: 64Mi # Update to size of imported image
```

## Using CoreWeave Object Storage

An image stored locally can easily be uploaded to [CoreWeave Object Storage](../../storage/object-storage.md), then imported to a `DataVolume`.

Once your [object store credentials are generated and imported to s3cmd](../../storage/object-storage.md#using-the-cloud-ui-and-s3cmd), make a bucket in which to store your images:

```bash
$ s3cmd mb s3://images

Bucket 's3://images/' created
```

Next, upload a locally stored image:

{% code overflow="wrap" %}
```bash
$ s3cmd put cirros-0.5.2-x86_64-disk.img s3://images

upload: 'cirros-0.5.2-x86_64-disk.img' -> 's3://images/cirros-0.5.2-x86_64-disk.img'  [part 1 of 2, 15MB] [1 of 1]
 15728640 of 15728640   100% in    1s    11.44 MB/s  done
upload: 'cirros-0.5.2-x86_64-disk.img' -> 's3://images/cirros-0.5.2-x86_64-disk.img'  [part 2 of 2, 558kB] [1 of 1]
 571904 of 571904   100% in    0s     5.59 MB/s  done
```
{% endcode %}

Create an object store user manifest with `Read` permissions:

```yaml
apiVersion: objectstorage.coreweave.com/v1alpha1
kind: User
metadata:
  name: object-store-import
  namespace: tenant-test-test
spec:
  owner: tenant-test-test
  access: read
```

Apply the user manifest:

```bash
$ kubectl apply -f object-store-import.yaml

user.objectstorage.coreweave.com/object-store-import created
```

The generated access key needs some additional information in order for a `DataVolume` to parse it. First, grab your `accessKey`:

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash"><strong>$ kubectl get secret tenant-test-test-object-store-import-obj-store-creds -o jsonpath='{.data.accessKey}'
</strong>
EBMAq2KEBQyxLBi2ZipHQE1b
</code></pre>

Then, use the `accessKey` to patch in an `accessKeyId` of the same value:

{% code overflow="wrap" %}
```bash
$ kubectl patch secret tenant-test-test-object-store-import-obj-store-creds -p '{"data":{"accessKeyId":"EBMAq2KEBQyxLBi2ZipHQE1b"}}'

secret/tenant-test-test-object-store-import-obj-store-creds patched
```
{% endcode %}

The updated secret will be referenced in your `DataVolume` manifest.

{% hint style="info" %}
**Note**

The path-mapping for the Object Store URL uses sub-path mapping.
{% endhint %}

{% code overflow="wrap" %}
```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: debian-import
spec:
  source:
      s3:
         url: https://object.lga1.coreweave.com/images/cirros-0.5.2-x86_64-disk.img
         secretRef: object-import-secret
  pvc:
    accessModes:
      - ReadWriteOnce
    volumeMode: Block
    storageClassName: block-nvme-ord1 # Update to region where your VS will run
    resources:
      requests:
        storage: 64Mi # Update to size of imported image
```
{% endcode %}

## Monitor the disk image import

After deploying the manifest above:

```bash
$ kubectl apply -f dv.yaml
            
datavolume.cdi.kubevirt.io/debian-import created
```

The status of the import can be followed by using `kubectl get --watch` while it is importing:

```
$ kubectl get --watch dv debian-import
NAME            PHASE     PROGRESS   RESTARTS   AGE
debian-import   Pending   N/A                   4s
debian-import   ImportScheduled   N/A                   7s
debian-import   ImportInProgress   N/A                   19s
debian-import   ImportInProgress   0.00%                 22s
debian-import   ImportInProgress   1.00%                 29s
debian-import   ImportInProgress   7.12%                 58s
...
debian-import   Succeeded          100.0%                11m


```

If the counter in the "`RESTARTS`" column increases, it means there has been an error while trying to import the image. Use `kubectl describe dv` to see the error:

```bash
$ kubectl describe dv debian-import

...
Events:
  Type     Reason             Age                From                   Message
  ----     ------             ----               ----                   -------
  Warning  ErrResourceExists  41s (x8 over 49s)  datavolume-controller  Resource "debian-import" already exists and is not managed by DataVolume
  Normal   Pending            40s                datavolume-controller  PVC debian-import Pending
  Normal   ImportScheduled    38s                datavolume-controller  Import into debian-import scheduled
  Normal   Bound              38s                datavolume-controller  PVC debian-import Bound
  Normal   ImportInProgress   14s                datavolume-controller  Import into debian-import in progress
  Warning  Error              6s (x2 over 11s)   datavolume-controller  Unable to process data: Virtual image size 2147483648 is larger than available size 576716800 (PVC size 2147483648, reserved overhead 0.000000%). A larger PVC is required.
```

{% hint style="info" %}
**Note**

Images are fully validated after import, which makes the import process slow. Import times will be decreased in the future.
{% endhint %}

## Launch a Virtual Server

After the image is finished importing, a Virtual Server can be launched with the imported image as the template for the root disk the same way they are launched using CoreWeave provided OS images.

Use [the Kubectl method](broken-reference) of deployment to create a Virtual Server manifest that specifies the source of the root disk:

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: example-vs
spec:
  region: ORD1
  os:
    type: linux
    enableUEFIBoot: false
  resources:
    cpu:
      # Reference CPU instance label selectors here:
      # https://docs.coreweave.com/coreweave-kubernetes/node-types
      type: amd-epyc-rome
      count: 4
    memory: 16Gi
  storage:
    root:
      size: 40Gi # Root disk will automatically be expanded
      storageClassName: block-nvme-ord1 # Needs to match the class of the imported volume
      source:
        pvc:
          namespace: tenant-test-test # Replace with your namespace
          name: debian-import
  # If the image supports cloudInit, the regular users configuration can be used
  #  users:
  #    - username: SET YOUR USERNAME HERE
  #      password: SET YOUR PASSWORD HERE  
  # To use key-based authentication replace and uncomment ssh-rsa below with your public ssh key
  #  sshpublickey: |
  #    ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
  network:
    public: true
    tcp:
      ports:
        - 22
```

{% hint style="info" %}
**Note**

When importing an image configured for `EFI` boot, set `spec.os.enableUEFIBoot` to `true`.&#x20;
{% endhint %}

Apply the manifest:

```bash
$ kubectl apply -f example-vs.yaml
               
virtualserver.virtualservers.coreweave.com/example-vs created
```

The Virtual Server will now initialize. Once fully launched and in `VirtualServerReady` status, it will be available over SSH (assuming the root disk image has supported SSH) as well as via [regular remote console](../../../virtual-servers/remote-access-and-control.md).

```bash
$ kubectl get vs example-vs

NAME           STATUS               REASON               STARTED   INTERNAL IP      EXTERNAL IP
example-vs     VirtualServerReady   VirtualServerReady   True      10.135.208.235   207.53.234.142
```

{% hint style="info" %}
**Note**

To export an Amazon AMI, chose the `raw` format when following the [AWS Export guide](https://docs.aws.amazon.com/vm-import/latest/userguide/vmexport\_image.html)
{% endhint %}
