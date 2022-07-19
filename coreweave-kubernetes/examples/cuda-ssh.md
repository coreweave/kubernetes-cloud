---
description: SSH server with root disk persistence useful for development and testing
---

# SSH Server with CUDA

To follow along, please clone the [GitHub repository](https://github.com/coreweave/kubernetes-cloud/tree/master/cuda-ssh) with the example manifests.

### Introduction

This example deploys a Kubernetes Deployment with a Linux container including the CUDA Runtime and development tools, including CUDNN as well as running an SSH server. The Deployment allocates 6 GPUs. The Pod includes an `initContainer` that copies the entire root system to a persistent volume on boot, and then mounts all directories on subsequent boots. This gives a VM-like container where manually installed applications will survive a restart.

The Kubenetes Control-Plane in the CoreWeave Cloud will ensure that the Deployment is continuously running. The Control-Plane will reserve GPU, CPU and RAM on CoreWeaves compute nodes. The example Deployment does showcase some node affinity rules. These are purely for demonstration purposes, and the entire affinity section can be removed without breaking the example.

{% content-ref url="../node-types.md" %}
[node-types.md](../node-types.md)
{% endcontent-ref %}

### Service

A [Service](https://kubernetes.io/docs/concepts/services-networking/service/) is included to show how to publish a Pod to the public Internet. The Service publishes the SSH server to the Internet.

{% content-ref url="../../docs/coreweave-kubernetes/networking/exposing-applications.md" %}
[exposing-applications.md](../../docs/coreweave-kubernetes/networking/exposing-applications.md)
{% endcontent-ref %}

## Persistent Storage

A [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) is allocated to the Pods root directories. The allocation is done via a [Persistent Volume Claim](https://github.com/atlantic-crypto/kubernetes-cloud-examples/blob/master/cuda-ssh/sshd-pvc.yaml) requesting a 200GB storage size and SSD backing. This volule claim is then mounted to the the different root directories in the Deployment definition. A separate, HDD backed 500GB Volume Claim is mounted under `/mnt/data` for data storage. Utilizing a persistent volume ensures that files persist even if the node currently running the Pod fails.

{% content-ref url="../storage.md" %}
[storage.md](../storage.md)
{% endcontent-ref %}

### Getting Started

Clone the repository. After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the components.

1.  Apply the resources. This can be used to both create and update existing manifests

    ```
     $ kubectl apply -f sshd-root-pvc.yaml
     persistentvolumeclaim/sshd-root-pv-claim configured
     $ kubectl apply -f sshd-data-pvc.yaml
     persistentvolumeclaim/sshd-data-pv-claim configured
     $ kubectl apply -f sshd-service.yaml
     service/sshd configured
     $ kubectl apply -f sshd-deployment.yaml
     deployment.apps/sshd configured
    ```
2.  List pods to see the Deployment working to instantiate all our requested instances

    ```
     $ kubectl get pods
     NAME                        READY   STATUS              RESTARTS   AGE
     sshd-7b5f48f555-5h5g6       0/1     ContainerCreating   0          2s
    ```
3.  After a little while, all pods should transition to the `Running` state

    ```
    $ kubectl get pods
    NAME                        READY   STATUS    RESTARTS   AGE
    sshd-7b5f48f555-5h5g6       0/1     Running   0          6s
    ```

Show the log for the init container to grab the auto-generated root password

```bash
$ kubectl logs -f sshd-7b5f48f555-5h5g6 init
Root password is: BdxbmsVsiONQY Initialization complete
```

To get the public IP assigned to the service, simply list all services

```
$ kubetl get service                                                                                                                                                                                                                               git:(master↓3|…
NAME       TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
sshd       LoadBalancer   10.134.100.93    64.79.105.198   22:30877/TCP     63m
```

The external IP is allocated for the life of the service, and will not change unless the service is deleted. You can now SSH to the SSH server running inside the Pod from the Internet.

```
$ ssh root@64.79.105.198
root@64.79.105.198's password:
root@sshd-demo:~# ls
lost+found
root@sshd-demo:~# nvidia-smi
Wed Oct 30 21:02:14 2019
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.50       Driver Version: 430.50       CUDA Version: 10.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA Graphics...  Off  | 00000000:01:00.0 Off |                  N/A |
|  0%   28C    P8     5W / 180W |     15MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  NVIDIA Graphics...  Off  | 00000000:02:00.0 Off |                  N/A |
|  0%   30C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   2  NVIDIA Graphics...  Off  | 00000000:03:00.0 Off |                  N/A |
|  0%   33C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   3  NVIDIA Graphics...  Off  | 00000000:04:00.0 Off |                  N/A |
|  0%   34C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   4  NVIDIA Graphics...  Off  | 00000000:08:00.0 Off |                  N/A |
|  0%   28C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   5  NVIDIA Graphics...  Off  | 00000000:09:00.0 Off |                  N/A |
|  0%   31C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
root@sshd-demo:~#
```

{% hint style="info" %}
The SSH Pod can be used as a simple Linux machine. You can install applications and libraries that will be persisted on restart. You will however not be able to do the following

1. Run Docker images. Docker images need to be run as their own Deployments, Pods or Jobs. If you need to run Docker images for development from inside an SSH container, please [contact support](mailto:support@coreweave.com).
2. Run systemd services. There is no systemd running in the container.
{% endhint %}
