---
description: Set up a Fortinet Firewall on CoreWeave Cloud
---

# Fortinet

The supported Fortinet Firewall product on CoreWeave Cloud is the `FGT_VM64_KVM`.

{% hint style="info" %}
**Note**

CoreWeave is not currently not able to supply licenses. Licenses will need to be [purchased separately from Fortinet](https://www.fortinet.com/corporate/about-us/request-a-quote).
{% endhint %}

## Setup

{% hint style="warning" %}
**Important**

The VPC **must be created** before the Firewall is deployed.
{% endhint %}

First, the Fortigate image must be imported to your namespace. You may either import it yourself, or [you can reach out to your CoreWeave Support Specialist to assist you](https://cloud.coreweave.com/contact).

{% hint style="success" %}
**Tip**

In the future, a selection of images will be available right from the Cloud, removing the need for a manual import.
{% endhint %}

### Importing the FGT image

{% hint style="warning" %}
**Important**

You must have a Fortinet account in order to have access to images.
{% endhint %}

Download the Fortigate image from [the Fortinet Firmware Images and Software Releases catalog](https://support.fortinet.com/Download/FirmwareImages.aspx).

<figure><img src="../../../.gitbook/assets/fg1.png" alt=""><figcaption><p>The Fortinet Firmware Images and Software Releases catalog with listed downloads</p></figcaption></figure>

Select the version you would like to download. In the example shown here, we have selected version `7.2.1`. Scroll down until you find an image file named `FGT_VM64_KVM-v7.2.1.F-build1254-FORTINET.out.kvm.zip`.

Once the image is downloaded, you will need to unzip it and upload it to a publicly accessible URL. This can be a CoreWeave Object Storage public bucket. Import the image to your namespace using the following manifest. Below is an example manifest for importing a Fortigate image in a given namespace.

| Option Name            | Instructions                                                  |
| ---------------------- | ------------------------------------------------------------- |
| `metadata.name`        | The name to assign to the DataVolume containing the FGT image |
| `metadata.namespace`   | Your namespace.                                               |
| `spec.source.http.url` | The source for the unpacked qcow2 image.                      |

{% hint style="info" %}
Read the guide on[ Importing External Images](../../../virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md) for more information.
{% endhint %}

#### **Example manifest**

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: fgt721
  namespace: tenant-example
spec:
  source:
      http:
         url: "http://example.com/fgt721.qcow2"
  pvc:
    accessModes:
      - ReadWriteOnce
    volumeMode: Block
    storageClassName: block-nvme-lga1
    resources:
      requests:
        storage: 2Gi
```

### Deploying Fortigate

Below is an example manifest for deploying a Fortigate instance into a given namespace.

| Option Name                         | Instructions                                                                                                                                                                                                                                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `metadata.name`                     | The name to assign to the Fortigate Firewall                                                                                                                                                                                                                                                     |
| `spec.network.vpcs.name`            | <p>The name of your VPC(s)<br><strong>Note:</strong> Multiple VPCs can be specified by adding additional <code>- name: vpc</code> items to the <code>vpcs.name</code> list</p>                                                                                                                   |
| `spec.public`                       | Specifies whether or not the CoreWeave networking IP should be publicly accessible. You will likely want this to be true                                                                                                                                                                         |
| `resources`                         | This correlates to the license you have purchased; refer to [Fortinet's FortiGate-VM virtual licenses and resources guide](https://docs.fortinet.com/document/fortigate-private-cloud/7.2.0/kvm-administration-guide/367417/fortigate-vm-virtual-licenses-and-resources) for further information |
| `storage.root.source.pvc.name`      | The DataVolume that was created previously                                                                                                                                                                                                                                                       |
| `storage.root.source.pvc.namespace` | Your namespace                                                                                                                                                                                                                                                                                   |

#### **Example manifest**

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: fgt-prod1
spec:
  initializeRunning: true
  network:
    vpcs:
    - name: vpc-lga1
    public: true
    directAttachLoadBalancerIP: true
  os:
    definition: a
    type: linux
  region: LGA1
  resources:
    cpu:
      count: 1
      type: amd-epyc-milan
    definition: a
    memory: 2Gi
  storage:
    root:
      accessMode: ReadWriteOnce
      size: 2Gi
      source:
        pvc:
          name: fgt721 
          namespace: tenant-example
      storageClassName: block-nvme-lga1
      volumeMode: Block
```
