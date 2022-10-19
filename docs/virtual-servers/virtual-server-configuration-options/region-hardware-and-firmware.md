---
description: >-
  Learn more about the Virtual Server configuration options for data center
  regions.
---

# Region, Hardware & Firmware

## Region

Broken up into three geographical buckets - **US East**, **Central** and **West** - our data centers each have redundant 200Gbps+ public internet connectivity from Tier 1 global carriers, and are connected to each other with 400Gbps+ of dark fiber transport to allow for easy, free transfers of data within CoreWeave Cloud.

Virtual Servers can be deployed across any of [CoreWeave's three data center regions](../../data-center-regions.md). It is generally advisable to select the data center region closest to your location.

{% hint style="info" %}
**Additional Resources**

See [Data Center Regions](https://docs.coreweave.com/data-center-regions) for more information on each data center, and to look up region labels for use in the following configuration methods.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

Selecting the data region for your Virtual Server is easily done by choosing a center from the **Geographic Location** section of the Virtual Server deployment screen.

From the **Geographic Location** menu on the CoreWeave Cloud UI, select the one in which you'd like the Virtual Server to be hosted[.](../../data-center-regions.md)

![Data center region selector in the CoreWeave Cloud UI.](<../../.gitbook/assets/image (110).png>)
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>\ \ Selecting a region for your Virtual Server is simple using the **Kubernetes manifest file**.

The data center region you'd like to use is configured by setting its label under the `region` selector in the `spec` section of the manifest.

#### Data center region configuration options

| Variable name | Variable type | Description                                                                    | Default value |
| ------------- | ------------- | ------------------------------------------------------------------------------ | ------------- |
| `region`      | String        | The label of the data center in which you'd like to deploy the Virtual Server. | `3`           |

**Example**

In this example, the Chicago (`ORD1`) data center is chosen under `spec.region`.

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
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

\ The data center region for the Virtual Server can be defined in the `vs_region` variable in your `variables.tf` file.\\

#### Data center region configuration options

| Variable name | Variable type | Description                                                   | Default value    |
| ------------- | ------------- | ------------------------------------------------------------- | ---------------- |
| `vs_region`   | String        | The data center region in which to deploy the Virtual Server. | `ORD1` (Chicago) |

\
\
**Example**

```json
variable "vs_region" {
  description = "Region default from vs_regions map"
  default     = "ORD1"
}
```
{% endtab %}
{% endtabs %}

## Hardware

CoreWeave Cloud offers [several high-performance NVIDIA GPUs and CPUs](https://docs.coreweave.com/resources/resource-based-pricing#gpu-instance-resource-pricing) for Virtual Servers. The amount of memory with which a Virtual Server runs can also be specified.

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

#### Hardware configuration options

CoreWeave Cloud offers [several high-performance NVIDIA GPUs and CPUs](https://docs.coreweave.com/resources/resource-based-pricing#gpu-instance-resource-pricing) for Virtual Servers. From the **Hardware Selection** menu, you can select and configure which of CoreWeave's CPU and GPU options for the Virtual Server.

![The Hardware Selection menu options for hardware.](<../../.gitbook/assets/image (96).png>)

####

#### Resource configuration options

The Virtual Server's **GPU and CPU resource specifications** are configured just below the hardware selection menu. Here, you can select whether the instance is **GPU-enabled, the GPU count, the CPU core count,** and allocated memory resources.

**CPU**

Select how many **CPU** **cores** you'd like the Virtual Server to have using the **Core Count** slider.

![](<../../.gitbook/assets/image (114).png>)

**GPU**

Select how many **GPUs** you'd like the Virtual Server to have using the **GPU Count** slider.

![](<../../.gitbook/assets/image (52) (1).png>)

**Memory**

Determine the amount of **memory** (in Gebibytes) the Virtual Server will have using the **Memory** slider.

![](<../../.gitbook/assets/image (10) (3).png>)

#### Definition

The resources' `definition` defaults to the `a` character, but can be changed to any descriptive string you'd like. In the Cloud UI, the resource definition string is set in the YAML manifest.

![Screenshot of the resources.definition field.](<../../.gitbook/assets/image (49).png>)

**Example**

```yaml
resources:
  definition: This is a high-intensity compute machine with a lot of GPUs.
```
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Using the Kubernetes CLI deployment method, hardware options are configured under the `resources` block in the Virtual Server manifest (e.g., `virtual-server.yaml`).

In this method, **hardware designations are defined as a kind of `resource`**, just like **CPU type, CPU core count, GPU count,** and **memory**.

#### Hardware and resource configuration options

Each of the following fields will be configured underneath the `resources` block in the YAML manifest.

| Field name             | Type   | Description                                                                                       | Default value |
| ---------------------- | ------ | ------------------------------------------------------------------------------------------------- | ------------- |
| `resources`            | Array  | <p>The top-level field.<br>Defines the resources and devices allocated to the Virtual Server.</p> | N/A           |
| `resources.definition` | String | The resource definition.                                                                          | `a`           |
| `resources.cpu`        | Array  | All CPU configuration fields.                                                                     | N/A           |
| `resources.cpu.type`   | String | The type of CPU to allocate.                                                                      | N/A           |
| `resources.cpu.count`  | Int    | The number of CPU cores to allocate.                                                              | N/A           |
| `resources.gpu`        | Array  | All GPU configuration fields.                                                                     | N/A           |
| `resources.gpu.type`   | String | The type of GPU to allocate.                                                                      | N/A           |
| `resources.gpu.count`  | Int    | The number of GPU units to allocate.                                                              | N/A           |
| `resources.memory`     | String | The amount of memory to allocate.                                                                 | N/A           |

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
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\ \ The Virtual Server's hardware and resource options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).

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

The firmware identification information for Virtual Servers is set by the Virtual Machine Instance (VMI) BIOS in the case of the firmware's UUID (that is, its MAC address), and by the VMI's SMBIOS in the case of the system-serial number. The firmware's UUID is by default a randomly-generated alphanumeric string. Both numbers are static across Virtual Server restarts.

It is **optional** to set them to anything other than their randomly-generated defaults.

{% hint style="info" %}
**Note**

You can read more about virtual hardware firmware configuration in [the Kubevirt documentation](https://kubevirt.io/user-guide/virtual\_machines/virtual\_hardware/#smbios-firmware), or see how its exposure is implemented in CoreWeave by viewing our [API reference](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1#VirtualServer.SetFirmwareSerial).
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>\ \ Firmware options must be set in the YAML tab from the Cloud UI. Firmware options are not currently exposed through the YAML manifest by default, so they must be added to the key-value map in the manifest.\
\*\*\*\*\
**Example**\\

***

![Example of firmware configuration in the YAML manifest tab of the Cloud UI.](<../../.gitbook/assets/image (9) (1).png>)
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Firmware options for Virtual Servers are configured under the `firmware` stanza.

| Field name                           | Field type | Description                                                       |
| ------------------------------------ | ---------- | ----------------------------------------------------------------- |
| <p><code>firmware</code><br><br></p> | Array      | Top-level field for firmware definitions                          |
| `firmware.uuid`                      | String     | UUID of the firmware to be deployed                               |
| `firmware.serial`                    | String     | The system-serial-number in SMBIOS of the firmware to be deployed |

\ **Example**

```yaml
  firmware:
    uuid: 906820cf-53b7-45d6-9a6e-1c389cb81016
    serial: 5cc667ec-0bba-4011-af9e-05659c64d061
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\\

{% hint style="info" %}
**Note**

It is not currently natively possible to configure firmware when using Terraform as the deployment method. This setting may be configured in conjunction with use of the Cloud UI or the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
