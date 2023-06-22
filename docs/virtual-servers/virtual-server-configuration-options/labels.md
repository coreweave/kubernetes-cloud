---
description: Add labels to your Virtual Server
---

# Labels

[Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) are key/value pairs that may be attached to Virtual Servers to offer better descriptions of their function to users. Labels also allow for efficient queries, such as during monitoring a certain set of resources.

Labels are distinct from [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/), which are not used to select objects but instead are used to apply arbitrary data to a given resource.

{% tabs %}
{% tab title="Cloud UI" %}
## Deployment method: <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, click the **Labels** expandable.

Here, a set of key-value labels may be specified:

<figure><img src="../../.gitbook/assets/image (29) (3).png" alt=""><figcaption></figcaption></figure>

Existing labels will appear in blue bubbles above the editable fields. To remove an existing label, click the "X" button beside its name. To edit it, click the pencil icon.

In this example, the label pairing `key: value` is added to the manifest. Labels appear in the `metadata.labels` section of the manifest.

<figure><img src="../../.gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

Example in plain text:

{% code overflow="wrap" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  namespace: tenant-sta-coreweave
  name: new-0647
  annotations:
    external-dns.alpha.kubernetes.io/hostname: new-0647.tenant-sta-coreweave.coreweave.cloud
  labels:
    key: value
```
{% endcode %}
{% endtab %}

{% tab title="CLI" %}
## Deployment method: <mark style="background-color:green;">Kubernetes CLI</mark>

Labels are specified in the Deployment manifest under the `metadata.labels` stanza.

Example in plain text:

{% code overflow="wrap" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
    namespace: tenant-sta-coreweave
    name: new-0647
    annotations:
        external-dns.alpha.kubernetes.io/hostname: new-0647.tenant-sta-coreweave.coreweave.cloud
    labels:
        key: value
```
{% endcode %}
{% endtab %}

{% tab title="Terraform" %}
## Deployment method: <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**

It is not currently possible to apply labels to Virtual Servers using Terraform, however [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
