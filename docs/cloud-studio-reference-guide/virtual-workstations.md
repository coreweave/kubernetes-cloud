---
description: Create Virtual Workstations on CoreWeave Cloud
---

# Virtual Workstations

Virtual Workstations are a great way for artists across the world to access applications requiring high powered CPU and GPU acceleration. Virtual Workstations improve artist workflows and reduce the burden of maintaining on-premises infrastructure, resulting in greater productivity, less strain on your team, and a better end-product for your clients.

Virtual Workstations are deployed on top of the open source project [Kubevirt](https://kubevirt.io/). The `virtctl` tool may be used for fine-grained control over Virtual Servers.

{% hint style="info" %}
**Tip**

Before continuing with this guide, you may want to learn a bit more about [Virtual Servers](broken-reference) (upon which Workstations are built), or a bit more about how to leverage `virtctl` for fine-grained control over Virtual Workstations.
{% endhint %}

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-cover data-type="files"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><p><strong>Get Started with Virtual Servers</strong></p><p></p><p>Learn all about CoreWeave <strong>Virtual Servers</strong> – what they are, how they work, and how to create them.</p></td><td></td><td><strong></strong></td><td><a href="../.gitbook/assets/virtualservers (1).jpeg">virtualservers (1).jpeg</a></td><td><a href="../../virtual-servers/getting-started.md">getting-started.md</a></td></tr><tr><td><strong>Managing Virtual Workstations using <code>virtctl</code></strong></td><td><p></p><p>The <a href="https://kubevirt.io/user-guide/operations/virtctl_client_tool/"><code>virtctl</code> tool</a> may be used for remotely controlling Virtual Workstations. If you require more <strong>fine-grained control</strong> over your Virtual Workstations, check out our Remote Access &#x26; Control guide.</p></td><td></td><td><a href="../.gitbook/assets/kubevirt (1).png">kubevirt (1).png</a></td><td><a href="../../virtual-servers/remote-access-and-control.md">remote-access-and-control.md</a></td></tr></tbody></table>

## Operating Systems

Virtual Workstations may be configured to run a variety of Operating Systems, including:

* Centos 7 (Teradici Desktop)
* Ubuntu 20.04 (Teradici Desktop)&#x20;
* Ubuntu 20.04
* Ubuntu 20.04 (No GPU)
* Ubuntu 18.04 (Teradici Desktop)
* Ubuntu 18.04
* Ubuntu 18.04 (No GPU)
* Windows 10 Professional
* Windows Server 2019 Standard
* Windows Server 2019 Datacenter

Workstations may be provisioned with GPUs or may be provisioned as CPU-only instances. CoreWeave offers a variety of CPUs, including AMD EPYC and Intel Xeon solutions. You can learn more about pricing and configuration in [our CPU-Only Instance Pricing guide](../../resources/resource-based-pricing.md#cpu-only-instance-resource-pricing).

## [Thinkbox Deadline](../vfx-and-rendering/vfx/deadline.md)

Workstations on CoreWeave Cloud support [Thinkbox Deadline](https://www.awsthinkbox.com/deadline), the most responsive modern render management solution for accessing render nodes and automatic workload scaling.

## Creating and configuring Virtual Workstations

In this example, we will create an array of Virtual Workstations with different configurations for both Windows and CentOS 7, and we will also be creating some lighter-weight machines for administrators. Later, we will configure special network policies in order to provide strong security barriers between different types of users.

To deploy our Workstations, we'll be using the [CoreWeave Cloud UI](../../virtual-servers/deployment-methods/coreweave-apps.md).

To get started creating a Virtual Workstation, first log in to your [CoreWeave Cloud account](https://cloud.coreweave.com). Once logged in, navigate to the Virtual Servers configuration screen by clicking the **Deploy Now** button below **Deploy Virtual Server** on the navigation card.

<figure><img src="../.gitbook/assets/image (43) (2).png" alt="&#x22;Deploy Virtual Server&#x22; menu card on the CoreWeave Cloud UI homepage"><figcaption><p>"Deploy Virtual Server" menu card on the CoreWeave Cloud UI homepage</p></figcaption></figure>

{% hint style="info" %}
**Note**

You can also navigate to the Virtual Server deployment screen by clicking the **Virtual Servers** link on the left-hand navigation.
{% endhint %}

Once you have [configured your Virtual Server](../../virtual-servers/getting-started.md) appropriately using the fields under the **Form** tab, navigate to the **YAML** tab.

From here, uncomment the `filesystems` stanza to mount in a shared storage volume as a filesystem.

<figure><img src="../.gitbook/assets/image (45).png" alt="Filesystems YAML stanza"><figcaption><p>Filesystems YAML stanza</p></figcaption></figure>

A valid specification may look something like the following:

```yaml
filesystems: 
  - name: render-outputs
    source:
      type: pvc
      name: render-outputs
```

### Creating machines for artists

For the artist machines, we will provision three separate VMs using either Teradici or Parsec for remote access.

{% hint style="info" %}
**Note**

At this time, **Parsec is not supported on CentOS 7.**

Also, please note that **V100s are not compatible** **with Teradici**. The best solution when using Teradici for remote access is to use a Quadro GPU, such as an A6000, A5000, A40, RTX6000, RTX5000 or RTX4000.

For more information, [view our Node Types guide.](../../coreweave-kubernetes/node-types.md)
{% endhint %}

To get started, log in to your CoreWeave Cloud account, then navigate to [the Applications page](https://apps.coreweave.com). From this page, navigate to the applications **Catalog** by clicking the Catalog tab at the top of the screen. From here, search for `virtual server`, and select the **virtual-server** application to bring up the configuration screen and configure your Virtual Server.

For this first machine, create a Windows VDI by selecting **Windows 10 Professional** from the OS buttons and related drop down.

<figure><img src="../../.gitbook/assets/image (63) (1) (1).png" alt="The Windows 10 selection box"><figcaption><p>The Windows 10 selection box</p></figcaption></figure>

Once you have specified the other details for your artist workstation, such as GPU type and number, CPU type and number, and so on, then input your user credentials.

{% hint style="warning" %}
**Important**

If you are utilizing Active Directory, you will have to put in a temporary user before you connect the storage volume.
{% endhint %}

The three examples in the reference namespace are:

* Windows 10 with Parsec (`artist-parsec`)
* Windows 10 with Teradici (`artist-tera-win`)
* CentOS 7 with Teradici (`artist-teridici-centos`)

{% hint style="info" %}
**Note**

You may choose to create your own [Parsec Teams account](https://parsec.app/teams) for management capabilities, or you can license and administer Parsec through CoreWeave. To do this, please contact your [CoreWeave support specialist](https://cloud.coreweave.com/contact).
{% endhint %}

To view the Workstation configurations as a YAML manifest, click the **YAML** tab. The configuration will look similar to the example Workstation manifest shown below. With the exception of the source image (`root.source`), all other values remain the same for each workstation.

<details>

<summary>Click to expand - Example Workstation manifest</summary>

```yaml
affinity: {}
initializeRunning: true
labels:
  user.group: artist
network:
  directAttachLoadBalancerIP: true
  floatingIPs: []
  public: true
  tcp:
    ports:
    - 22
    - 443
    - 60443
    - 4172
    - 3389
  udp:
    ports:
    - 4172
    - 3389
persistentVolumes: []
region: ORD1
resources:
  cpu:
    count: 8
    type: ""
  definition: a
  gpu:
    count: 1
    type: Quadro_RTX_4000
  memory: 32Gi
storage:
  additionalDisks: []
  filesystems: []
  root:
    accessMode: ReadWriteOnce
    size: 255Gi
    source:
      name: virtual-artist-20211102-block-ord1
      namespace: tenant-sta-vfx1-reference
      type: pvc
    storageClassName: block-nvme-ord1
    volumeMode: Block
users:
- password: password
  username: username
```

</details>

Next, click the **Deploy** button to launch the Virtual Server in your namespace.

Once the Virtual Server is running, log into it, then start Parsec and enter your credentials.

{% hint style="info" %}
**Note**

You may decide at this point to load up a Virtual Server with the applications you'd like to be incorporated in a base image. For more information on how to do this, review our [Root Disk Lifecycle Management guide](../../virtual-servers/root-disk-lifecycle-management/).
{% endhint %}

### Windows with Teradici

To deploy a Windows 10 Workstation with Teradici installed, the process is almost the same as the above, except that the [Cloud-init](https://cloud-init.io/) values will be leveraged through the YAML editor in order to automatically install Teradici on deployment.

By navigating to the YAML tab inside the Virtual Server deployment interface, find the following block, which will be commented out by default as shown here:

```yaml
#cloudInit: |
#  # Write a simple script
#  write_files:
#  - content: |
#      #!/bin/bash
#      echo "Hello world!"
#    path: /home/myuser/script.sh
#    permissions: '0744'
#    owner: myuser:myuser
#  # Update packages
#  package_update: true
#  # Install packages
#  packages:
#    - curl
#    - git
#  # Run additional commands
#  runcmd:
#    - [df, -h]
#    - [git, version]
#    - [curl, --version ]
#    - [bash, /home/myuser/script.sh]
```

To install Teradici on startup, simply uncomment the first line, then add:

```
cloudInit:
  teradici: true
```

Next, deploy the Virtual Server by clicking the **Deploy** button. Once the Virtual Server is done initializing, the credentials specified in the creation interface may be used to connect to it.

{% hint style="info" %}
**Note**

If you would like to add additional applications on initialization, the Windows package manager [Chocolatey](https://chocolatey.org/) is recommended. To use Chocolatey, add a list of application names to the `choco_install` parameter in the YAML specification in the `cloudInit` block.

For example:

```yaml
cloudInit:
    choco_install: [googlechrome,firefox,vlc]
```

For a list of valid application names, refer to [the Chocolatey community packages directory](https://community.chocolatey.org/packages).
{% endhint %}

For the final machine, follow the same steps outlined above, with the modification that under **Operating System Additions**, toggle on **Teradici** and **NVIDIA Drivers**.

<figure><img src="../.gitbook/assets/Screen Shot 2021-11-08 at 3.37.58 PM.png" alt="Operating System Addition toggles, only be available with Virtual Servers running Linux"><figcaption><p>Operating System Addition toggles, only be available with Virtual Servers running Linux</p></figcaption></figure>

For the Linux-based Workstation, storage will be mounted in via [Virtiofs](https://virtio-fs.gitlab.io/). To configure the filesystem for this kind of Workstation, navigate to the YAML editor by clicking the **YAML** tab at the top of the screen, then find the `filesystem` block inside the manifest. Edit the block to specify the filesystem source, type, and name:

```yaml
filesystems: 
  - name: render-outputs
    source:
      type: pvc
      name: render-outputs
```

### Configuring administrators

Typically, administrators and support staff do not need the same resources as artists for their work. Setting up an administrator machine can be done in a few simple steps.

First, launch a new Virtual Machine configured to run Windows 10.

![Cloud UI Virtual Server configuration menu](<../.gitbook/assets/Screen Shot 2021-11-08 at 3.46.02 PM.png>)

{% hint style="warning" %}
**Important**

Windows machines are not accessible via Teradici without a NVIDIA graphics card. In this case, RDP or Parsec may be used for administrator remote access instead.
{% endhint %}

In our reference namespace, we will create two administrator Windows 10 machines with both Teradici and Parsec in the same way as our artist machines, labeled `admin-teradici` and `admin-parsec`, respectively.
