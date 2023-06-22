---
description: Select the name for a Virtual Server
---

# Name

The Virtual Server's name can be any combination of lowercase letters, numbers, and hyphens.&#x20;

It cannot have capital letters, whitespace, or other special characters. Shorter names are preferred because this is part of the server's DNS name.

{% hint style="warning" %}
**Name conflicts**

Deploying a Virtual Server creates a [Block Storage Volume](../../storage/storage/#block-storage-volumes) with the same name as the server.

Ensure the Virtual Server's name doesn't conflict with any [Storage Volumes](../../storage/storage/) in your namespace. If there is an existing Storage Volume with that name, the deployment will fail.&#x20;
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

From the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md) Virtual Server deployment menu, enter a server name.

<figure><img src="../../.gitbook/assets/image (2) (2).png" alt=""><figcaption><p>Enter the Virtual Server name</p></figcaption></figure>
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Enter a name for your Virtual Server is simple using the **Kubernetes manifest file**.

The name you'd like to use is configured by setting its label under the `name` selector in the `metadata` section of the manifest.

### Name configuration options

| Variable name | Variable type | Description                                        | Default value |
| ------------- | ------------- | -------------------------------------------------- | ------------- |
| `name`        | String        | The name you'd like to use for the Virtual Server. | none          |

In the example below, the name `example-123` is set under `metadata.name`.

```yaml
---
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
    name: example-123
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

The name for the Virtual Server can be defined in the `vs_name` variable in your `variables.tf` file.

### Name configuration options

| Variable name | Variable type | Description                                        | Default value |
| ------------- | ------------- | -------------------------------------------------- | ------------- |
| `vs_name`     | String        | The name you'd like to use for the Virtual Server. | `MY-VS`       |

Terraform example:

```json
variable "vs_name" {
  description = "Virtual Server hostname"
  default     = "MY-VS"
}
```
{% endtab %}
{% endtabs %}
