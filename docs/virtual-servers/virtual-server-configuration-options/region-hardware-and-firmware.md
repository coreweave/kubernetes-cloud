---
description: Select the data center region, hardware, and firmware for a Virtual Server
---

# Region, Hardware and Firmware

## Region

Virtual Servers may be deployed across any of data center regions. CoreWeave's [data center regions](../../data-center-regions.md) are broken up into three geographical buckets - **US East**, **Central** and **West.** Each provides redundant 200Gbps+ public Internet connectivity from Tier 1 global carriers, and are connected to each other using 400Gbps+ of dark fiber transport to allow for easy, free transfers of data within CoreWeave Cloud.

{% hint style="info" %}
**Note**

It is generally advised to select the data center region closest to your location.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, click the **Region** expandable, then select the region in which to host the Virtual Server by clicking on it.

<figure><img src="../../.gitbook/assets/image (86).png" alt="Screenshot of region selector"><figcaption></figcaption></figure>
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Selecting a region for your Virtual Server is simple using the **Kubernetes manifest file**.

The data center region you'd like to use is configured by setting its label under the `region` selector in the `spec` section of the manifest.

### Data center region configuration options

| Variable name | Variable type | Description                                                                    | Default value |
| ------------- | ------------- | ------------------------------------------------------------------------------ | ------------- |
| `region`      | String        | The label of the data center in which you'd like to deploy the Virtual Server. | `3`           |

In the example below, the Chicago (`ORD1`) data center is chosen under `spec.region`.

```yaml
---
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-ubuntu2004-block-pvc
spec:
  region: ORD1
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

The data center region for the Virtual Server can be defined in the `vs_region` variable in your `variables.tf` file.

### Data center region configuration options

| Variable name | Variable type | Description                                                   | Default value    |
| ------------- | ------------- | ------------------------------------------------------------- | ---------------- |
| `vs_region`   | String        | The data center region in which to deploy the Virtual Server. | `ORD1` (Chicago) |

Terraform example:

```json
variable "vs_region" {
  description = "Region default from vs_regions map"
  default     = "ORD1"
}
```
{% endtab %}
{% endtabs %}

## Hardware

CoreWeave Cloud offers [several high-performance NVIDIA GPUs and CPUs](../../../resources/resource-based-pricing.md) for Virtual Servers. The amount of memory with which a Virtual Server runs can also be specified.

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, click the **Hardware** expandable, then select the hardware kind (GPU or CPU) and the hardware itself. Clicking the GPU tab will display all available GPU options, and clicking the CPU tab will do the same for CPU types.

{% hint style="info" %}
**Note**

For more information on hardware, see [Node Types](../../../coreweave-kubernetes/node-types.md).
{% endhint %}

The **GPU Count**, **Core Count**, and **Memory** amount (in `Gi`) are chosen using the sliders at the bottom of the section.

<figure><img src="../../.gitbook/assets/image (51).png" alt="Screenshot of the Virtual Server hardware configuration menu"><figcaption></figcaption></figure>

Each hardware selector also displays a meter registering the availability of that hardware type per region.

### Resource definition (YAML only)

In the CRD's YAML manifest, the `.spec.resources.definition` field is used as a way to describe the chosen resources. The default value of this field is `a` - this is just a placeholder, which can be changed to any string.

<figure><img src="../../.gitbook/assets/image (3) (4).png" alt="Screenshot of the .spec.resources.definition field, mirrored in plain text below"><figcaption></figcaption></figure>

Example in plain text:

```yaml
  spec:
    region: LAS1
    resources:
      cpu:
        count: 4
        type: amd-epyc-milan
      definition: a
      memory: 12Gi
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Using the Kubernetes CLI deployment method, hardware options are configured under the `resources` block in the Virtual Server manifest (e.g., `virtual-server.yaml`).

In this method, **hardware designations are defined as a kind of `resource`**, just like **CPU type, CPU core count, GPU count,** and **memory**.

#### Hardware and resource configuration options

Each of the following fields will be configured underneath the `resources` block in the YAML manifest.

| Field name             | Type   | Description                                                                                       |
| ---------------------- | ------ | ------------------------------------------------------------------------------------------------- |
| `resources`            | Array  | <p>The top-level field.<br>Defines the resources and devices allocated to the Virtual Server.</p> |
| `resources.definition` | String | The resource definition. Defaults to `a`.                                                         |
| `resources.cpu`        | Array  | All CPU configuration fields.                                                                     |
| `resources.cpu.type`   | String | The type of CPU to allocate.                                                                      |
| `resources.cpu.count`  | Int    | The number of CPU cores to allocate.                                                              |
| `resources.gpu`        | Array  | All GPU configuration fields.                                                                     |
| `resources.gpu.type`   | String | The type of GPU to allocate.                                                                      |
| `resources.gpu.count`  | Int    | The number of GPU units to allocate.                                                              |
| `resources.memory`     | String | The amount of memory to allocate.                                                                 |

**Example**

```yaml
  resources:
    gpu:
      type: Quadro_RTX_4000
      count: 1
    cpu:
      count: 4
    memory: 16Gi
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

The Virtual Server's hardware and resource options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).

#### Hardware and resource configuration options

The following table describes the variables usable for Virtual Server configuration, as well as whether or not the module defines any default values for them.

| Variable name   | Variable type | Description                                                                                                                                                                                                                        | Default value     |
| --------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `vs_cpu_count`  | Integer       | <p>Number of CPUs requested.</p><p><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span> <strong>This option cannot be used if <code>vs_gpu_enable</code> is set to <code>true</code>.</strong></p>               | `3`               |
| `vs_gpu_enable` | Boolean       | Enable GPU (or not) for this Virtual Server.                                                                                                                                                                                       | `true`            |
| `vs_gpu`        | String        | <p>The name of the GPU model to be used for the Virtual Server.<br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span> <strong>Required if <code>vs_gpu_enable</code> is set to <code>true</code>.</strong></p> | `Quadro_RTX_4000` |
| `vs_gpu_count`  | Integer       | <p>Number of GPUs requested for the Virtual Server.<br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span> <strong>Required if <code>vs_gpu_enable</code> is set to <code>true</code>.</strong></p>             | `1`               |
| `vs_memory`     | String        | Memory specified for the Virtual Server, in Gi (eg. `16Gi`).                                                                                                                                                                       | `16Gi`            |

\
**Example**

```json
variable "vs_memory" {
  description = "Virtual Server RAM"
  default     = "16Gi"
}

variable "vs_root_storage" {
  description = "Virtual Server root device storage (i.e 80Gi)"
  default     = "80Gi"
}

variable "vs_os_type" {
  default = "linux"
}

variable "vs_image" {
  description = "OS image"
  default     = "ubuntu2004-docker-master-20210601-ord1"
}

variable "vs_gpu" {
  description = "GPU"
  default     = "Quadro_RTX_4000"
}

variable "vs_gpu_enable" {
  default = true
}

variable "vs_cpu_count" {
  default = 3
}

variable "vs_gpu_count" {
  default = 1
}
```
{% endtab %}
{% endtabs %}

## Firmware

Firmware identification information for Virtual Servers is set by the Virtual Machine Instance (VMI). The firmware's UUID (MAC address) is set by the BIOS, and its system-serial number is set by the VMI's SMBIOS.

The firmware's UUID defaults a randomly-generated alphanumeric string. Both numbers are static across Virtual Server restarts.

It is optional to set these; if not set, they will have randomly-generated defaults.

{% hint style="info" %}
**Note**

You can read more about virtual hardware firmware configuration in [the Kubevirt documentation](https://kubevirt.io/user-guide/virtual\_machines/virtual\_hardware/#smbios-firmware), or see how its exposure is implemented in CoreWeave by viewing our [API reference](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1#VirtualServer.SetFirmwareSerial).
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

In the Cloud UI, firmware options must be set using the YAML editor. Firmware options are not currently exposed through the YAML manifest by default, so they must be added to the key-value map in the manifest.

Example in plain text:

```yaml
firmware:
  uuid: 5d307ca9-b3ef-428c-8861-06e72d69f223
  serial: e4686d2c-6e8d-4335-b8fd-81bee22f4815
```
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Firmware options for Virtual Servers are configured under the `firmware` stanza.

| Field name                           | Field type | Description                                                       |
| ------------------------------------ | ---------- | ----------------------------------------------------------------- |
| <p><code>firmware</code><br><br></p> | Array      | Top-level field for firmware definitions                          |
| `firmware.uuid`                      | String     | The UUID of the firmware to be deployed                           |
| `firmware.serial`                    | String     | The system-serial-number in SMBIOS of the firmware to be deployed |

Example in plain text:

```yaml
  firmware:
    uuid: 906820cf-53b7-45d6-9a6e-1c389cb81016
    serial: 5cc667ec-0bba-4011-af9e-05659c64d061
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**

It is not currently natively possible to configure firmware when using Terraform as the deployment method. This setting may be configured in conjunction with use of the Cloud UI or the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
