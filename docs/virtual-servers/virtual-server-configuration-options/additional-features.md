---
description: Learn more about other configurations available for Virtual Servers.
---

# Additional Features

Discussed below are the additional features Virtual Servers offer for finer-grained control and niche use cases.

## Ephemeral root disks

In many use cases, such as data processing or pixel-streaming, Virtual Servers do not need to be long-living, and in fact, they are best used ephemerally. In these instances, leveraging **ephemeral root disks** will speed up instantiation, as well as lower hosting costs.

* :alarm\_clock: Ephemeral root disks don't require a new root volume to be allocated, removing this time-consuming step from the instantiation process to make for **faster boot times**.
* :sparkles: Removing ephemeral root disks means they no longer need to be hosted, which **reduces hosting costs** overall.
* :writing\_hand: Ephemeral disks are **still writeable**; modifications made at run-time are temporarily stored in the ephemeral disk of the active node. All changes written to the root disk are only lost when the Virtual Server is shut down or restarted.

{% hint style="info" %}
**Note**

A shared filesystem volume, NFS, SMB, or Object storage should be used to store persistent data in data-processing use cases.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>\ <mark style="background-color:green;"></mark>

{% hint style="info" %}
**Note**

It is not currently possible to deploy ephemeral root disks using the Cloud UI. See the CLI option.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

****\
****When configuring an ephemeral root storage disk, the source image is cloned into a `ReadOnlyMany` type volume, as shown in the example below.\
****

{% hint style="info" %}
**Additional Resources**

[View this snippet on our GitHub](../../../virtual-server/examples/kubectl/virtual-server-ephemeral-root-disk.yaml) for further context.
{% endhint %}



```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: image-rox
spec:
  accessModes:
  - ReadOnlyMany
  dataSource:
    kind: PersistentVolumeClaim
    name: <source-root-disk-pvc> # This name will be the same name as a DataVolume/VirtualServer used as the source.
  resources:
    requests:
      storage: 40Gi # Must match the size of the source volume
  storageClassName: block-nvme-ord1
  volumeMode: Block
---
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: example-vs
spec:
  region: ORD1
  os:
    type: linux
  resources:
    gpu:
      type: Quadro_RTX_4000
      count: 1
    cpu:
      count: 4
    memory: 16Gi
  storage:
    root:
      size: 40Gi
      storageClassName: block-nvme-ord1
      ephemeral: true
      source:
        pvc:
          namespace: tenant-example # Replace with your namespace
          name: image-rox
  # Change user name and pasword
  # User is on the sudoers list
  #  users:
  #    - username: SET YOUR USERNAME HERE
  #      password: SET YOUR PASSWORD HERE  
  # To use key-based authentication replace and uncomment ssh-rsa below with your public ssh key
  #  sshpublickey: |
  #    ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
  network:
    public: false
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

<mark style="background-color:orange;"></mark>

{% hint style="info" %}
**Note**

It is not currently possible to deploy ephemeral root disks using the Terraform module. See the CLI option. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## RunStrategy

Configuring the [RunStrategy](https://kubevirt.io/user-guide/virtual\_machines/run\_strategies/#run-strategies) for the Virtual Server determines what CoreWeave's Virtual Server orchestration infrastructure will do on instance crash or shutdown. The default RunStrategy is `RerunOnFailure`, meaning Kubevirt will not restart the system when someone issues a shutdown command from the OS.\
\
All available RunStrategy options:

* `Always`: A Virtual Server will always be present. If the Virtual Server crashed, a new one will be spawned.
* `RerunOnFailure`: A VirtualMachineInstance will be respawned if the previous instance failed in an error state. It will not be re-created if the guest stopped successfully (e.g. shut down from inside guest).
* `Manual`: The presence of a VirtualMachineInstance or lack thereof is controlled exclusively by the start/stop/restart VirtualMachine subresource endpoints.
* `Halted`: No VirtualMachineInstance will be present. If a guest is already running, it will be stopped. This is the same behavior as `spec.running: false`.

{% hint style="info" %}
**Additional Resources**\
See [the Kubevirt documentation](https://kubevirt.io/user-guide/virtual\_machines/run\_strategies/#run-strategies) for more information.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">Cloud UI</mark>

<mark style="background-color:blue;"></mark>

{% hint style="info" %}
**Note**

It is not currently possible to configure RunStrategy from the Cloud UI. See the CLI option.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

To change the default RunStrategy for a Virtual Server, define the strategy to use in the `spec.runStrategy` field.

| Field name    | Field type                                                                                             | Description                                                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `runStrategy` | [VirtualMachineRunStrategy](https://pkg.go.dev/kubevirt.io/client-go/api/v1#VirtualMachineRunStrategy) | Defines [RunStrategy](https://kubevirt.io/user-guide/virtual\_machines/run\_strategies/#run-strategies) parameter. Default value is `RerunOnFailure`. |



**Example**

```yaml
  runStrategy: Always
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\ <mark style="background-color:orange;"></mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure runStrategy through Terraform. This feature may be configured in conjunction with the Cloud UI or Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## useVirtioTransitional

Enables virtio-transitional to support compatibility with older guest Operating Systems. The default value is `false`.&#x20;

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">Cloud UI</mark>

<mark style="background-color:green;"></mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure useVirtioTransitional through the Cloud UI. This feature may be configured in conjunction with the Kubernetes CLI.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>\ <mark style="background-color:green;"></mark>\ <mark style="background-color:green;"></mark>Enabling virtio-transitional is done by configuring the Kubernetes manifest.

| Field name              | Field type |
| ----------------------- | ---------- |
| `useVirtioTransitional` | Boolean    |

\
**Example**

```yaml
useVirtioTransitional: false
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\ <mark style="background-color:orange;"></mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure useVirtioTransitional through Terraform. This feature may be configured in conjunction with the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## terminationGracePeriodSeconds

Specifies the number in seconds before the guest is killed, allowing the operating system to be shut down gracefully. The default value for Linux-based systems is 60. Windows shutdown may take some time so the default value is 300s. "A 0 value for the grace period option means that the virtual machine should not have a grace period observed during shutdown."

{% tabs %}
{% tab title="Cloud UI" %}
{% hint style="info" %}
**Note**\
****It is not currently possible to configure useVirtioTransitional through the Cloud UI. This feature may be configured in conjunction with the Kubernetes CLI.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>\


Configuring the termination grace period is done through the Kubernetes manifest.\


| Field name                      | Field type | Default value                                                                |
| ------------------------------- | ---------- | ---------------------------------------------------------------------------- |
| `terminationGracePeriodSeconds` | Integer    | <p><code>60</code> - Linux systems<br><code>300</code> - Windows systems</p> |

\
**Example**

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\ <mark style="background-color:orange;"></mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure terminationGracePeriodSeconds through Terraform. This feature may be configured in conjunction with the Cloud UI or Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## initializeRunning

Determines whether or not the Virtual Server should be started as soon as it is created and initialized.

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">Cloud UI</mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure `initializeRunning` through the Cloud UI. This feature may be configured in conjunction with the Kubernetes CLI.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>\


Configuring `initializeRunning` is done through the Kubernetes manifest.\


| Field name          | Field type |
| ------------------- | ---------- |
| `initializeRunning` | Boolean    |

\
**Example**

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**\
****It is not currently possible to configure `initializeRunning` through the Cloud UI. This feature may be configured in conjunction with the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## Floating Services

Floating services, sometimes called floating IPs, allows users to create their own load balancing Services with static IP addresses, which can then be used to configure custom DNS or custom IP addresses.

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>\ <mark style="background-color:blue;"></mark>\ <mark style="background-color:blue;"></mark>To configure Floating IPs on the Cloud UI, navigate to the YAML tab and find the `floatingIPs` field. This field is an array of load balancer Service names. If configured, the Virtual Server will be assigned floating IPs from the load balancer IP of each service.\ <mark style="background-color:blue;"></mark>

![The floatingIPs option as exposed through the YAML tab on the Cloud UI](<../../.gitbook/assets/image (1) (4) (1).png>)
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

To deploy a Floating IP service, configure the following fields.\


| Field name                           | Field type | Description                                              |
| ------------------------------------ | ---------- | -------------------------------------------------------- |
| `network.floatingIPs`                | List       | A list of Service references to be added as floating IPs |
| `network.floatingIPs[ ].serviceName` | String     | <p>The name of the Service<br></p>                       |

\
**Example**

```yaml
  network:
    floatingIPs:
    - <svc-name>
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

<mark style="background-color:orange;"></mark>

{% hint style="info" %}
**Note**

It is not currently possible to deploy floating IPs using the Terraform module. See the Cloud UI or CLI options. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
