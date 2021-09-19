# CLI

Virtual Servers are a Kubernetes Custom Resource available on CoreWeave Cloud, and as such, `kubectl` can be used to create and modify the resource. The Virtual Server manifest used in the following example is available in the [examples](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/kubectl) section of the CoreWeave Cloud repository. 

### Understanding the Virtual Server Manifest

The Virtual Server manifest is broken into two parts, `metadata` and `spec`. The `metadata` section, as is the case with most Kubernetes manifests, contains the name of your Virtual Server and the namespace where it will be deployed. The `spec` contains configuration fields that define how the Virtual Server will be created. These fields are as follows:

{% hint style="info" %}
The following fields are within the manifest spec
{% endhint %}

| Field | Type | Description |
| :--- | :--- | :--- |
| region | String | Defines the region where the Virtual Server is deployed |
| os | {} | Defines the Operating System type |
| os.type | String | The Operating System type - Linux/Windows |
| os.enableUEFIBoot | Boolean | Enable the UEFI bootloader |
| resources | {} | Defines the resources and devices allocated to the Virtual Server |
| resources.definition | String | The resource definition - defaults to 'a' |
| resources.cpu | {} | Defines the CPU allocation  |
| resources.cpu.type | String | The type of CPU to allocate |
| resources.cpu.count | Int | The number of CPU cores to allocate |
| resources.gpu | {} | Defines the GPU allocation |
| resources.gpu.type | String | The type of GPU to allocate |
| resources.gpu.count | Int | The number of GPU\(s\) to allocate |
| resources.memory | String | The amount of memory to allocate |
| storage | {} | Defines the root storage and additional storage devices |
| storage.root | {} | Defines the root file system PVC |
| storage.root.size | String | The volume size |
| storage.root.source \[¹\] | {} | The DataVolume source for the root file system   |
| storage.root.storageClassName | String | The storage class name for the root PVC |
| storage.root.volumeMode | String | The volume mode for the root PVC |
| storage.root.accessMode | String | The access mode name for the root PVC  |
| storage.root.ephemeral | Boolean | Set whether the root disk is ephemeral |
| storage.additionalDisks | \[\] | A list of PVC references to be added as disk devices |
| storage.additionalDisks\[ \].name | String | Name of the disk |
| storage.additionalDisks\[ \].spec \[²\] | {} | The VolumeSource for the disk |
| storage.filesystems  | \[\] | A list of PVC references to be mounted |
| storage.filesystems\[ \].name | String | Name of the mount |
| storage.filesystems\[ \].spec \[²\] | {} | The VolumeSource for the file system mount |
| users | \[\] | A list of users to be added by cloud-init \(if supported by the OS\) |
| users\[ \].username | String | Username for the user |
| users\[ \].password | String | Password for the user |
| network | {} | Defines the network configuration |
| network.directAttachLoadBalancerIP | Boolean | Directly attach a loadbalancer IP to the Virtual Server |
| network.floatingIPs | \[\] | A list of service references to be added as floating IPs |
| network.floatingIPs\[ \].serviceName | String | Name of the service |
| network.tcp | {} | Defines the TCP network configuration |
| network.tcp.ports | \[\] | List of TCP ports to expose |
| network.udp | {} | Defines the UDP network configuration |
| network.udp.ports | \[\] | List of UDP ports to expose |
| network.public | Boolean | Whether a public IP will be assigned |
| initializeRunning | Boolean | The Virtual Server will be started as soon as it is created and initialized |

{% hint style="info" %}
\[¹\] - See [DataVolumeSource](https://pkg.go.dev/kubevirt.io/containerized-data-importer/pkg/apis/core/v1alpha1#DataVolumeSource) for further information

\[²\] - See [VolumeSource](https://pkg.go.dev/kubevirt.io/client-go/api/v1#VolumeSource) for further information
{% endhint %}

{% hint style="info" %}
Note: Certain fields are mutually exclusive. These are: 

* GPU type and CPU type
* TCP ports or UDP ports and directAttachLoadbalancerIP 
{% endhint %}

### Deploying a Virtual Server

Using the [virtual-server.yaml](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server.yaml) example manifest we can easily deploy a Virtual Server using `kubectl`. Replace `name` and `namespace` in the metadata object to match the name and namespace for your Virtual Server. Once complete, deploy the Virtual Server manifest with `kubectl`: 

```bash
kubectl apply -f virtual-server.yaml
```

Once deployed, your Virtual Server will begin the initialization process. The status of your Virtual Server can be examined with \(replace "example-vs" with your Virtual Server name\):

```bash
kubectl get vs example-vs
NAME                STATUS               REASON                                           STARTED   INTERNAL IP      EXTERNAL IP
example-vs          Initializing         Waiting for VirtualMachineInstance to be ready   False                      123.123.123.123
```

The initialization process may take a moment, but once complete the Virtual Server status will return as either VirtualServerStopped or VirtualServerReady, depending on how initializeRunning was set: 

```bash
kubectl get vs example-vs
NAME                STATUS                 REASON               STARTED   INTERNAL IP      EXTERNAL IP
example-vs          VirtualServerStopped   VirtualServerStopped False                      123.123.123.123 
```

```bash
kubectl get vs example-vs
NAME                STATUS               REASON               STARTED   INTERNAL IP      EXTERNAL IP
example-vs          VirtualServerReady   VirtualServerReady   True      1.2.3.4          123.123.123.123  
```

Your Virtual Server is now ready to be accessed. See [Remote Access and Control](../remote-access-and-control.md) for how to access your Virtual Server.

