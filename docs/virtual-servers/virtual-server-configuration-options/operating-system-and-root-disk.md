---
description: Learn more about the Operating Systems available for Virtual Servers.
---

# Operating System and Root Disk

CoreWeave Cloud supports a variety of [Linux distributions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/linux-images?q=system+images) and [Windows versions](https://docs.coreweave.com/virtual-servers/coreweave-system-images/windows-images?q=system+images) system images for Virtual Servers.

## Available Operating System versions

Click the OS type tab to see all currently available OS versions.

{% tabs %}
{% tab title="Linux" %}
### Linux

| Name   | Versions            |
| ------ | ------------------- |
| Rocky  | 8                   |
| CentOS | 7                   |
| Ubuntu | 18.04, 20.04, 22.04 |
{% endtab %}

{% tab title="Windows" %}
### Windows

| Name                    | Version |
| ----------------------- | ------- |
| Windows Professional    | 10      |
| Windows Professional    | 11      |
| Windows Server Standard | 2019    |
| Windows Server Standard | 2022    |
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Note**

The size of the Virtual Server's root disk size can be _**increased**_ after initialization, and the operating system will automatically expand to accommodate. However, the root disk size **cannot be reduced** after initial deployment.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, click the **Operating System** expandable.

Select the Operating System you'd like to run (CentOS, Rocky, Ubuntu, or Windows), and a corresponding version. Then, set the **Root Disk Size** using the provided slider.

<figure><img src="../../.gitbook/assets/image (46) (1).png" alt="Screenshot of OS selection menu"><figcaption><p>Linux configuration example</p></figcaption></figure>

You can also configure the size of the **root disk** of the Virtual Server from here using the **Root Disk Size** slider. To add a [system image](../coreweave-system-images/) addition such as NVIDIA Drivers or Teradici, click the slider into the "on" position for each desired add-on.

<figure><img src="../../.gitbook/assets/image (42).png" alt=""><figcaption><p>Windows configuration example</p></figcaption></figure>

### **UEFI bootloader**

If you are using a custom disk image, and need to configure UEFI bootloader options, you must do so from the YAML tab on the configuration screen. This option is configured in the `os.enableUEFIboot` field, which can be set to either `true` or `false`.

<figure><img src="../../.gitbook/assets/image (73).png" alt="" width="491"><figcaption></figcaption></figure>

Example in plaintext:

```yaml
  os:
    definition: a
    enableUEFIBoot: false
    type: linux
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

| Field name          | Type    | Description                                                                                                     |
| ------------------- | ------- | --------------------------------------------------------------------------------------------------------------- |
| `os`                | Array   | Top-level field. Defines the Operating System specifications for the Virtual Server.                            |
| `os.type`           | String  | The Operating System type, whether Linux or Windows.                                                            |
| `os.enableUEFIBoot` | Boolean | <p>Whether or not to enable</p><p>the <a href="https://wiki.ubuntu.com/EFIBootLoaders">UEFI bootloader</a>.</p> |

YAML example:

```yaml
  os:
    type: linux
    enableUEFIBoot: false
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

The Virtual Server's Operating System options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).

{% hint style="info" %}
**Note**

You can find the name of Operating System images (`vs_image`) in [the System Images section](../coreweave-system-images/).
{% endhint %}

#### Operating System and root disk storage configuration options

The table below describes all available configuration options for the Operating System.

| Variable name | Variable type | Description                                                                                 | Default value                                                                                                            |
| ------------- | ------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `vs_os_type`  | String        | The type (Windows or Linux) of Operating System with which to provision the Virtual Server. | `linux`                                                                                                                  |
| `vs_image`    | String        | The name of the image to be used for the Operating System.                                  | <p><code>ubuntu2004-docker-master-20210601-ord1</code> </p><p>(The Ubuntu 20.04 image stored in the Chicago region.)</p> |

{% hint style="info" %}
**Note**

UEFI bootloading options are not currently available through use of this Terraform module.
{% endhint %}

Example in plain text:

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
