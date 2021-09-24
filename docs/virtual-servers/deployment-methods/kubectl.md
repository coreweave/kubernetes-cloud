# CLI

Virtual Servers are a Kubernetes Custom Resource available on CoreWeave Cloud, and as such, `kubectl` can be used to create and modify the resource. The Virtual Server manifest used in the following example is available in the [examples](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl) section of the CoreWeave Cloud repository. 

### Understanding the Virtual Server Manifest

The Virtual Server manifest is broken into two parts, `metadata` and `spec`. The `metadata` section, as is the case with most Kubernetes manifests, contains the name of your Virtual Server and the namespace where it will be deployed. The `spec` contains configuration fields that define how the Virtual Server will be created. These fields are as follows:

{% hint style="info" %}
The following fields are within the manifest spec
{% endhint %}

| Field | Type | Description |
| :--- | :--- | :--- |
| region | String | Defines the region where the Virtual Server is deployed |
| os | {} | Defines the Operating System type |
| os.type | String | The Operating System type - Linux/Windows |
| os.enableUEFIBoot | Boolean | Enable the UEFI bootloader |
| resources | {} | Defines the resources and devices allocated to the Virtual Server |
| resources.definition | String | The resource definition - defaults to 'a' |
| resources.cpu | {} | Defines the CPU allocation  |
| resources.cpu.type | String | The type of CPU to allocate |
| resources.cpu.count | Int | The number of CPU cores to allocate |
| resources.gpu | {} | Defines the GPU allocation |
| resources.gpu.type | String | The type of GPU to allocate |
| resources.gpu.count | Int | The number of GPU\(s\) to allocate |
| resources.memory | String | The amount of memory to allocate |
| storage | {} | Defines the root storage and additional storage devices |
| storage.root | {} | Defines the root file system PVC |
| storage.root.size | String | The volume size |
| storage.root.source \[¹\] | {} | The DataVolume source for the root file system   |
| storage.root.storageClassName | String | The storage class name for the root PVC |
| storage.root.volumeMode | String | The volume mode for the root PVC |
| storage.root.accessMode | String | The access mode name for the root PVC  |
| storage.root.ephemeral | Boolean | Set whether the root disk is ephemeral |
| storage.additionalDisks | \[\] | A list of PVC references to be added as disk devices |
| storage.additionalDisks\[ \].name | String | Name of the disk |
| storage.additionalDisks\[ \].spec \[²\] | {} | The VolumeSource for the disk |
| storage.filesystems  | \[\] | A list of PVC references to be mounted |
| storage.filesystems\[ \].name | String | Name of the mount |
| storage.filesystems\[ \].spec \[²\] | {} | The VolumeSource for the file system mount |
| users | \[\] | A list of users to be added by cloud-init \(if supported by the OS\) |
| users\[ \].username | String | Username for the user |
| users\[ \].password | String | Password for the user |
| network | {} | Defines the network configuration |
| network.directAttachLoadBalancerIP | Boolean | [Directly attach a loadbalancer IP to the Virtual Server](../../coreweave-kubernetes/exposing-applications.md#attaching-service-ip-directly-to-pod) |
| network.floatingIPs | \[\] | A list of service references to be added as floating IPs |
| network.floatingIPs\[ \].serviceName | String | Name of the service |
| network.tcp | {} | Defines the TCP network configuration |
| network.tcp.ports | \[\] | List of TCP ports to expose |
| network.udp | {} | Defines the UDP network configuration |
| network.udp.ports | \[\] | List of UDP ports to expose |
| network.public | Boolean | Whether a public IP will be assigned |
| initializeRunning | Boolean | The Virtual Server will be started as soon as it is created and initialized |

{% hint style="info" %}
\[¹\] - See [DataVolumeSource](https://pkg.go.dev/kubevirt.io/containerized-data-importer/pkg/apis/core/v1alpha1#DataVolumeSource) for further information

\[²\] - See [VolumeSource](https://pkg.go.dev/kubevirt.io/client-go/api/v1#VolumeSource) for further information

\[³\] - See [Cloud Init](https://cloudinit.readthedocs.io/en/latest/topics/examples.html%20) for more examples
{% endhint %}

{% hint style="info" %}
Certain fields are mutually exclusive:

* GPU type and CPU type
* TCP ports or UDP ports and directAttachLoadbalancerIP 
{% endhint %}

### Deploying a Virtual Server

We provide a few simple examples [Virtual Server manifests](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl). 

| Example | File | GPU |
| :--- | :--- | :--- |
| Attach block PVC | [virtual-server-block-pvc.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-block-pvc.yaml) | Yes |
| Attach shared PVC | [virtual-server-shared-pvc.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-shared-pvc.yaml) | Yes |
| Directly attaching a Load Balancer IP | [virtual-server-direct-attach-lb.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-direct-attach-lb.yaml) | Yes |
| Windows with CPU compute only | [virtual-server-windows-cpu-only.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-windows-cpu-only.yaml) | No |
| Windows with directly attached Load Balancer IP | [virtual-server-windows-internal-ip-only.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-windows-internal-ip-only.yaml) | No |

All examples can be easily deployed in the same way using `kubectl.` The most comprehensive Virtual server example is [virtual-server-block-pvc.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-block-pvc.yaml).

{% hint style="warning" %}
The username and password field in the example manifests are unset. Before applying the manifest, set a secure username and password.
{% endhint %}

#### Deploying Virtual Server With Block PVC

```text
kubectl apply -f virtual-server-block-pvc.yaml
```

The file [virtual-server-block-pvc.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-block-pvc.yaml) ****contains two manifests. The first part creates a 20Gi block type PVC with attributes `accessModes: ReadWriteOnce` and `storageClassName: block-nvme-ord1`.

{% hint style="info" %}
See the full list of [Storage Classes](https://docs.coreweave.com/coreweave-kubernetes/storage) for further details.
{% endhint %}

{% hint style="info" %}
See [Root Disk Lifecycle Management](https://docs.coreweave.com/virtual-servers/root-disk-lifecycle-management) how to manage the Virtual Machine disks in Kubernetes
{% endhint %}

Once deployed, your Virtual Server will begin the initialization process. The status of your Virtual Server can be examined:

```text
$ kubectl get vs vs-ubuntu2004-block-pvc
NAME                     STATUS               REASON                                           STARTED   INTERNAL IP      EXTERNAL IP
vs-ubuntu2004-block-pvc  Initializing         Waiting for VirtualMachineInstance to be ready   False                      123.123.123.123
```

Once initialization is complete, the status will then transition to VirtualServerReady.

```text
$ kubectl get vs vs-ubuntu2004-block-pvc
NAME                      STATUS               REASON               STARTED   INTERNAL IP     EXTERNAL IP
vs-ubuntu2004-block-pvc   VirtualServerReady   VirtualServerReady   True      10.147.196.24   207.53.234.124
```

You can now access your Virtual Server using the`virtctl`command. 

{% hint style="info" %}
See [Remote Access and Control](https://docs.coreweave.com/virtual-servers/remote-access-and-control) for further details on how to install and use `virtctl`.
{% endhint %}

Virtual Server, built upon [Kubevirt](https://kubevirt.io/), deploys three resources:

* Virtual Machine

```text
$ kubectl get vm vs-ubuntu2004-block-pvc
NAME                      AGE   VOLUME
vs-ubuntu2004-block-pvc   31m   

```

* Virtual Machine Instance

```text
$kubectl get vmi vs-ubuntu2004-block-pvc
NAME                      AGE   PHASE     IP              NODENAME
vs-ubuntu2004-block-pvc   31m   Running   10.147.196.24   g0aa1fd
```

* `virt-launcher` pod which coexists with `vmi` 

```text
$ kubectl get pods | grep virt-launcher
virt-launcher-vs-ubuntu2004-block-pvc-m8mqt      1/1     Running     0          94s
```

Depending on the current state of Virtual Server, the `vmi` will either be running or terminated.

| `virtctl` command | `vs` state | `vmi` state | `pod` state |
| :--- | :--- | :--- | :--- |
| `virtctl stop` &lt;name&gt; | `VirtualServerStopped` | deleted | deleted |
| `virtctl start <name>` or `virtctl restart <name>` | `VirtualServerReady` | running | running |

{% hint style="info" %}
See [Kubevirt Lifecycle](https://kubevirt.io/user-guide/virtual_machines/lifecycle/) for further details
{% endhint %}

In our example, Virtual Server creates two additional resources:

* Block PVC

```text
$ kubectl get pvc vs-ubuntu2004-block-pvc
NAME                      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
vs-ubuntu2004-block-pvc   Bound    pvc-3ec3a05c-dc53-4f29-8f02-ff95de06f750   40Gi       RWO            block-nvme-ord1   26m
```

* Service

```text
$ kubectl get svc vs-ubuntu2004-block-pvc-tcp
NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
vs-ubuntu2004-block-pvc-tcp   LoadBalancer   10.135.203.211   207.53.234.124   22:32849/TCP   43m
```

#### Format and Mount the Block PVC

The block PVC is raw and not mounted. In order to format the disk, first, login into the new system:

```text
$ virtctl console vs-ubuntu2004-block-pvc
Successfully connected to vs-ubuntu2004-block-pvc console. The escape sequence is ^]
vs-ubuntu2004-block-pvc login: myuser
Password: 

Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.8.0-45-generic x86_64)

  System information as of Wed Sep 15 15:08:18 UTC 2021

  System load:  0.1               Processes:                145
  Usage of /:   6.5% of 38.60GB   Users logged in:          0
  Memory usage: 1%                IPv4 address for docker0: 192.168.99.1
  Swap usage:   0%                IPv4 address for enp3s0:  10.147.196.29
Your Hardware Enablement Stack (HWE) is supported until April 2025.

Last login: Wed Sep 15 15:02:21 UTC 2021 on ttyS0
myuser@vs-ubuntu2004-block-pvc:~$ 

```

The new disk is `/dev/vdb`:

```text
myuser@vs-ubuntu2004-block-pvc:~$ sudo fdisk -l
Disk /dev/loop0: 55.48 MiB, 58159104 bytes, 113592 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

...

Disk /dev/vda: 40 GiB, 42949672960 bytes, 83886080 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: F4869E7B-CC51-47AF-A921-6114387E6DE4

Device      Start      End  Sectors  Size Type
/dev/vda1  227328 83886046 83658719 39.9G Linux filesystem
/dev/vda14   2048    10239     8192    4M BIOS boot
/dev/vda15  10240   227327   217088  106M EFI System

Partition table entries are not in disk order.


Disk /dev/vdb: 20 GiB, 21474836480 bytes, 41943040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

Before we can use it, the disk first needs to be formatted:

```text
myuser@vs-ubuntu2004-block-pvc:~$ sudo mkfs.ext4 /dev/vdb
mke2fs 1.45.5 (07-Jan-2020)
Discarding device blocks: done                            
Creating filesystem with 5242880 4k blocks and 1310720 inodes
Filesystem UUID: 26859f53-6e1c-4367-a83d-44d81c3b05f0
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done 
```

and then mounted:

```text
myuser@vs-ubuntu2004-block-pvc:~$ sudo mkdir /mnt/vdb && sudo mount /dev/vdb /mnt/vdb
myuser@vs-ubuntu2004-block-pvc:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            7.9G     0  7.9G   0% /dev
tmpfs           1.6G  1.1M  1.6G   1% /run
/dev/vda1        39G  2.6G   37G   7% /
tmpfs           7.9G     0  7.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           7.9G     0  7.9G   0% /sys/fs/cgroup
/dev/loop0       56M   56M     0 100% /snap/core18/1988
/dev/loop2       71M   71M     0 100% /snap/lxd/19647
/dev/loop1       56M   56M     0 100% /snap/core18/2128
/dev/vda15      105M  7.8M   97M   8% /boot/efi
/dev/loop3       33M   33M     0 100% /snap/snapd/11107
/dev/loop4       33M   33M     0 100% /snap/snapd/12883
tmpfs           1.6G     0  1.6G   0% /run/user/1001
/dev/vdb         20G   45M   19G   1% /mnt/vdb
```



