# Resource Based Pricing

CoreWeave Cloud is built to provide significant flexibility in hardware selection, allowing customization of CPU, RAM, storage and GPU requests when scheduling your workloads. Resources are scheduled using these provided configurations, providing savings and simplicity on top of legacy cloud alphabet-soup instance type selection.

While we also show pricing and allow scheduling based upon ["Standard Instances"](https://www.coreweave.com/pricing), all CoreWeave Cloud instances are configurable, and all billing is à la carte, priced by the hour, billed by the minute. All billing is based upon the greater of resources requested in an instance, or, if burstable, the actual resources consumed during any minute billing window.

### GPU Instance Resource Pricing

The following components are configurable in GPU based instances.

| Type | Description                 | Label                | Cost per Hour | VRAM       |
| ---- | --------------------------- | -------------------- | ------------- | ---------- |
| GPU  | NVIDIA H100 HGX (80GB)      | H100\_NVLINK_\__80GB | $4.78         |            |
| GPU  | NVIDIA H100 for PCIe (80GB) | H100\_PCIE           | $4.25         |            |
| GPU  | NVIDIA A100 HGX (80GB)      | A100\_NVLINK_\__80GB | $2.21         |            |
| GPU  | NVIDIA A100 HGX (40GB)      | A100\_NVLINK         | $2.06         | 40GB HBM2e |
| GPU  | NVIDIA A100 for PCIe (40GB) | A100\_PCIE\_40GB     | $2.06         | 40GB HBM2e |
| GPU  | NVIDIA A100 for PCIe (80GB) | A100\_PCIE\_80GB     | $2.21         |            |
| GPU  | NVIDIA V100 for NVLINK      | Tesla\_V100\_NVLINK  | $0.80         | 16GB HBM2  |
| GPU  | NVIDIA A40                  | A40                  | $1.28         | 48GB GDDR6 |
| GPU  | NVIDIA RTX A6000            | RTX\_A6000           | $1.28         | 48GB GDDR6 |
| GPU  | NVIDIA RTX A5000            | RTX\_A5000           | $0.77         | 24GB GDDR6 |
| GPU  | NVIDIA RTX A4000            | RTX\_A4000           | $0.61         | 16GB GDDR6 |
| GPU  | NVIDIA Quadro RTX 5000      | Quadro\_RTX\_5000    | $0.57         | 16GB GDDR6 |
| GPU  | NVIDIA Quadro RTX 4000      | Quadro\_RTX\_4000    | $0.24         | 8GB GDDR6  |
| CPU  | AMD Epyc Milan vCPU         | amd-epyc-milan       | $0.010        | N/A        |
| CPU  | AMD Epyc Rome vCPU          | amd-epyc-rome        | $0.010        | N/A        |
| CPU  | Intel Xeon Scalable         | intel-xeon-scalable  | $0.010        | N/A        |
| CPU  | Intel Xeon v4               | intel-xeon-v4        | $0.010        | N/A        |
| RAM  | System RAM per GB           | memory               | $0.005        | N/A        |

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
```

In the above example, the cost per hour of the instance would be:

```
Instance Configuration:

4     NVIDIA Tesla V100 for NVLINK
32    vCPU
128Gi System RAM

Instance Cost:
    Tesla_V100_NVLINK -> $0.80 * 4
    vCPU              -> $0.01 * 32
    System RAM        -> $0.005 * 128
                      =  $4.16 per hour
```

### CPU Only Instance Resource Pricing

Instances without a GPU attached are configurable in combinations of vCPU and system RAM. For these instances, system RAM is included in the vCPU price. Combinations can be configured in multiples of:

| CPU Type            | Label               | RAM per vCPU | Cost per vCPU per Hour |
| ------------------- | ------------------- | ------------ | ---------------------- |
| AMD Epyc Milan      | amd-epyc-milan      | 4GB          | $0.035                 |
| AMD Epyc Rome       | amd-epyc-rome       | 4GB          | $0.030                 |
| Intel Xeon Scalable | intel-xeon-scalable | 4GB          | $0.030                 |
| Intel Xeon v4       | intel-xeon-v4       | 4GB          | $0.020                 |
| Intel Xeon v3       | intel-xeon-v3       | 4GB          | $0.0125                |

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

**Public IP Addresses**

IP Addresses are billed at $4.00 per IP per month. For periods of use less than one month, this charge is pro-rated like other billing, by the minute. If a Public IP Address is assigned to an instance and the instance is not running, billing will CONTINUE to accrue for this reserved Public IP Address.

**Billing Periods**

All CoreWeave Cloud billing periods cover the calendar month (i.e. 1 January 12:00am UTC thru 1 February 12:00am UTC).
