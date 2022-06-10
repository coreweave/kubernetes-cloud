---
description: Importing a qcow2 image from a Internet URL
---

# Importing a QCOW2 image

Images from external URLs can be imported and used as source images for both root and additional disks in Virtual Servers. In addition to `qcow2`, `raw` and `iso` images are also supported. Images may be compressed with either `gz` or `xz`.

{% hint style="info" %}
Most operating systems and virtual appliances provide a cloud image in qcow2 or raw format. These are all compatible and ready to use with this guide. Using a .iso installation media (ie virtual DVD) requires additional parameters not covered by this document.
{% endhint %}

### Importing Disk Image

A `DataVolume` is used to both do the import and store the imported image.

{% code title="debian-import-datavolume.yaml" %}
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
{% endcode %}

```bash
$ kubectl apply -f dv.yaml                  
datavolume.cdi.kubevirt.io/debian-import created
```

The status of the import can be followed by getting the `DataVolume` while it is importing.

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

If the counter in "RESTARTS" is increasing, it means there is an error while trying to import the image. Describe the `DataVolume` to see the error.

```
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
Images are fully validated after import, which makes the import process slow. Import times will be decreased in the future.
{% endhint %}

### Launching a Virtual Server

After the import, a Virtual Server can be launched with the imported image as the template for the root disk just as with the CoreWeave provided OS images.

{% code title="example-vs.yaml" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: example-vs
spec:
  region: ORD1
  os:
    type: linux
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
{% endcode %}

```bash
$ kubectl apply -f example-vs.yaml                  
virtualserver.virtualservers.coreweave.com/example-vs created
```

The Virtual Server will now start, and be available over SSH (assuming the image supports SSH) as well as [regular remote console](../../../virtual-servers/remote-access-and-control.md).

```
$ kubectl get vs example-vs
NAME           STATUS               REASON               STARTED   INTERNAL IP      EXTERNAL IP
example-vs     VirtualServerReady   VirtualServerReady   True      10.135.208.235   207.53.234.142
```

{% hint style="info" %}
To export an Amazon AMI, chose the `raw` format when following the [AWS Export guide](https://docs.aws.amazon.com/vm-import/latest/userguide/vmexport\_image.html)
{% endhint %}
