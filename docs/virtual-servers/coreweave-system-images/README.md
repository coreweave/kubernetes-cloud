# CoreWeave System Images

Operating System images provided by CoreWeave Cloud include enhancements and features to reduce friction when running Virtual Servers in the Cloud.

## Identifying Images

Operating system source images provided by CoreWeave for Virtual Servers live in the `vd-images` namespace on CoreWeave Cloud. Several metadata properties exist for easy identification.

Using [`kubectl`](../../coreweave-kubernetes/getting-started.md#install-kubernetes-command-line-tools) with the metadata labels listed above, individual images are easily queried.

### Metadata labels

<table><thead><tr><th width="389">Label</th><th>Description</th></tr></thead><tbody><tr><td><code>images.coreweave.cloud/family</code></td><td>Identifies the OS type, usually Windows or Linux</td></tr><tr><td><code>images.coreweave.cloud/features</code></td><td>Identifies image specific features, such as Teradici enabled or nVidia drivers</td></tr><tr><td><code>images.coreweave.cloud/id</code></td><td>Image ID used during CI/CD</td></tr><tr><td><code>images.coreweave.cloud/latest</code></td><td>Boolean tag for the latest image revision</td></tr><tr><td><code>images.coreweave.cloud/name</code></td><td>Complete image name, as displayed in the Web UI</td></tr><tr><td><code>images.coreweave.cloud/os-name</code></td><td>Name of the parent OS</td></tr><tr><td><code>images.coreweave.cloud/os-version</code></td><td>Subsection of OS, such as "Standard" or "Professional Edition"</td></tr><tr><td><code>images.coreweave.cloud/private</code></td><td>Boolean tag for testing images, not intended to be used in production environments</td></tr><tr><td><code>images.coreweave.cloud/region</code></td><td>The datacenter region where the image resides</td></tr><tr><td><code>images.coreweave.cloud/version</code></td><td>Date tag for when the image was built</td></tr></tbody></table>

## Example query commands

List all (non-private) latest images available for use.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false
```
{% endcode %}

Sort all images by **region**.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false --sort-by=.spec.storageClassName
```
{% endcode %}

Show all **Windows images** only.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=windows
```
{% endcode %}

Show all **Windows 10 images** only.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Windows_10
```
{% endcode %}

Show all Windows **10 images** by **region**.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Windows_10,images.coreweave.cloud/region=ord1 -o jsonpath='{.items[*].metadata.name}'
```
{% endcode %}

Show all **Linux images** only.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=linux
```
{% endcode %}

Show all **Ubuntu images** only.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Ubuntu
```
{% endcode %}

Show all **Ubuntu 20.04** **images** only.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=Ubuntu_20.04
```
{% endcode %}

Show all **Ubuntu 20.04** **images** by **region**.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=Ubuntu_20.04,images.coreweave.cloud/region=ord1 -o jsonpath='{.items[*].metadata.name}'
```
{% endcode %}

Show all **Linux images** and **their features**, filtered by **region**.

{% code overflow="wrap" %}
```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=linux,images.coreweave.cloud/region=ord1 -o=custom-columns="PVC:metadata.name,NAME:metadata.labels['images\.coreweave\.cloud\/name'],FEATURES:metadata.labels['images\.coreweave\.cloud\/features'],SIZE:status.capacity.storage,STORAGECLASS:.spec.storageClassName" --sort-by='.metadata.name'
```
{% endcode %}
