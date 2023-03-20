---
description: Deploy containerized applications onto CoreWeave Cloud
---

# Custom Containers

This guide walks through the steps necessary to deploy a basic containerized application onto CoreWeave Cloud. The configurations used in the following example are intentionally kept simple, although [many additional configuration options are available](../virtual-servers/deployment-methods/kubectl.md#configuration-quick-reference).

## Prerequisites

This guide presumes that you:

* already have [an active CoreWeave Cloud account](getting-started.md),
* have already [configured and installed a kubeconfig file](getting-started.md#generate-the-kubeconfig-file) for use with CoreWeave Kubernetes,
* have an application that has already successfully been containerized using Docker or a similar container runtime.

If you have not already completed these steps, first visit [Get Started with CoreWeave](getting-started.md).

{% hint style="info" %}
**Additional Resources**

For an even more pared down example of Deployments, refer to Kubernetes' official example, [Run a Stateless Application Using a Deployment](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/).&#x20;
{% endhint %}

## Overview

The basic steps to deploying your own custom containerized application onto CoreWeave Cloud are as follows:

1. [Prepare the container registry](custom-containers.md#prepare-the-container-registry)
2. [Create a storage volume for the application](custom-containers.md#create-a-storage-volume-optional) (optional)
3. [Build the application's Deployment manifest](custom-containers.md#build-the-deployment-manifest)
   1. [Define the application's resources](custom-containers.md#define-the-applications-resources)
   2. [Define the Kubernetes affinities](custom-containers.md#define-kubernetes-affinities)
   3. [Associate the storage volume with the application](custom-containers.md#associate-the-storage-volume-if-applicable) (if applicable)
4. [Apply the Deployment](custom-containers.md#apply-the-deployment)

## Prepare the container registry

To deploy a locally built, containerized application, the container image must first be pushed to a container image repository.

CoreWeave provides an easy way to deploy a [Docker Registry](https://docs.docker.com/registry/) instance into your namespace for this purpose. Simply install the [Docker Registry application](https://docs.docker.com/registry/) from [the applications Catalog](applications-catalog.md) on the [Cloud UI](../../virtual-servers/deployment-methods/coreweave-apps.md). Once deployed, the Docker Registry instance may be configured for access both within and outside of the CoreWeave environment.

All requests to the Docker Registry instance are authenticated. Credentials are automatically provisioned in an `imagePullSecret` in the namespace, which contains the credentials that are either manually configured during setup or automatically generated for you.

{% hint style="warning" %}
**Important**

Public repositories are not currently supported by Docker Registry on CoreWeave Cloud.
{% endhint %}

The [Service Account](https://cloud.google.com/iam/docs/understanding-service-accounts) used by default may optionally be patched to use this pull secret, so that Pods deployed in the namespace will always have access to the registry. Alternatively, you may opt to create a separate Service Account during the application deployment process, which can then be used on a specific Pod in order to allow pulling from the container registry without specifying an `imagePullSecret`.

{% hint style="info" %}
**Additional Resources**

For more information on Docker Registry, see [the official Docker documentation](https://docs.docker.com/registry/).
{% endhint %}

### Storage backends

The Docker Registry instance requires a storage backend. [CoreWeave's S3-compatible Object Storage](../storage/object-storage.md) or a [persistent volume](../storage/storage/) may be used as backends.

### Install Docker Registry into your CoreWeave namespace

To install the Docker Registry application, first [log in to your CoreWeave Cloud account](https://cloud.coreweave.com), then navigate to the Applications Catalog.

From the Catalog homepage, search for `docker`. Then, select the version of the Docker Registry application that you'd like to deploy.

<figure><img src="../.gitbook/assets/image (8) (3).png" alt="Screenshot of docker-registry in the applications Catalog"><figcaption><p>Locate the docker-registry application in the applications Catalog</p></figcaption></figure>

Clicking on the application's card will open its deployment page, which contains further information about the application itself. Click the **Deploy** button to navigate to the application's configuration screen, which is used to configure the instance.

Finally, click the **Deploy** button in the bottom right-hand corner of the screen to launch the instance. Once the application is deployed to the set specifications, you will be redirected to the application's status page.

From this page, the **Application Secrets** can be accessed from the section at the top right-hand section of the screen. Clicking the eye icon beside each field will reveal the field's contents in plain text. This **Secrets** area also contains the registry password. This is either the value of the password set explicitly in the configuration screen, or it is a newly created, randomly-generated password.

<figure><img src="../.gitbook/assets/image (10) (2) (1).png" alt=""><figcaption><p>The application secrets include the configured or randomly-generated registry password</p></figcaption></figure>

Alternatively, use `kubectl` to retrieve the registry credentials via the command line:

{% code overflow="wrap" %}
```bash
$ kubectl get --namespace <NAMESPACE> secret test-docker-registry-secret -o=go-template='{{ printf "username: %s\npassword: %s" (.data.username | base64decode) (.data.password | base64decode) }}'
```
{% endcode %}

The **installation notes** on the application's deployment screen provides all of the following commands, with your namespace and URL set in place.

&#x20;Next, log in to your Docker Registry instance. First export `REGISTRY_USERNAME` to the username acquired using `kubectl get secret`:

{% code overflow="wrap" %}
```bash
$ export REGISTRY_USERNAME=$(kubectl get secret test-docker-registry-secret -o=go-template='{{ .data.username | base64decode }}')
```
{% endcode %}

Then, use `docker login` while sourcing your credentials with `kubectl`:

{% code overflow="wrap" %}
```bash
$ kubectl get --namespace <NAMESPACE> secret test-docker-registry-secret \
        -o=go-template='{{ .data.password | base64decode }}' \
        | docker login <PROVIDED URL> -u $REGISTRY_USERNAME --password-stdin
```
{% endcode %}

If you are not using Kubectl, you may use `docker login` normally by using `docker login`, then entering the registry password when prompted:

{% code overflow="wrap" %}
```bash
$ docker login <REGISTRY NAME>.<COREWEAVE URL> -u docker
```
{% endcode %}

:tada: Congratulations! You can now build and push images to your Docker Registry instance hosted on CoreWeave Cloud!

## Build the container

The next step is to build and push the new container. In this example, we'll assume that the Dockerfile is located in the current working directory.

Build and tag the image using `docker build`:

{% code overflow="wrap" %}
```bash
$ docker build -t <URL>/<APP NAME>:<TAG VERSION> .
```
{% endcode %}

Then, push the newly built image to the newly created container image registry using `docker push`, passing in the given URL of the new registry and the application's name and tag:

{% code overflow="wrap" %}
```bash
$ docker push <URL>/<APP NAME>:<TAG VERSION>
```
{% endcode %}

{% hint style="danger" %}
**Warning**

**Never use `latest` as a tag; always push images to a new tag.** Due to aggressive caching for faster repeat spin-up times, re-using the same tag can lead to some of your Pods running an out-of-date version of your code.
{% endhint %}

## Create a storage volume (optional)

For the purposes of this example walkthrough, the application requires backend storage. [Create a storage volume](../storage/storage/using-storage-cloud-ui.md#creating-storage-volumes) from the Cloud UI, and give it a name that will be easy to associate with the application later.

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>In this example, a storage volume with the name <code>kobold-ai</code> is created</p></figcaption></figure>

{% hint style="warning" %}
**Important**

When creating your storage volume, it is generally recommended to ensure that the [data center region](../data-center-regions.md) it is being allocated to is the same as your associated workload. See ["Define Kubernetes affinities"](custom-containers.md#define-kubernetes-affinities) for instructions on how to ensure the workload is scheduled to the same region.
{% endhint %}

{% hint style="info" %}
**Note**

If your application requires a lot of storage, it is recommended to configure a PVC with at least `1TB` of space.
{% endhint %}

In this example, the application will benefit from having a file browser, so we'll install [the FileBrowser application](../storage/filebrowser.md) from the Applications Catalog, and configure it with an equally recognizable name:

<figure><img src="../.gitbook/assets/image (10) (2).png" alt="Screenshot: A FileBrowser instance named after the application to which it will be associated"><figcaption><p>A FileBrowser instance named after the application to which it will be associated</p></figcaption></figure>

## Build the Deployment manifest

Containerized applications are deployed onto CoreWeave Cloud using [Kubernetes Deployment manifests](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). Every detail of how the application's container will be deployed into Kubernetes - including which storage volumes to attach, and what resources are to be allocated for the application's use - is declared in the application's manifest.

Each Deployment consists of an `.apiVersion` section, a `.kind` section, a `.metadata` section, and a `.spec` section. Actual container specifications are defined in the `.spec` section.

The example manifest below demonstrates how our example [Kobold AI](https://koboldai.net/) application will be deployed into CoreWeave Kubernetes:

{% hint style="info" %}
**Additional Resources**

Deployment manifests are a fundamental component of Kubernetes. Refer to [the official documentation on Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#writing-a-deployment-spec) for more information on how to compose Deployments.
{% endhint %}

### Example manifest

The following is a complete example manifest deploying an instance of Kobold AI. The construction of this manifest is broken down below.

<details>

<summary>Click to expand - <code>kobol-ai.yaml</code></summary>

<pre class="language-yaml"><code class="lang-yaml">apiVersion: apps/v1
kind: Deployment
metadata:
  name: koboldai-test
spec:
  strategy:
    type: Recreate
  replicas: 1
  selector:
     matchLabels:
      app.kubernetes.io/name: koboldai-test
  template:
    metadata:
      labels:
        app.kubernetes.io/name: koboldai-test
<strong>    spec:
</strong>      containers:
        - name: koboldai
          image: &#x3C;MY URL>:koboldai/koboldai:3
          resources:
            limits:
              cpu: 8
              memory: 64Gi
              nvidia.com/gpu: 1
          volumeMounts:
            - name: kobold-ai-data
              mountPath: /kobold-ai-data
      volumes:
        - name: kobold-ai-data
          persistentVolumeClaim:
            claimName: "kobold-ai-data"
<strong>      affinity:
</strong>        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: gpu.nvidia.com/class
                operator: In
                values:
                  - A40
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: topology.kubernetes.io/region
                operator: In
                values:
                  - LGA1
</code></pre>

</details>

### Define the application's resources

#### `.spec.containers.resources`

The resources required for the application are specified in the Deployment manifest within the `spec` block.

```yaml
   spec:
      containers:
        - name: <container-name>
          image: koboldai/koboldai:<version>
          resources:
            limits:
              cpu: 8
              memory: 64Gi
              nvidia.com/gpu: 1
```

Here, the container is defined by the YAML list within this block. First, the container `name` is specified (`spec.containers.name`). Then, the image that is to be used to create the container is given (`spec.containers.name.image`).

{% hint style="info" %}
**Note**

Kubernetes uses the Docker Hub public registry as its default container image registry. This means that unless the full URL of an alternative repository is explicitly set in the `image` field, Kubernetes will automatically search for the given name and tag pairing (in this example, that is `koboldai/koboldai:3`) in the public Docker Hub registry.

Because the image in this example _is_ being sourced from Docker Hub, the given URL is not more specific in this example.

[Learn more about how Kubernetes handles images in the official documentation](https://kubernetes.io/docs/concepts/containers/images/#image-names).
{% endhint %}

Finally, the CoreWeave Cloud resources to be allocated to the container are defined in the `resources` block. In the given example, the resources defined for the Kobold AI container are given solely in terms of `limits`. This means that the container's maximum resource consumption limit is restricted to only those resources that are explicitly set by the manifest.

{% hint style="info" %}
**Additional Resources**

Learn more about limits and requests in [the Kubernetes official documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
{% endhint %}

In this case, that means that the container may have up to `8` CPUs, up to `64Gi` of memory, and up to one NVIDIA GPU. The specific _type_ of NVIDIA GPU to use is set using `affinities`.

### Associate the storage volume (if applicable)

#### `.spec.volumes`

The persistent storage volume [created earlier](custom-containers.md#create-a-storage-volume) is associated with the application in the Deployment manifest in the `spec.volumes` stanza, within the `spec.volumes.persistentVolumeClaim.claimName` field specifically.

The value of this field will need to exactly match the name of the storage volume created for the application, as demonstrated in this excerpted stanza from [the example manifest](custom-containers.md#example-manifest) above:

```yaml
      volumes:
        - name: kobold-ai-data
          persistentVolumeClaim:
              claimName: "kobold-ai-data"
```

Additionally, as shown in the same example manifest, the `volumeMounts` block immediately preceding the `volumes` block defines to which path on the container the storage volume will be mounted:

```yaml
          volumeMounts:
            - name: kobold-ai-data
              mountPath: /kobold-ai-data
```

This dictates that the storage volume defined in `.spec.volumes` will be mounted to the `mountPath` of `/kobold-ai-data` on the Pods.

## Define Kubernetes affinities

#### `.spec.affinity`

[Kubernetes `affinities`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) are used to assign specific workloads to specific node types. On CoreWeave, they are used to determine on which node types workloads should run, as well in which [data center region](../data-center-regions.md) workloads should run.

### Define the node types

On CoreWeave Cloud, affinities are used to select [the CoreWeave node type](../../coreweave-kubernetes/node-types.md) you'd like a workload to run on.

In [the example manifest](custom-containers.md#example-manifest) given above, the `spec.affinity` block declares that the type of GPU the workloads should run on is an `NVIDIA A40`. The `matchExpressions` list contains the key-value set `key: gpu.nvidia.com/class`, which defines that an NVIDIA GPU will be used for these workloads.

Below that, the `values` list includes one item, `A40`, declaring that the specific GPU node type to use will be `A40`.

```yaml
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: gpu.nvidia.com/class
                operator: In
                values:
                  - A40
```

{% hint style="info" %}
**Additional Resources**

For more information on node types and their affinities for use with Deployment manifests, see [Node Types](../../coreweave-kubernetes/node-types.md).
{% endhint %}

#### Node type fallback options

Fallback options can be included by adding other node type values to this list; node types will be selected in the order of the list. For example:

```yaml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu.nvidia.com/class
            operator: In
            values:
              - A40
              - A6000
```

In this case, an `A6000` will be selected as a fallback option should the container cannot be scheduled to an `A40` for some reason.

{% hint style="info" %}
**Note**

The resource section and the affinity section is unique to CoreWeave servers - other examples of affinities found outside of CoreWeave's documentation are likely differ.
{% endhint %}

### Define the region

It is particularly important that if your application is using a storage volume, as has been true for our example, it is important to assign the workload's data center region to the same one to which [the associated storage volume](custom-containers.md#create-a-storage-volume-optional) was deployed.

For this example, our storage volume was deployed to `LGA1`, so the application's manifest is given the affinity to only schedule workloads on nodes in the same region:

```yaml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/region
            operator: In
            values:
              - LGA1
```

## Apply the Deployment

Once the Deployment is complete, deploy the manifest using `kubectl`:

```bash
$ kubectl apply -f <filename>.yaml
```

For example, if we were to launch this application, the command would be...

```bash
$ kubectl apply -f kobald-ai.yaml
```

...with the expected output:

```bash
deployment.apps/koboldai-test created
```

After deploying the manifest, view the running Pods that the Deployment has just created using `kubectl get pods`:

```
NAME                                                      READY   STATUS    RESTARTS   AGE
koboldai-test-844567464d-6r6cb                            1/1     Running   0          119s
```

:tada: Congratulations, your application is now deployed onto CoreWeave Cloud!

{% hint style="info" %}
**Additional Resources**

For additional and more advanced examples of containerized application Deployments, see [the Examples section](../../coreweave-kubernetes/examples/).
{% endhint %}
