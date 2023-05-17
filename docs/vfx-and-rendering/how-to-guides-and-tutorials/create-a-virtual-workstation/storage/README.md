---
description: Learn how to configure and use storage for your VFX Cloud Studio
---

# Create and Access Storage

This tutorial walks through creating and using the most basic storage volume appropriate for a VFX studio.

{% hint style="info" %}
**Note**

If your studio configuration requires a more custom solution, [reach out to your CoreWeave Support Specialist](https://cloud.coreweave.com/contact).
{% endhint %}

## Create a storage volume

Create a new shared filesystem volume in your namespace.

Creating storage volumes is as simple as navigating to the Storage Volumes page in the Cloud UI, and clicking **New Volume**. Refer to [Using Storage - Cloud UI](../../../../storage/storage/using-storage-cloud-ui.md) for more information.

## Attach a storage volume

Near the bottom of the deployment form is the **Attach Volumes** section. Here, created volumes may be selected to attach to the Virtual Workstation. To attach a listed volume to the Virtual Workstation, click the toggle beside the desired volume to "Attached."

<figure><img src="../../../../.gitbook/assets/image (20).png" alt="Screenshot of the volume attachment toggles"><figcaption><p>Volumes are detached by default, so must be explicitly attached using the toggles</p></figcaption></figure>

## Exposing storage

{% hint style="warning" %}
**Important**

It is strongly recommended that application workloads that require storage volumes be placed in the same data center region as their associated storage volumes.

See [Custom Containers](../../../../coreweave-kubernetes/custom-containers.md) for examples, or refer to the [Advanced Label Selectors page](../../../../../coreweave-kubernetes/label-selectors.md) for more information on scheduling workloads to the same data center region as their storage volumes.
{% endhint %}

CoreWeave provides a few different methods for exposing storage volumes to external Workstations or to on-premise services, but storage volumes may also be exposed in other ways using custom, containerized images.

The three out-of-the-box methods for connecting storage volumes for render outputs are:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="./#exposing-storage-via-nfs"><strong>NFS server</strong></a></td><td>Recommended for Linux and macOS machines</td><td></td><td><a href="nfs.md">nfs.md</a></td></tr><tr><td><a href="./#connecting-to-samba-windows"><strong>Samba</strong></a></td><td>Recommended for Windows machines</td><td></td><td><a href="samba.md">samba.md</a></td></tr><tr><td><a href="./#exposing-storage-via-filebrowser"><strong>FileBrowser</strong></a></td><td>Recommended for any OS</td><td></td><td><a href="../../../../storage/filebrowser.md">filebrowser.md</a></td></tr></tbody></table>

{% hint style="info" %}
**Note**

To associate storage volumes using specified mount paths, see [Using Storage - Kubectl: Attaching Storage Volumes](../../../../storage/storage/using-storage-kubectl.md#attaching-storage-volumes).
{% endhint %}
