# Linux Images

CoreWeave offers a variety of operating system base images, enhanced to run on CoreWeave Cloud, stored in the `vd-images` namespace.

## Distributions and flavors

### Distributions

CoreWeave provides out of the box support for several popular Linux distributions:

* Ubuntu Linux 20.04
* Ubuntu Linux 22.04
* CentOS 7
* _Rocky Linux 8 support coming soon!_ :calendar:

{% hint style="info" %}
**Note**

Most "Generic Cloud" distribution images are drop-in compatible with the CoreWeave Cloud Virtual Server platform. \
\
For more information on importing an image, see [Importing a QCOW2 image](../root-disk-lifecycle-management/importing-a-qcow2-image.md#importing-disk-image).
{% endhint %}

### Flavors :ice\_cream:

Linux images provided by CoreWeave Cloud are available in three different flavors:

* Docker
* Docker + NVIDIA Drivers
* Docker + NVIDIA Drivers + Teradici Graphics Agent

{% hint style="info" %}
**Note**

Image flavors are tagged with the [metadata label](./#metadata-labels) `images.coreweave.cloud/features`
{% endhint %}

### Docker

All images are pre-installed with the [Docker Engine](https://docs.docker.com/engine/). Docker only images are not intended to be used with a GPU, and therefore do not have a desktop environment installed, or contain NVIDIA drivers.&#x20;

### Docker + NVIDIA

Images with feature tags `nvidia` and `docker` e.g. `nvidia_docker`, include the [Docker Engine](https://docs.docker.com/engine/), the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker), and [NVIDIA GPU drivers](https://www.nvidia.com/en-us/drivers/unix/). NVIDIA driver version is periodically changed in new image releases, pending validation and dependency matches.

While these images contain NVIDIA drivers and are therefore intended to be used with a GPU, no desktop environment is pre-installed.&#x20;

### Docker + NVIDIA + Teradici

Images with feature tags `nvidia`, `teradici`, and `docker` e.g. `nvidia_teradici_docker`, include the [Docker Engine](https://docs.docker.com/engine/), the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker), [NVIDIA GPU drivers](https://www.nvidia.com/en-us/drivers/unix/), and the [Teradici Graphics Agent](https://docs.teradici.com/find/product/cloud-access-software/2022.04/graphics-agent-for-linux?subscriptionName=cloud-access-plus). Out of the box, the graphics agent points to a CoreWeave Licensing Server, where Teradici subscription licenses are billed at an hourly rate.

Intended for use as a Virtual Workstation, Teradici tagged images come pre-installed with the [GNOME](https://www.gnome.org/) Desktop Environment.

Virtual Servers deployed with Teradici can be accessed using [their Software Client](https://docs.teradici.com/find/product/cloud-access-software/2022.04/software-client-for-linux?subscriptionName=cloud-access-plus) for Windows, macOS, and Linux.&#x20;

## cloud-init

All Linux images provided by CoreWeave Cloud include [cloud-init](https://github.com/canonical/cloud-init) for instance instantiation.&#x20;

Cloud-init provides a powerful way to provision an instance programmatically, or pass through generic metadata.

{% hint style="info" %}
**Additional Resources**

See more in [Cloud-init](../virtual-server-configuration-options/cloud-init.md).
{% endhint %}

### cloud-init Modules

cloud-init has various modules that process different directives from the provided metadata manifest.&#x20;

Modules are processed based on the configuration file located in `/etc/cloud/cloud.cfg`. As default, the following modules are processed:

```yaml
# The modules that run in the 'init' stage
cloud_init_modules:
 - migrator
 - seed_random
 - bootcmd
 - write-files
 - [ growpart, always ]
 - [ resizefs, always ]
 - disk_setup
 - [ mounts, always ]
 - [ set_hostname, always ]
 - update_hostname
 - update_etc_hosts
 - ca-certs
 - rsyslog
 - users-groups
 - ssh

# The modules that run in the 'config' stage
cloud_config_modules:
# Emit the cloud config ready event
# this can be used by upstart jobs for 'start on cloud-config'.
 - emit_upstart
 - snap
 - ssh-import-id
 - keyboard
 - locale
 - set-passwords
 - grub-dpkg
 - apt-pipelining
 - apt-configure
 - ubuntu-advantage
 - ntp
 - timezone
 - disable-ec2-metadata
 - runcmd
 - byobu

# The modules that run in the 'final' stage
cloud_final_modules:
 - package-update-upgrade-install
 - fan
 - landscape
 - lxd
 - ubuntu-drivers
 - write-files-deferred
 - puppet
 - chef
 - mcollective
 - salt-minion
 - reset_rmc
 - refresh_rmc_and_interface
 - rightscale_userdata
 - scripts-vendor
 - scripts-per-once
 - scripts-per-boot
 - scripts-per-instance
 - [ scripts-user, always ]
 - ssh-authkey-fingerprints
 - keys-to-console
 - install-hotplug
 - phone-home
 - final-message
 - power-state-change
```

{% hint style="info" %}
**Note**

For more information, see cloud-init's [Module Reference](https://cloudinit.readthedocs.io/en/latest/topics/modules.html#module-reference).
{% endhint %}

Modules in `cloud.cfg` that do not have a frequency specified follow the default behavior outlined in the [Module Reference](https://cloudinit.readthedocs.io/en/latest/topics/modules.html#module-reference). CoreWeave images configure select modules to process "always", vs "once-per-instance":

* `growpart`
* `resizefs`
* `mounts`
* `set_hostname`
* `scripts-user`

This ensures, respectively:&#x20;

* Partitions are re-sized after disk expansion
* File Systems are re-sized after disk expansion
* New Shared File Systems and other mounts are auto added to `fstab` and mounted
* `hostname` updates are respected
* Userdata scripts are always processed

### Virtual Server cloud-init abstractions

Some properties in a [Virtual Server Manifest](../deployment-methods/kubectl.md#understanding-the-virtual-server-manifest) map to cloud-init properties, and automatically populate those fields:&#x20;

#### `spec.users[]`

`spec.users[]` in a Virtual Server manifest populates cloud-init metadata for the [users and groups module](https://cloudinit.readthedocs.io/en/latest/topics/modules.html#users-and-groups).

The resultant metadata generated looks like this:

```yaml
users:
- lock_passwd: false
  name:
  plain_text_passwd:
  shell: /bin/bash
  ssh_authorized_keys:
  - ""
  sudo: ALL=(ALL) NOPASSWD:ALL
```

#### `storage.filesystems[]`

Adding [File System](../../storage/storage/#shared-file-system-volumes) mounts to a Virtual Server manifest populates cloud-init metadata for the [mounts module](https://cloudinit.readthedocs.io/en/latest/topics/modules.html#mounts).

The resultant metadata generated looks like this:

```yaml
mounts:
- - viofs-${name}
  - /mnt/${name}
  - virtiofs
  - rw,noatime,_netdev,nofail
  - "0"
  - "2"

```

#### `metadata.name`

The name of a Virtual Server is used to set the `hostname`, using the cloud-init [Update Hostname module](https://cloudinit.readthedocs.io/en/latest/topics/modules.html?highlight=hostname#update-hostname).&#x20;

The resultant metadata generated looks like this:&#x20;

```yaml
hostname: ${name}
```

#### Additional cloud-init metadata

Outside of the cloud-init abstractions provided in the Virtual Server spec, additional cloud-init metadata can be added to a manifest via `spec.cloudInit[]`. Metadata is passed as a multi-line string literal. As an example using the cloud-init [Package Update module](https://cloudinit.readthedocs.io/en/latest/topics/modules.html#package-update-upgrade-install):

```yaml
cloudInit: |
  package_update: true
```

The additional cloud-init metadata will be merged with the abstracted fields from the Virtual Server spec. The resultant, full metadata generated looks like this:

```yaml
hostname:
ssh_pwauth: "True"
users:
- lock_passwd: false
  name:
  plain_text_passwd:
  shell: /bin/bash
  ssh_authorized_keys:
  - ""
  sudo: ALL=(ALL) NOPASSWD:ALL
package_update: true

```

### Additional cloud-init metadata examples

Using additional cloud-init metadata provides an easy, repeatable method of configuring an instance at initial deployment. Actions that one may perform manually when deploying a new instance can be automated via cloud-init.&#x20;

#### Set system time zone

```yaml
cloudInit: |
  set_timezone: america/los_angeles
```

#### Update package repositories and packages

```yaml
cloudInit: |
  package_update: true
  package_upgrade: true
```

{% hint style="info" %}
**Note**

This performs `apt update && apt upgrade` or `yum upgrade` on first boot.
{% endhint %}

#### Install packages

```yaml
cloudInit: |
  packages:
    - cowsay
    - nyancat
    - [libpython2.7, 2.7.3-0ubuntu3.1]
```

{% hint style="info" %}
**Note**

Prior to installing packages, the repository database is updated. If no package version is specified, the latest version is installed.
{% endhint %}

#### Run arbitrary commands

```yaml
cloudInit: |
  runcmd:
    - [ ls, -l, / ]
    - ls -l /root
    - [ sh, -c, echo "=========hello world=========" ]
```

{% hint style="info" %}
**Note**

Commands and arguments can be formatted in any of the ways listed above.
{% endhint %}

#### Inject and run a `bash` script

```yaml
cloudInit: |
  write_files:
    - content: |
        #!/bin/bash
        echo "Hello World" > /tmp/test.txt
      owner: root:root
      path: /tmp/init.sh
      permissions: '0755'
  runcmd:
    - [ bash, /tmp/init.sh ]
```

#### Partition, format, and mount a new Block Volume

```yaml
cloudInit: |
  # The disk_setup directive instructs Cloud-init to partition a disk.
  disk_setup:
    /dev/vdc:
      table_type: gpt
      layout: True
      overwrite: False
  # fs_setup describes the how the file systems are supposed to look.
  fs_setup:
    - label: None
      filesystem: ext4
      device: /dev/vdc
      partition: 'auto'
  # 'mounts' contains a list of lists; the inner list are entries for an /etc/fstab line
  mounts:
   - [ vdc, /mnt/block-pvc, auto, "defaults" ]
```

### Full cloud-init Virtual Server manifest example

The Virtual Server manifest below combines all the examples above:

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-ubuntu2204
spec:
  region: ORD1
  os:
    type: linux
  resources:
    gpu:
      type: Quadro_RTX_4000
      count: 1
    cpu:
      count: 4
    memory: 16Gi
  storage:
    root:
      size: 40Gi
      storageClassName: block-nvme-ord1
      source:
        pvc:
          namespace: vd-images
          name: ubuntu2204-nvidia-515-43-04-1-teradici-docker-master-20220522-ord1
    additionalDisks:
      - name: vs-block-pvc
        spec:
          persistentVolumeClaim:
            claimName: vs-block-pvc
  users:
    - username:
      password:
  network:
    directAttachLoadBalancerIP: false
    public: true
  initializeRunning: true
  cloudInit: |
    set_timezone: america/los_angeles
    package_update: true
    package_upgrade: true
    packages:
      - git-all
      - unrar
      - openjdk-11-jdk
    write_files:
      - content: |
          #!/bin/bash
          KUBECTL_VERSION=v1.19.16
          curl -o /usr/local/bin/kubectl -sL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl
          chmod +x /usr/local/bin/kubectl
        owner: root:root
        path: /tmp/install_kubectl.sh
        permissions: '0755'
      - content: |
          #!/bin/bash
          VIRTCTL_VERSION="v0.38.1"
          curl -o /usr/local/bin/virtctl -sL https://github.com/kubevirt/kubevirt/releases/download/${VIRTCTL_VERSION}/virtctl-${VIRTCTL_VERSION}-linux-amd64
          chmod +x /usr/local/bin/virtctl
        owner: root:root
        path: /tmp/install_virtctl.sh
        permissions: '0755'
    runcmd:
      - [ bash, /tmp/install_kubectl.sh ]
      - [ bash, /tmp/install_virtctl.sh ]
      - [ bash, -c, echo alias k=kubectl >> /etc/bash.bashrc ]
      - [ bash, -c, echo alias virt=virtctl >> /etc/bash.bashrc ]
    # The disk_setup directive instructs Cloud-init to partition a disk.
    disk_setup:
      /dev/vdc:
        table_type: gpt
        layout: True
        overwrite: False
    # fs_setup describes the how the file systems are supposed to look.
    fs_setup:
      - label: None
        filesystem: ext4
        device: /dev/vdc
        partition: 'auto'
    # 'mounts' contains a list of lists; the inner list are entries for an /etc/fstab line
    mounts:
     - [ vdc, /mnt/vs-block-pvc, auto, "defaults" ]
```

After creating the Virtual Server, output from the cloudInit directives can be found in `/var/log/cloud-init-output.log`:

{% code overflow="wrap" %}
```bash
$ sudo cat /var/log/cloud-init-output.log

Cloud-init v. 22.1-14-g2e17a0d6-0ubuntu1~22.04.5 running 'init-local' at Sun, 05 Jun 2022 17:20:40 +0000. Up 6.62 seconds.
Cloud-init v. 22.1-14-g2e17a0d6-0ubuntu1~22.04.5 running 'init' at Sun, 05 Jun 2022 17:20:40 +0000. Up 7.32 seconds.
```
{% endcode %}
