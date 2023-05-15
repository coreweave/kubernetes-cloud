---
description: Learn more about storage on Virtual Servers.
---

# Storage

High-performance, network-attached storage for both [containerized workloads](https://docs.coreweave.com/coreweave-kubernetes/getting-started) and Virtual Servers is easy to provision and manage on CoreWeave Cloud. Available in both all-NVMe and HDD tiers, Storage Volumes can be created as Block Volumes or Shared File System Volumes, and can be resized at any time. Storage is managed separately from compute resources, and can be moved between instances and hardware types.

## Create a storage volume

To create a storage volume, refer to [Get Started with Storage.](../../storage/storage/)

## Attach a storage volume

{% tabs %}
{% tab title="Cloud UI" %}
## Deployment method: <mark style="background-color:blue;">CoreWeave Cloud UI</mark>&#x20;

Existing storage volumes may be attached to Virtual Servers under the **Attach Volumes** expandable.

**For more information, refer to** [**Using Storage - Cloud UI**](../../storage/storage/using-storage-cloud-ui.md#attach-a-storage-volume-using-the-cloud-ui)**.**

<figure><img src="../../.gitbook/assets/image (47).png" alt="The &#x22;Attach volumes&#x22; expandable"><figcaption></figcaption></figure>
{% endtab %}

{% tab title="CLI" %}
## Deployment method: <mark style="background-color:green;">Kubernetes CLI</mark>

**Refer to** [**Using Storage - CLI**](../../storage/storage/using-storage-kubectl.md)**.**
{% endtab %}

{% tab title="Terraform" %}
## Deployment method: <mark style="background-color:orange;">Terraform</mark>

Storage volumes must be created and attached using either [the CLI](../../storage/storage/using-storage-kubectl.md) or [the Cloud UI](../../storage/storage/using-storage-cloud-ui.md).
{% endtab %}
{% endtabs %}
