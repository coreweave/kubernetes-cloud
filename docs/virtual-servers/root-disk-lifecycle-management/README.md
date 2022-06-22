---
description: Manage custom OS images on CoreWeave Cloud
---

# Root Disk Lifecycle Management

When instantiating Virtual Servers, it is often desired to have a customized template root disk image to instantiate off. CoreWeave provides standard images with the base OS, GPU drivers and utilities like Docker. There are multiple ways to customize the CoreWeave provided images into your own templates, or import a new image from an external source.

**Expanding a VM Root Disk**

{% content-ref url="expanding-disks.md" %}
[expanding-disks.md](expanding-disks.md)
{% endcontent-ref %}

**Manual Customization and Cloning**

{% content-ref url="creating-a-virtual-server-base-image.md" %}
[creating-a-virtual-server-base-image.md](creating-a-virtual-server-base-image.md)
{% endcontent-ref %}

**Automatic provisioning and CI integration using Packer**

1. [Copying CoreWeave Images to a Writeable PVC](exporting-coreweave-images-to-a-writable-pvc.md)
2. [Using Hashicorp Packer to create and update OS Images](using-packer-to-create-and-update-os-images/)
   1. [Creating a Packer Worker Virtual Server](using-packer-to-create-and-update-os-images/creating-a-packer-worker-virtual-server.md)
   2. [Configuring a Windows Image sourced from CoreWeave Cloud](using-packer-to-create-and-update-os-images/configuring-a-windows-image-sourced-from-coreweave-cloud.md)
   3. [Configuring a Linux image sourced from CoreWeave Cloud](using-packer-to-create-and-update-os-images/configuring-a-linux-image-sourced-from-coreweave-cloud.md)
   4. [Configuring an externally sourced cloud Linux image](using-packer-to-create-and-update-os-images/configuring-an-externally-sourced-cloud-linux-image.md)
3. [Exporting images to QCOW2](exporting-images-to-qcow2.md)

**Exporting and Importing images from external sources**

{% content-ref url="exporting-images-to-qcow2.md" %}
[exporting-images-to-qcow2.md](exporting-images-to-qcow2.md)
{% endcontent-ref %}

{% content-ref url="importing-a-qcow2-image.md" %}
[importing-a-qcow2-image.md](importing-a-qcow2-image.md)
{% endcontent-ref %}
