---
description: An example Virtual Server running CentOS 7 with LUKS encryption
---

# CentOS 7 Virtual Server with LUKS Encryption

The following example demonstrates how to deploy a Virtual Server running CentOS 7 with an encrypted partition on the root disk. The method used for this example is to [deploy a manifest using the Kubernetes command line](../deployment-methods/kubectl.md).

The manifest used to deploy this Virtual Server includes [cloud-init directives](centos-7-virtual-server-with-luks-encryption.md#cloud-init), which are used to encrypt unallocated space on the root disk. By using a separate partition instead of a separate block volume, additional Virtual Servers can be created by cloning the encrypted partition from the same disk.

This process essentially consists of [configuring a Deployment manifest](centos-7-virtual-server-with-luks-encryption.md#configure-the-deployment-manifest) for the Virtual Server, which includes several critical [cloud-init directives](centos-7-virtual-server-with-luks-encryption.md#cloud-init), and then [deploying it](centos-7-virtual-server-with-luks-encryption.md#deploy-the-virtual-server).

## Configure the Deployment manifest

The following manifest will be used to deploy the CentOS 7 Virtual Server. However, a few properties need to be adjusted prior to deployment.

<details>

<summary><strong>Click to expand - <code>centos-7-luks-partition.yml</code></strong></summary>

<pre class="language-yaml"><code class="lang-yaml">apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: centos7-luks
spec:
  region: LGA1
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
      storageClassName: block-nvme-lga1
      source:
        pvc:
          namespace: vd-images
          # Reference querying source image here:
          # https://docs.coreweave.com/virtual-servers/coreweave-system-images
          name: centos7-nvidia-510-85-02-docker-master-20220831-lga1
<strong>  users:
</strong>  - sshpublickey: ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
    username: user
  network:
    directAttachLoadBalancerIP: false
    public: true
    tcp:
      ports:
      - 22
  cloudInit: |
    runcmd:
      - [bash, -c, sgdisk -n 2:34:2047 -t 2:ef02 /dev/vda -g ]
      - [bash, -c, partprobe /dev/vda ]
      - [bash, -c, grub2-install /dev/vda ]
      - [bash, -c, (echo "@reboot /encrypt_init.sh")| crontab - ]
      - [bash, -c, touch /etc/cloud/cloud-init.disabled ]
      - [bash, -c, shutdown -h +1 ]
    write_files:
      - content: |
          #!/bin/bash
          PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
          sed -i 's/growpart,\ always/growpart,\ once-per-instance/g' /etc/cloud/cloud.cfg
          sed -i 's/resizefs,\ always/resizefs,\ once-per-instance/g' /etc/cloud/cloud.cfg
          rm -rf /var/lib/cloud/instances/*/scripts/runcmd
          rm -f /etc/cloud/cloud-init.disabled
   
          sgdisk -e /dev/vda
          partprobe /dev/vda
          sgdisk -n 3::0 /dev/vda
          partprobe /dev/vda
   
          phrase=$(openssl rand -base64 32)
          echo -n $phrase | cryptsetup -q luksFormat /dev/vda3 -
          echo -n $phrase | cryptsetup -q luksOpen /dev/vda3 CryptedPart1 -
          dd if=/dev/urandom of=/root/keyfile1 bs=1024 count=4
          chmod 0400 /root/keyfile1
          echo -n $phrase | cryptsetup luksAddKey /dev/vda3 /root/keyfile1 -
          mkfs.ext4 /dev/mapper/CryptedPart1
          mkdir /encryptedfs
          echo "/dev/mapper/CryptedPart1 /encryptedfs ext4 defaults 1 2" >> /etc/fstab
          echo "CryptedPart1 /dev/vda3 /root/keyfile1 luks" >> /etc/crypttab
          mount -a
          echo -n $phrase | cryptsetup -q luksRemoveKey /dev/vda3 -
          (echo "")| crontab -
          rm -- "$0"
        owner: root:root
        path: /encrypt_init.sh
        permissions: '0755'
  initializeRunning: true
  
</code></pre>

</details>

### Root disk size

`.spec.storage.root.size`

First, the desired size of the **unencrypted** portion of the root disk, where the Operating System resides, must be specified. After initialization, expanding this part of the disk will require manual re-partitioning.

In this example, the given value for the disk size is `40Gi`.

```yaml
  storage:
    root:
      size: 40Gi
```

### Root disk image

`.spec.storage.root.source.pvc.name`

The root disk image source must be specified. It is best practice to always use [the latest available root disk image](../coreweave-system-images/#listing-all-latest-images-available-for-use).

The latest CentOS 7 image with NVIDIA drivers can be found by invoking the following command:

{% code overflow="wrap" %}
```bash
$ kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=CentOS_7,images.coreweave.cloud/region=lga1 -o=custom-columns="PVC:metadata.name,NAME:metadata.labels['images\.coreweave\.cloud\/name'],FEATURES:metadata.labels['images\.coreweave\.cloud\/features'],SIZE:status.capacity.storage,STORAGECLASS:.spec.storageClassName" --sort-by='.metadata.name'
```
{% endcode %}

In this example, the value given is `centos7-nvidia-510-85-02-docker-master-20220831-lga1`.

```yaml
  storage:
    root:
      size: 40Gi
      storageClassName: block-nvme-lga1
      source:
        pvc:
          namespace: vd-images
          # Reference querying source image here:
          # https://docs.coreweave.com/virtual-servers/coreweave-system-images
          name: centos7-nvidia-510-85-02-docker-master-20220831-lga1
```

{% hint style="info" %}
**Additional Resources**

For more information for querying disk image sources, see [System Images](https://docs.coreweave.com/virtual-servers/coreweave-system-images).
{% endhint %}

### Users

`.spec.users[]`

Next, the [user accounts](../virtual-server-configuration-options/user-accounts.md) for the Virtual Server are specified in the `.users` array. In this example, users are authenticated using SSH keys (`sshpublickey`) only.

In the `sshpublickey` field, use [the user's personal public key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), along with a desired username set in the `username` field.

In this example, only one user is added with the `username` of `user` and a valid truncated key for the SSH key value:

```yaml
  - sshpublickey: ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
    username: user
```

More than one user may be added. See [User Accounts](../virtual-server-configuration-options/user-accounts.md#cli) for more information.

## cloud-init

Preparing the Virtual Server for an encrypted partition requires some pre-requisite steps, which are handled, along with encryption configuration, by [cloud-init](../coreweave-system-images/linux-images.md#cloud-init).

<details>

<summary>Click to expand - <code>cloud-init</code> directives excerpted from the manifest</summary>

<pre class="language-yaml" data-overflow="wrap"><code class="lang-yaml">  cloudInit: |
    runcmd:
      - [bash, -c, sgdisk -n 2:34:2047 -t 2:ef02 /dev/vda -g ]
      - [bash, -c, partprobe /dev/vda ]
      - [bash, -c, grub2-install /dev/vda ]
      - [bash, -c, (echo "@reboot /encrypt_init.sh")| crontab - ]
      - [bash, -c, touch /etc/cloud/cloud-init.disabled ]
      - [bash, -c, shutdown -h +1 ]
    write_files:
      - content: |
          #!/bin/bash
          PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
          sed -i 's/growpart,\ always/growpart,\ once-per-instance/g' /etc/cloud/cloud.cfg
          sed -i 's/resizefs,\ always/resizefs,\ once-per-instance/g' /etc/cloud/cloud.cfg
          rm -rf /var/lib/cloud/instances/*/scripts/runcmd
          rm -f /etc/cloud/cloud-init.disabled
   
          sgdisk -e /dev/vda
          partprobe /dev/vda
          sgdisk -n 3::0 /dev/vda
          partprobe /dev/vda
   
          phrase=$(openssl rand -base64 32)
          echo -n $phrase | cryptsetup -q luksFormat /dev/vda3 -
          echo -n $phrase | cryptsetup -q luksOpen /dev/vda3 CryptedPart1 -
          dd if=/dev/urandom of=/root/keyfile1 bs=1024 count=4
          chmod 0400 /root/keyfile1
          echo -n $phrase | cryptsetup luksAddKey /dev/vda3 /root/keyfile1 -
          mkfs.ext4 /dev/mapper/CryptedPart1
          mkdir /encryptedfs
          echo "/dev/mapper/CryptedPart1 /encryptedfs ext4 defaults 1 2" >> /etc/fstab
          echo "CryptedPart1 /dev/vda3 /root/keyfile1 luks" >> /etc/crypttab
<strong>          mount -a
</strong><strong>          echo -n $phrase | cryptsetup -q luksRemoveKey /dev/vda3 -
</strong>          (echo "")| crontab -
          rm -- "$0"
        owner: root:root
        path: /encrypt_init.sh
        permissions: '0755'
</code></pre>

</details>

The following aspects are handled by cloud-init in this manifest:

### GPT Configuration

By default, Virtual Server images are configured with an [Master Boot Record (MBR) partition table](https://en.wikipedia.org/wiki/Master\_boot\_record), which does not support sizes above `2Ti`. Because of this, the disk needs to be converted to a [GUID Partition Table (GPT)](https://en.wikipedia.org/wiki/GUID\_Partition\_Table). This process also requires re-partitioning, as GRUB must reside on a BIOS boot partition.

All of this is accomplished with a few commands in the `runcmd` cloud-init directive:

```yaml
 cloudInit: |
    runcmd:
      - [bash, -c, sgdisk -n 2:34:2047 -t 2:ef02 /dev/vda -g ]
      - [bash, -c, partprobe /dev/vda ]
      - [bash, -c, grub2-install /dev/vda ]
```

### Startup script bootstrapping

By default, `cloudInit` automatically[ expands the root disk partition to use all available unallocated space](../coreweave-system-images/linux-images.md#cloud-init-modules).

Because of this, the space allocated to the Virtual Server at creation time will automatically be used for the Operating System partition. To prevent this from happening on subsequent restarts after the disk has been expanded for the encrypted partition, we need to temporarily disable `cloudInit`.&#x20;

Since the Virtual Server needs to be powered off to expand its disk, we need to inject a script using the `write_files` cloud-init directive to do so, then instruct it to run at next start up using the `runcmd` directive:

```yaml
  - [bash, -c, (echo "@reboot /encrypt_init.sh")| crontab - ]
  - [bash, -c, touch /etc/cloud/cloud-init.disabled ]
  - [bash, -c, shutdown -h +1 ]
```

### Configuration startup script

After expanding the root disk and starting the Virtual Server back up, the script called `encrypt_init.sh` , which was injected via `write_files`, completes the configuration.

Then, cloud-init is re-enabled for subsequent reboots once the `growpart` and `resizefs` modules are disabled:

```yaml
   write_files:
      - content: |
          #!/bin/bash
          PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
          sed -i 's/growpart,\ always/growpart,\ once-per-instance/g' /etc/cloud/cloud.cfg
          sed -i 's/resizefs,\ always/resizefs,\ once-per-instance/g' /etc/cloud/cloud.cfg
          rm -rf /var/lib/cloud/instances/*/scripts/runcmd
          rm -f /etc/cloud/cloud-init.disabled
```

The GPT header is then moved to the expanded end of disk, and a new partition is created with the new unallocated space:

```yaml
          sgdisk -e /dev/vda
          partprobe /dev/vda
          sgdisk -n 3::0 /dev/vda
          partprobe /dev/vda
```

This new partition is initialized with LUKS, using a temporary key:

```yaml
          phrase=$(openssl rand -base64 32)
          echo -n $phrase | cryptsetup -q luksFormat /dev/vda3 -
          echo -n $phrase | cryptsetup -q luksOpen /dev/vda3 CryptedPart1 -
```

A key file is generated and secured, so the partition can be auto-mounted at boot:

```yaml
          dd if=/dev/urandom of=/root/keyfile1 bs=1024 count=4
          chmod 0400 /root/keyfile1
          echo -n $phrase | cryptsetup luksAddKey /dev/vda3 /root/keyfile1 -
```

The encrypted partition is formatted to `ext4`, added to `fstab`, and then mounted:

```yaml
          mkdir /encryptedfs
          echo "/dev/mapper/CryptedPart1 /encryptedfs ext4 defaults 1 2" >> /etc/fstab
          echo "CryptedPart1 /dev/vda3 /root/keyfile1 luks" >> /etc/crypttab
          mount -a
```

The initial temporary key is removed, the startup script is removed from `crontab`, and finally, the script deletes itself:

```yaml
          echo -n $phrase | cryptsetup -q luksRemoveKey /dev/vda3 -
          (echo "")| crontab -
          rm -- "$0"
```

The script's output can be found in`/var/mail/root`, and can be viewed using `cat`.

## Deploy the Virtual Server

With the manifest fully configured and the cloud-init directives in place, the Virtual Server is deployed using `kubectl`:

```bash
$ kubectl apply -f centos-7-luks-part.yaml
```

One of the `cloudInit` directives powers off the Virtual Server after it completes initialization so the disk can be expanded for the encrypted partition.

Deployment progress may be monitored by invoking `kubectl --watch`:

```bash
$ kubectl get vs centos7-luks --watch

NAME           STATUS    REASON                                                    STARTED   INTERNAL IP   EXTERNAL IP
centos7-luks   Pending   Waiting for DataVolume to be ready - CSICloneInProgress   False                   216.153.61.34
centos7-luks   Pending   Waiting for VirtualMachineInstance to be ready            False                   216.153.61.34
centos7-luks   Pending   Waiting for VirtualMachine to be ready                    False                   216.153.61.34
centos7-luks   Pending   virt-launcher pod has not yet been scheduled              False                   216.153.61.34
centos7-luks   Pending   Guest VM is not reported as running                       False                   216.153.61.34
centos7-luks   Pending   Guest VM is not reported as running                       False     10.147.97.61   216.153.61.34
centos7-luks   VirtualServerReady   VirtualServerReady                                        True      10.147.97.61   216.153.61.34
centos7-luks   VirtualServerReady   VirtualServerReady                                        True      10.147.97.61   216.153.61.34
centos7-luks   Pending              virt-launcher pod is terminating                          False     10.147.97.61   216.153.61.34
centos7-luks   Pending              virt-launcher pod is terminating                          False     10.147.97.61   216.153.61.34
centos7-luks   VirtualMachineInstanceShutdown   VirtualMachineInstance stopped                            False     10.147.97.61   216.153.61.34
```

Once the Virtual Server is created and spun down, the root disk may be expanded to create the encrypted partition.

In this example, the desired size of the encrypted volume is `5Ti`. Since the root disk size was initially set to `40Gi`, the Virtual Server is expanded to a total size of `5040Gi` using `kubectl patch`:

{% code overflow="wrap" %}
```bash
$ kubectl patch vs centos7-luks -p '{"spec":{"storage":{"root":{"size": "5040Gi"}}}}' --type=merge
```
{% endcode %}

With the root disk expanded, the Virtual Server can be started up again:

```powershell
$ virtctl start centos7-luks

VM centos7-luks was scheduled to start
```

### Confirm the disk state

Confirming that the encrypted partition has been created, formatted, and mounted is achieved by SSHing into the Virtual Server and running `df -h`:

```bash
$ df -h

Filesystem                Size  Used Avail Use% Mounted on

devtmpfs                  7.8G     0  7.8G   0% /dev
tmpfs                     7.9G     0  7.9G   0% /dev/shm
tmpfs                     7.9G   18M  7.9G   1% /run
tmpfs                     7.9G     0  7.9G   0% /sys/fs/cgroup
/dev/vda1                  40G  6.7G   34G  17% /
/dev/mapper/CryptedPart1  4.9T   24K  4.6T   1% /encryptedfs
tmpfs                     1.6G     0  1.6G   0% /run/user/1000
```
