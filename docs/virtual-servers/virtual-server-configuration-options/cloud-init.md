---
description: Learn more about CloudInit for Virtual Servers.
---

# Cloud-init

[Cloud-init](https://cloudinit.readthedocs.io/en/latest/) is a tool used to configure aspects of Virtual Servers at the time of instance boot. At that time, cloud-init will identify where it is running (in this case, CoreWeave Cloud), will read any provided metadata from the cloud environment, and then initialize the system on which it is running according to that metadata.

Some examples of what cloud-init is used for are:

* automatically configuring SSH access keys
* setting up storage or network devices
* configuring additional user accounts
* running custom scripts at system initialization

Any parameters given to cloud-init through the implementation options below will use the standard cloud-init configurations.

{% hint style="info" %}
**Additional Resources**

See [the cloud-init website](https://cloudinit.readthedocs.io/en/latest/topics/examples.html) for examples of cloud-init, and for usage reference.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>\


Cloud-init configuration options must be configured in the YAML manifest, shown under the YAML tab on the Virtual Server creation screen.

The `cloudInit` block holds all the cloud-init configuration options.



**Example**

In this example, cloud-init is configured to create a file with a simple script that prints "Hello world!". It will be given the permission mask of `0744`, and owned by `myuser`.

Additionally, a package update command will be run on the machine, and the `curl` and `git` packages will be installed on the machine.

Lastly, the system will run the commands shown under `runcmd` to list out the amount of free disk space in human-readable format (`df -h`), the version of git installed on the system (`git version`), the version of `curl` installed on the system (`curl --version`), and finally, the script created at the top of the block under `write_files` will be passed to bash to run (`bash /home/myuser/script.sh`).



![An example Cloud-init configuration, as shown in the YAML tab on the Cloud UI](<../../.gitbook/assets/image (95).png>)



The example above in plaintext:

```
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
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

[Cloud-init](https://cloudinit.readthedocs.io/en/latest/) parameters are configured for Virtual Servers using the `cloudInit` field.



| cloudInit | String | Define [cloud-init](https://cloudinit.readthedocs.io/en/latest/) parameter |
| --------- | ------ | -------------------------------------------------------------------------- |

#### **Example**

In the example given below, cloud-init is given a few parameters to:

* write an in-line script that prints `"Hello world!"`
* updates packages on the server
* installs `curl` and `git`
* runs additional commands (such as `df -h`)

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
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\


{% hint style="info" %}
**Note**

It is not currently natively possible to configure Cloud-init settings natively via the Terraform module. This setting may be configured in conjunction with use of the [Cloud UI](cloud-init.md#cloud-ui) or the [Kubernetes CLI](cloud-init.md#cli), or Cloud-init may be used independently of the CoreWeave Terraform module. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
