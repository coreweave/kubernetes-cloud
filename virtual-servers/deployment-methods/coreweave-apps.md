---
description: >-
  Learn more about deploying VirtualServers onto CoreWeave Cloud via the
  CoreWeave Cloud UI.
---

# CoreWeave Cloud UI

The [CoreWeave Cloud UI](https://apps.coreweave.com/) is a responsive, Web-based dashboard enabling users to configure, deploy, and manage Virtual Servers using visual methods to deploy Virtual Servers.

![The CoreWeave Cloud UI dashboar](<../../docs/.gitbook/assets/image (75).png>)

## Getting Started

### [Request an account on CoreWeave Cloud](https://cloud.coreweave.com/request-account)

**Before you can access the CoreWeave Cloud UI, you must first** [**request an account**](https://cloud.coreweave.com/request-account)**.**

The CoreWeave team will respond to your request **within** **24 hours** of account creation request submission to assist you.

Once you have an account and account credentials, log in to the dashboard from the sign-in page at [**https://cloud.coreweave.com**](https://cloud.coreweave.com).

{% hint style="info" %}
**Note**

See [Obtain Access Credentials](../../docs/coreweave-kubernetes/getting-started/#obtain-access-credentials) for more information.
{% endhint %}

![The CoreWeave Cloud UI sign-in page](<../../docs/.gitbook/assets/image (78).png>)

## Create a Virtual Server

![The CoreWeave Cloud UI dashboard](<../../docs/.gitbook/assets/image (79).png>)

Once you've signed in to your CoreWeave Cloud account, the dashboard landing page is the first page you will see. From here, you can **configure, launch, and manage Virtual Servers.**

To launch a new Virtual Server from the Cloud UI dashboard, navigate to the **Virtual Servers** menu option located in the upper left-hand side of the sidebar menu or click the **Deploy Now** button in the card in the top-middle of the dashboard - either option will bring you to the Virtual Server dashboard.

![Virtual Server menu options from the Cloud UI dashboard](<../../docs/.gitbook/assets/image (67).png>)

From the Virtual Servers dashboard, you can configure a Virtual Server to your desired specifications. The Virtual Server configuration screen provides a graphical interface for setting up a Virtual Server. Virtual Servers can be configured, then easily deployed, right from this screen.

{% hint style="info" %}
**Note**

Not every Virtual Server configuration option is exposed through the options displayed graphically on the configuration screen. For more fine-tuned control, or to save the Virtual Server configuration file to replicate additional Virtual Servers, you can view the generated YAML chart under the **YAML** tab.
{% endhint %}

![The Virtual Server configuration screen in the CoreWeave Cloud UI](<../../docs/.gitbook/assets/image (69) (3).png>)

### Configuration

To learn about configure your Virtual Server, see [Virtual Server Configuration Options](../../docs/virtual-servers/virtual-server-configuration-options/).

## Cloud UI tools

Once your Virtual Server has begun deploying, you will be automatically redirected to the **status page**. From here, the Virtual Server can be **restarted**, **upgraded** (or changed), **deleted**, or **stopped**.

![Virtual Server state controls](<../../docs/.gitbook/assets/image (49) (1).png>)

### Virtual terminal

Additionally featured on the status page is a virtual terminal, allowing immediate access to the Virtual Server once it is in a ready state.

{% hint style="info" %}
**Note**

For Virtual Servers running **Windows**, it may take time to install and upgrade the OS. Additionally, the Web-based terminal is not supported by Virtual Servers utilizing **custom EDID.**
{% endhint %}

![Post-deployment status page and terminal, using a Linux-based Virtual Server as an example.](../../docs/.gitbook/assets/vs-statuswithterm.png)

{% hint style="info" %}
**Note**

Clicking the **Upgrade** button will bring you back to the Hardware Selection page shown above. From there, you can change options such as GPU type, CPU core amounts, root disk size, and so on.
{% endhint %}

#### The Virtual Server Helm chart

The configuration fields in the Cloud UI generates a [Helm chart](https://helm.sh/docs/topics/charts/) that defines the Virtual Server's attributes. This chart enables you to utilize the same configuration for additional Virtual Server deployments, and exposes additional options for finer-tuned configuration, and allows you to create additional Virtual Servers, deployed via the Web UI or from the command line.

To view the Virtual Server's generated YAML chart, click on the **YAML** tab below the **Name** field.

{% hint style="info" %}
**Note**

After the server has been deployed, the YAML manifest can be viewed by clicking the **Upgrade** button from the [status page](coreweave-apps.md#the-status-page).
{% endhint %}

![Form, YAML, and Change view tabs within the Virtual Server configuration screen](../../docs/.gitbook/assets/vs-yaml-config.png)

This YAML manifest also exposes additional configurations, which may be adjusted directly.

### Virtual Server events

A basic diagnostic log of all actions involving the Virtual Server will be recorded in a list under the **Events** tab.

{% hint style="info" %}
**Note**

The events listed under the **Events** tab are short-lived, and should mostly be used for diagnostics or simply for tracing the status of the Virtual Server.
{% endhint %}

![Event history for a new Virtual Server](<../../docs/.gitbook/assets/image (50) (1).png>)
