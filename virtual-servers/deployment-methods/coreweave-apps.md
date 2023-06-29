---
description: Deploy Virtual Servers via the Cloud UI
---

# CoreWeave Cloud UI

The [CoreWeave Cloud UI](https://apps.coreweave.com/) is a responsive, Web-based dashboard enabling users to configure, deploy, and manage Virtual Servers.

## Prerequisites

This guide presumes you have [an active CoreWeave Cloud account](../../docs/welcome-to-coreweave/getting-started.md#create-an-account). Once you have an active account, log in to the Cloud UI dashboard at [`https://cloud.coreweave.com`](https://cloud.coreweave.com).

## Create a Virtual Server

From the CoreWeave Cloud main dashboard, either navigate to the **Virtual Servers** menu in the left-hand navigation, or click the **Deploy Now** button in the **Deploy Virtual Server** box in the center of the page.

<figure><img src="../../docs/.gitbook/assets/image (21).png" alt="Screenshot of the Virtual Server link in both places"><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

The [**CoreWeave Cloud**](https://cloud.coreweave.com/virtualservers) Virtual Server has more features than the [**CoreWeave Apps**](https://apps.coreweave.com) edition, but you can use either one. You may see a selection screen like this when deploying.

![Deploy a Virtual Server](<../../docs/.gitbook/assets/image (17) (5).png>)&#x20;

These instructions are for **CoreWeave Cloud** Virtual Server.
{% endhint %}

The Virtual Server hub is where all existing Virtual Servers are listed. From here, you can manage current Virtual Servers, or create a new one.&#x20;

To create a new Virtual Server, click the **New Virtual Server** button.

<figure><img src="../../docs/.gitbook/assets/image (59).png" alt="Screenshot of the Virtual Server menu"><figcaption><p>Deploy a Virtual Server</p></figcaption></figure>

## Deployment options

The Virtual Server hub has several deployment options. Choose the option that best suits your use-case.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th></tr></thead><tbody><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f9d1-1f373">🧑🍳</span> <a href="coreweave-apps.md#new-server-1">New server</a></h3></td><td>A <strong>new</strong> deployment selects all settings from scratch to build a custom-configured Virtual Server.</td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f46d">👭</span> <a href="coreweave-apps.md#clone-an-existing-server-1"><strong>Clone an existing server</strong></a></h3></td><td>A <strong>clone</strong> deployment takes a complete snapshot of an existing Virtual Server's configuration, and all files.</td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f4dd">📝</span> <a href="coreweave-apps.md#deploy-from-a-template-1">Deploy from a t<strong>emplate</strong></a></h3></td><td>A <strong>template</strong> deployment copies the configuration from an existing Virtual Server, but doesn't copy the state or data.</td></tr><tr><td><h3><span data-gb-custom-inline data-tag="emoji" data-code="1f4c0">📀</span> <a href="coreweave-apps.md#deploy-custom-with-pvc-1">Deploy c<strong>ustom</strong></a></h3></td><td>A <strong>custom</strong> deployment loads the OS image from an existing PVC or a remote HTTP source.</td></tr></tbody></table>

## :cook: New server

A new Virtual Server is the default option. Choose all the parameters from scratch to build a custom-configured machine tailored to your needs.

The deployment page has two panes: the web UI, and the [Custom Resource Definition (CRD) YAML manifest](coreweave-apps.md#edit-the-crd-manifest-using-the-yaml-editor). Changes made in either pane are reflected in both.

While [configuration options](coreweave-apps.md#configuration-options) can be made in either pane, not all options are exposed in the Web UI. For complete control over the Virtual Server configuration, edit the [YAML](coreweave-apps.md#edit-the-crd-manifest-using-the-yaml-editor) directly. The YAML manifest can be copied from here to use with the CLI, and pasted back to this page in later deployments.&#x20;

When the web editor has focus, sensitive values such as passwords are obscured with asterisks in the YAML editor. Click the YAML pane to give it focus and reveal the sensitive values, or click the **Hide YAML** button between the panes to close the YAML.

<figure><img src="../../docs/.gitbook/assets/image (4) (2).png" alt="New Virtual Server deployment page"><figcaption><p>New Virtual Server deployment page</p></figcaption></figure>

There are three buttons in the upper-right corner of the web UI pane:

<figure><img src="../../docs/.gitbook/assets/image (12) (4).png" alt="Option buttons"><figcaption><p>Option buttons</p></figcaption></figure>

* **Magic wand button:** Revert the form to the last valid configuration.
* **Arrow button:** Reset the form, clearing all fields.
* **Load or clone from existing button:** Deploy a new Virtual Server from a [template](coreweave-apps.md#deploy-from-a-template-1), or [clone](coreweave-apps.md#clone-an-existing-server-1) an existing Virtual Server.

## :two\_women\_holding\_hands:**Clone an existing server**

A clone is a snapshot of an existing Virtual Server, including the PVC containing the OS and all files. Deploying a clone Virtual Server creates an exact duplicate of an existing Virtual Server in its current state.

{% hint style="info" %}
**Note**

Shut down the existing source server before cloning. The deployment page does not allow cloning a running server.&#x20;
{% endhint %}

### Clone from the New Virtual Server form

One way to initiate a clone deployment is to open the New Virtual Server form, as if [deploying from scratch](coreweave-apps.md#new-server-from-scratch-1). Then, click **Load or clone from existing** in the upper-right, which opens the **Select Template** modal.

Select an existing Virtual Server in the drop-down presented. Then toggle the **Clone (use resource as source)** option to create an exact clone of the selected Virtual Server.

<figure><img src="../../docs/.gitbook/assets/image (10) (2).png" alt="Clone server modal"><figcaption><p>Clone server modal</p></figcaption></figure>

### Clone from an existing server entry

Another way to deploy a clone is to select **Clone** from the **more** menu of an existing server. Or, expand the server details and click **Clone**.

<figure><img src="../../docs/.gitbook/assets/image (3) (2).png" alt="Deployment options"><figcaption><p>Deployment options</p></figcaption></figure>

## :pencil: Deploy from a t**emplate**

A template uses an existing Virtual Server as a model. Deploying from a template creates a new Virtual Server with the same configuration as the original, but without the state or a copy of the data.

The steps to deploy as a template are similar to [deploying a clone](coreweave-apps.md#clone-an-existing-server-1), but choose the **Use As Template** option instead. In the Select Template modal, leave the Clone option untoggled:

<figure><img src="../../docs/.gitbook/assets/image (18) (2).png" alt="Leave Clone untoggled to create a template"><figcaption><p>Leave <strong>Clone</strong> untoggled to create a template</p></figcaption></figure>

### Adjusting configuration when using a template

Changing the configuration options before deployment is allowed when using a template. For example, change the Region when deploying from a template to use the same server configuration in a different datacenter.

While this is also possible with cloning, there's less risk of deployment failure when using a template because templates don't copy the source server's files or state.&#x20;

## :dvd: Deploy c**ustom**

A custom deployment loads the operating system image from an existing PVC or a remote HTTP source.

To deploy a custom Virtual Server, follow the same steps as if deploying a [new server from scratch](coreweave-apps.md#new-server-1), then select either **Image From Remote Source**, or **Image From PVC** in the Operating System section.&#x20;

<figure><img src="../../docs/.gitbook/assets/image (8) (1).png" alt="Choose a Custom option"><figcaption><p>Choose a Custom option</p></figcaption></figure>

#### Image from remote source

Supply an OS image over HTTP in `qcow2`, `raw` and `iso` formats, optionally compressed with either `gz` or `xz`.&#x20;

#### Image from PVC

This makes a copy of an existing PVC. This option isn't shown if there aren't any eligible PVC's deployed in your namespace. The PVC can be copied from an existing Virtual Server, or by [importing a disk image](../../docs/virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md).&#x20;

{% hint style="info" %}
**Note**

If copying an existing Virtual Server, make sure to shut down the server before using its PVC as an image.&#x20;
{% endhint %}

## Configuration options

Click any of the specification cards to learn more about each configuration option.

<table data-card-size="large" data-view="cards"><thead><tr><th>Specification</th><th>Description</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md"><strong>Name</strong></a></td><td>The name of the <a href="../getting-started.md">Virtual Server</a></td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md">region-hardware-and-firmware.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware-1.md#region"><strong>Region</strong></a></td><td>The <a href="../../docs/coreweave-kubernetes/data-center-regions.md">data center region</a> in which to deploy the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware-1.md#region">#region</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware-1.md#hardware"><strong>Hardware</strong></a></td><td>The type and number of <a href="../../coreweave-kubernetes/node-types.md">GPUs</a> to allocate to the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware-1.md#hardware">#hardware</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md"><strong>Operating System</strong></a></td><td>The <a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md">Operating System</a> to run on the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md">operating-system-and-root-disk.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md"><strong>Network</strong></a></td><td>Attach a <a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md">Public IP or a LoadBalancer IP</a> to the Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/networking.md">networking.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/storage.md"><strong>Attach Volumes</strong></a></td><td>Attach <a href="../../docs/virtual-servers/virtual-server-configuration-options/storage.md#attach-a-storage-volume">volumes</a> in the same namespace to the Virtual Server</td><td><a href="../../docs/storage/storage/using-storage-cloud-ui.md">using-storage-cloud-ui.md</a></td></tr><tr><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md"><strong>Users</strong></a></td><td>Create <a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md">user accounts</a> on your Virtual Server</td><td><a href="../../docs/virtual-servers/virtual-server-configuration-options/user-accounts.md">user-accounts.md</a></td></tr></tbody></table>

### Edit the CRD manifest using the YAML editor

Not all Virtual Server configuration options are exposed in the Web UI.

For more fine-grained control over the Virtual Server configuration, use the YAML pane on the right side of the screen.

The YAML editor allows the Custom Resource Definition (CRD) of the Virtual Server to be edited directly, offering a high level of both flexible customization and transparency. The CRD's YAML may also be copied from here for future programmatic deployments using the CLI.

<figure><img src="../../docs/.gitbook/assets/image (72).png" alt="Screenshot demonstrating that the YAML editor button is on the right-hand side of the screen"><figcaption><p>The View/Hide YAML tab is located on the right-hand side of the screen</p></figcaption></figure>

### Deploy the Virtual Server

When you are ready to launch your new Virtual Server, click the **Deploy Now** button.

## Cloud UI tools

### Virtual Server status page

Once your Virtual Server has begun deploying, you will be automatically redirected to the **status page**. From here, the Virtual Server can be stopped (shut down), restarted, edited, [cloned](coreweave-apps.md#clone-an-existing-server-1), used as a [template](coreweave-apps.md#deploy-from-a-template-1), or deleted.

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
