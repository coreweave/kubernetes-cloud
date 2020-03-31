# CoreWeave Kubernetes Cloud
## Introduction
The Kubernetes environment enables a flexible and reliable method of deploying workloads and services on CoreWeave's Accelerated Compute Cloud.

## Deployment examples
Please see the folders in this repository for ready to deploy Kubernetes manifest examples.

## Node Labels
Selecting the right hardware for your workload is important. All compute nodes are tagged with a set of labels specifying the hardware type that is available inside. [Affinity Rules](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) should be leveraged on workloads to ensure that the desired type of hardware (ie. GPU model) gets assigned to the Pod. The following labels are currently available.

| Label                                    | Possible Values                | Description                                                                                                                                                                       |
|------------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cpu.coreweave.cloud/family                | i9, i7, i5, celeron, xeon, epyc | The CPU family of the CPU in the node                                                                                                                                             |
| ethernet.coreweave.cloud/speed            | 1G, 10G                        | The uplink speed from the node to the backbone                                                                                                                                    |
| gpu.nvidia.com/count                     | 4-8                            | Number of GPUs provisioned in the node. Using this selector is not recommended as the GPU resource requests are the correct method of selecting GPU count requirement             |
| gpu.nvidia.com/model                     | GeForce_GTX_1070_Ti (see list) | GPU model provisioned in the node                                                                                                                                                 |
| gpu.nvidia.com/vram                      | 6, 8, 11, 16                   | GPU VRAM in Gigabytes on the GPUs provisioned in the node                                                                                                                         |
| gpu.nvidia.com/nvlink                    | true, false                    | Denotes if GPUs are interconnected with NVLink                                                                                                                                    |
| pci.coreweave.cloud/version               | 1, 2, 3, 4                     | PCI Express Version for GPU interfaces                                                                                                                                            |
| pci.coreweave.cloud/speed                 | 2.5, 5, 8, 16                  | PCI Express Link Speed for GPU interfaces in GT/s                                                                                                                                 |
| pci.coreweave.cloud/lanes                 | 1, 4, 16                       | PCI Express Lanes (Bus width) for GPU interfaces                                                                                                                                  |
| topology.kubernetes.io/region            | ORD1, EWR1, EWR2, BUF1         | The region the node is placed in. Clusters will not span multiple regions and support for accessing a node in another region than your primary region is currently not supported  |

## GPU Availability

| Vendor | Generation | Model       | VRAM GB | Label               |
|--------|------------|-------------|---------|---------------------|
| NVIDIA | Pascal     | P106-100    | 6       | P106-100            |
| NVIDIA | Pascal     | 1060        | 6       | GeForce_GTX_1060_6GB|
| NVIDIA | Pascal     | P104-100    | 8       | P104-100            |
| NVIDIA | Pascal     | 1070        | 8       | GeForce_GTX_1070    |
| NVIDIA | Pascal     | 1070 Ti     | 8       | GeForce_GTX_1070_Ti |
| NVIDIA | Pascal     | 1080 Ti     | 11      | GeForce_GTX_1080_Ti |
| NVIDIA | Volta      | Titan V 6Gb | 6       | Titan_V_6           |
| NVIDIA | Volta      | V100        | 16      | Tesla_V100          |

## GPU Availability

| Vendor | Generation | Model       | VRAM GB | Label               |
|--------|------------|-------------|---------|---------------------|
| NVIDIA | Pascal     | P106-100    | 6       | P106-100            |
| NVIDIA | Pascal     | 1060        | 6       | GeForce_GTX_1060_6GB|
| NVIDIA | Pascal     | P104-100    | 8       | P104-100            |
| NVIDIA | Pascal     | 1070        | 8       | GeForce_GTX_1070    |
| NVIDIA | Pascal     | 1070 Ti     | 8       | GeForce_GTX_1070_Ti |
| NVIDIA | Pascal     | 1080 Ti     | 11      | GeForce_GTX_1080_Ti |
| NVIDIA | Volta      | Titan V 6Gb | 6       | Titan_V_6           |
| NVIDIA | Volta      | V100        | 16      | Tesla_V100          |

## Getting Started
### Install Kubernetes Command Line Tools

Cut-and-paste instructions are below. For more detail please reference the [official documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

#### Mac OS 
```shell
brew install kubectl
```

#### Linux
```shell
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.16.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

```

### Set Up Access
You will have received a pre-populated `kube-config` file from CoreWeave as part of your onboarding package. The snippet below assumes that you have no other Kubernetes credentials stored on your system, if you do you will need to open both files and copy the `cluster`, `context` and `user` from the supplied `kube-config` file into your existing `~/.kube/config` file.

Replace `~/Downloads` with the path to the `kube-config` supplied by CoreWeave.
```shell
mkdir -p ~/.kube/
mv ~/Downloads/kube-config ~/.kube/config
```

### Verify Access
Since your new account will not have any resources, listing the secrets is a good start to make sure proper communication with the cluster.
```shell
$ kubectl get secret                                                                                                                                                                                                                            git:(master|…
NAME                           TYPE                                  DATA   AGE
default-token-frqgm            kubernetes.io/service-account-token   3      5d3h
```

Once access is verified you can deploy the examples found in this repository.
