# Node Types

A wide range of GPU options are available, allowing you to select the most optimal compute resource for your workload. If GPU resources are not requested, the workload will be executed on a CPU only node.

### GPU Availability

| Vendor | Class | Generation | CUDA Cores | VRAM | Label |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NVIDIA | Tesla V100 NVLINK | Volta | 5,120 | 16 GB | Tesla\_V100\_NVLINK |
| NVIDIA | Tesla V100 | Volta | 5,120 | 16 GB | Tesla\_V100 |
| NVIDIA | Multi Purpose Turing | Turing | 2,000+ | 8+ GB  | NV\_Turing |
| NVIDIA | Tesla P100 | Pascal | 3,584 | 16 GB | Tesla\_P100\_NVLINK |
| NVIDIA | Multi Purpose Pascal | Pascal | 2,000+ | 8 GB | NV\_Pascal |

### System Resources

Each GPU includes a certain amount of host CPU and RAM, these are included at no additional fee.

| Class | vCPU | RAM | Great For |
| :--- | :--- | :--- | :--- |
| Tesla V100 NVLINK | 4 Xeon Silver | 32 GB | Deep learning, neural network training, HPC |
| Tesla V100 | 3 | 20 GB | AI inference, rendering, batch processing, hashcat |
| Mutli Purpose Turing | 3 | 16 GB | Machine learning, rendering, batch processing |
| Tesla P100 NVLINK | 4 Xeon Silver | 32 GB | Entry level HPC, rendering, batch processing |
| Multi Purpose Pascal | 1 | 8 GB | Video transcoding, rendering, batch processing |

{% hint style="warning" %}
If a workload requests more peripheral compute resources \(vCPU, RAM\) than offered in a standard instance size, additional costs will incur. 

Please reach out to [cloud.support@coreweave.com](mailto:%20cloud.support@coreweave.com) for additional information on enhanced vCPU/RAM combinations and their costs.
{% endhint %}

### CPU Availability

| CPU Model | RAM per vCPU | Label |
| :--- | :--- | :--- |
| Intel Xeon v1 | 3 GB | xeon |
| AMD Epyc Rome | 4 GB | epyc |

{% hint style="info" %}
Workloads without GPU requests are always scheduled on CPU nodes. If a specific CPU model is not [explicitly selected](node-types.md#requesting-compute-in-kubernetes), the scheduler will automatically schedule workloads requesting few CPU cores on Epyc class CPUs, as these perform exceptionally well on single thread workloads.
{% endhint %}

### Requesting Compute in Kubernetes

A combination of [resource requests ](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)and[ node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity) is used to select the type and amount of compute for your workload. CoreWeave Cloud relies only on these native Kubernetes methods for resource allocation, allowing maximum flexibilty.

{% tabs %}
{% tab title="Single Tesla V100" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 3
        memory: 16Gi
        nvidia.com/gpu: 1
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - Tesla_V100
```
{% endtab %}

{% tab title="4x Tesla V100 NVLINK" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 15
        memory: 128Gi
        nvidia.com/gpu: 4
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - Tesla_V100_NVLINK
```
{% endtab %}

{% tab title="Dual Pascal" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 2
        memory: 16Gi
        nvidia.com/gpu: 2
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - NV_Pascal
```
{% endtab %}

{% tab title="16 Core Xeon CPU" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 16
        memory: 48Gi
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: cpu.coreweave.cloud/family
            operator: In
            values:
              - xeon
```
{% endtab %}

{% tab title="Single Epyc CPU" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 1
        memory: 4Gi
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: cpu.coreweave.cloud/family
            operator: In
            values:
              - epyc
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Kubernetes allows resources to be scheduled with `requests` and `limits.` When only `limits` are specified, the `requests` are set to the same amount as the limit.
{% endhint %}

