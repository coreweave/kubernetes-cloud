# CoreWeave System Images

#### Operating System images provided by CoreWeave Cloud include enhancements and features to reduce friction when running Virtual Servers in the cloud.

#### This section documents how to use CoreWeave specific features, and operating system enhancements one should be aware of.

## Identifying Images

Operating system source images provided by CoreWeave for Virtual Servers live in the `vd-images` namespace. There are several metadata properties that exist for easy identification:

#### Metadata Labels

* `images.coreweave.cloud/family`
  * Identifies the OS type, usually Windows or Linux
* `images.coreweave.cloud/features`
  * Identifies image specific features, such as Teradici enabled or nVidia drivers
* `images.coreweave.cloud/id`
  * Image ID used during CI/CD
* `images.coreweave.cloud/latest`
  * Boolean tag for the latest image revision
* `images.coreweave.cloud/name`
  * Complete image name, as displayed in the Web UI
* `images.coreweave.cloud/os-name`
  * Parent OS
* `images.coreweave.cloud/os-version`
  * Subsection of OS, such as Standard or Professional Edition
* `images.coreweave.cloud/private`
  * Boolean tag for testing images not intended to be used
* `images.coreweave.cloud/region`
  * Datacenter region the image resides in
* `images.coreweave.cloud/version`
  * Date tag for when the image was built

### Querying Images using Metadata Labels

Using [`kubectl`](../../../coreweave-kubernetes/getting-started.md#install-kubernetes-command-line-tools) via CLI and the metadata labels listed above, individual images are easily queried.

#### Listing all latest images available for use

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false
```

#### Sorting all images by Region

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false --sort-by=.spec.storageClassName
```

#### Filtering by Windows Images

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=windows
```

#### Filtering by Windows 10

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Windows_10
```

#### Extracting just the image name, filtering Windows 10 by Region

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Windows_10,images.coreweave.cloud/region=ord1 -o jsonpath='{.items[*].metadata.name}'
```

#### Filtering by Linux Images

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=linux
```

#### Filtering by Ubuntu Images

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/os-name=Ubuntu
```

#### Filtering by Ubuntu 20.04

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=Ubuntu_20.04
```

#### Extracting just the image name, filtering Ubuntu 20.04 by Region

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/name=Ubuntu_20.04,images.coreweave.cloud/region=ord1 -o jsonpath='{.items[*].metadata.name}'
```

#### Listing all Linux Images and their features, filtering by Region

```shell
kubectl get pvc -n vd-images -l images.coreweave.cloud/latest=true,images.coreweave.cloud/private=false,images.coreweave.cloud/family=linux,images.coreweave.cloud/region=ord1 -o=custom-columns="PVC:metadata.name,NAME:metadata.labels['images\.coreweave\.cloud\/name'],FEATURES:metadata.labels['images\.coreweave\.cloud\/features'],SIZE:status.capacity.storage,STORAGECLASS:.spec.storageClassName" --sort-by='.metadata.name'
```
