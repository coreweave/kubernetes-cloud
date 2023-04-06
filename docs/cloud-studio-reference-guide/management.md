---
description: Set up management for your CoreWeave VFX Cloud Studio
---

# Management

There are many ways to manage your Cloud Studio Workstations. When using Teradici, the recommended method of Workstation management [Leostream](https://leostream.com/) in combination with the [Teradici PCoIP Connection Manager and Security Gateway](http://www.teradici.com/web-help/pcoip\_connection\_manager\_security\_gateway/19.08/).

The Teradici Security Gateway and Connection Manager allows for centralized provisioning and connection brokering through a common gateway, while Leostream integrates Active Directory credentials to dynamically assign machines to users.

## Setup

First, create a new CentOS-based [Virtual Server](broken-reference). In this example, we will provision a machine with 8 vCPU cores and `32Gi` of memory running CentOS 7 with no GPU. Configure a direct attached IP address, then deploy the machine. Once this machine is instantiated, use SSH to connect to the instance, then install Leostream:

1. Update `yum` packages using `sudo yum update`.
2. Download and run the Leostream binary by running `sudo curl http://downloads.leostream.com/broker.prod.sh | sudo bash`
3. Begin the Leostream service by invoking `service leostream start`.

The `service start` command will start the Leostream connection broker, which will then begin looking for incoming connections. Enter the directly attached IP address configured for your Virtual Server acting as the connection broker. You should see the Leostream login screen. From here, you can set up Leostream licensing. Log in with the default administrator credentials `admin:leo`.

{% hint style="info" %}
**Additional Resources**

For more instructions on installing and configuring the Leostream broker, visit [Leostream's website](https://www.leostream.com/wp-content/uploads/2018/11/installation\_guide.pdf).
{% endhint %}

Once your connection broker is installed, log in to configure the broker. Navigate to **Configuration --> Protocol Plans**. From here, create a protocol plan that prioritizes Teradici PCoIP. Additionally, if you are utilizing Active Directory, navigate to **Setup --> Authentication Servers**, and enter the details for your domain controller.

Once the connection broker is running, the next step is to connect the Teradici machines to your broker.

To do this on Linux, use SSH or Teradici to open the command line. Once authenticated, run the following commands to install the Teradici Agent.

{% hint style="info" %}
**Note**

These commands will launch a GUI installer, so be prepared to connect via Teradici. When prompted to configure the connection broker, input the IP address of the connection broker Virtual Server created earlier.
{% endhint %}

1. Update `yum` packages using `sudo yum update`.
2. Install the required Java package using `sudo yum install LibXScrnSaver java-1.7.0-openjdk.x86_64`.
3. Download the Leostream agent using `wget https://s3.amazonaws.com/downloads.leostream.com/LeostreamAgentJava-5.2.6.0.jar`.
4. Run the Java `jar` using `sudo java -jar ./LeostreamAgentJava-5.2.6.0.jar`.

Finally, to finish the management interface, install the Teradici Security Gateway and Connection Manager. This can be installed from [the applications Catalogue](https://apps.coreweave.com) by searching for **Teradici Connection Manager**. In the deployment interface, specify the connection broker IP address.

Once deployed, users should be able to connect directly to the connection manager and have their session properly routed.
