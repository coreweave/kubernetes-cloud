---
description: Learn more about the Operating Systems available for Virtual Servers.
---

# Operating System & Root Disk

CoreWeave Cloud supports a variety of both [Linux distributions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/linux-images?q=system+images) and [Windows versions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/windows-images?q=system+images) system images for Virtual Servers.

{% hint style="info" %}
**Note**

The size of the Virtual Server's root disk size can be _**increased**_ after initialization, and the operating system will automatically expand to accommodate. However, the root disk size **cannot be **_**reduced**_ after initial deployment.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

<mark style="background-color:blue;"></mark>

From the **Operating System / Root Disk Storage** menu, you can select and configure the desired operating system image (CentOS, Ubuntu, or Windows) for the Virtual Server.

You can also configure the size of the **root disk** of the Virtual Server from here using the **Root Disk Size** slider.



![The Operating System and Root Disk Size configuration section.](<../../.gitbook/assets/image (56) (2).png>)



### **UEFI bootloader**

If you are using a custom image, and need to configure UEFI bootloader options for the Virtual Server, you must do so from the YAML tab on the configuration screen.

This option can be configured in the `os.uefi` field in the YAML manifest under the YAML tab.



#### **Example**

![The os.uefi option configured under the YAML tab in the configuration screen.](<../../.gitbook/assets/image (56).png>)



### Operating System add**itions**

See [**System Images**](../coreweave-system-images/) for more information on Teradici, Parsec, and NVIDIA drivers.
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

<mark style="background-color:green;"></mark>

| Field name          | Type    | Description                                                                                                      |
| ------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| `os`                | Array   | Top-level field. Defines the Operating System specifications for the Virtual Server.                             |
| `os.type`           | String  | The Operating System type, whether Linux or Windows.                                                             |
| `os.enableUEFIBoot` | Boolean | <p>Whether or not to enable </p><p>the <a href="https://wiki.ubuntu.com/EFIBootLoaders">UEFI bootloader</a>.</p> |

####

#### Example

```yaml
  os:
    type: linux
    enableUEFIBoot: false
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

<mark style="background-color:orange;"></mark>\ <mark style="background-color:orange;"></mark>The Virtual Server's Operating System options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).



{% hint style="info" %}
**Note**

You can find the name of Operating System images (`vs_image`) in [the System Images section](https://docs.coreweave.com/virtual-servers/coreweave-system-images).
{% endhint %}

###

### Operating System and root disk storage configuration options

The table below describes all available configuration options for the Operating System.



| Variable name | Variable type | Description                                                                                 | Default value                                                                                   |
| ------------- | ------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `vs_os_type`  | String        | The type (Windows or Linux) of Operating System with which to provision the Virtual Server. | `linux`                                                                                         |
| `vs_image`    | String        | The name of the image to be used for the Operating System.                                  | `ubuntu2004-docker-master-20210601-ord1` (The Ubuntu 20.04 image stored in the Chicago region.) |



{% hint style="info" %}
**Note**

UEFI bootloading options are not currently available through use of this Terraform module.
{% endhint %}

****\
**Example**

```json
variable "vs_os_type" {
  default = "linux"
}

variable "vs_image" {
  description = "OS image"
  default     = "ubuntu2004-docker-master-20210601-ord1"
}
```
{% endtab %}
{% endtabs %}
