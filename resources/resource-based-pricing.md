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

<table><thead><tr><th width="235">Description</th><th width="224">Label</th><th>Cost per hour</th><th>VRAM</th></tr></thead><tbody><tr><td>H100 HGX (80GB)</td><td><code>H100_NVLINK_80GB</code></td><td>$4.78</td><td>N/A</td></tr><tr><td>H100 for PCIe (80GB)</td><td><code>H100_PCIE</code></td><td>$4.25</td><td>N/A</td></tr><tr><td>A100 HGX (80GB)</td><td><code>A100_NVLINK_80GB</code></td><td>$2.21</td><td>N/A</td></tr><tr><td>A100 HGX (40GB)</td><td><code>A100_NVLINK</code></td><td>$2.06</td><td>40GB HBM2e</td></tr><tr><td>A100 for PCIe (40GB)</td><td><code>A100_PCIE_40GB</code></td><td>$2.06</td><td>40GB HBM2e</td></tr><tr><td>A100 for PCIe (80GB)</td><td><code>A100_PCIE_80GB</code></td><td>$2.21</td><td>N/A</td></tr><tr><td>V100 for NVLINK</td><td><code>Tesla_V100_NVLINK</code></td><td>$0.80</td><td>16GB HBM2</td></tr><tr><td>A40</td><td><code>A40</code></td><td>$1.28</td><td>48GB GDDR6</td></tr><tr><td>RTX A6000</td><td><code>RTX_A6000</code></td><td>$1.28</td><td>48GB GDDR6</td></tr><tr><td>RTX A5000</td><td><code>RTX_A5000</code></td><td>$0.77</td><td>24GB GDDR6</td></tr><tr><td>RTX A4000</td><td><code>RTX_A4000</code></td><td>$0.61</td><td>16GB GDDR6</td></tr><tr><td>Quadro RTX 5000</td><td><code>Quadro_RTX_5000</code></td><td>$0.57</td><td>16GB GDDR6</td></tr><tr><td>Quadro RTX 4000</td><td><code>Quadro_RTX_4000</code></td><td>$0.24</td><td>8GB GDDR6</td></tr></tbody></table>

## CPU component pricing

The following CPU components are also configurable in GPU based instances. For CPU-only instances, see [CPU-only instance pricing](resource-based-pricing.md#cpu-only-instance-pricing).

<table><thead><tr><th width="257">Node type</th><th width="241">Label</th><th>Cost per hour</th></tr></thead><tbody><tr><td>AMD Epyc Milan vCPU</td><td><code>amd-epyc-milan</code></td><td>$0.010</td></tr><tr><td>AMD Epyc Rome vCPU</td><td><code>amd-epyc-rome</code></td><td>$0.010</td></tr><tr><td>Intel Xeon Scalable</td><td><code>intel-xeon-scalable</code></td><td>$0.010</td></tr><tr><td>Intel Xeon v4</td><td><code>intel-xeon-v4</code></td><td>$0.010</td></tr></tbody></table>

## CPU-only instance pricing

Instances **without a GPU attached** are configurable as combinations of vCPU and system RAM.

For these instances, system RAM is included in the vCPU price. Combinations can be configured in multiples of the following.

<table><thead><tr><th width="192">CPU Type</th><th width="189">Label</th><th width="150">RAM per vCPU</th><th>Cost per vCPU per Hour</th></tr></thead><tbody><tr><td>AMD Epyc Milan</td><td>amd-epyc-milan</td><td>4GB</td><td>$0.035</td></tr><tr><td>AMD Epyc Rome</td><td>amd-epyc-rome</td><td>4GB</td><td>$0.030</td></tr><tr><td>Intel Xeon Scalable</td><td>intel-xeon-scalable</td><td>4GB</td><td>$0.030</td></tr><tr><td>Intel Xeon v4</td><td>intel-xeon-v4</td><td>4GB</td><td>$0.020</td></tr><tr><td>Intel Xeon v3</td><td>intel-xeon-v3</td><td>4GB</td><td>$0.0125</td></tr></tbody></table>

## RAM

RAM may be specified as an additional component on its own.

<table><thead><tr><th width="259">Component</th><th width="242">Label</th><th>Cost per hour</th></tr></thead><tbody><tr><td>System RAM per GB</td><td><code>memory</code></td><td>$0.005</td></tr></tbody></table>

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

<table><thead><tr><th width="148.33333333333331">CPU amount</th><th width="204">Instance type</th><th width="200">Unit cost per hour</th><th>System RAM</th></tr></thead><tbody><tr><td>6</td><td>AMD Epyc Rome</td><td>$0.03</td><td><code>24Gi</code></td></tr></tbody></table>

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

<table><thead><tr><th width="216">Instance type</th><th width="166.33333333333331">Instance count</th><th>Unit cost per hour</th></tr></thead><tbody><tr><td>Tesla V100 NVLINK</td><td>4</td><td>$0.80</td></tr></tbody></table>

<table><thead><tr><th width="219">vCPU count</th><th>vCPU cost per hour</th></tr></thead><tbody><tr><td>32</td><td>$0.01</td></tr></tbody></table>

<table><thead><tr><th width="221">RAM amount</th><th>RAM cost per hour</th></tr></thead><tbody><tr><td><code>128Gi</code></td><td>$0.005</td></tr></tbody></table>

The per hour cost of these resources equals `($0.80 x 4) + ($0.01 x 32) + ($0.005 x 128)`, or $4.16 per hour.

## **Public IP address pricing**

IP Addresses are billed at $4.00 per IP per month.

For periods of use less than one month, this charge is prorated by the minute just as all other billing. If a public IP address is assigned to an instance but the instance is not running, billing **will continue to accrue** for this reserved Public IP Address.

## **Billing periods**

All CoreWeave Cloud billing periods cover the calendar month.

For example, a billing period that begins on `1 January 12:00am UTC` ends on `1 February 12:00am UTC`.
