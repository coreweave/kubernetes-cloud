# Configuring a Linux image sourced from CoreWeave Cloud

**Objective:** Use our Packer Virtual Server to configure a Linux image from CoreWeave Cloud.\
**Overview:** Combining examples from [Configuring a Windows Image sourced from CoreWeave Cloud](configuring-a-windows-image-sourced-from-coreweave-cloud.md) and [Configuring an externally sourced cloud Linux image](configuring-an-externally-sourced-cloud-linux-image.md), we will use our [Packer Worker Virtual Server](creating-a-packer-worker-virtual-server.md#deploying-virtual-server) to configure a Linux image sourced from CoreWeave Cloud.

#### References:

{% file src="../../../.gitbook/assets/centos.json" %}

## Selecting a source image

Following the example in [Copying CoreWeave Images to a Writeable PVC](../exporting-coreweave-images-to-a-writable-pvc.md), we will search for the latest CentOS image in the vd-images namespace:&#x20;

![](<../../../.gitbook/assets/image (5).png>)

We will then clone this image into our namespace:

{% tabs %}
{% tab title="YAML" %}
{% code title="volume_clone.yaml" %}
```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  annotations:
  labels:
  name: centos7-docker-master-clone-20210813-ord1
  namespace: tenant-<name>
spec:
  pvc:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: 40Gi
    storageClassName: block-nvme-ord1
    volumeMode: Block
  source:
    pvc:
      name: centos7-docker-master-20210813-ord1
      namespace: vd-images
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Setting up the Packer Environment

Following the example in [Creating a Packer Worker Virtual Server](creating-a-packer-worker-virtual-server.md#deploying-virtual-server), we'll mount our CentOS PVC as an additional disk:

{% tabs %}
{% tab title="YAML" %}
{% code title="packer_vs.yaml" %}
```yaml
    additionalDisks:
    - name: CentOS_7
      spec:
        persistentVolumeClaim:
          claimName: centos7-docker-master-clone-20210813-ord1
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Configuring the Packer manifest

Our Packer manifest will be a combination of our previous [Windows](configuring-a-windows-image-sourced-from-coreweave-cloud.md#configuring-the-packer-manifest) and [Ubuntu](configuring-an-externally-sourced-cloud-linux-image.md#configuring-packer-manifest) examples:

{% tabs %}
{% tab title="JavaScript" %}
{% code title="centos.json" %}
```javascript
{
    "builders": [
        {
            "type": "qemu",
            "accelerator": "kvm",
            "communicator": "ssh",
            "headless": true,
            "disk_image": false,
            "cpus": "6",
            "memory": "16384",
            "format": "raw",
            "iso_checksum": "none",
            "iso_url": "/dev/vdb",
            "skip_resize_disk": false,
            "skip_compaction": false,
            "disk_size": "40000M",
            "qemuargs": [
                ["-machine","pc-q35-4.2,accel=kvm,usb=off,vmport=off,dump-guest-core=off"],
                ["-cpu", "host"],
                [ "-smp", "cpus=4,sockets=1" ],
                [ "-cdrom", "cidata.iso" ],
                ["-drive", "file=/dev/vdb"]
            ],
            "ssh_username": "user",
            "ssh_password": "packer",
            "net_device": "virtio-net",
            "shutdown_command": "sudo shutdown --poweroff --no-wall now"
        }
    ],
    "provisioners": [
        {
            "type": "shell",
            "execute_command": "{{.Vars}} sudo -S -E bash '{{.Path}}'",
            "inline": [
                "yum update -y",
                "yum upgrade -y",
                "yum clean all -y"
            ]
        }
    ]
}
```
{% endcode %}

{% hint style="info" %}
**/dev/vdb** refers to our cloned block device
{% endhint %}

{% hint style="info" %}
The credentials in this configuration are created when the VM reads the image output of  [**create-ci-data.sh**](configuring-an-externally-sourced-cloud-linux-image.md#generate-credentials-for-the-packer-vm)****
{% endhint %}

{% hint style="info" %}
In this example, we are using the shell provisioner to install package updates. To learn more and view more provisioners, view [Hashicorp's documentation](https://www.packer.io/docs/provisioners/shell).
{% endhint %}
{% endtab %}
{% endtabs %}

## Execute Packer docker image

Similar to our [Windows example](configuring-a-windows-image-sourced-from-coreweave-cloud.md#execute-packer-docker-image), we'll kick off our CentOS build with `launch-docker.sh win.json`. Since we're writing to our PVC directly, all changes are made directly to our cloned disk.
