---
description: An example detailing a CentOS 7 Virtual Server deployed with LUKS encryption
---

# CentOS 7 Virtual Server with LUKS Encryption

## Deploying the encrypted root disk partition

The following example demonstrates how to deploy a Virtual Server running CentOS 7 with an encrypted partition on the root disk. This process encompasses deploying a Virtual Server with [cloud-init directives](centos-7-virtual-server-with-luks-encryption.md#using-cloud-init) used to encrypt unallocated space on the root disk.

{% hint style="info" %}
**Note**

Using a separate partition as opposed to a separate block volume provides the advantage of being able to create additional Virtual Servers with the encrypted partition cloned from the same disk.
{% endhint %}

### Configuring the Virtual Server manifest

The manifest below exemplifies how to deploy a LUKS-encrypted CentOS 7 Virtual Server.

<details>

<summary><strong>Click to expand - centos-7-luks-partition.yml</strong></summary>

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
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
  users:
  - sshpublickey: ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
    username:
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
          rm /etc/cloud/cloud-init.disabled
   
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
  
```

</details>

Before deploying this Virtual Server manifest, a few properties need to be changed:

#### `spec.storage.root.size`

It is important to specify the desired size of the **unencrypted** portion of the root disk, where the operating system resides, at creation time. Expanding the operating system partition afterwards will require manual re-partitioning.

The default value in this example is:

`size: 40Gi`

#### `spec.storage.root.source.pvc.name`

It is best practice to always use [the latest available root disk image](../coreweave-system-images/#listing-all-latest-images-available-for-use). The latest CentOS 7 image with NVIDIA drivers can be found by invoking the command:

```bash
$ kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=CentOS_7,images.coreweave.cloud/region=lga1 -o=custom-columns="PVC:metadata.name,NAME:metadata.labels['images\.coreweave\.cloud\/name'],FEATURES:metadata.labels['images\.coreweave\.cloud\/features'],SIZE:status.capacity.storage,STORAGECLASS:.spec.storageClassName" --sort-by='.metadata.name'
```

The value in this example is:

`name: centos7-nvidia-510-85-02-docker-master-20220831-lga1`

#### `spec.users[]`

This example uses `sshpublickey` only, which is the best option for security to pair with an encrypted disk.

In the `sshpublickey` field, use [your personal public key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), along with a desired username configured in the `username` field.

In this example, there is no default `username` provided.

The default public key is an invalid, truncated key:

&#x20;`- sshpublickey: ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname.`

### Deploying the Virtual Server

With the manifest properly configured, it can be deployed using `kubectl`:

```bash
$ kubectl apply -f centos-7-luks-part.yaml
```

The `cloudInit` directive given will power off the Virtual Server initialization is completed so that the disk can be expanded for the encrypted partition.

]We can monitor its progress by invoking `kubectl --watch`:

```powershell
PS C:\> kubectl apply -f centos7-luks.yaml

virtualserver.virtualservers.coreweave.com/centos7-luks created

PS C:\> kubectl get vs centos7-luks --watch

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

Once our Virtual Server has been created and spun down, we can expand the root disk to create our encrypted partition.

For this example, we want a `5Ti` encrypted volume. Since we started out with a root disk size of `40Gi`, we'll expand our Virtual Server to `5040Gi`:

```bash
$ kubectl patch vs centos7-luks -p '{"spec":{"storage":{"root":{"size": "5040Gi"}}}}' --type=merge
```

With our root disk now expanded, we can restart the Virtual Server:

```powershell
PS C:\> kubectl patch vs centos7-luks -p '{"spec":{"storage":{"root":{"size": "5000Gi"}}}}'  --type=merge

virtualserver.virtualservers.coreweave.com/centos7-luks patched

PS C:\> virtctl start centos7-luks

VM centos7-luks was scheduled to start
```

Via SSH, we can confirm that our encrypted partition has been created, formatted, and mounted:

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



## How cloud-init is used in these steps

Preparing the Virtual Server for an encrypted partition requires some pre-requisite steps, which are handled along with the encryption configuration by [cloud-init](../coreweave-system-images/linux-images.md#cloud-init).

The following breaks down how cloud-init is used to configure an encrypted partition in this example.

### GPT Configuration

Virtual Server images by default are configured with an MBR partition table, which does not support sizes above `2Ti`. Because of this, the disk needs to be converted to a [GUID Partition Table (GPT)](https://en.wikipedia.org/wiki/GUID\_Partition\_Table). This also requires re-partitioning, as GRUB must reside on a BIOS boot partition.

This is accomplished with a few commands in the `runcmd` directive:

```yaml
- [bash, -c, sgdisk -n 2:34:2047 -t 2:ef02 /dev/vda -g ]
- [bash, -c, partprobe /dev/vda ]
- [bash, -c, grub2-install /dev/vda ]
```

### Startup script bootstrapping

By default, `cloudInit` [will automatically expand the root disk partition to use all available unallocated space](../coreweave-system-images/linux-images.md#cloud-init-modules).

Because of this, the space allocated to the Virtual Server at creation time will automatically be used for the operating system partition. To prevent this from happening on subsequent restarts after we expand the disk for the encrypted partition, we need to temporarily disable `cloudInit`.&#x20;

Since the Virtual Server needs to be powered off to expand its disk, we need to inject a script via `write_files` and instruct it to run at next start up via `runcmd`:

```yaml
- [bash, -c, (echo "@reboot /encrypt_init.sh")| crontab - ]
- [bash, -c, touch /etc/cloud/cloud-init.disabled ]
- [bash, -c, shutdown -h +1 ]
```

### Configuring the startup script

After expanding the root disk and starting the Virtual Server back up, `encrypt_init.sh` , injected via `write_files`, completes the configuration.

Cloud-init is re-enabled for subsequent reboots, after disabling the `growpart` and `resizefs` modules:

```bash
sed -i 's/growpart,\ always/growpart,\ once-per-instance/g' /etc/cloud/cloud.cfg
sed -i 's/resizefs,\ always/resizefs,\ once-per-instance/g' /etc/cloud/cloud.cfg
rm /etc/cloud/cloud-init.disabled
```

The GPT header is moved to the expanded end of disk, and a new partition is created with the new unallocated space:

```bash
sgdisk -e /dev/vda
partprobe /dev/vda
sgdisk -n 3::0 /dev/vda
partprobe /dev/vda
```

The new partition is initialized with LUKS, using a temporary key:

```bash
phrase=$(openssl rand -base64 32)
echo -n $phrase | cryptsetup -q luksFormat /dev/vda3 -
echo -n $phrase | cryptsetup -q luksOpen /dev/vda3 CryptedPart1 -
```

A key file is generated and secured, so the partition can be auto-mounted at boot:

```bash
dd if=/dev/urandom of=/root/keyfile1 bs=1024 count=4
chmod 0400 /root/keyfile1
echo -n $phrase | cryptsetup luksAddKey /dev/vda3 /root/keyfile1 -
```

The encrypted partition is formatted to `ext4`, added to `fstab`, then mounted:

```bash
 mkdir /encryptedfs
 echo "/dev/mapper/CryptedPart1 /encryptedfs ext4 defaults 1 2" >> /etc/fstab
 echo "CryptedPart1 /dev/vda3 /root/keyfile1 luks" >> /etc/crypttab
 mount -a
```

The initial temporary key is removed, the startup script is removed from `crontab`, and the script deletes itself:

```bash
echo -n $phrase | cryptsetup -q luksRemoveKey /dev/vda3 -
(echo "")| crontab -
rm -- "$0"
```

{% hint style="info" %}
**Note**

The script output can be found in`/var/mail/root` and can be viewed using `cat`.
{% endhint %}
