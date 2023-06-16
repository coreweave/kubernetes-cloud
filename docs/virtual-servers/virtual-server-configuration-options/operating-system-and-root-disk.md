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

<table><thead><tr><th width="340">Name</th><th>Versions</th></tr></thead><tbody><tr><td>Rocky</td><td>8</td></tr><tr><td>CentOS</td><td>7</td></tr><tr><td>Ubuntu</td><td>18.04, 20.04, 22.04</td></tr></tbody></table>
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

<figure><img src="../../.gitbook/assets/image (42) (3).png" alt=""><figcaption><p>Windows configuration example</p></figcaption></figure>

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

<table><thead><tr><th>Field name</th><th width="129">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>os</code></td><td>Array</td><td>Top-level field. Defines the Operating System specifications for the Virtual Server.</td></tr><tr><td><code>os.type</code></td><td>String</td><td>The Operating System type, whether Linux or Windows.</td></tr><tr><td><code>os.enableUEFIBoot</code></td><td>Boolean</td><td><p>Whether or not to enable</p><p>the <a href="https://wiki.ubuntu.com/EFIBootLoaders">UEFI bootloader</a>.</p></td></tr></tbody></table>

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

<table><thead><tr><th width="157">Variable name</th><th width="124">Variable type</th><th>Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>vs_os_type</code></td><td>String</td><td>The type (Windows or Linux) of Operating System with which to provision the Virtual Server.</td><td><code>linux</code></td></tr><tr><td><code>vs_image</code></td><td>String</td><td>The name of the image to be used for the Operating System.</td><td><p><code>ubuntu2004-docker-master-20210601-ord1</code> </p><p>(The Ubuntu 20.04 image stored in the Chicago region.)</p></td></tr></tbody></table>

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
