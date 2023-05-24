---
description: Use advanced label selectors for precise workload scheduling
---

# Advanced Label Selectors

Selecting the right hardware for your workloads is key for performance. While the basic node labels as listed in the [Node Types](node-types.md#requesting-compute-in-kubernetes) list are typically all that is needed to include in a Deployment manifest to schedule workloads properly, there are some situations in which more specific designations may be required, such as some instances of [deploying custom containers](../docs/coreweave-kubernetes/custom-containers.md).

On CoreWeave, compute nodes are tagged with [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/), which specify their hardware type. In turn, [Kubernetes affinities](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) are specified in [workload Deployment manifests](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) to select these labels, ensuring that your workloads are correctly scheduled to the desired hardware type.

{% hint style="info" %}
**Note**

For any questions about advanced scheduling or other special requirements, please [contact support](mailto:%20cloud.support@coreweave.com).
{% endhint %}

The following labels are attached to nodes on CoreWeave Cloud, and may be selected using affinities in the Deployment manifests, as demonstrated in the following affinity usage examples.

## CPU model

<table><thead><tr><th width="291">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>node.coreweave.cloud/cpu</code></td><td>The CPU family of the CPU on the node</td><td>See <a href="node-types.md#cpu-availability">CPU-only instances</a> for a list of types and their values</td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: node.coreweave.cloud/cpu
            operator: In
            values:
              - amd-epyc-rome
              - intel-xeon-v4
```

## GPU count

{% hint style="warning" %}
**Important**

Using this selector is not recommended. Instead, request GPU resources by setting the GPU count in the Deployment spec; see the guide on deploying [Custom Containers](../docs/coreweave-kubernetes/custom-containers.md#define-the-applications-resources) for examples.
{% endhint %}

<table><thead><tr><th width="286.3333333333333">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>gpu.nvidia.com/count</code></td><td>Number of GPUs provisioned in the node</td><td><code>4</code> to <code>8</code>; must be included as a string</td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/count
            operator: In
            values:
              - "3"
```

## GPU model

<table><thead><tr><th width="289.3333333333333">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>gpu.nvidia.com/class</code></td><td>The GPU model provisioned in the node</td><td>See <a href="node-types.md#component-availability">Node Types</a> for a list of types and their values</td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - A40
```

## GPU VRAM

<table><thead><tr><th width="289.3333333333333">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>gpu.nvidia.com/vram</code></td><td>The GPU VRAM, in Gigabytes, on the GPUs provisioned in the node</td><td>See the <strong>VRAM</strong> column in <a href="node-types.md#component-availability">the GPU-enabled Node Types list</a></td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/vram
            operator: In
            values:
              - "8"
```

## Uplink speed

<table><thead><tr><th width="283.3333333333333">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>ethernet.coreweave.cloud/speed</code></td><td>Uplink speed from node to the backbone</td><td><code>10G</code>, <code>40G</code>, <code>100G</code></td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: ethernet.coreweave.cloud/speed
            operator: In
            values:
              - 40G
```

## NVLink

{% hint style="warning" %}
**Important**

This label is currently applicable only for `Tesla_V100` nodes.
{% endhint %}

<table><thead><tr><th width="286">Label</th><th width="233.33333333333331">Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>gpu.nvidia.com/nvlink</code></td><td>Denotes whether or not GPUs are interconnected with NVLink</td><td><code>true</code>, <code>false</code></td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/nvlink
            operator: In
            values:
              - true
```

## Data center region

<table><thead><tr><th width="280.3333333333333">Label</th><th>Refers to</th><th>Value options</th></tr></thead><tbody><tr><td><code>topology.kubernetes.io/region</code></td><td>The region the node is placed in</td><td><code>ORD1</code>, <code>LAS1</code>, <code>LGA1</code></td></tr></tbody></table>

### Affinity usage example

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/region
            operator: In
            values:
              - ORD1
```
