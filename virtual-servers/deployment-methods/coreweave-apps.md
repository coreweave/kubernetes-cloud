---
description: Deploy Virtual Servers via the Cloud UI
---

# CoreWeave Cloud UI

The [CoreWeave Cloud UI](https://apps.coreweave.com/) is a responsive, Web-based dashboard enabling users to configure, deploy, and manage Virtual Servers using visual methods to deploy Virtual Servers.

## Prerequisites

This guide presumes you have [an active CoreWeave Cloud account](../../docs/coreweave-kubernetes/getting-started.md#create-an-account).

Once you have an active account, log in to the Cloud UI dashboard at [`https://cloud.coreweave.com`](https://cloud.coreweave.com).

## Create a Virtual Server

Once signed in to your CoreWeave Cloud account, navigate to the **Virtual Servers** menu located in the upper left-hand side of the sidebar menu, or click the **Deploy Now** button under **Deploy Virtual Servers** in the top-middle of the dashboard - this will redirect you to the Virtual Server hub.

<figure><img src="../../docs/.gitbook/assets/image (45).png" alt="Screenshot of the CoreWeave Cloud UI main page"><figcaption><p>Navigate to the Virtual Server creation page either from the Deploy Now button or using the side navigation</p></figcaption></figure>

The Virtual Server hub is where all existing Virtual Servers are listed. From here, you can manage current Virtual Servers, or create a new one. To create a new Virtual Server, click the **New Virtual Server** button.

<figure><img src="../../docs/.gitbook/assets/image (59).png" alt="Screenshot of the Virtual Server menu"><figcaption></figcaption></figure>

### Create a new Virtual Server from scratch

All [configuration options](coreweave-apps.md#configuration-options) for the Virtual Server may be set from the **New Virtual Server** screen. For more fine-grained control, click the **Show YAML Editor** button to directly interact with [the CRD YAML manifest](coreweave-apps.md#edit-the-crd-manifest-using-the-yaml-editor) of the Virtual Server.

All configuration options for the Virtual Server are set from the **New Virtual Server screen**.

<figure><img src="../../docs/.gitbook/assets/image (41).png" alt="New Virtual Server configuration screen"><figcaption></figcaption></figure>

In the upper right-hand corner of the Virtual Server configuration screen, there are three buttons:

* **Magic wand:** Revert the form to the last valid configuration
* **Arrow:** Reset the form, clearing all fields
* **Load or clone from existing:** Load an existing Virtual Server as a [template, or clone](coreweave-apps.md#templates-and-clones) an existing Virtual Server

<figure><img src="../../docs/.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>

### Templates and clones

Virtual Servers may also be created as clones of an existing Virtual Server, or from an existing Virtual Server acting as its template.

#### **What are clones and templates?**

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th></tr></thead><tbody><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f46d">👭</span><strong>Clones</strong></h3></td><td>A <strong>clone</strong> uses the PVC of an existing Virtual Server with an OS snapshot. Creating a clone will create a new Virtual Server that will be an exact duplicate of an existing Virtual Machine in its current state.</td><td></td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f4dd">📝</span> <strong>Templates</strong></h3></td><td>A <strong>template</strong> uses the root PVC used to create an existing Virtual Server. This will produce a new Virtual Server with the same configurations as the previous Virtual Server, but the new Virtual Server will not be in the same state or contain the same data as the existing one.</td><td></td></tr></tbody></table>

To create a new Virtual Server as a clone or from a template, click the **Load or clone from existing** button in the upper right-hand corner of the screen.

<figure><img src="../../docs/.gitbook/assets/image (76).png" alt="Screenshot demonstrating that the load or copy from existing button is the third button on the top right"><figcaption><p>The <strong>Load or clone from existing button</strong> is represented by a copy icon</p></figcaption></figure>

This will open the **Select Template** modal.

To use an existing Virtual Server as a template, select it from the drop-down presented. Or, toggle on the **Clone (use resource as source)** option to create an exact clone of the selected Virtual Server.

{% hint style="info" %}
**Note**

There must already be at least one existing Virtual Server from which to make a clone or use as a template.
{% endhint %}

<figure><img src="../../docs/.gitbook/assets/image (87).png" alt=""><figcaption></figcaption></figure>

### Configuration options

Click on any of the specification cards to learn more about each configuration option:

<table data-card-size="large" data-view="cards"><thead><tr><th>Specification</th><th>Description</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Name</strong></td><td>The name of the <a href="../getting-started.md">Virtual Server</a></td><td></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md#region"><strong>Region</strong></a></td><td>The <a href="../../docs/data-center-regions.md">data center region</a> in which to deploy the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md#region">#region</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md#hardware"><strong>Hardware</strong></a></td><td>The type and number of <a href="../../coreweave-kubernetes/node-types.md">GPUs</a> to allocate to the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md#hardware">#hardware</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md"><strong>Operating System</strong></a></td><td>The <a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md">Operating System</a> to run on the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md">operating-system-and-root-disk.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md"><strong>Network</strong></a></td><td>Attach a <a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md">Public IP or a LoadBalancer IP</a> to the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md">networking.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/storage.md"><strong>Attach Volumes</strong></a></td><td>Attach <a href="../../docs/virtual-servers/virtual-server-configuration-options/storage.md#attach-a-storage-volume">volumes</a> in the same namespace to the Virtual Server</td><td><a href="../../docs/storage/storage/using-storage-cloud-ui.md">using-storage-cloud-ui.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md"><strong>Users</strong></a></td><td>Create <a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md">user accounts</a> on your Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md">user-accounts.md</a></td></tr></tbody></table>

### Edit the CRD manifest using the YAML editor

Not all Virtual Server configuration options are exposed through the options displayed in the Web UI.

For more fine-grained control over the Virtual Server configuration, click the **EDIT YAML** tab on the right-hand edge of the screen to expand the YAML editor.

The YAML editor allows the Custom Resource Definition (CRD) of the Virtual Server to be edited directly, offering a high level of both flexible customization and transparency. The CRD's YAML may also be copied from here for future programmatic deployments using the CLI.

<figure><img src="../../docs/.gitbook/assets/image (72).png" alt="Screenshot demonstrating that the YAML editor button is on the right-hand side of the screen"><figcaption><p>The View/Hide YAML tab is located on the right-hand side of the screen</p></figcaption></figure>

### Deploy the Virtual Server

When you are ready to launch your new Virtual Server, click the **Deploy Now** button.

## Cloud UI tools

### Virtual Server status page

Once your Virtual Server has begun deploying, you will be automatically redirected to the **status page**. From here, the Virtual Server can be stopped (shut down), restarted, edited, [cloned](coreweave-apps.md#templates-and-clones), used as a [template](coreweave-apps.md#templates-and-clones), or deleted.

Click the new Virtual Server to expand its menu for more information and to see all options.

<figure><img src="../../docs/.gitbook/assets/image (67).png" alt=""><figcaption></figcaption></figure>

### Virtual terminal

Additionally featured on the status page is a **virtual terminal**, allowing immediate access to the Virtual Server once it is in a ready state through a VNC terminal. To open the virtual terminal, click the **Terminal** button in the Virtual Server's expanded menu, or click the ellipses on the right hand side of its name.

{% hint style="info" %}
**Note**

For Virtual Servers running **Windows**, it may take time to install and upgrade the OS. Additionally, the Web-based terminal is not supported by Virtual Servers utilizing **custom EDID.**
{% endhint %}

Clicking the **Upgrade** button will bring you back to the Hardware Selection page shown above. From there, you can change options such as GPU type, CPU core amounts, root disk size, and so on.

### Events

A basic diagnostic log of all actions involving the Virtual Server are recorded in a list, viewed by clicking the **Events** button.

{% hint style="info" %}
**Note**

The events listed under **Events** are short-lived, so should mostly be used for diagnostic purposes or for tracing the status of the Virtual Server.
{% endhint %}

<figure><img src="../../docs/.gitbook/assets/image (48).png" alt="Screenshot of the events list"><figcaption></figcaption></figure>
