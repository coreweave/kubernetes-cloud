---
description: Learn more about other configurations available for Virtual Servers.
---

# Additional Features

Below are some additional features Virtual Servers offering even finer-grained control and configuration options for niche use cases.

{% hint style="info" %}
**Note**

All additional features discussed in this document must be configured using the YAML editor if deploying a Virtual Server using the Cloud UI.
{% endhint %}

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
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

When configuring an ephemeral root storage disk on the Cloud UI, the source image is cloned into a `ReadOnlyMany` type volume, as shown in the example below. Use the Cloud UI YAML editor to incorporate the configuration into the Virtual Server's manifest.

<pre class="language-yaml"><code class="lang-yaml"><strong>---
</strong>apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: image-rox
spec:
  accessModes:
  - ReadOnlyMany
  dataSource:
    kind: PersistentVolumeClaim
    name: &#x3C;source-root-disk-pvc> # This name will be the same name as a DataVolume/VirtualServer used as the source.
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
</code></pre>

{% hint style="info" %}
**Additional Resources**

[View this snippet on our GitHub](../../../virtual-server/examples/kubectl/virtual-server-ephemeral-root-disk.yaml) for further context.
{% endhint %}
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

When configuring an ephemeral root storage disk, the source image is cloned into a `ReadOnlyMany` type volume, as shown in the example below.

<pre class="language-yaml"><code class="lang-yaml"><strong>---
</strong>apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: image-rox
spec:
  accessModes:
  - ReadOnlyMany
  dataSource:
    kind: PersistentVolumeClaim
    name: &#x3C;source-root-disk-pvc> # This name will be the same name as a DataVolume/VirtualServer used as the source.
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
</code></pre>

{% hint style="info" %}
**Additional Resources**

[View this snippet on our GitHub](../../../virtual-server/examples/kubectl/virtual-server-ephemeral-root-disk.yaml) for further context.
{% endhint %}
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

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

<table><thead><tr><th width="243.5">Option</th><th>Description</th></tr></thead><tbody><tr><td><code>Always</code></td><td>A Virtual Server will always be present. If the Virtual Server crashed, a new one will be spawned.</td></tr><tr><td><code>RerunOnFailure</code></td><td><mark style="background-color:green;">Default.</mark> A <code>VirtualMachineInstance</code> will be respawned if the previous instance failed in an error state. It will not be re-created if the guest stopped successfully (e.g. shut down from inside guest).</td></tr><tr><td><code>Manual</code></td><td>The presence of a <code>VirtualMachineInstance</code> or lack thereof is controlled exclusively by the start/stop/restart VirtualMachine subresource endpoints.</td></tr><tr><td><code>Halted</code></td><td>No VirtualMachineInstance will be present. If a guest is already running, it will be stopped. This is the same behavior as <code>spec.running: false</code>.</td></tr></tbody></table>

{% hint style="info" %}
**Additional Resources**\
See [the Kubevirt documentation](https://kubevirt.io/user-guide/virtual\_machines/run\_strategies/#run-strategies) for more information.
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">Cloud UI</mark>

To change the default RunStrategy for a Virtual Server, define the strategy to use in the `spec.runStrategy` field using the YAML editor.

<table><thead><tr><th width="202.05647618918073">Field name</th><th width="262.35377875136913">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>runStrategy</code></td><td><a href="https://pkg.go.dev/kubevirt.io/client-go/api/v1#VirtualMachineRunStrategy">VirtualMachineRunStrategy</a></td><td>Defines <a href="https://kubevirt.io/user-guide/virtual_machines/run_strategies/#run-strategies">RunStrategy</a> parameter. Default value is <code>RerunOnFailure</code>.</td></tr></tbody></table>

Example in plain text:

```yaml
  runStrategy: Always
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

To change the default RunStrategy for a Virtual Server, define the strategy to use in the `spec.runStrategy` field.

<table><thead><tr><th width="199.05647618918073">Field name</th><th width="262.35377875136913">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>runStrategy</code></td><td><a href="https://pkg.go.dev/kubevirt.io/client-go/api/v1#VirtualMachineRunStrategy">VirtualMachineRunStrategy</a></td><td>Defines <a href="https://kubevirt.io/user-guide/virtual_machines/run_strategies/#run-strategies">RunStrategy</a> parameter. Default value is <code>RerunOnFailure</code>.</td></tr></tbody></table>

Example in plain text:

```yaml
  runStrategy: Always
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**\
It is not currently possible to configure runStrategy through Terraform. This feature may be configured in conjunction with the Cloud UI or Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## useVirtioTransitional

Enables virtio-transitional to support compatibility with older guest Operating Systems. The default value is `false`.&#x20;

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">Cloud UI</mark>

Open the YAML editor to configure virtio-transitional.

<table><thead><tr><th width="302.1730103806228">Field name</th><th>Field type</th></tr></thead><tbody><tr><td><code>useVirtioTransitional</code></td><td>Boolean</td></tr></tbody></table>

Example in plain text:

```yaml
useVirtioTransitional: false
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Enabling virtio-transitional is done by configuring the Kubernetes manifest.

<table><thead><tr><th width="281.66666666666663">Field name</th><th>Field type</th></tr></thead><tbody><tr><td><code>useVirtioTransitional</code></td><td>Boolean</td></tr></tbody></table>

\
Example in plain text:

```yaml
useVirtioTransitional: false
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**\
It is not currently possible to configure useVirtioTransitional through Terraform. This feature may be configured in conjunction with the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## terminationGracePeriodSeconds

Specifies the number in seconds before the guest is killed, allowing the operating system to be shut down gracefully. The default value for Linux-based systems is 60. Windows shutdown may take some time so the default value is 300s. "A 0 value for the grace period option means that the virtual machine should not have a grace period observed during shutdown."

{% tabs %}
{% tab title="Cloud UI" %}
## Deployment method: <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

Open the YAML editor to configure `terminationGracePeriodSeconds`.

<table><thead><tr><th width="360.41564792176035">Field name</th><th width="119">Field type</th><th>Default values</th></tr></thead><tbody><tr><td><code>terminationGracePeriodSeconds</code></td><td>Integer</td><td><code>60</code> - Linux systems<br><code>300</code> - Windows systems</td></tr></tbody></table>

Example in plain text:

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Configuring the termination grace period is done through the Kubernetes manifest.

<table><thead><tr><th width="360.41564792176035">Field name</th><th width="150">Field type</th><th>Default value</th></tr></thead><tbody><tr><td><code>terminationGracePeriodSeconds</code></td><td>Integer</td><td><code>60</code> - Linux systems<br><code>300</code> - Windows systems</td></tr></tbody></table>

Example in plain text:

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\


{% hint style="info" %}
**Note**\
It is not currently possible to configure terminationGracePeriodSeconds through Terraform. This feature may be configured in conjunction with the Cloud UI or Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## initializeRunning

Determines whether or not the Virtual Server should be started as soon as it is created and initialized.

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

Open the YAML editor to configure `initializeRunning`.

<table><thead><tr><th width="283.74590044991317">Field name</th><th width="150">Field type</th></tr></thead><tbody><tr><td><code>initializeRunning</code></td><td>Boolean</td></tr></tbody></table>

Example in plain text:

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

Configuring `initializeRunning` is done through the Kubernetes manifest.

<table><thead><tr><th width="278.6519660994684">Field name</th><th width="150">Field type</th></tr></thead><tbody><tr><td><code>initializeRunning</code></td><td>Boolean</td></tr></tbody></table>

Example in plain text:

```yaml
terminationGracePeriodSeconds: 60
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**\
It is not currently possible to configure `initializeRunning` through the Cloud UI. This feature may be configured in conjunction with the Kubernetes CLI. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}

## Floating Services

Floating services, sometimes called floating IPs, allows users to create their own load balancing Services with static IP addresses, which can then be used to configure custom DNS or custom IP addresses.

{% tabs %}
{% tab title="Cloud UI" %}
## **Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

Open the YAML editor to configure floating services under the `.network.floatingIPs` stanza . This field is a list of load balancer Service names. If configured, the Virtual Server will be assigned floating IPs from the load balancer IP of each service.

<table><thead><tr><th width="289.39440482720784">Field name</th><th width="92">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>network.floatingIPs</code></td><td>List</td><td>A list of Service references to be added as floating IPs</td></tr><tr><td><code>network.floatingIPs[ ].serviceName</code></td><td>String</td><td>The name of the Service<br></td></tr></tbody></table>

Example in plain text:

```yaml
  network:
    floatingIPs:
    - <svc-name>
```
{% endtab %}

{% tab title="CLI" %}
## **Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

To deploy a Floating IP service, configure the following fields.

<table><thead><tr><th width="289.39440482720784">Field name</th><th width="92">Field type</th><th>Description</th></tr></thead><tbody><tr><td><code>network.floatingIPs</code></td><td>List</td><td>A list of Service references to be added as floating IPs</td></tr><tr><td><code>network.floatingIPs[ ].serviceName</code></td><td>String</td><td>The name of the Service<br></td></tr></tbody></table>

Example in plain text:

```yaml
  network:
    floatingIPs:
    - <svc-name>
```
{% endtab %}

{% tab title="Terraform" %}
## **Deployment method:** <mark style="background-color:orange;">Terraform</mark>

{% hint style="info" %}
**Note**

It is not currently possible to deploy floating IPs using the Terraform module. See the Cloud UI or CLI options. Alternatively, [you may extend the Virtual Server Terraform module yourself](../../../virtual-server/examples/terraform/vs.tf).
{% endhint %}
{% endtab %}
{% endtabs %}
