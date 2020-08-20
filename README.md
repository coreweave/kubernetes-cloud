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
| gpu.nvidia.com/class                     | Tesla_V100  (see list) | GPU model provisioned in the node                                                                                                                                                 |
| gpu.nvidia.com/vram                      | 8, 16                   | GPU VRAM in Gigabytes on the GPUs provisioned in the node                                                                                                                         |
| gpu.nvidia.com/nvlink                    | true, false                    | Denotes if GPUs are interconnected with NVLink                                                                                                                                    |
| pci.coreweave.cloud/version               | 1, 2, 3, 4                     | PCI Express Version for GPU interfaces                                                                                                                                            |
| pci.coreweave.cloud/speed                 | 2.5, 5, 8, 16                  | PCI Express Link Speed for GPU interfaces in GT/s                                                                                                                                 |
| pci.coreweave.cloud/lanes                 | 1, 4, 16                       | PCI Express Lanes (Bus width) for GPU interfaces                                                                                                                                  |
| topology.kubernetes.io/region            | ORD1, EWR1, EWR2, BUF1         | The region the node is placed in  |

## GPU Availability

| Vendor | Class | Generation | CUDA Cores | VRAM | Label |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NVIDIA | Tesla V100 NVLINK | Volta | 5,120 | 16 GB | Tesla\_V100\_NVLINK |
| NVIDIA | Tesla V100 | Volta | 5,120 | 16GB | Tesla\_V100 |
| NVIDIA | Multi Purpose Turing | Turing | 2,000+ | 8+ GB  | NV\_Turing |
| NVIDIA | Tesla P100 | Pascal | 3,584 | 16 GB | Tesla\_P100\_NVLINK |
| NVIDIA | Multi Purpose Pascal | Pascal | 2,000+ | 8 GB | NV\_Pascal |

## System Resources

Each GPU includes a certain amount of host CPU and RAM, these are included at no additional fee.

| Class | vCPU | RAM | Great For |
| :--- | :--- | :--- | :--- |
| Tesla V100 NVLINK | 4 Xeon Gold | 32 GB | Deep learning, neural network training, HPC |
| Tesla V100 | 3 | 16 GB | AI inference, rendering, batch processing, hashcat |
| Mutli Purpose Turing | 3 | 16 GB | Machine learning, rendering, batch processing |
| Tesla P100 | 6 | 32 GB | Entry level HPC, rendering, batch processing |
| Multi Purpose Pascal | 1 | 8 GB | Video transcoding, rendering, batch processing |

A workload requesting more resources than allowed for the specific GPU class will have its resources capped to the maximum allowable amount.  
  
For example, launching a Pod with a request for Mutli Purpose Pascal GPUs will have its resource request capped to 2 CPU and 16GB RAM. 

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
