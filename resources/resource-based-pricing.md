---
description: Customize your hardware configurations with à la carte pricing
---

# Resource Based Pricing

CoreWeave's entire infrastructure is purpose-built for compute-intensive workloads, and everything from our servers to our storage and networking solutions are designed to deliver best-in-class performance that are up to **35x faster and 80% less expensive** than generalized public Clouds.

Hardware selection is significantly flexible, allowing for custom configurations of CPU, GPU, RAM, and storage requests when scheduling workloads. Resources are scheduled using provided configurations, granting both savings and simplicity on top of legacy Cloud instance type selection.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4dc">📜</span> Learn about CoreWeave node types</td><td></td><td></td><td><a href="../coreweave-kubernetes/node-types.md">node-types.md</a></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f517">🔗</span> View pricing tiers on our website</td><td></td><td></td><td><a href="https://www.coreweave.com/gpu-cloud-pricing">https://www.coreweave.com/gpu-cloud-pricing</a></td></tr></tbody></table>

## Instance pricing

While CoreWeave allows scheduling and [provides pricing based on standard instances](https://www.coreweave.com/gpu-cloud-pricing), all CoreWeave Cloud instances are highly configurable. All billing is à la carte; priced by the hour, and billed by the minute.

All billing is based on the greater of resources requested in an instance. If the instance is configured to be burstable, billing is based on the actual resources consumed during any minute billing window.

## NVIDIA GPU instance pricing

The following components are configurable in GPU based instances.

| Description          | Label               | Cost per hour | VRAM       |
| -------------------- | ------------------- | ------------- | ---------- |
| H100 HGX (80GB)      | `H100_NVLINK_80GB`  | $4.78         | N/A        |
| H100 for PCIe (80GB) | `H100_PCIE`         | $4.25         | N/A        |
| A100 HGX (80GB)      | `A100_NVLINK_80GB`  | $2.21         | N/A        |
| A100 HGX (40GB)      | `A100_NVLINK`       | $2.06         | 40GB HBM2e |
| A100 for PCIe (40GB) | `A100_PCIE_40GB`    | $2.06         | 40GB HBM2e |
| A100 for PCIe (80GB) | `A100_PCIE_80GB`    | $2.21         | N/A        |
| V100 for NVLINK      | `Tesla_V100_NVLINK` | $0.80         | 16GB HBM2  |
| A40                  | `A40`               | $1.28         | 48GB GDDR6 |
| RTX A6000            | `RTX_A6000`         | $1.28         | 48GB GDDR6 |
| RTX A5000            | `RTX_A5000`         | $0.77         | 24GB GDDR6 |
| RTX A4000            | `RTX_A4000`         | $0.61         | 16GB GDDR6 |
| Quadro RTX 5000      | `Quadro_RTX_5000`   | $0.57         | 16GB GDDR6 |
| Quadro RTX 4000      | `Quadro_RTX_4000`   | $0.24         | 8GB GDDR6  |

## CPU component pricing

The following CPU components are also configurable in GPU based instances. For CPU-only instances, see [CPU-only instance pricing](resource-based-pricing.md#cpu-only-instance-pricing).

| Node type           | Label                 | Cost per hour |
| ------------------- | --------------------- | ------------- |
| AMD Epyc Milan vCPU | `amd-epyc-milan`      | $0.010        |
| AMD Epyc Rome vCPU  | `amd-epyc-rome`       | $0.010        |
| Intel Xeon Scalable | `intel-xeon-scalable` | $0.010        |
| Intel Xeon v4       | `intel-xeon-v4`       | $0.010        |

## CPU-only instance pricing

Instances **without a GPU attached** are configurable as combinations of vCPU and system RAM.

For these instances, system RAM is included in the vCPU price. Combinations can be configured in multiples of the following.

| CPU Type            | Label               | RAM per vCPU | Cost per vCPU per Hour |
| ------------------- | ------------------- | ------------ | ---------------------- |
| AMD Epyc Milan      | amd-epyc-milan      | 4GB          | $0.035                 |
| AMD Epyc Rome       | amd-epyc-rome       | 4GB          | $0.030                 |
| Intel Xeon Scalable | intel-xeon-scalable | 4GB          | $0.030                 |
| Intel Xeon v4       | intel-xeon-v4       | 4GB          | $0.020                 |
| Intel Xeon v3       | intel-xeon-v3       | 4GB          | $0.0125                |

## RAM

RAM may be specified as an additional component on its own.

| Component         | Label    | Cost per hour |
| ----------------- | -------- | ------------- |
| System RAM per GB | `memory` | $0.005        |

## Example configurations

Below is an example configuration provided in an excerpt of a YAML manifest, in which 6 AMD Epyc Rome vCPUs with 24GB of RAM are requested.

{% hint style="info" %}
**Additional Resources**

In this example, the node type is chosen using an `affinity`. For more information on using affinities to select hardware, see [Node Types](../coreweave-kubernetes/node-types.md) and [Advanced Label Selectors](../coreweave-kubernetes/label-selectors.md).
{% endhint %}

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

In this example, the requested resources are:

| CPU amount | Instance type | Unit cost per hour | System RAM |
| ---------- | ------------- | ------------------ | ---------- |
| 6          | AMD Epyc Rome | $0.03              | `24Gi`     |

The total per hour cost of this instance would be $0.03 x 6, equaling $0.18 per hour.

In this example, a hardware configuration of `4` Tesla V100 NVLINK GPUs with 32 Intel Xeon Scalable vCPU and 128GB of RAM is requested:

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

In this example, the requested resources are:

| Instance type     | Instance count | Unit cost per hour |
| ----------------- | -------------- | ------------------ |
| Tesla V100 NVLINK | 4              | $0.80              |

| vCPU count | vCPU cost per hour |
| ---------- | ------------------ |
| 32         | $0.01              |

| RAM amount | RAM cost per hour |
| ---------- | ----------------- |
| `128Gi`    | $0.005            |

The per hour cost of these resources equals `($0.80 x 4) + ($0.01 x 32) + ($0.005 x 128)`, or $4.16 per hour.

## **Public IP address pricing**

IP Addresses are billed at $4.00 per IP per month.

For periods of use less than one month, this charge is prorated by the minute just as all other billing. If a public IP address is assigned to an instance but the instance is not running, billing **will continue to accrue** for this reserved Public IP Address.

## **Billing periods**

All CoreWeave Cloud billing periods cover the calendar month.

For example, a billing period that begins on `1 January 12:00am UTC` ends on `1 February 12:00am UTC`.
