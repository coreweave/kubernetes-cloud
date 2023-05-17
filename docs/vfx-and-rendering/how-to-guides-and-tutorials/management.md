---
description: Remotely manage CoreWeave Cloud Studios
---

# Manage Cloud Studios

{% hint style="info" %}
**Note**

Other management strategies are forthcoming to this guide.
{% endhint %}

If Teradici is in use, the recommended management method is to use [Leostream](https://leostream.com/) in combination with the [Teradici PCoIP Connection Manager and Security Gateway](http://www.teradici.com/web-help/pcoip\_connection\_manager\_security\_gateway/19.08/). The Teradici Security Gateway and Connection Manager allows for centralized provisioning and connection brokering through a common gateway, while Leostream integrates Active Directory credentials to dynamically assign machines to users.

Leostream works by running a broker on one machine, then running agents on participating machines.

## Create the Leostream broker

First, create the machine on which to run Leostream.

[Create a new Virtual Server](broken-reference) running CentOS 7. For this example, a machine is provisioned with `8` vCPU cores and `32Gi` of memory, with no GPU.

Configure a direct attach IP address, then deploy the machine. Once the machine is instantiated, use SSH to connect to the instance, then install Leostream.

### Install Leostream

Update packages using `yum`.

```bash
$ sudo yum update
```

Download the Leostream binary.

```bash
$ curl http://downloads.leostream.com/broker.prod.sh
```

Run the binary.

```bash
$ sudo ./broker.prod.sh
```

Begin the Leostream service.

```bash
$ service leostream start
```

This `start` command starts the Leostream connection broker, which then begins looking for incoming connections. When prompted, input the directly attached IP address that was configured for the Virtual Server acting as the connection broker. This should open the Leostream login page where licensing is set up. Log in using the default administrator credentials `admin:leo`.

{% hint style="info" %}
**Additional Resources**

For more instructions on installing and configuring the Leostream broker, see [Installing the Connection Broker](https://support.leostream.com/support/solutions/articles/66000480276-installing-from-the-leostream-repository).
{% endhint %}

### Configure the broker

From the Leostream admin dashboard, navigate to **Configuration --> Protocol Plans**. From here, create a protocol plan that prioritizes **Teradici PCoIP**.

If Active Directory is in use, navigate to **Setup --> Authentication Servers**, then enter the details for your domain controller.

### Connect agent machines to the broker

To connect Teradici machines to the broker machine using Linux, use Teradici to open a command line, as the commands will open GUI pages. When prompted to configure the connection broker, input the IP address of [the connection broker](management.md#create-the-leostream-machine) machine. The process described below will need to be performed on each agent machine.

Update packages using `yum`.

```bash
$ sudo yum update
```

Install the required Java package.

```bash
$ sudo yum install LibXScrnSaver java-1.7.0-openjdk.x86_64.
```

Download the Leostream agent.

```bash
$ wget https://s3.amazonaws.com/downloads.leostream.com/LeostreamAgentJava-5.2.6.0.jar
```

Run the Java `jar` file to install the agent.

```bash
$ sudo java -jar ./LeostreamAgentJava-5.2.6.0.jar
```

### Install the connection manager

Finally, to finish the management interface, install the Teradici Security Gateway and Connection Manager from CoreWeave's[ Applications Catalog](https://apps.coreweave.com) by searching for **Teradici Connection Manager**. In the deployment screen, specify the connection broker's IP address when prompted. Then click the **Deploy** button.

Once deployed, users should be able to connect directly to the connection manager to have their session properly routed.
