# Ethereum Miner

To follow along, please clone the [GitHub repository](https://github.com/coreweave/kubernetes-cloud/tree/master/miner) with the example manifests.

## Introduction

This example leverages a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) to always maintain 3 instances of [Ethminer](https://github.com/ethereum-mining/ethminer). Each instance, in Kubernetes terminology called a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) is allocated 1 GPU. The number of instances can be changed by changing `replicas` in the Deployment spec.

The Kubenetes Control-Plane in the CoreWeave Cloud will ensure that there are 3 instances ([Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)) of Ethminer running at all times. The Control-Plane will reserve GPU, CPU and RAM on CoreWeaves compute nodes. Pods in the same deployment can be scheduled on the same or multiple physical nodes, depending on resource availability. If co-location of Pods is required for some reason, ie. shared ephemeral or block storage, this can be controlled with [affinity rules](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity).

The example Deployment does showcase some node affinity rules. These are purely for demonstration purposes, and the entire affinity section can be removed without breaking the example.

## Getting Started

After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the Ethminer Deployment and service.

1.  Apply the resources. This can be used to both create and update existing manifests

    ```
     $ kubectl apply -f ethminer-deployment.yaml
     deployment.apps/ethminer configured
    ```
2.  List pods to see the Deployment working to instantiate all our requested instances

    ```
     $ kubectl get pods
     NAME                        READY   STATUS              RESTARTS   AGE
     ethminer-6d6f667877-fqmr6   0/1     ContainerCreating   0          2s
     ethminer-6d6f667877-jt9xs   0/1     ContainerCreating   0          2s
     ethminer-6d6f667877-x6hdx   0/1     ContainerCreating   0          2s
    ```
3.  After a little while, all pods should transition to the `Running` state

    ```
    $ kubectl get pods
    NAME                        READY   STATUS    RESTARTS   AGE
    ethminer-6d6f667877-fqmr6   0/1     Running   0          6s
    ethminer-6d6f667877-jt9xs   0/1     Running   0          6s
    ethminer-6d6f667877-x6hdx   0/1     Running   0          6s
    ```
4.  The Deployment will also show that all desired Pods are up and running

    ```
     $ kubectl get deployment
     NAME       READY   UP-TO-DATE   AVAILABLE   AGE
     ethminer   3/3     3            3           73m
    ```
5.  Describing a Pod will help troubleshoot a Pod that does not want to start and gives other relevant information about the Pod

    ```
     $ kubectl describe pod ethminer-6d6f667877-fqmr6
     ....
     Events:
       Type    Reason     Age    From               Message
       ----    ------     ----   ----               -------
       Normal  Scheduled  3m35s  default-scheduler  Successfully assigned tenant-test/ethminer-6d6f667877-fqmr6 to g04c23d
       Normal  Pulling    3m34s  kubelet, g04c23d   Pulling image "fish2/docker-ethminer:latest"
       Normal  Pulled     3m33s  kubelet, g04c23d   Successfully pulled image "fish2/docker-ethminer:latest"
       Normal  Created    3m33s  kubelet, g04c23d   Created container miner
       Normal  Started    3m32s  kubelet, g04c23d   Started container miner
    ```
6.  Finally a shell can be accessed inside the container for interactive testing

    ```
     $ kubectl exec -it ethminer-6d6f667877-kjmsr bash
     root@ethminer-6d6f667877-kjmsr:~# nvidia-smi
     Wed Oct 30 20:07:08 2019
     +-----------------------------------------------------------------------------+
     | NVIDIA-SMI 430.50       Driver Version: 430.50       CUDA Version: 10.1     |
     |-------------------------------+----------------------+----------------------+
     | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
     | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
     |===============================+======================+======================|
     |   0  NVIDIA Graphics...  Off  | 00000000:01:00.0 Off |                  N/A |
     | 45%   63C    P2   132W / 180W |   3549MiB /  8119MiB |    100%      Default |
     +-------------------------------+----------------------+----------------------+

     +-----------------------------------------------------------------------------+
     | Processes:                                                       GPU Memory |
     |  GPU       PID   Type   Process name                             Usage      |
     |=============================================================================|
     +-----------------------------------------------------------------------------+
     root@ethminer-6d6f667877-kjmsr:~#
    ```
