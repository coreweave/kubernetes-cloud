This directory contains several examples of the manifests for `VirtualServer` service.

To run any of the examples issue: `kubectl apply -f <manifest_file_name.yaml>`

- [virtual-server-direct-attach-lb.yaml](virtual-server-direct-attach-lb.yaml) shows how to attach directly the virtual machine to the load balancer.
  
  **pros:**
  - can handle more IP trafic to VM - the trafic is routed directly to VM.
  - IP of the VM matches the assigned ingress IP

  **cons:**
  - cannot handle replicas, the same cannot get all benefits from load balancer

- [virtual-server-shared-pvc.yaml](virtual-server-shared-pvc.yaml) attaches shared `PVC` to the virtual machine instance. The `PVC` formated already and mounted as `/mnt/shared-pvc`.

- [virtual-server-windows.yaml](virtual-server-windows.yaml) creates Windows10 virtual machine instance. In order to get the external IP and use remote desktop via `RDP` protocol, issue the following commnad: 
  ```
  kubectl get svc vs-windows10-tcp -o jsonpath="{.status.loadBalancer.ingress[*].ip}"
  ```

- [virtual-server-block-pvc.yaml](virtual-server-block-pvc.yaml) attaches block `PVC` to the virtual machine instance. The new disk is raw and need to be formatted.

  ```
  myuser@vs-ubuntu2004-block-pvc:~$ sudo fdisk /dev/vdb

  Welcome to fdisk (util-linux 2.34).
  Changes will remain in memory only, until you decide to write them.
  Be careful before using the write command.

  Device does not contain a recognized partition table.
  Created a new DOS disklabel with disk identifier 0xfffa9647.

  Command (m for help): n
  Partition type
    p   primary (0 primary, 0 extended, 4 free)
    e   extended (container for logical partitions)
  Select (default p): p
  Partition number (1-4, default 1): 1
  First sector (2048-41943039, default 2048): 2048
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-41943039, default 41943039): 41943039

  Created a new partition 1 of type 'Linux' and of size 20 GiB.

  Command (m for help): q

  myuser@vs-ubuntu2004-block-pvc:~$ sudo mkfs.ext4 /dev/vdb
  mke2fs 1.45.5 (07-Jan-2020)
  Discarding device blocks: done                            
  Creating filesystem with 5242880 4k blocks and 1310720 inodes
  Filesystem UUID: 0a05b295-9518-41f3-8b64-18d5902d419e
  Superblock backups stored on blocks: 
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
    4096000

  Allocating group tables: done                            
  Writing inode tables: done                            
  Creating journal (32768 blocks): done
  Writing superblocks and filesystem accounting information: done 

  ```

  Now, the disk is ready:
  ```
  myuser@vs-ubuntu2004-block-pvc:~$ sudo mkdir /mnt/vdb && sudo mount /dev/vdb /mnt/vdb
  myuser@vs-ubuntu2004-block-pvc:~$ df -h
  Filesystem      Size  Used Avail Use% Mounted on
  udev            7.9G     0  7.9G   0% /dev
  tmpfs           1.6G  1.1M  1.6G   1% /run
  /dev/vda1        39G  2.6G   37G   7% /
  tmpfs           7.9G     0  7.9G   0% /dev/shm
  tmpfs           5.0M     0  5.0M   0% /run/lock
  tmpfs           7.9G     0  7.9G   0% /sys/fs/cgroup
  /dev/vda15      105M  7.8M   97M   8% /boot/efi
  /dev/loop0       71M   71M     0 100% /snap/lxd/19647
  /dev/loop1       56M   56M     0 100% /snap/core18/1988
  /dev/loop2       33M   33M     0 100% /snap/snapd/11107
  /dev/loop3       33M   33M     0 100% /snap/snapd/12704
  /dev/loop4       56M   56M     0 100% /snap/core18/2128
  /dev/loop5       71M   71M     0 100% /snap/lxd/21029
  tmpfs           1.6G     0  1.6G   0% /run/user/1001
  /dev/vdb         20G   45M   19G   1% /mnt/vdb
  ```

Additional examples and documentation:

- [Kubernetes documentation](https://docs.coreweave.com/coreweave-kubernetes/getting-started)
- [VirtualServer documentation](https://docs.coreweave.com/virtual-servers/getting-started)
- [Advanced Label selectors](https://docs.coreweave.com/coreweave-kubernetes/label-selectors)
- [CPU and GPU Availability](https://docs.coreweave.com/coreweave-kubernetes/node-types)
- [Storage](https://docs.coreweave.com/coreweave-kubernetes/storage)

