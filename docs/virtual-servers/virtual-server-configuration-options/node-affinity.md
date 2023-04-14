---
description: Learn more about configuring Kubernetes node affinity for Virtual Servers.
---

# Node Affinity

[Kubernetes Affinities](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) can be used to schedule Virtual Servers onto specific hardware or specific types of hardware. If no Affinity is set, Virtual Servers will be automatically load-balanced according to the internal CoreWeave Cloud orchestration algorithm.

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the Cloud UI, the affinity for the Virtual Server can be configured in the `affinity` field in the YAML manifest as shown below.

![YAML manifest screenshot of affinity field.](<../../.gitbook/assets/image (14) (2) (1).png>)

```json
affinity: {}
```
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

**Type:** [Affinity](https://pkg.go.dev/k8s.io/kubernetes/pkg/apis/core#Affinity)

Defines the Kubernetes [affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) for the Virtual Server, if there is one.

| Field name | Type   | Description                                                                                                                                                                     | Default value |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `affinity` | string | Defines the Kubernetes [affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) for the Virtual Server, if there is one. | none          |
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**\
It is not currently possible to configure Node Affinity using the Terraform module. This setting may be configured in conjunction with use of the Cloud UI or the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
