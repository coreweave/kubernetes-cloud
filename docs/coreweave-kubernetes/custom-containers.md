---
description: Deploy containerized applications onto CoreWeave Cloud
---

# Custom Containers

This guide walks through the steps necessary to deploy a basic containerized application onto CoreWeave Cloud. The configurations implemented in the following example are intentionally kept simple, although [many additional configuration options are available](../virtual-servers/deployment-methods/kubectl.md#configuration-quick-reference).

This guide presumes that you already have an active CoreWeave Cloud account, and have already configured and installed a kubeconfig file for use with CoreWeave Kubernetes. It also assumes you have an application that has already successfully been containerized using Docker or a similar container runtime.

If you have not already completed these steps, first visit [Get Started with CoreWeave](getting-started.md).

{% hint style="info" %}
**Additional Resources**

For an even more pared down example of Deployments, refer to Kubernetes' official example, [Run a Stateless Application Using a Deployment](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/).&#x20;
{% endhint %}

## Prepare the container registry

To deploy a custom application that has been locally built, the image must first be pushed to an image repository.

CoreWeave provides an easy way to deploy a Docker Registry instance into your namespace for this purpose by installing the [Docker Registry application](https://docs.docker.com/registry/) via [the applications Catalog](serverless/applications-catalog.md). Once deployed, the Docker Registry instance may be configured for access both within and outside of the CoreWeave environment.

{% hint style="warning" %}
**Important**

Public repositories are not currently supported by Docker Registry on CoreWeave.
{% endhint %}

All requests to the registry are always authenticated. Credentials are automatically provisioned into a `imagePullSecret` in the namespace as they are configured during setup or auto-generated for you.

{% hint style="info" %}
**Note**

In the example below, an instance of [Kobold AI](https://koboldai.net/) will be pushed onto CoreWeave Cloud, whose image is sourced from an already publicly available image repository.
{% endhint %}

The default [Service Account](https://cloud.google.com/iam/docs/understanding-service-accounts) is also optionally patched to always use this pull secret, so that Pods deployed in the namespace will always have access to the images in the registry. Alternatively, you may opt to create a separate Service Account during the application deployment process that can be used on a Pod to allow pulling from the container registry without specifying a image pull secret.

{% hint style="info" %}
**Additional Resources**

For more information on Docker Registry, see [the official Docker documentation](https://docs.docker.com/registry/).
{% endhint %}

### Storage backends

[CoreWeave's S3-compatible Object Storage](../storage/object-storage.md) may be used as a backend storage solution for the container registry, or a [persistent volume](../storage/storage/) may be configured as a backend.

## Install Docker Registry into your CoreWeave namespace

To install the Docker Registry application, first log in to your CoreWeave Cloud account, then navigate to the applications Catalog.

From the Catalog homepage, search for `docker`. Then select the version of the Docker Registry application that you'd like to deploy.

<figure><img src="../.gitbook/assets/image (8).png" alt="Screenshot of docker-registry in the applications Catalog"><figcaption><p>Locate the docker-registry application in the applications Catalog</p></figcaption></figure>

Clicking on the application card will open the deployment page, which contains further information about the application itself. Clicking the **Deploy** button will navigate to the application's settings screen, where the instance is configured.

Finally, click the **Deploy** button in the bottom right-hand corner of the screen to launch the instance. Once the application is deployed to the configured specifications, you will be redirected to the application's status page.

From this page, access the **Application Secrets** from the section at the top right-hand part of the screen. Clicking the eye icon beside each field will reveal the field's contents. This secrets area contains the registry password - either that which was configured previously, or the new randomly-generated password.

<figure><img src="../.gitbook/assets/image (10) (2) (1).png" alt=""><figcaption><p>The application secrets include the configured or randomly-generated registry password</p></figcaption></figure>

Alternatively, to retrieve the registry credentials via the command line, run the following Kubectl command.

{% hint style="info" %}
**Note**

The installation notes on the application's deployment screen provides all of the following commands, with your namespace and URL already addeK.
{% endhint %}

{% code overflow="wrap" %}
```bash
$ kubectl get --namespace <NAMESPACE> secret test-docker-registry-secret -o=go-template='{{ printf "username: %s\npassword: %s" (.data.username | base64decode) (.data.password | base64decode) }}'
```
{% endcode %}

Following along with the installation notes provided on this screen, to log in to your Docker Registry instance, first export the `REGISTRY_USERNAME` to the username accessible via `kubectl get secret`:

{% code overflow="wrap" %}
```bash
$ export REGISTRY_USERNAME=$(kubectl get secret test-docker-registry-secret -o=go-template='{{ .data.username | base64decode }}')
```
{% endcode %}

Next, log in to the Docker Registry instance using `docker login` while sourcing your credentials using `kubectl`:

{% code overflow="wrap" %}
```bash
$ kubectl get --namespace <NAMESPACE> secret test-docker-registry-secret \
        -o=go-template='{{ .data.password | base64decode }}' \
        | docker login <PROVIDED URL> -u $REGISTRY_USERNAME --password-stdin
```
{% endcode %}

If you are not using Kubectl, you can use `docker login` normally by using `docker login` and entering the registry password when prompted:

{% code overflow="wrap" %}
```bash
$ docker login <REGISTRY NAME>.<COREWEAVE URL> -u docker
```
{% endcode %}

Congratulations! You can now build and push images to your Docker Registry instance hosted on CoreWeave Cloud!

For example, if your Dockerfile is in your local current working directory, you can build the image:

{% code overflow="wrap" %}
```bash
$ docker build -t <URL>/<APP NAME>:<TAG VERSION> .
```
{% endcode %}

Then push the built image to your new registry:

{% code overflow="wrap" %}
```bash
$ docker push <URL>/<APP NAME>:<TAG VERSION>
```
{% endcode %}

{% hint style="warning" %}
**Important**

Never use the `latest` tag; always push to a new tag. Due to aggressive caching for faster repeat spin-up times, re-using tags will lead to some of your Pods running an out of date version of your code.
{% endhint %}

## Create a storage volume

If your application requires storage, you'll need to create a storage volume. To do this, navigate to the **Storage** page from the CoreWeave Cloud homepage. [Create a storage volume](../storage/storage/using-storage-cloud-ui.md#creating-storage-volumes), giving it a name that is easy to associate with the relevant application.

Optionally, if your application may benefit from having a visual file browser, install [the FileBrowser application](../storage/filebrowser.md), configured with an equally recognizable name.

<figure><img src="../.gitbook/assets/image (7) (3).png" alt="Screenshot of a PVC volume and the FileBrowser application installed in the namespace"><figcaption><p>For the Kobold AI example, we have created both a PVC storage volume (left) and a FileBrowser instance (right)</p></figcaption></figure>

If your application requires a lot of storage, it is recommended to configure a PVC with at least 1TB of space, similar to the configuration settings determined for this example.

## Build the Deployment

Containerized applications are deployed onto CoreWeave Cloud using [Kubernetes YAML Deployment manifests](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). Every detail of how the application container will be deployed into Kubernetes - including which storage volumes to attach, and what resources are to be allocated for the application's use - is described in the application's manifest.

The YAML manifest below demonstrates how the example Kobol AI application will be deployed into CoreWeave Kubernetes.

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
          image: koboldai/koboldai:latest
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
</code></pre>

</details>

Each Deployment consists of an `.apiVersion` section, a `.kind` section, a `.metadata` section, and a `.spec` section. The actual container specifications are defined in the `.spec` section.

{% hint style="info" %}
**Additional Resources**

Deployment manifests are a fundamental component of Kubernetes. Refer to [the official documentation on Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#writing-a-deployment-spec) for more information on how to compose Deployments.
{% endhint %}

### Storage

The persistent storage volume created earlier is associated with the application in the Deployment manifest in the `volumes.persistentVolumeClaim.claimName` field.

The value of this field will need to match the name of the storage volume you've created for your application, as demonstrated in this piece of the example manifest above:

```yaml
      volumes:
        - name: kobold-ai-data
          persistentVolumeClaim:
              claimName: "kobold-ai-data"
```

Additionally, as shown in the example manifest, the `volumeMounts` block immediately preceding the `volumes` block defines to which path on the container the storage volume will be mounted:

```yaml
          volumeMounts:
            - name: kobold-ai-data
              mountPath: /kobold-ai-data
```

This means that the storage volume defined in `.volumes` will be mounted to the `mountPath` of `/kobold-ai-data` on the container.

### Resources

The resources required for the application are specified in the Deployment manifest within the `spec` block.

```yaml
   spec:
      containers:
        - name: koboldai
          image: koboldai/koboldai:latest
          resources:
            limits:
              cpu: 8
              memory: 64Gi
              nvidia.com/gpu: 1
```

The `koboldai` container is defined by the YAML list within this block. First, the container `name` is specified (`spec.containers.name`). Then, the image that is to be used to create the container is given (`spec.containers.name.image`).

{% hint style="info" %}
**Note**

Kubernetes' default image repository is the Docker Hub public registry. This means that unless the full URL of an alternative repository is explicitly set in the `image` field, Kubernetes will automatically search for the given name and tag pairing (in this example, that's `koboldai/koboldai:latest`) in the public Docker Hub registry matching those names and tags. This is also why the given URL is not more specific in this example. [Learn more about how Kubernetes handles images in the official documentation](https://kubernetes.io/docs/concepts/containers/images/#image-names).
{% endhint %}

Finally, the CoreWeave Cloud resources to be allocated to the container are defined in the `resources` block. In the given example, the resources defined for the Kobold AI container are given solely in terms of `limits`. This means that the container's maximum resource consumption limit is restricted to only those resources that are explicitly set by the manifest.

{% hint style="info" %}
**Additional Resources**

Learn more about limits and requests in [the Kubernetes official documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
{% endhint %}

In this case, that means that the container may have up to `8` CPUs, up to `64Gi` of memory, and up to one NVIDIA GPU. The specific _type_ of NVIDIA GPU to use is set using `affinities`.

### Affinities

In Kubernetes, `affinities` are used to assign specific pods to specific nodes. In CoreWeave Cloud, affinities are also used to select [the CoreWeave node type](../../coreweave-kubernetes/node-types.md) you'd like a container to run on.

In the example given above, the `spec.affinity` block dictates that the type of GPU the container should run on is an NVIDIA A40.

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

The `matchExpressions` list contains the `key: gpu.nvidia.com/class` key value set, which defines that an NVIDIA GPU will be used for this container. Below that, the `values` list includes one item, `A40`, specifying that the GPU node type to use will be an A40. Fallback options can be included by adding other node type values to this list; node types will be selected in the order of the list. For example:

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
              - A100_PCIE_40GB
```

In this case, an A100 PCIE 40GB will be selected as a fallback option should the container cannot be scheduled to an A40 for some reason.

{% hint style="info" %}
**Note**

The resource section and the affinity section is unique to CoreWeave servers - other examples of affinities found outside of CoreWeave's documentation are likely differ.
{% endhint %}

## Apply the Deployment

Finally, once the Deployment is complete, deploy the manifest using `kubectl`.

```bash
$ kubectl apply -f <filename>yaml.
```

For example, if we were to launch this application, the command would be...

```bash
$ kubectl apply -f kobald-ai.yaml
```

...with expected output:

```bash
deployment.apps/koboldai-test created
```

After deploying the manifest, view the running Pods that the Deployment has just created using `kubectl get pods`.

```
NAME                                                      READY   STATUS    RESTARTS   AGE
koboldai-test-844567464d-6r6cb                            1/1     Running   0          119s
```

:tada: Congratulations, your application is now deployed onto CoreWeave Cloud!

{% hint style="info" %}
**Additional Resources**

For additional, more advanced examples of Deployments, see [the Examples section](../../coreweave-kubernetes/examples/).
{% endhint %}
