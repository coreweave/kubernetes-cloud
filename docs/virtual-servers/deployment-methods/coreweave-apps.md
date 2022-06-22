# CoreWeave Apps Web UI

**Objective:** Deploy a [Virtual Server](../getting-started.md) via the CoreWeave Cloud Web interface.\
**Overview:** [CoreWeave Apps](https://apps.coreweave.com) provides a responsive, user-friendly UI to access our wide [array of compute](https://www.coreweave.com/pricing). In this guide, we'll cover deploying, modifying and accessing Virtual Servers on the web.

## Accessing the Cloud UI

To access CoreWeave Apps, navigate to [https://cloud.coreweave.com/](https://cloud.coreweave.com) and get signed in:

![CoreWeave Cloud Login](<../../.gitbook/assets/image (43).png>)

{% hint style="info" %}
To get your own sign-in, reach out to [request an account](https://cloud.coreweave.com/request-account).
{% endhint %}

You'll be greeted with the Cloud dashboard pictured below. To launch a Virtual Server, select the "Launch a VM" link:

![CoreWeave Cloud Dashboard](<../../.gitbook/assets/image (44).png>)

You'll be taken to our Virtual Server deployment chart, where you can configure a VM to your desired specification:

![Virtual Server deployment chart](<../../.gitbook/assets/image (45).png>)

## Configuring a VM with the Virtual Server deployment Chart

Configure your instance name - this will also serve as your Operating System hostname.

![Instance name](<../../.gitbook/assets/image (46).png>)

Configure your Geographic Location - this is the datacenter your Virtual Server will be hosted out of.

![Region selector](<../../.gitbook/assets/image (47).png>)

{% hint style="info" %}
If you're attaching an existing storage volume, the datacenter location should match.
{% endhint %}

Configure your Operating System image + additions, and root disk size

![Operating system image](<../../.gitbook/assets/image (48).png>)

{% hint style="info" %}
Root disk storage size can be increased later, and the operating system will automatically expand to accommodate. Disk storage size _cannot_ be reduced, however
{% endhint %}

Configure your desired GPU type/count, CPU count, and RAM.

![](<../../.gitbook/assets/image (57).png>)

{% hint style="info" %}
CPU classes can only be specified in a CPU only instance. GPU nodes are pre-configured with frequency optimized CPUs.
{% endhint %}

Configure a Public IP for your Virtual Server.

![Public IP Selector](<../../.gitbook/assets/image (51).png>)

{% hint style="info" %}
If the Virtual Server will only be accessed from within your namespace, or you're using a remote access tool like [Parsec](https://parsec.app), you may not need a Public facing IP address.
{% endhint %}

Configure the desired User Account information to login to the Virtual Server

![Account information](<../../.gitbook/assets/image (52).png>)

### Viewing your configured Virtual Server Manifest

Note that all the options you've selected are viewable in the `YAML` tab, which allows you to store and re-use your configuration for subsequent Virtual Servers, either via the Web UI or via [CLI](kubectl.md). Additional configuration options are also exposed in the `YAML`:

![YAML](<../../.gitbook/assets/image (53).png>)

## Post Deployment

Once your Virtual Server has been deployed, you'll be taken to a status page:

![Virtual Server Status Page](<../../.gitbook/assets/image (54).png>)

From within the status page, you can start, stop, or restart your Virtual Server:

![Control Virtual Server State](<../../.gitbook/assets/image (55).png>)

{% hint style="info" %}
Selecting "Upgrade" will bring you back to the Hardware Selection page shown above, where you can change options like GPU type, CPU cores, root disk size, etc.
{% endhint %}

Events for these actions are reflected in the table below:

![Events for a newly started Virtual Server](<../../.gitbook/assets/image (56).png>)
