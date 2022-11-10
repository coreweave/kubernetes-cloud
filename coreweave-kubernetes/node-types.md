# Node Types

We have configured a "Standard Instance" that we have found to be useful for most workloads for each GPU type offered on CoreWeave Cloud. These instances are a starting point, but can be configured entirely to suit your use case or compute needs.

You can view Standard Instance configurations on the [pricing page](https://www.coreweave.com/pricing).

For more information about the à la carte pricing of compute components on CoreWeave Cloud, click below.

{% content-ref url="../resources/resource-based-pricing.md" %}
[resource-based-pricing.md](../resources/resource-based-pricing.md)
{% endcontent-ref %}

## Component Availability

When custom configuring your instances on CoreWeave Cloud, the following table outlines the physical limitation of how many GPUs are available per instance.

<table><thead><tr><th>Class</th><th>Generation</th><th>VRAM</th><th>Max per Instance</th><th>Label</th><th data-hidden>Vendor</th><th data-hidden>CUDA Cores</th></tr></thead><tbody><tr><td>A100 NVLINK</td><td>Ampere</td><td>80 GB</td><td>8</td><td>A100_NVLINK<em>_</em>80GB</td><td></td><td></td></tr><tr><td>A100 NVLINK</td><td>Ampere</td><td>40 GB</td><td>8</td><td>A100_NVLINK</td><td>NVIDIA</td><td>6,912</td></tr><tr><td>A100 PCIe</td><td>Ampere</td><td>40 GB</td><td>8</td><td>A100_PCIE_40GB</td><td>NVIDIA</td><td>6,912</td></tr><tr><td>A100 PCIe</td><td>Ampere</td><td>80 GB</td><td>8</td><td>A100_PCIE_80GB</td><td>NVIDIA</td><td>6,912</td></tr><tr><td>A40</td><td>Ampere</td><td>48 GB</td><td>8</td><td>A40</td><td>NVIDIA</td><td>10,752</td></tr><tr><td>A6000</td><td>Ampere</td><td>48 GB</td><td>8</td><td>RTX_A6000</td><td>NVIDIA</td><td>10,752</td></tr><tr><td>RTX A5000</td><td>Ampere</td><td>24 GB</td><td>8</td><td>RTX_A5000</td><td>NVIDIA</td><td>8,192</td></tr><tr><td>RTX A4000</td><td>Ampere</td><td>16 GB</td><td>7</td><td>RTX_A4000</td><td>NVIDIA</td><td>6,144</td></tr><tr><td>Tesla V100 NVLINK</td><td>Volta</td><td>16 GB</td><td>8</td><td>Tesla_V100_NVLINK</td><td>NVIDIA</td><td>5,120</td></tr><tr><td>RTX 5000</td><td>Turing</td><td>16 GB</td><td>4</td><td>Quadro_RTX_5000</td><td>NVIDIA</td><td>3,072</td></tr><tr><td>RTX 4000</td><td>Turing</td><td>8 GB</td><td>7</td><td>Quadro_RTX_4000</td><td>NVIDIA</td><td>2,304</td></tr></tbody></table>

{% hint style="warning" %}
If a workload requests more peripheral compute resources (vCPU, RAM) than offered in a standard instance size, [additional costs will incur](../resources/resource-based-pricing.md).
{% endhint %}

## CPU Availability

CPU Only nodes are available for tasks such as control-plane services, databases, ingresses and CPU rendering.

| CPU Model           | Max RAM per vCPU | Max vCPU per Workload | Label               |
| ------------------- | ---------------- | --------------------- | ------------------- |
| Intel Xeon v3       | 4 GB             | 70                    | intel-xeon-v3       |
| Intel Xeon v4       | 4 GB             | 70                    | intel-xeon-v4       |
| Intel Xeon Scalable | 4 GB             | 94                    | intel-xeon-scalable |
| AMD Epyc Rome       | 4 GB             | 46                    | amd-epyc-rome       |
| AMD Epyc Milan      | 4 GB             | 46                    | amd-epyc-milan      |

{% hint style="info" %}
Workloads without GPU requests are always scheduled on CPU nodes.
{% endhint %}

### Requesting Compute in Kubernetes

A combination of [resource requests ](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)and[ node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity) is used to select the type and amount of compute for your workload. CoreWeave Cloud relies only on these native Kubernetes methods for resource allocation, allowing maximum flexibilty. The label used to select GPU type is `gpu.nvidia.com/class` and CPU type is `node.coreweave.cloud/cpu`. Please note that these labels are mutually exclusive, CPU type can't be explicitly selected for GPU nodes.

{% tabs %}
{% tab title="Single A100 80GB" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 15
        memory: 97Gi
        nvidia.com/gpu: 1
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - A100_PCIE_80GB
```
{% endtab %}

{% tab title="8x A100 NVLINK" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      requests:
        cpu: 90
        memory: 700Gi
      limits:
        nvidia.com/gpu: 8
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - A100_NVLINK
```
{% endtab %}

{% tab title="A100 With Fallback To A40" %}
```yaml
spec:
  containers:
  - name: example
    resources:
      limits:
        cpu: 12
        memory: 24Gi
        nvidia.com/gpu: 1
        
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - A100_PCIE_40GB
              - A40
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 20
          preference:
            matchExpressions:
              - key: gpu.nvidia.com/class
                operator: In
                values:
                  - A100_PCIE_40GB
```
{% endtab %}

{% tab title="16 Core Xeon v3/v4 CPU" %}
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
          - key: node.coreweave.cloud/cpu
            operator: In
            values:
              - intel-xeon-v3
              - intel-xeon-v4
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
          - key: node.coreweave.cloud/cpu
            operator: In
            values:
              - amd-epyc-rome
              - amd-epyc-milan
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Kubernetes allows resources to be scheduled with `requests` and `limits.` When only `limits` are specified, the `requests` are set to the same amount as the limit.
{% endhint %}
