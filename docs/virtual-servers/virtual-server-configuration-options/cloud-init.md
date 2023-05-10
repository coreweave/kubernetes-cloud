---
description: Learn more about CloudInit for Virtual Servers.
---

# Cloud-init

[Cloud-init](https://cloudinit.readthedocs.io/en/latest/) is a tool used to configure aspects of Virtual Servers at the time of instance boot. At that time, cloud-init will identify where it is running (in this case, CoreWeave Cloud), will read any provided metadata from the cloud environment, and then initialize the system on which it is running according to that metadata.

Cloud-init is frequently used to do things like:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f511">🔑</span> Automatically configure SSH access keys</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f5c4">🗄</span> Set up storage or network devices</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f9d1">🧑</span> Configure additional user accounts</td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4dc">📜</span> Run custom scripts on system initialization</td><td></td><td></td></tr></tbody></table>

Any parameters given to cloud-init through the implementation options below will use the standard cloud-init configurations.

{% hint style="info" %}
**Additional Resources**

See [the cloud-init website](https://cloudinit.readthedocs.io/en/latest/topics/examples.html) for examples of cloud-init, and for usage reference.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

Cloud-init configuration options must be configured in the YAML editor. All cloud-init configuration options are held within the `cloudInit` stanza:

```yaml
cloudInit: |
  write_files:
  - content: |
    #!/bin/bash
    echo "Hello world!"
    path: /home/myuser/script.sh
    permissions: `0744`
    owner: myuser:myuser
    package_update: true
    packages:
      - curl
      - git
    runcmd:
      - [df, -h]
      - [git, version]
      - [curl, --version]
      - [bash, /home/myuser/script.sh]
```

In the example above, cloud-init is configured to create a file with a simple script that prints the string `Hello world!`. It's given a permission mask of `0744`, and is owned by `myuser`.

Additionally, a package `update` command will be run on the machine. Then, the `curl` and `git` packages will be installed on the machine.

Lastly, the system will run the commands given under the `runcmd` list:

1. First, the amount of free disk space will be printed in human-readable format (`df -h`).
2. Then, the version of `git` installed on the system earlier will be output (`git version`).&#x20;
3. Similarly, the version of `curl` installed on the system will be printed (`curl --version`).
4. Finally, the script created at the top of the block under `write_files` will be passed to bash to run (`bash /home/myuser/script.sh`).
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

[Cloud-init](https://cloudinit.readthedocs.io/en/latest/) parameters are configured for Virtual Servers using the `cloudInit` field.

| `cloudInit` | String | Define [cloud-init](https://cloudinit.readthedocs.io/en/latest/) parameter |
| ----------- | ------ | -------------------------------------------------------------------------- |

```yaml
  cloudInit: |
    # Write a simple script that outputs "Hello world!"
    write_files:
    - content: |
        #!/bin/bash
        echo "Hello world!"
      path: /home/myuser/script.sh
      permissions: '0744'
      owner: myuser:myuser
    # Update packages
    package_update: true
    # Install curl and git packages
    packages:
      - curl
      - git
    # Run additional commands
    runcmd:
      - [df, -h]
      - [git, version]
      - [curl, --version ]
      - [bash, /home/myuser/script.sh]
```

In the example given above, cloud-init is given a few parameters, which accomplish the following:

1. First, the amount of free disk space will be printed in human-readable format (`df -h`).
2. Then, the version of `git` installed on the system earlier will be output (`git version`).&#x20;
3. Similarly, the version of `curl` installed on the system will be printed (`curl --version`).
4. Finally, the script created at the top of the block under `write_files` will be passed to bash to run (`bash /home/myuser/script.sh`).
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**

It is not currently natively possible to configure Cloud-init settings natively via the Terraform module. This setting may be configured in conjunction with use of the [Cloud UI](cloud-init.md#cloud-ui) or the [Kubernetes CLI](cloud-init.md#cli), or Cloud-init may be used independently of the CoreWeave Terraform module.

Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
