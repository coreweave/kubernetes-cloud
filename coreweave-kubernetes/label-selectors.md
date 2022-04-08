---
description: Label selectors are available for precise placement of workloads
---

# Advanced Label Selectors

Selecting the right hardware for your workload is important. All compute nodes are tagged with a set of labels specifying the hardware type. [Affinity Rules](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) should be leveraged on workloads to ensure that the desired type of hardware (ie. GPU model) gets assigned to your job.

{% hint style="info" %}
The basic node selectors demonstrated in [Node Types](node-types.md#requesting-compute-in-kubernetes) are usually all that is needed to properly schedule workloads. Please [contact support](mailto:%20cloud.support@coreweave.com) for any questions about advanced scheduling or special requirements.
{% endhint %}

| Label                          | Possible Values                                                                         | Description                                                                                                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| node.coreweave.cloud/cpu       | ([see list](../resources/resource-based-pricing.md#cpu-only-instance-resource-pricing)) | The CPU family of the CPU in the node                                                                                                                                 |
| ethernet.coreweave.cloud/speed | 1G, 10G, 40G, 100G                                                                      | The uplink speed from the node to the backbone                                                                                                                        |
| gpu.nvidia.com/count           | 4-8                                                                                     | Number of GPUs provisioned in the node. Using this selector is not recommended as the GPU resource requests are the correct method of selecting GPU count requirement |
| gpu.nvidia.com/class           | ([see list](node-types.md#gpu-availability))                                            | GPU model provisioned in the node                                                                                                                                     |
| gpu.nvidia.com/vram            | ([see list](node-types.md#gpu-availability))                                            | GPU VRAM in Gigabytes on the GPUs provisioned in the node                                                                                                             |
| gpu.nvidia.com/nvlink          | true, false                                                                             | Denotes if GPUs are interconnected with NVLink. Currently applicable only for Tesla\_V100                                                                             |
| topology.kubernetes.io/region  | <p>ORD1, EWR1,</p><p>LAS1, LGA1</p>                                                     | The region the node is placed in                                                                                                                                      |

#### Examples

{% tabs %}
{% tab title="Schedule in ORD1 only" %}
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
{% endtab %}

{% tab title="16 Core Xeon CPU with 10GE " %}
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
              - intel-xeon-v4
          - key: ethernet.coreweave.cloud/speed
            operator: In
            values:
              - 10G
```
{% endtab %}
{% endtabs %}

####
