---
description: SSH server with root disk persistence useful for development and testing
---

# SSH Server with CUDA

In this example, a Linux container is deployed as an SSH server on a Pod. The container includes development tools, the CUDA Runtime, and cuDNN.

The Deployment allocates a single Pod with six GPUs. The Pod consists of two containers:

* an `initContainer`, which copies the filesystem of the base image from ephemeral storage into a Persistent Volume on the server's first launch, and
* an SSH server container, which mounts the Persistent Volume in place of ephemeral storage as its complete filesystem. This persists data and newly-installed applications, even if the Pod is rebooted, in the same way a Virtual Machine does.

{% hint style="warning" %}
**Important**

Only the standard root-level directories and their children are persisted, such as `/etc/*`. Newly-created root-level directories, such as `/MyApp`, will still reside in ephemeral storage. The exact list of **persistent** root-level directories is defined [in `sshd-deployment.yaml` in the `volumeMounts` stanza](cuda-ssh.md#click-to-expand-the-volumemounts-stanza-sshd-deployment.yaml).
{% endhint %}

## Prerequisites

This guide presumes that the user has an active CoreWeave account and a corresponding namespace. The guide also presumes that `kubectl` is installed on the host machine. For more information, see [Get Started with CoreWeave](../../docs/coreweave-kubernetes/getting-started.md).

### Example source code

To follow along, clone [the GitHub repository containing the example manifests](https://github.com/coreweave/kubernetes-cloud/tree/master/cuda-ssh).

## Overview

This walkthrough uses several different components, defined in [the example source code](https://github.com/coreweave/kubernetes-cloud/tree/master/cuda-ssh) repository.

### Deployment

[`sshd-deployment.yaml`](../../cuda-ssh/sshd-deployment.yaml)

The `sshd` application Deployment. The example Deployment in this guide also showcases some [node affinity rules](../label-selectors.md). These are purely for demonstration purposes - the entire affinity section may be removed without breaking the example. The Kubernetes control plane in CoreWeave Cloud reserves GPU, CPU and RAM resources on CoreWeaves compute nodes, and ensures that Deployments are continuously running.

### Service

[`sshd-service.yaml`](../../cuda-ssh/sshd-service.yaml)

A [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/) is included to demonstrate how to publish a Pod to the public Internet. The Service publishes the SSH server to the Internet by exposing port `22` of the server to handle incoming SSH connections.

{% hint style="info" %}
**Note**

Only port `22` is exposed on the server by default.
{% endhint %}

### PVCs

[`sshd-root-pvc.yaml`](../../cuda-ssh/sshd-root-pvc.yaml) and [`sshd-data-pvc.yaml`](../../cuda-ssh/sshd-data-pvc.yaml)

There are two [Persistent Volume Claims (PVCs)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) included in this example's source code, `sshd-root-pvc.yaml` and `sshd-data-pvc.yaml`.

`sshd-root-pvc` houses critical runtime details, such as the OS install and installed programs, in high-performance storage, while `sshd-data-pvc` provides a larger, slower, decoupled storage space in order to isolate custom application data.

This decoupling of PVCs allows for SSD performance for critical programs and system files without tying the user to SSD pricing for all data. It also allows the Operating System and any other programs to be wiped, reinstalled, updated, and so forth, without destroying valuable data in the process.

In this example, a PVC is allocated to the Pod's root directories. The allocation is done via a Persistent Volume Claim defined in `sshd-root-pvc.yaml`, and requests `200Gi` of SSD-backed storage.

{% code title="sshd-root-pvc.yaml" %}
```yaml
spec:
  # https://docs.coreweave.com/storage/storage
  storageClassName: block-nvme-ord1
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 200Gi
```
{% endcode %}

The volume claim is then mounted to the different root directories in the Deployment definition under the `volumeMounts` stanza.

{% hint style="info" %}
**Note**

The `volumeMounts` stanza defines the complete list of persistent, root-level directories.
{% endhint %}

<details>

<summary>Click to expand - The <code>volumeMounts</code> stanza (<code>sshd-deployment.yaml</code>)</summary>

```yaml
volumeMounts:
- name: data-storage
  mountPath: /mnt/data
- name: root-storage
  mountPath: /bin
  subPath: bin
- name: root-storage
  mountPath: /boot
  subPath: boot
- name: root-storage
  mountPath: /etc
  subPath: etc
- name: root-storage
  mountPath: /home
  subPath: home
- name: root-storage
  mountPath: /lib
  subPath: lib
- name: root-storage
  mountPath: /lib64
  subPath: lib64
- name: root-storage
  mountPath: /opt
  subPath: opt
- name: root-storage
  mountPath: /root
  subPath: root
- name: root-storage
  mountPath: /sbin
  subPath: sbin
- name: root-storage
  mountPath: /srv
  subPath: srv
- name: root-storage
  mountPath: /usr
  subPath: usr
- name: root-storage
  mountPath: /var
  subPath: var
- name: run-lock
  mountPath: /run/lock
```

</details>

A separate, `500Gi` HDD-backed Volume Claim is defined in `sshd-data-pvc.yaml`:

{% code title="sshd-data-pvc.yaml" %}
```yaml
spec:
  # https://docs.coreweave.com/storage/storage
  storageClassName: block-hdd-ord1
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi
```
{% endcode %}

{% hint style="info" %}
**Note**

It is also possible to define this volume as an [NVME](../../docs/storage/storage/#volume-types-and-tiers) volume.
{% endhint %}

This PVC is later mounted to the Pod defined in the Deployment at the mount path `/mnt/data`, as shown in this excerpt:

{% code title="sshd-deployment.yaml" %}
```yaml
volumeMounts:
- name: data-storage
  mountPath: /mnt/data
```
{% endcode %}

Utilizing Persistent Volumes, as is the case here, decouples storage from the Pod. This decoupling provides a tremendous benefit: ephemeral storage by comparison is very volatile. Even if a Pod restarts on the same node, its associated ephemeral storage is wiped before it finishes restarting. Decoupling storage from the Pod instead protects the data inside of it by ensuring any associated data survives a Pod restart, or even node failure.

{% hint style="info" %}
**Additional Resources**

To learn more about storage, visit [Get Started with Storage](../../docs/storage/storage/).
{% endhint %}

## Apply all resources

To get started with this demo, first use `kubectl` to deploy all resources to your namespace. In the following steps, `kubectl apply -f` is used to target each resource's manifest in order to deploy it into the namespace.

```bash
# Create the persistent storage volumes
kubectl apply -f sshd-root-pvc.yaml -f sshd-data-pvc.yaml

# Create the SSH service along with its public IP
kubectl apply -f sshd-service.yaml

# Launch the SSH server
kubectl apply -f sshd-deployment.yaml
```

Next, `kubectl rollout status` is used to watch the progress of the SSH server's deployment.

```bash
$ kubectl rollout status deployment/sshd
```

### Upload an SSH public key

Once the SSH Pod is running and the Service is up, a public SSH key must be uploaded onto the server for authentication. This can be done using the following `kubectl exec` command:

{% code overflow="wrap" %}
```bash
$ kubectl exec -i deployment/sshd -c sshd -- /bin/tee --append /root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
```
{% endcode %}

To use this command, a public SSH key must be present at `~/.ssh/id_rsa.pub`. Alternatively, the path to the key may be adjusted to provide a key that is located elsewhere. If there is not an SSH public key available on the system, use `ssh-keygen` to create one at this default path.

### Get the Service's public IP address

The following filtered `kubectl get service` command may be used to acquire the public IP address of the Service. This address is used as the target address for SSH.

{% code overflow="wrap" %}
```bash
$ kubectl get service/sshd -o 'jsonpath=service/sshd public IP: {.status.loadBalancer.ingress[0].ip}{"\n"}'
```
{% endcode %}

Or, to view the IP address alongside the rest of the Service's information, use `kubectl get service/sshd`.

```bash
$ kubectl get service/sshd

NAME   TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)   AGE
sshd   LoadBalancer   10.134.100.9   64.79.105.198   22/TCP    28m
```

{% hint style="info" %}
**Note**

The public IP (`EXTERNAL-IP`) is allocated for the life of the Service. This address will not change unless the Service is deleted.
{% endhint %}

### Acquire the host key fingerprint

When connecting over SSH, it is important to verify that the host key presented while connecting matches the one on the deployed server, or the security of the connection will be compromised.\


To display the deployed server's host key fingerprints for manual comparison, run the following `kubectl exec` command:

{% code overflow="wrap" %}
```bash
$ kubectl exec deployment/sshd -c sshd -- find /etc/ssh -type f -name 'ssh_host_*_key.pub' -exec ssh-keygen -lf '{}' ';'
```
{% endcode %}

Alternatively, to add the correct host key directly to the current user's SSH `known_hosts` file and have SSH validate it automatically, run the following command:\


{% code overflow="wrap" %}
```bash
$ kubectl get service/sshd -o 'jsonpath={.status.loadBalancer.ingress[0].ip}' | kubectl exec -i deployment/sshd -c sshd -- sh -c 'export IP=$(cat -) && ssh-keyscan localhost | sed -e "s/localhost/${IP}/g"' >> ~/.ssh/known_hosts
```
{% endcode %}

### Connect to the Service

At last, connect to the Service using `ssh`:

```bash
$ ssh root@<SERVICE'S PUBLIC IP>
```

The following demonstrates a successful SSH connection to a demo server, and the output of the `ls` and `nvidia-smi` commands.

As is also demonstrated here, PyTorch is pre-installed with the container base image, and can be used immediately.

```bash
$ ssh root@64.79.105.198

root@sshd-demo:~# ls /mnt/data
lost+found

root@sshd-demo:~# python -c 'import torch; print(torch.cuda.device_count())'
6

root@sshd-demo:~# nvidia-smi
Mon Jun 12 21:02:14 2023
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.105.17   Driver Version: 525.105.17   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA RTX A5000    On   | 00000000:01:00.0 Off |                  Off |
| 42%   31C    P8    15W / 230W |     66MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  NVIDIA RTX A5000    On   | 00000000:25:00.0 Off |                  Off |
| 44%   32C    P8    15W / 230W |     66MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   2  NVIDIA RTX A5000    On   | 00000000:41:00.0 Off |                  Off |
| 41%   30C    P8    18W / 230W |     66MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   3  NVIDIA RTX A5000    On   | 00000000:61:00.0 Off |                  Off |
| 40%   29C    P8    18W / 230W |     89MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   4  NVIDIA RTX A5000    On   | 00000000:81:00.0 Off |                  Off |
| 40%   30C    P8    17W / 230W |     66MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   5  NVIDIA RTX A5000    On   | 00000000:A1:00.0 Off |                  Off |
| 40%   29C    P8    19W / 230W |     66MiB / 24564MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
```

## Limitations

This setup may be used as a simple Linux machine. Applications and libraries may be installed that will persist on restart. Please note that the following is not possible in this setup:

* **Running Docker images.**\
  Docker images need to be run as their own Deployments, Pods or Jobs. If you need to run Docker images for development from inside an SSH container, please [contact support](mailto:support@coreweave.com).
* **Run `systemd` services.**\
  There is no `systemd` running in the container.

For a full Virtual Machine experience, see [Get Started with Virtual Servers](../../virtual-servers/getting-started.md).
