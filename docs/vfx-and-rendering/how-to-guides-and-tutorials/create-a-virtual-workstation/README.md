---
description: Get started with creating a Virtual Workstation
---

# Create a Virtual Workstation

A Virtual Workstation is a specialized use of a CoreWeave [Virtual Server](broken-reference).

In this tutorial, several Virtual Workstations are created using the [CoreWeave Cloud UI](../../../../virtual-servers/deployment-methods/coreweave-apps.md). The first machines demonstrate different configurations for artist use for both Windows and CentOS 7. Then, a few lighter-weight machines are deployed for administrator use.

[Network Policies](networking.md) are deployed to provide strong security barriers between these different types of users.

## Prerequisites

This guide assumes that the user already has [an active CoreWeave Cloud account](../../../welcome-to-coreweave/getting-started.md).

## Create a Virtual Workstation

Log in to your [CoreWeave Cloud account](https://cloud.coreweave.com), then navigate to [the Virtual Servers configuration screen ](https://cloud.staging.coreweave.com/virtualservers)either by clicking the **Deploy Now** button on the **Deploy Virtual Server** card, or by clicking the **Virtual Servers** link on the left-hand navigation.

<figure><img src="../../../.gitbook/assets/image (43) (1).png" alt="&#x22;Deploy Virtual Server&#x22; menu card on the CoreWeave Cloud UI homepage"><figcaption><p>"Deploy Virtual Server" menu card on the CoreWeave Cloud UI homepage</p></figcaption></figure>

## Create additional machines for artists

Simple Virtual Workstations for artist use are easily created from the Virtual Server deployment form. In these examples, either [Teradici or Parsec](../../../virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md#operating-system-additions) is installed as an Operating System add-on to provide remote access to the machines.

{% hint style="info" %}
**Note**

* You may choose to create your own [Parsec Teams account](https://parsec.app/teams) for management capabilities, or you can license and administer Parsec through CoreWeave. To do this, please contact your [CoreWeave support specialist](https://cloud.coreweave.com/contact).
* V100s are **not compatible** with Teradici. The best solution when using Teradici for remote access is to use a Quadro GPU, such as an A6000, A5000, A40, RTX6000, RTX5000 or RTX4000. For more information, see[ Node Types](../../../../coreweave-kubernetes/node-types.md).
{% endhint %}

Begin by repeating the process for [creating a new Virtual Workstation](./#create-a-virtual-workstation): navigate to the Virtual Server creation screen and begin configuring the machine.

For this tutorial, the first artist machine will run **Windows 10 Professional**. Select **Windows 10 Professional** from [the Operating System configuration screen](../../../virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md):

<figure><img src="../../../.gitbook/assets/image (19) (4).png" alt=""><figcaption><p>Select "Windows 10 Professional" from the Operating System expandable</p></figcaption></figure>

Continue to configure the artist machine.

{% hint style="warning" %}
**Important**

If you are utilizing Active Directory, you will have to put in a temporary user before you connect the storage volume.
{% endhint %}

### Windows with Parsec

To deploy a Windows 10 Workstation with Parsec, click the **Parsec Remote Desktop** toggle under **Operating System Additions**.

<figure><img src="../../../.gitbook/assets/image (3) (4).png" alt=""><figcaption></figcaption></figure>

Next, click the **Deploy** button to launch the Virtual Workstation in your namespace. Once the Virtual Workstation is running, log into it. Start Parsec, then enter your credentials.

### Windows with Teradici

To deploy a Windows 10 Workstation with Teradici instead of Parsec, click the Teradici toggle under **Operating System Additions**.

<figure><img src="../../../.gitbook/assets/image (23) (4).png" alt=""><figcaption></figcaption></figure>

Deploy the Virtual Server by clicking the **Deploy** button. Once the Virtual Server is done initializing, the credentials specified in the creation interface may be used to connect to it.

Next, click the **Deploy** button to launch the Virtual Workstation in your namespace. Once the Virtual Workstation is running, log into it. Start Teradici, then enter your credentials.

{% hint style="success" %}
**Tip**

To add additional applications upon initialization, the Windows package manager [Chocolatey](https://chocolatey.org/) is recommended.

To use Chocolatey, add a list of application names to the `choco_install` parameter in the Workstation [YAML manifest](./#workstation-yaml-manifest) in the `cloudInit` block.

For example:

```yaml
cloudInit:
    choco_install: [googlechrome,firefox,vlc]
```

For a list of valid application names, refer to [the Chocolatey community packages directory](https://community.chocolatey.org/packages).
{% endhint %}

### Linux Workstations

{% hint style="info" %}
**Note**

At this time, Parsec is **not supported** on CentOS 7. Teradici requires NVIDIA Drivers to be installed.
{% endhint %}

Storage in Linux Workstations is mounted in via [Virtiofs](https://virtio-fs.gitlab.io/). The process is the same as the other workstations: select the desired Linux distribution and version, then toggle the desired Operating System Additions.

<figure><img src="../../../.gitbook/assets/image (28) (3).png" alt=""><figcaption></figcaption></figure>

### Workstation YAML manifests

If you are comfortable with Kubernetes, you may view the Workstation configurations as YAML manifests. Click the **EDIT YAML** tab on the right-hand side to expand the YAML editor.

Workstation configurations will look similar to this example manifest:

<details>

<summary>Click to expand - Example Workstation manifest</summary>

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
    namespace: tenant-coreweave-name
    name: new-1252
    annotations:
        external-dns.alpha.kubernetes.io/hostname: new-1252.tenant-coreweave-name.coreweave.cloud
    labels: {}
spec:
    region: LGA1
    resources:
        definition: a
        gpu:
            type: Quadro_RTX_4000
            count: 1
        cpu:
            count: 4
        memory: 8Gi
    os:
        definition: a
        enableUEFIBoot: false
        type: windows
    storage:
        root:
            storageClassName: block-nvme-lga1
            volumeMode: Block
            accessMode: ReadWriteOnce
            size: 79Gi
            source:
                pvc:
                    namespace: vd-images
                    name: win10-master-20230331-lga1
        filesystems: []
        additionalDisks: []
    network:
        public: true
        directAttachLoadBalancerIP: true
    users:
        -
            username: ''
            password: ''
    cloudInit: |
        autologon: true
        parsec: true
        edid: true
    readinessProbe:
        failureThreshold: 30
        initialDelaySeconds: 10
        periodSeconds: 20
        tcpSocket:
            port: 1337
    runStrategy: RerunOnFailure
    initializeRunning: true

```

</details>

With the exception of the source image (`root.source`), which specifies the Operating System image, all other values will remain the same for each workstation.

{% hint style="info" %}
**Note**

You may decide at this point to load up a Virtual Workstation with the applications you'd like to be incorporated in a base image. For more information on how to do this, review our [Root Disk Lifecycle Management guide](../../../../virtual-servers/root-disk-lifecycle-management/).
{% endhint %}

### Configuring administrators

Typically, administrators and support staff do not need the same resources as artists for their work. Setting up an administrator machine can be done in a few simple steps.

In this example, a new Virtual Machine is configured running Windows 10.

<figure><img src="../../../.gitbook/assets/image (25) (3).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

When artist machines are powered off, only the use of [persistent storage](../../../storage/storage/) and [public IP addresses](../../../../resources/resource-based-pricing.md#public-ip-address-pricing) are billed.
{% endhint %}
