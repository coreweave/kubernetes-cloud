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

| Label                      | Refers to                             | Value options                                                                                 |
| -------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------- |
| `node.coreweave.cloud/cpu` | The CPU family of the CPU on the node | See [CPU-only instances](node-types.md#cpu-availability) for a list of types and their values |

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

| Label                  | Refers to                              | Value options                            |
| ---------------------- | -------------------------------------- | ---------------------------------------- |
| `gpu.nvidia.com/count` | Number of GPUs provisioned in the node | `4` to `8`; must be included as a string |

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

| Label                  | Refers to                             | Value options                                                                               |
| ---------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------- |
| `gpu.nvidia.com/class` | The GPU model provisioned in the node | See [Node Types](node-types.md#component-availability) for a list of types and their values |

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

| Label                 | Refers to                                                       | Value options                                                                                      |
| --------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `gpu.nvidia.com/vram` | The GPU VRAM, in Gigabytes, on the GPUs provisioned in the node | See the **VRAM** column in [the GPU-enabled Node Types list](node-types.md#component-availability) |

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

| Label                            | Refers to                              | Value options        |
| -------------------------------- | -------------------------------------- | -------------------- |
| `ethernet.coreweave.cloud/speed` | Uplink speed from node to the backbone | `10G`, `40G`, `100G` |

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

| Label                   | Refers to                                                  | Value options   |
| ----------------------- | ---------------------------------------------------------- | --------------- |
| `gpu.nvidia.com/nvlink` | Denotes whether or not GPUs are interconnected with NVLink | `true`, `false` |

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

| Label                           | Refers to                        | Value options          |
| ------------------------------- | -------------------------------- | ---------------------- |
| `topology.kubernetes.io/region` | The region the node is placed in | `ORD1`, `LAS1`, `LGA1` |

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
