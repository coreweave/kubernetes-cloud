# Node Types

A wide range of GPU options are available, allowing you to select the most optimal compute resource for your workload. If GPU resources are not requested, the workload will be executed on a CPU only node.

### GPU Availability

| Vendor | Class | Generation | CUDA Cores | VRAM | Label |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NVIDIA | Tesla A100 NVLINK | Ampere | 6,912 | 40GB | Tesla\_A100\_NVLINK |
| NVIDIA | Tesla V100 NVLINK | Volta | 5,120 | 16 GB | Tesla\_V100\_NVLINK |
| NVIDIA | Tesla V100 | Volta | 5,120 | 16 GB | Tesla\_V100 |
| NVIDIA | RTX 6000 | Turing | 4,608 | 24 GB | Quadro\_RTX\_6000 |
| NVIDIA | RTX 5000 | Turing | 3,072 | 16 GB | Quadro\_RTX\_5000 |
| NVIDIA | RTX 4000 | Turing | 2,304 | 8 GB  | Quadro\_RTX\_4000 |
| NVIDIA | Tesla P100 | Pascal | 3,584 | 16 GB | Tesla\_P100\_NVLINK |
| NVIDIA | Multi Purpose Pascal | Pascal | 2,000+ | 8 GB | NV\_Pascal |

### System Resources

Each GPU includes a certain amount of host CPU and RAM, these are included at no additional fee. Allocating multiple GPUs to a single workload will increase the CPU and RAM allocation proportionally.

| Class | vCPU | RAM | Great For |
| :--- | :--- | :--- | :--- |
| Tesla A100 NVLINK | 30 Epyc | 240 GB | Complex Deep Neural Network training, HPC |
| Tesla V100 NVLINK | 4 Xeon Silver | 32 GB | Deep Neural Network training, HPC |
| Tesla V100 | 3 | 20 GB | AI inference, Rendering, Batch processing, Hashcat |
| RTX 6000 | 8 | 60 GB | Complex DNN Training, Rendering, Batch processing |
| RTX 5000 | 8 | 60 GB | Machine learning, Rendering, Batch processing |
| RTX 4000 | 3 | 16 GB | Machine learning, Rendering, Game streaming |
| Tesla P100 NVLINK | 4 Xeon Silver | 32 GB | Entry level HPC, Rendering, Batch processing |
| Multi Purpose Pascal | 1 | 8 GB | Transcoding, Rendering, Game streaming, Batch |

{% hint style="warning" %}
If a workload requests more peripheral compute resources \(vCPU, RAM\) than offered in a standard instance size, additional costs will incur. 

Additional CPU and RAM is billed in increments of $0.07/hr for 1 vCPU + 8 GB RAM.
{% endhint %}

### CPU Availability

CPU Only nodes are available for tasks such as control-plane services, databases, ingresses and CPU rendering. 

| CPU Model | RAM per vCPU | Max CPU per Workload | Label |
| :--- | :--- | :--- | :--- |
| Intel Xeon v1/v2 | 3 GB | 94 | xeon |
| AMD Epyc Rome | 4 GB | 46 | epyc |

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

