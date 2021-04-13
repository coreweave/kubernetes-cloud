---
description: Label selectors are available for precise placement of workloads
---

# Advanced Label Selectors

Selecting the right hardware for your workload is important. All compute nodes are tagged with a set of labels specifying the hardware type. [Affinity Rules](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) should be leveraged on workloads to ensure that the desired type of hardware \(ie. GPU model\) gets assigned to your job.

{% hint style="info" %}
The basic node selectors demonstrated in [Node Types](node-types.md#requesting-compute-in-kubernetes) are usually all that is needed to properly schedule workloads. Please [contact support](mailto:%20cloud.support@coreweave.com) for any questions about advanced scheduling or special requirements.
{% endhint %}

<table>
  <thead>
    <tr>
      <th style="text-align:left">Label</th>
      <th style="text-align:left">Possible Values</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">cpu.coreweave.cloud/family</td>
      <td style="text-align:left">i9, i7, i5, celeron, xeon, epyc</td>
      <td style="text-align:left">The CPU family of the CPU in the node</td>
    </tr>
    <tr>
      <td style="text-align:left">ethernet.coreweave.cloud/speed</td>
      <td style="text-align:left">1G, 10G</td>
      <td style="text-align:left">The uplink speed from the node to the backbone</td>
    </tr>
    <tr>
      <td style="text-align:left">gpu.nvidia.com/count</td>
      <td style="text-align:left">4-8</td>
      <td style="text-align:left">Number of GPUs provisioned in the node. Using this selector is not recommended
        as the GPU resource requests are the correct method of selecting GPU count
        requirement</td>
    </tr>
    <tr>
      <td style="text-align:left">gpu.nvidia.com/class</td>
      <td style="text-align:left">Tesla_V100 (<a href="node-types.md#gpu-availability">see list</a>)</td>
      <td
      style="text-align:left">GPU model provisioned in the node</td>
    </tr>
    <tr>
      <td style="text-align:left">gpu.nvidia.com/vram</td>
      <td style="text-align:left">8, 16</td>
      <td style="text-align:left">GPU VRAM in Gigabytes on the GPUs provisioned in the node</td>
    </tr>
    <tr>
      <td style="text-align:left">gpu.nvidia.com/nvlink</td>
      <td style="text-align:left">true, false</td>
      <td style="text-align:left">Denotes if GPUs are interconnected with NVLink. Currently applicable only
        for Tesla_V100</td>
    </tr>
    <tr>
      <td style="text-align:left">topology.kubernetes.io/region</td>
      <td style="text-align:left">
        <p>ORD1, EWR1, EWR2,</p>
        <p>LAS1</p>
      </td>
      <td style="text-align:left">The region the node is placed in</td>
    </tr>
  </tbody>
</table>

#### Examples

{% tabs %}
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
          - key: cpu.coreweave.cloud/family
            operator: In
            values:
              - xeon
          - key: ethernet.coreweave.cloud/speed
            operator: In
            values:
              - 10G
```
{% endtab %}
{% endtabs %}

#### 

