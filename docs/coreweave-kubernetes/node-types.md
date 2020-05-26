# Node Types

A wide range of GPU options are available, allowing you to select the most optimal compute resource for your workload. If GPU resources are not requested, the workload will be executed on a CPU only node.

### GPU Availability

| Vendor | Generation | Model | VRAM | Label |
| :--- | :--- | :--- | :--- | :--- |
| NVIDIA | Volta | Tesla V100 | 16 GB | Tesla\_V100 |
| NVIDIA | Turing | RTX 2080 Ti | 11 GB | GeForce\_RTX\_2080\_Ti |
| NVIDIA | Turing | RTX 2060 Super | 8 GB  | GeForce\_RTX\_2060\_Super |
| NVIDIA | Pascal | GTX 1080 Ti | 11 GB | GeForce\_GTX\_1080\_Ti |
| NVIDIA | Pascal | GTX 1070 Ti | 8 GB | GeForce\_GTX\_1070\_Ti |
| NVIDIA | Pascal | GTX 1070 | 8 GB | GeForce\_GTX\_1070 |
| NVIDIA | Pascal | P104-100 | 8 GB | P104-100 |
| NVIDIA | Pascal | GTX 1060 | 6 GB | GeForce\_GTX\_1060\_6GB |
| NVIDIA | Pascal | P106-100 | 6 GB | P106-100 |

### System Resources

Each GPU includes a certain amount host CPU and RAM, these are included at no additional fee.

| GPU Model | vCPU | RAM | Great For |
| :--- | :--- | :--- | :--- |
| Tesla V100 NVLINK | 4 Xeon Gold | 32 GB | Deep learning, neural network training, HPC |
| Tesla V100 | 3 | 16 GB | AI inference, rendering, batch processing, hashcat |
| RTX 2080 Ti | 3 | 16 GB | Machine learning, neural network training, HPC |
| RTX 2060 Super | 3 | 16 GB | Machine learning, rendering, batch processing |
| GTX 1080 Ti | 1 | 11 GB | Machine learning, rendering, batch processing |
| GTX 1070 Ti | 1 | 8 GB | Video transcoding, rendering, batch processing |
| GTX 1070 | 1 | 8 GB | Video transcoding, rendering, batch processing |
| P104-100 | 0.5 | 8 GB | Batch processing, blockchain compute, hashcat |
| GTX 1060 | 0.5 | 6 GB | Video transcoding, batch processing |
| P106-100 | 0.5 | 6 GB | Batch processing, blockchain compute |

{% hint style="warning" %}
A workload requesting more resources than allowed for the specific GPU class will have it's resources clamped to the maximum allowable amount.  
  
For example, launching a Pod with a request for 2 1070Tis will have it's resource request capped to 2 CPU and 16GB RAM. 
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

A combination of [resource requests ](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)and[ node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity) is used to select the type and amount of compute to your workload. CoreWeave Cloud relies only on these native Kubernetes methods for resource allocation, allowing maximum flexibilty.

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
          - key: gpu.nvidia.com/model
            operator: In
            values:
              - Tesla_V100
```
{% endtab %}

{% tab title="Dual GeForce 1070 \(Ti\)" %}
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
          - key: gpu.nvidia.com/model
            operator: In
            values:
              - GeForce_GTX_1070
              - GeForce_GTX_1070_Ti
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

