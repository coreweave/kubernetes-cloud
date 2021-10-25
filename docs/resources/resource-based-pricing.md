# Resource Based Pricing

CoreWeave Cloud is built to provide significant flexibility in hardware selection, allowing customization of CPU, RAM, storage and GPU requests when scheduling your workloads. Resources are scheduled using these provided configurations, providing savings and simplicity on top of legacy cloud alphabet-soup instance type selection.

While we also show pricing and allow scheduling based upon ["Standard Instances"](https://www.coreweave.com/pricing), all CoreWeave Cloud instances are configurable, and all billing is à la carte, priced by the hour, billed by the minute. All billing is based upon the greater of resources requested in an instance, or, if burstable, the actual resources consumed during any minute billing window.

### GPU Instance Resource Pricing

The following components are configurable in GPU based instances.

| Type | Description            | Resource Label        | Cost per Hour | VRAM       |
| ---- | ---------------------- | --------------------- | ------------- | ---------- |
| GPU  | NVIDIA A100 for NVLINK | A100\_NVLINK          | $2.06         | 40GB HBM2e |
| GPU  | NVIDIA A100 for PCIE   | A100\_PCIE\_40GB      | $2.06         | 40GB HBM2e |
| GPU  | NVIDIA V100 for NVLINK | Tesla\_V100\_NVLINK   | $0.80         | 16GB HBM2  |
| GPU  | NVIDIA A40             | A40                   | $1.28         | 48GB GDDR6 |
| GPU  | NVIDIA RTX A6000       | RTX\_A6000            | $1.28         | 48GB GDDR6 |
| GPU  | NVIDIA RTX A5000       | RTX\_A5000            | $0.77         | 24GB GDDR6 |
| GPU  | NVIDIA RTX A4000       | RTX\_A4000            | $0.61         | 16GB GDDR6 |
| GPU  | NVIDIA Quadro RTX 5000 | Quadro\_RTX_\__5000   | $0.57         | 16GB GDDR6 |
| GPU  | NVIDIA Quadro RTX 4000 | Quadro\_RTX\_4000     | $0.24         | 8GB GDDR6  |
| GPU  | NVIDIA V100 for PCIe   | Tesla\_V100           | $0.47         | 16GB HBM2  |
| CPU  | AMD Epyc Milan vCPU    | amd-epyc-milan        | $0.010        | N/A        |
| CPU  | AMD Epyc Rome vCPU     | amd-epyc-rome         | $0.010        | N/A        |
| CPU  | AMD Threadripper       | amd-threadripper-zen2 | $0.010        | N/A        |
| CPU  | Intel Xeon Scalable    | intel-xeon-scalable   | $0.010        | N/A        |
| CPU  | Intel Xeon v4          | intel-xeon-v4         | $0.010        | N/A        |
| CPU  | Intel Xeon v3          | intel-xeon-v3         | $0.005        | N/A        |
| CPU  | Intel Xeon v2          | intel-xeon-v2         | $0.005        | N/A        |
| RAM  | System RAM per GB      | memory                | $0.005        | N/A        |

An example, guaranteed request, hardware configuration of 4 Tesla V100 NVLINK GPUs with 32 Intel Xeon Scalable vCPU and 128GB of RAM would look something like:

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
          - key: node.coreweave.cloud/cpu
            operator: In
            values:
              - intel-xeon-scalable    
```

In the above example, the cost per hour of the instance would be:

```
Instance Configuration:

4x NVIDIA Tesla V100 for NVLINK
32 Intel Xeon Scalable vCPU
128Gi System RAM

Instance Cost:
    Tesla_V100_NVLINK -> $0.80 * 4
    Xeon Scalable vCPU-> $0.01 * 32
    System RAM        -> $0.005 * 128
                      =  $4.16 per hour
```

### CPU Only Instance Resource Pricing

Instances without a GPU attached are configurable in combinations of vCPU and system RAM. For these instances, system RAM is included in the vCPU price. Combinations can be configured in multiples of:

| CPU Type            | Resource Label      | Ram per vCPU | Cost per vCPU per Hour |
| ------------------- | ------------------- | ------------ | ---------------------- |
| AMD Epyc Milan      | amd-epyc-milan      | 4GB          | $0.035                 |
| AMD Epyc Rome       | amd-epyc-rome       | 4GB          | $0.030                 |
| Intel Xeon Scalable | intel-xeon-scalable | 4GB          | $0.030                 |
| Intel Xeon v4       | intel-xeon-v4       | 4GB          | $0.020                 |
| Intel Xeon v2       | intel-xeon-v2       | 3GB          | $0.009                 |
| Intel Xeon v1       | intel-xeon-v1       | 3GB          | $0.009                 |

An example configuration requesting 6 AMD Epyc Rome vCPU with 24GB of RAM would look like:

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
          - key: node.coreweave.cloud/cpu
            operator: In
            values:
              - amd-epyc-rome   
```

In the above example, the cost per hour of the instance would be:

```
Instance Configuration:

6 AMD Epyc Rome vCPU
24Gi System RAM

Instance Cost:
    AMD Epyc vCPU     -> $0.03 * 6
                      =  $0.18 per hour
```

**Billing Periods**

All CoreWeave Cloud billing periods cover the calendar month (i.e. 1 January 12:00am UTC thru 1 February 12:00am UTC).
