## CUDA Development Toolkit with SSH Server
### Introduction
This example deploys a simple Kubernetes [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) with a Linux container including the CUDA Runtime and development tools as well as running an SSH server. The Pod is allocate 6 GPUs.

The Kubenetes Control-Plane in the Atlantic Cloud will ensure that the Pod is continuously running. The Control-Plane will reserve GPU, CPU and RAM on Atlantics compute nodes.
The example Pod does showcase some node affinity rules. These are purely for demonstration purposes, and the entire affinity section can be removed without breaking the example.

### Service
A [Service](https://kubernetes.io/docs/concepts/services-networking/service/) is included to show how to publish a Pod to the public Internet. The Service publishes the SSH server to the Internet.

## Persistent Storage
A [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) is allocated to the Pods `/root` directory. The allocation is done via a [Persistent Volume Claim](https://github.com/atlantic-crypto/kubernetes-cloud-examples/blob/master/sshd/sshd-pvc.yaml) requesting the storage size and backing storage type (SSD, HDD). This volule claim is then mounted to the `/root` directory in the Pod definition. Utilizing a persistent volume ensures that files persist even if the node currently running the Pod fails.

### Getting Started

Clone the repository and modify the SSH password in `sshd-pod.yaml`. After installing `kubectl` and adding your Atlantic Cloud access credentials, the following steps will deploy the components.

1. Apply the resources. This can be used to both create and update existing manifests
   ```shell
    $ kubectl apply -f sshd-pvc.yaml
    persistentvolumeclaim/sshd-pv-claim configured
    $ kubectl apply -f sshd-service.yaml
    service/sshd configured
    $ kubectl apply -f sshd-pod.yaml
    pod/sshd-demo configured
   ````

2. List pods to see the Deployment working to instantiate all our requested instances
   ```shell
    $ kubectl get pods
    NAME                        READY   STATUS              RESTARTS   AGE
    sshd-demo                   0/1     ContainerCreating   0          2s
    ```
    
3. After a little while, all pods should transition to the `Running` state
   ```shell
   $ kubectl get pods
   NAME                        READY   STATUS    RESTARTS   AGE
   sshd-demo                   0/1     Running   0          6s
   ```
   
To get the public IP assigned to the service, simply list all services

```shell
$ kubetl get service                                                                                                                                                                                                                               git:(master↓3|…
NAME       TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
sshd       LoadBalancer   10.134.100.93    64.79.105.198   22:30877/TCP     63m
```

The external IP is allocated for the life of the service, and will not change unless the service is deleted. You can now SSH to the SSH server running inside the Pod from the Internet.

```shell
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
|   0  GeForce GTX 107...  Off  | 00000000:01:00.0 Off |                  N/A |
|  0%   28C    P8     5W / 180W |     15MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX 107...  Off  | 00000000:02:00.0 Off |                  N/A |
|  0%   30C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   2  GeForce GTX 107...  Off  | 00000000:03:00.0 Off |                  N/A |
|  0%   33C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   3  GeForce GTX 107...  Off  | 00000000:04:00.0 Off |                  N/A |
|  0%   34C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   4  GeForce GTX 107...  Off  | 00000000:08:00.0 Off |                  N/A |
|  0%   28C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   5  GeForce GTX 107...  Off  | 00000000:09:00.0 Off |                  N/A |
|  0%   31C    P8     5W / 180W |      9MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
root@sshd-demo:~#
```