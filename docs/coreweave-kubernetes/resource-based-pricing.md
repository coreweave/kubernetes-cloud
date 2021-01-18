# Resource Based Pricing

CoreWeave Cloud is built to provide significant flexibility in hardware selection, allowing customization of CPU, RAM, storage and GPU requests when scheduling your workloads. Resources are scheduled using these provided configurations, providing savings and simplicity on top of legacy cloud alphabet-soup instance type selection.

While we also show pricing and allow scheduling based upon ["Standard Instances"](https://www.coreweave.com/pricing), all CoreWeave Cloud instances are configurable, and all billing is à la carte, priced by the hour, billed by the minute. All billing is based upon the greater of resources requested in an instance, or, if burstable, the actual resources consumed during any minute billing window.

### GPU Instance Resource Pricing

The following components are configurable in GPU based instances.

| Type | Description | Resource Label | Cost per Hour | VRAM |
| :--- | :--- | :--- | :--- | :--- |
| GPU | NVIDIA A100 for NVLINK | A100\_NVLINK | $2.06 | 40GB HBM2e |
| GPU | NVIDIA V100 for NVLINK | Tesla\_V100\_NVLINK | $0.80 | 16GB HBM2 |
| GPU | NVIDIA V100 for PCIe | Tesla\_V100 | $0.47 | 16GB HBM2 |
| GPU | NVIDIA Quadro RTX 6000 | Quadro\_RTX\_6000 | $0.97 | 24GB GDDR6 |
| GPU | NVIDIA Quadro RTX 5000 | Quadro\_RTX_\__5000 | $0.57 | 16GB GDDR6 |
| GPU | NVIDIA Quadro RTX 4000 | Quadro\_RTX\_4000 | $0.24 | 8GB GDDR6 |
| GPU | NVIDIA P100 for NVLINK | Tesla\_P100\_NVLINK | $0.55 | 16GB HBM2 |
| CPU | AMD Epyc vCPU | epyc | $0.010 | N/A |
| CPU | Intel Xeon vCPU | xeon | $0.005 | N/A |
| RAM | System RAM per GB | memory | $0.005 | N/A |

An example, guaranteed request, hardware configuration of 4 Tesla V100 NVLINK GPUs with 32 Intel Xeon vCPU and 128GB of RAM would look something like:

```yaml
  containers:
  - name: v100-example
    resources:
      requests:
        cpu: 32
        memory: 128Gi
        nvidia.com/gpu: 4
      limits:
        cpu: 32
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
          - key: cpu.coreweave.cloud/family
            operator: In
            values:
              - xeon    
```

In the above example, the cost per hour of the instance would be:

```text
Instance Configuration:

4x NVIDIA Tesla V100 for NVLINK
32 Intel Xeon vCPU
128Gi System RAM

Instance Cost:
    Tesla_V100_NVLINK -> $0.80 * 4
    Xeon vCPU         -> $0.005 * 32
    System RAM        -> $0.005 * 128
                      =  $4.00 per hour
```

### CPU Only Instance Resource Pricing

Instances without a GPU attached are configurable in combinations of vCPU and system RAM. Combinations can be configured in multiples of:

| CPU Type | Resource Label | Ram per vCPU | Cost per vCPU per Hour |
| :--- | :--- | :--- | :--- |
| AMD Epyc | epyc | 4GB | $0.03 |
| Intel Xeon v1/v2 | xeon | 3GB | $0.009 |

An example configuration requesting 6 AMD Epyc vCPU with 24GB of RAM would look like:

```yaml
  containers:
  - name: epyc-example
    resources:
      requests:
        cpu: 6
        memory: 24Gi      
      limits:
        cpu: 6
        memory: 24Gi        
        
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

In the above example, the cost per hour of the instance would be:

```text
Instance Configuration:

6 AMD Epyc vCPU
24Gi System RAM

Instance Cost:
    AMD Epyc vCPU     -> $0.03 * 6
                      =  $0.18 per hour
```



