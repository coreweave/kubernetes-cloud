# Manually creating a Virtual Server base image

**Objective:** Configure a Virtual Server instance to serve as the source for subsequent Virtual Server deployment instances.

\
**Overview:** CoreWeave offers a variety of operating system base images, enhanced to run on CoreWeave Cloud, via our **vd-images** namespace. This guide details using one of these base images, customizing it with desired changes, and using it as a source disk for subsequent machines in a private tenant namespace.

## Deploy source Virtual Server

{% hint style="success" %}
Be sure to review [Getting Started](../../docs/coreweave-kubernetes/getting-started.md#obtain-access-credentials) and the [kubectl Virtual Server deployment method](../../docs/virtual-servers/deployment-methods/kubectl.md#deploying-a-virtual-server) before starting this guide.
{% endhint %}

First, we will deploy a Windows Virtual Server using a [reference YAML](../../virtual-server/examples/kubectl/virtual-server-windows.yaml). This will serve as the source disk for our subsequent instances:

`$ kubectl create -f virtual-server-windows-source.yaml`

{% tabs %}
{% tab title="YAML" %}
{% code title="virtual-server-windows-source.yaml" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-windows10-source
spec:
  region: LAS1
  os:
    type: windows
  resources:
    gpu:
      type: Quadro_RTX_4000
      count: 1
    cpu:
      count: 3
    memory: 16Gi
  storage:
    root:
      size: 80Gi
      storageClassName: block-nvme-las1
      source:
        pvc:
          namespace: vd-images
          # Reference querying source image here:
          # https://docs.coreweave.com/virtual-servers/root-disk-lifecycle-management/exporting-coreweave-images-to-a-writable-pvc#identifying-source-image
          name: win10-master-20210813-las1
  # Set user name and pasword
  users:
    - username:
      password:
  network:
    public: true
    directAttachLoadBalancerIP: true
  initializeRunning: true
```
{% endcode %}

{% hint style="warning" %}
Note this instance exists in **LAS1** - subsequent instances should match this region, or will suffer extended spin-up times. A base disk can also be cloned across regions.
{% endhint %}
{% endtab %}
{% endtabs %}

We can monitor the Virtual Server spinning up with `kubectl get pods --watch`

![Output of "kubectl get pods --watch"](<../../docs/.gitbook/assets/image (30) (1).png>)

Once our VS has reached "Running" status, we can get an External IP to connect to it with `kubectl get vs`

![Output of "kubectl get vs"](<../../.gitbook/assets/image (31) (1) (1) (1) (1).png>)

{% hint style="info" %}
Allow \~5 minutes after "Running" status for the Virtual Server to complete initial start procedures.
{% endhint %}

## Customizing the Virtual Server Instance

Once the Virtual Server is ready, we can use the External IP to connect to it via RDP (`mstsc`):

![Windows RDP Client](<../../docs/.gitbook/assets/image (37) (1).png>)

Or via OpenSSH:

![Connection prompt via SSH](<../../docs/.gitbook/assets/image (32).png>)

Or even via Console (useful for instances where a Public IP is not desired) using `virtctl console vs-windows10-source`:

![Output of "virtctl console vs-windows10-source"](<../../docs/.gitbook/assets/image (36) (1).png>)

{% hint style="info" %}
Review [Remote Access and Control](../remote-access-and-control.md#installing-virtctl) for more information on `virtctl`
{% endhint %}

When customization of the instance is complete, stop it using `virtctl` (`virtctl stop vs-windows10-source`). Note that shutting down from within the operating system will cause the instance to start back up with a new pod - the instance must be shutdown using `virtctl`.

Using `kubectl get vs`, we can confirm `Started: False`:

![Output of "kubectl get vs"](<../../docs/.gitbook/assets/image (35) (2).png>)

## Referencing source PVC in a new instance

We can see that the PVC created along with our source Virtual Server persists with it shut off:

![Output of "kubectl get pvc"](<../../docs/.gitbook/assets/image (34) (1).png>)

We will reference this PVC to create a new Virtual Server:

{% tabs %}
{% tab title="YAML" %}
{% code title="virtual-server-windows-new.yaml" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-windows10-new
spec:
  region: LAS1
  os:
    type: windows
  resources:
    gpu:
      type: Quadro_RTX_4000
      count: 1
    cpu:
      count: 3
    memory: 16Gi
  storage:
    root:
      size: 80Gi
      storageClassName: block-nvme-las1
      source:
        pvc:
          # Reference your tenant here
          # Reference your source VS PVC here
          namespace: tenant-<name>
          name: vs-windows10-source
  # Set user name and pasword
  users:
    - username:
      password:
  network:
    public: true
    directAttachLoadBalancerIP: true
  initializeRunning: true
```
{% endcode %}

{% hint style="info" %}
Note our namespace and PVC name has changed to match our source VS.
{% endhint %}
{% endtab %}
{% endtabs %}

The root disk of `vs-windows10-new` will be automatically cloned from `vs-windows10-source`.

## Cloning source disk PVC

The root disk we are using to clone new instances is tied to the Virtual Server with which it was created. If we wish to delete our Virtual Server `vs-windows10-source`, but retain its root disk as a clone source, we will need to clone the PVC.

Using `pvc-clone.sh`, located in CoreWeave's Kubernetes Cloud [GitHub repository](../../virtual-server/pvc-clone.sh), we will clone our Virtual Server's root disk:

{% tabs %}
{% tab title="Bash" %}
```bash
Usage: ./pvc-clone.sh <source vmi> <destination pvc name>
$ ./pvc-clone.sh vs-windows10-source windows10-base-disk
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
This will clone a PVC within the same region in which it was created.
{% endhint %}

![Output of pvc-clone.sh](<../../docs/.gitbook/assets/image (39) (2).png>)

We can now safely delete our Virtual Server with `k delete vs vs-windows10-source`:

![Output of "kubectl delete vs"](<../../docs/.gitbook/assets/image (33) (2).png>)

With `k get pvc`, we can see our original Virtual Server PVC is now deleted, and only the clone remains:

![Output of "kubectl get pvc"](<../../docs/.gitbook/assets/image (29) (2).png>)

We'll adjust our Virtual Server spec to suit:

{% tabs %}
{% tab title="YAML" %}
{% code title="virtual-server-windows-new.yaml" %}
```yaml
      source:
        pvc:
          # Reference your tenant here
          # Reference your source VS PVC here
          namespace: tenant-<name>
          name: windows10-base-disk-20210907-block-las1
```
{% endcode %}
{% endtab %}
{% endtabs %}
