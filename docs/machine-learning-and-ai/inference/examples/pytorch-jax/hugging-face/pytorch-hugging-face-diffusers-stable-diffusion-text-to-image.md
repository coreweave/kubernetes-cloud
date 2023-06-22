---
description: >-
  Deploy Stable Diffusion for scalable, high fidelity, text-to-image generation
  on CoreWeave Cloud
---

# Stable Diffusion: Text to Image

The [Stable Diffusion](https://huggingface.co/CompVis/stable-diffusion-v1-4) open source diffusion model, built by our friends at [Stability.AI](https://stability.ai/), takes a text prompt as input to generate high-quality images with photorealistic capabilities. Stability.AI also offers a UI for the model and an API service via [Dream Studio](https://beta.dreamstudio.ai/).

The following tutorial is a step-by-step guide to deploy Stable Diffusion as an autoscaling Inference Service on CoreWeave Cloud that provides an HTTP API in order to generate images from a text prompt.

<figure><img src="../../../../../.gitbook/assets/red-forest.png" alt=""><figcaption><p>An image generated from the prompt: "Red forest, digital art, trending"</p></figcaption></figure>

## Tutorial code

To follow along with this tutorial, clone the source code from CoreWeave's GitHub:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/stable-diffusion" %}

## Prerequisites

For this tutorial, the following tools are required:

* [kubectl](https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools)
* [docker](https://docs.docker.com/get-docker/)
* A CoreWeave Cloud account ([with Kubectl configured to use your CoreWeave kubeconfig](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials))
* A [Docker Hub](https://hub.docker.com/) account
* A [Hugging Face](https://huggingface.co/) account with an [API Token](https://huggingface.co/settings/tokens)
  * [Completed registration](https://huggingface.co/CompVis/stable-diffusion-v1-4) for model usage - due to the generative power of this model, it is necessary to register your contact information via Hugging Face before the model can be used

{% hint style="success" %}
**Tip**

Optionally, but highly recommended, is the use of CoreWeave's serialization library, [Tensorizer](pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md#tensorizer), which serializes the Stable Diffusion model in order to make model serving lightning fast and considerably more cost-effective.\
\
[Learn more about Tensorizer](../../../tensorizer.md).
{% endhint %}

## Docker images

The tutorial requires two images. The downloader image may be sourced from [its public image](https://github.com/wbrown/gpt\_bpe). The model image may either be built locally and pushed to a container image registry, or may also be sourced from the publicly available images.

<table><thead><tr><th width="200.33333333333331">Kind</th><th width="335">Description</th><th>Public image source</th></tr></thead><tbody><tr><td><strong>The downloader image</strong></td><td><p>This image downloads the model to a <a href="../../../../../storage/storage/">shared storage volume</a>. The individual inference Pods will load the model from this storage so as to avoid downloading it over the internet every time they scale up.</p><p></p><p>Referenced in the <a href="../../../../../../online-inference/stable-diffusion/02-model-download-job.yaml">02-model-download-job.yaml</a> file.</p></td><td><code>ghcr.io/wbrown/gpt_bpe/model_downloader:6d77d9c</code></td></tr><tr><td><strong>The model image</strong></td><td><p>Runs the <code>CompVis/stable-diffusion-v1-4</code> model.</p><p></p><p>Referenced in the <a href="../../../../../../online-inference/stable-diffusion/03-inference-service.yaml">03-inference-service.yaml</a> file.</p></td><td><code>harubaru1/stable-diffusion:17</code></td></tr></tbody></table>

### Build the model image from a Dockerfile

To build the model image from a Dockerfile, first clone [the tutorial's source code](pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md#tutorial-code). Then, change directories into `kubernetes-cloud/online-inference/stable-diffusion`. From there, log in to Docker.

```bash
$ docker login
$ export DOCKER_USER=coreweave
```

{% hint style="warning" %}
**Important**

The default Docker tag is `latest`. Using this tag is **strongly** **discouraged**, as containers are cached on the nodes and in other parts of the CoreWeave stack. Always use a unique tag; never push to the same tag twice. Once you have pushed to a tag, **do not** **push to that tag again**.
{% endhint %}

A simple versioning scheme is implemented by using the tag `1` for the first iteration of the image, and so on. Build the `stable-diffusion` model image using `docker build` in the current directory.

```bash
$ docker build -t $DOCKER_USER/stable-diffusion:1 -f Dockerfile . 
```

{% hint style="info" %}
**Note**

This example assumes a public Docker registry. To use a private registry, an [`imagePullSecret` ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)must first be defined.
{% endhint %}

Finally, push both images with an initial tag of `1`, or whatever other simple tagging scheme you'd like to use.

```bash
$ docker build -t $DOCKER_USER/stable-diffusion:1 -f Dockerfile . 
```

## Deploy Kubernetes resources

In the manifests discussed below, you may either point the `image` in the following manifests to the image built earlier, or you may use the publicly-available images, as are referenced in the following manifests:

### PVC

The `00-model-pvc.yaml` file deploys the Persistent Volume Claim (PVC) in which the model will be stored. To create it, apply the `00-model-pvc.yaml` file.

```bash
$ kubectl apply -f 00-model-pvc.yaml
```

### Model Repository Registration

Due to the generative power of this model, it is necessary to register your contact information via Hugging Face before the model can be used. If you have not already done so, create a [Hugging Face](https://huggingface.co/) account and [API Token.](https://huggingface.co/settings/tokens)

To do this, ensure you are logged in to the Hugging Face, then navigate to the[ HuggingFace Model Repository page](https://huggingface.co/CompVis/stable-diffusion-v1-4).

### Secret

From [the Access Token page in your Hugging Face profile settings](https://huggingface.co/settings/tokens), locate an existing token or generate a new token. Copy its contents, then Base64-encode it using `base64`.

```bash
$ echo -n "<YOUR TOKEN>" | base64

VE9LRU5fSEVSRQ==
```

In the `01-huggingface-secret.yaml` file, replace the `token` value with the newly generated Base64-encoded token. Then, create the secret using `kubectl create`.

```bash
$ kubectl create -f 01-huggingface-secret.yaml
```

### Model job download

To deploy the job that downloads the model to the PVC, `apply` the `02-model-download-job.yaml` file from the `kubernetes-cloud/online-inference/stable-diffusion/` directory.

```bash
$ kubectl apply -f 02-model-download-job.yaml
```

To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```bash
$ kubectl get pods

NAME                              READY   STATUS      RESTARTS   AGE
stable-diffusion-download-vsznr   0/1     Completed   0          3h14m
```

Or, follow the job logs to monitor its progress:

```bash
$ kubectl logs -l job-name=stable-diffusion-download --follow
```

### InferenceService

Once the model has finished downloading, deploy the `InferenceService` by applying the `03-inference-service.yaml` file.

```bash
$ kubectl apply -f 03-inference-service.yaml
```

Loading up the model into GPU memory may take a couple of minutes. To monitor the progress of this, wait to see the KServe workers start in the Pod logs.

{% code overflow="wrap" %}
```bash
$ kubectl logs -l serving.kubeflow.org/inferenceservice=stable-diffusion --container kfserving-container
```
{% endcode %}

Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL.

```bash
$ kubectl get isvc stable-diffusion  
                                                                   
NAME               URL                                                                              READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                        AGE
stable-diffusion   http://stable-diffusion.tenant-example-example.knative.chi.coreweave.com   True           100                              stable-diffusion-predictor-default-00001   64m
```

Using the provided URL, you can make an HTTP request via your preferred means.

Here is an example utilizing cURL:

{% code overflow="wrap" %}
```bash
curl http://stable-diffusion.tenant-example-example.knative.chi.coreweave.com/v1/models/stable-diffusion-v1-4:predict -d '{"prompt": "California sunset on the beach, red clouds, Nikon DSLR, professional photography", "parameters": {"seed": 424242, "width": 768}}' --output sunset.png \
&& open sunset.png
```
{% endcode %}

<figure><img src="../../../../../.gitbook/assets/sunset.png" alt="Generated photo of a sunset. An image generated from the prompt: &#x22;California sunset on the beach, red clouds, Nikon DSLR, professional photography&#x22;"><figcaption><p>An image generated from the prompt: "California sunset on the beach, red clouds, Nikon DSLR, professional photography"</p></figcaption></figure>

## Supported request parameters

The following request parameters are supported:

* `guidance_scale`
* `num_inference_steps`
* `seed`
* `width`
* `height`

Parameters may be passed in per request. For example:

{% code overflow="wrap" %}
```shell-session
$ curl http://stable-diffusion.tenant-example-example.knative.chi.coreweave.com/v1/models/stable-diffusion-v1-4:predict -d \ '{"prompt": "California sunset on the beach, red clouds, Nikon DSLR, professional photography", "parameters": {"guidance_scale": 14.0, "num_inference_steps"
: 100, "seed": 424242, "width": 1024, "height": 768}}' --output sunset.png \
&& open sunset.png
```
{% endcode %}

## Hardware and performance

This example is set to one A40 node for the production of higher resolution images. Inference times are around `4.78` seconds for a default resolution of `512x512` with `50` steps. Larger resolutions take longer - for example, a resolution of `1024x768` takes around `47` seconds.

{% hint style="info" %}
**Note**

Multi-GPU Inference is not supported.
{% endhint %}

Depending on use case, GPUs with less VRAM will also work down to 8GB GPUs, such as the Quadro RTX 4000, however output resolution will be limited by memory to `512x512`.

### Benchmarks

The graph and table below compare recent GPU benchmark inference speeds for Stable Diffusion processing on different GPUs:

<figure><img src="../../../../../.gitbook/assets/image (7) (1) (1).png" alt="A graph displaying a comparison of benchmark inference times for Stable Diffusion on different GPUs"><figcaption></figcaption></figure>

<table><thead><tr><th width="336">GPU</th><th>Seconds</th></tr></thead><tbody><tr><td>Quadro RTX 4000</td><td>9.91</td></tr><tr><td>Quadro RTX 5000</td><td>7.94</td></tr><tr><td>A6000</td><td>4.45</td></tr><tr><td>A40</td><td>4.78</td></tr><tr><td>A100 40GB PCIE</td><td>3.35</td></tr><tr><td>A100 40GB NVLINK</td><td>3.29</td></tr><tr><td>A100 80GB NVLINK</td><td>3.19</td></tr><tr><td>AWS A100 40GB</td><td>4.10</td></tr></tbody></table>

{% hint style="info" %}
**Additional Resources**

Refer to the[ Node Types](https://docs.coreweave.com/coreweave-kubernetes/node-types) page for all available GPUs and their selectors.
{% endhint %}

### Autoscaling

Scaling is controlled in the `InferenceService` configuration. This example is set to always run one replica regardless of number of requests.

Increasing the number of `maxReplicas` will allow CoreWeave's infrastructure to automatically scale up replicas when there are multiple outstanding requests to your endpoints. Replicas will automatically be scaled down as demand decreases.

#### Example

```yaml
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 1
```

By setting `minReplicas` to `0`, Scale-to-Zero can be enabled, which will completely scale down the `InferenceService` when there have been no requests for a period of time. When a service is scaled to zero, no cost is incurred.

## Optional steps

The following additional steps are optional, but will allow for quicker and less resource-intensive spin-up by serializing the Stable Diffusion model through the use of our model serialization library, [Tensorizer](https://github.com/coreweave/tensorizer/).

### Tensorizer

[CoreWeave's Tensorizer](https://github.com/coreweave/tensorizer/) is a module, model, and tensor serializer/deserializer that makes it possible to load models in **less than 5 seconds**, making it easier and more cost-effective to serve the model at scale.

Because transfers occur nearly instantly to the GPU when using Tensorizer, the amount of CPU and RAM necessary for the instance is also reduced, resulting in lower incurred costs by a reduction in the amount of resources used.

{% embed url="https://github.com/coreweave/tensorizer/" %}

## Using CoreWeave Object Storage

Optionally, [CoreWeave Object Storage](../../../../../storage/object-storage.md) may be used for storing models. To use it, first [create both an access key and a secret key](../../../../../storage/object-storage.md#get-started). Then, create a bucket using the `s3cmd` tool:

```shell-session
$ s3cmd mb s3://BUCKET
```

Once you have generated an access key and a secret key, copy and Base64-encode both keys.

```shell-session
$ echo -n "<YOUR ACCESS KEY>" | base64
QUNDRVNTX0tFWV9IRVJF

$ echo -n "<YOUR SECRET KEY>" | base64
U0VDUkVUX0tFWV9IRVJF
```

You will also have to Base64-encode the hostname that you intend to use for storing the serialized model. For the purpose of this example, we will be using the `ORD1` region, where our hostname is the Object Storage endpoint URL `object.ord1.coreweave.com`.

```shell-session
$ echo -n "object.ord1.coreweave.com" | base64
b2JqZWN0Lm9yZDEuY29yZXdlYXZlLmNvbQ==
```

In the YAML manifest named `01-optional-s3-secret.yaml`, use these newly Base64-encoded values for the respective values of the `access_key`, `secret_key`, and `url` fields. Then, create the Secret:

```shell-session
$ kubectl create -f 01-optional-s3-secret.yaml
```

### Model Serialization Job

To serialize the Stable Diffusion model that has already been downloaded, deploy the serialization job from the `kubernetes-cloud/online-inference/stable-diffusion/` directory by applying its manifest (`02-optional-serialize-job.yaml`).

```shell-session
$ kubectl apply -f 02-optional-serialize-job.yaml
```

The serialized model will be written to the PVC that was created earlier.

### Object Storage upload job

In the `03-optional-s3-upload-job.yaml` file, edit the container's `args` field to use the created bucket, by replacing the `INSERT_BUCKET_HERE` placeholder with the bucket URL.

```yaml
 args:
  - >
    /usr/bin/s3cmd
    --access_key=${AWS_KEY}
    --secret_key=${AWS_SECRET}
    put --recursive --acl-public
    /mnt/models/CompVis/stable-diffusion-v1-4
    s3://<BUCKET URL>/
```

To upload the serialized model to [CoreWeave Object Storage](pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md#object-storage), apply the `03-optional-s3-upload-job.yaml` manifest, which initiates a job to upload the model.

```shell-session
$ kubectl apply -f 03-optional-s3-upload-job.yaml
```

{% hint style="danger" %}
**Warning**

Objects uploaded through the Upload Job are stored with ACL that allows public `read` permissions.
{% endhint %}

### Serialized model deployment

In order to deploy the serialized model from [CoreWeave Object Storage](pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md#object-storage), retrieve the public URI:

```
http://object.ord1.coreweave.com/<YOUR_BUCKET>/stable-diffusion-v1-4
```

Edit the `03-inference-service.yaml` file to supplement the public object URI, and include the `--tensorized` flag to the container's `command` arguments.

```yaml
containers:
  - name: kserve-container
    image: ghcr.io/coreweave/ml-containers/sd-inference:bb1ac67
    command:
      - "python3"
      - "/app/service.py"
      - "--model-id=http://object.ord1.coreweave.com/YOUR_BUCKET/stable-diffusion-v1-4"
      - "--tensorized"
```

Finally, to deploy the serialized model on an `InferenceService`, apply the inference service manifest using `kubectl`.

```shell-session
$ kubectl apply -f 03-inference-service.yaml
```

To verify the deployment, [run the same cURL command](pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md#inferenceservice) used to test the `InferenceService` deployment earlier.
