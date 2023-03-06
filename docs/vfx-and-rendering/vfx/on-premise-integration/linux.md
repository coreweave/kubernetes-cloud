---
description: Install CloudLink on a Linux server
---

# CoreWeave CloudLink on Linux

[CoreWeave CloudLink](./#coreweave-cloudlink) can be run on any Linux server or Virtual Machine capable of running [Docker Containers](https://www.docker.com). The following guide will walk through how to install CloudLink on any such Linux system.

This guide will also explain how to expose both **Windows File Sharing (SMB/CIFS)** and **NFS** to CoreWeave. You are likely already using one of the two, and will want to expose whichever protocol you are currently using.

{% hint style="info" %}
**Note**

Depending on storage system, CIFS can sometimes provide better performance than NFS.
{% endhint %}

## Prerequisites

* A Linux server or Virtual Machine on a modern CPU with at least 2 cores and 256MB of RAM available
* Good network connectivity to existing storage infrastructure
* Good connectivity to the Internet

## Setup

### Install CloudLink on CoreWeave Cloud

First, [log in to your CoreWeave Cloud account](https://cloud.coreweave.com), then navigate to [the applications Catalog](https://apps.coreweave.com/) on CoreWeave Cloud. Search for `CloudLink`, then select the CloudLink application. Deploy the CloudLink Server into your CoreWeave namespace by clicking the **Deploy** button in the upper right-hand corner.

{% hint style="info" %}
&#x20;**Note**

It is likely that your CoreWeave specialist has already done this for you, in which case, this step can be skipped.
{% endhint %}

The server status screen shown after deployment will provide you with the CloudLink server's IP, which you will need later for use with docker-compose.

### Install services with docker-compose

Unless Docker is already installed, install it now by running the following one-line install command:

```bash
$ curl -fsSL https://get.docker.com | sh
```

Unless docker-compose is already installed, install it now by running the following commands:

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose 
```

Using a text editor of your choice, such as Nano or Vi, copy and paste the template below and into a new file named `docker-compose.yml`:

{% code title="docker-compose.yml" %}
```yaml
version: '2.2'
services:
  cloudlink-client:
    image: coreweave/cloud-link:0.0.8
    environment:
    - FRP_SERVER=cloudlink-server.example.coreweave.cloud
    - FILE_SERVER=127.0.0.1
    - DEADLINE_WEBSERVICE=127.0.0.1
    - DEADLINE_WEBSERVICE_PORT=8082
    - DEADLINE_RCS=127.0.0.1
    - DEADLINE_RCS_PORT=4433
    restart: always
    network_mode: host
    privileged: true
```
{% endcode %}

| Variable              | Description                                                                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `FRP_SERVER`          | CoreWeave CloudLink Server IP                                                                                                                    |
| `FILE_SERVER`         | NFS/SMB/CIFS File Server. This is only `127.0.0.1` (localhost) if CloudLink is running on the same system and acting as file server for the host |
| `DEADLINE_WEBSERVICE` | If running the Deadline Repository locally, this is the IP address of the server running the Deadline Web service                                |
| `DEADLINE_RCS`        | If running the Deadline Repository locally, this is the IP address of the server running Deadline RCS                                            |

To launch all of these services, invoke `docker-compose up -d` in the directory containing the `docker-compose.yml` file.

To ensure all deployed containers are running correctly, run `docker ps`. You should see `coreweave/cloud-link:0.0.3` listed. If the `STATUS` column simply lists an up time with no restarts, then CloudLink is running correctly.

{% hint style="warning" %}
**Important**

If the container is restarting, it means that the CoreWeave CloudLink server cannot be reached. Validate the `FRP_SERVER` environment variable and that outbound connections on port `7000` to that IP address is allowed in your firewall.

[Contact your CoreWeave Support Specialist to test file access and finish setup.](https://cloud.coreweave.com/contact)

There may be some additional considerations which you may want to take into account, such as:

* Ensuring that NFS exports from your NFS file server are set to insecure to allow non-privileged source ports
* Ensuring NFS allows the connection from the server or VM running CloudLink
{% endhint %}

**If using** **Windows File Sharing (SMB/CIFS):**&#x20;

* Ensure that a specific User Account has been created for CoreWeave.
* Provide the username and password to your CoreWeave Support Specialist.
* Give this User Account permissions on all Shared Folders that should be accessible from CoreWeave Cloud.
* Take note of the share names, and provide them to your CoreWeave Support Specialist.
