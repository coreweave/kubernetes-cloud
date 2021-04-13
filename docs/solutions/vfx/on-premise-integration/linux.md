# Linux

Any Linux server or Virtual Machine that can run [Docker Containers](https://www.docker.com/) can run  [CoreWeave CloudLink](./#cloud-link). 

#### Requirements

* A Linux server or Virtual Machine on a modern CPU with at least two cores and 256MB of RAM available
* Good network connectivity to storage infrastructure
* Good connectivity to the Internet

### Setup

This guide will show you how to expose both **SMB/CIFS \(Windows File Sharing\)** and **NFS** to CoreWeave. You are likely already using one of the two, and will want to expose whichever protocol you are currently using. Depending on storage system, CIFS can sometimes provide better performance than NFS.

1. Deploy the CloudLink Server in your CoreWeave namespace on [Apps](https://apps.coreweave.com). It is likely that your CoreWeave specialist has already done this for you, and this step can be skipped. 
2. Unless you already have Docker installed, install it by running the simple one-line install command 

   ```text
   curl -fsSL https://get.docker.com | sh
   ```

3. Unless already installed, install docker-compose 

   ```text
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose 
   ```

4. Create a file with your editor of choice, such as nano / vi. Use the template below and name the file `docker-compose.yml`. Explanation for each variable that can be set is in the table under the snippet.

{% code title="docker-compose.yml" %}
```yaml
version: '2.2'
services:
  cloudlink-client:
    image: coreweave/cloud-link:0.0.3
    environment:
    - FRP_SERVER=207.53.234.184
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

| Variable | Description |
| :--- | :--- |
| FRP\_SERVER | CoreWeave CloudLink Server IP from Step 1 |
| FILE\_SERVER | NFS/SMB/CIFS File Server. This is only 127.0.0.1 if Cloud Link is running on the same system acting as file server. |
| DEADLINE\_WEBSERVICE | If running the Deadline Repository locally, IP address of the server running the Deadline Webservice |
| DEADLINE\_RCS | If running the Deadline Repository locally, IP address of the server running the Deadline RCS |

