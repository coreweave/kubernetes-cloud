---
description: >-
  Deploy GPT-J or GPT-NeoX using NVIDIA Triton Inference Server with the
  FasterTransformer backend
---

# Triton Inference Server - FasterTransformer GPT-J and GPT-NeoX 20B

In this example, we'll demonstrate how to deploy EleutherAI GPT-J and GPT-NeoX on [NVIDIA Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server) with the [FasterTransformer](https://github.com/NVIDIA/FasterTransformer) backend via an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) using an HTTP API to perform Text Generation. This deployment will run on a [CoreWeave Cloud NVIDIA RTX A5000 and A6000 GPUs](../../../coreweave-kubernetes/node-types.md), with Autoscaling and Scale-to-Zero enabled.

<figure><img src="../../.gitbook/assets/Screen Shot 2022-08-10 at 2.25.16 PM.png" alt="A diagram demonstrating the architecture utilized in this demo"><figcaption><p>The architecture utilized in this demo</p></figcaption></figure>

## What is FasterTransformer?

> _In NLP, encoder and decoder are two important components, with the transformer layer becoming a popular architecture for both components. FasterTransformer implements a highly optimized transformer layer for both the encoder and decoder for inference. On Volta, Turing and Ampere GPUs, the computing power of Tensor Cores are used automatically when the precision of the data and weights are FP16._
>
> _FasterTransformer is built on top of CUDA, cuBLAS, cuBLASLt and C++. We provide at least one API of the following frameworks: TensorFlow, PyTorch and Triton backend. Users can integrate FasterTransformer into these frameworks directly. For supporting frameworks, we also provide example codes to demonstrate how to use, and show the performance on these frameworks._

\- [NVIDIA FasterTransformer](https://github.com/NVIDIA/FasterTransformer/blob/main/README.md)

FasterTransformer provides up to 40% faster GPT-J inference over an implementation based on vanilla [Hugging Face Transformers](https://huggingface.co/docs/transformers/index). FasterTransformer also supports multi-GPU inference for additional speed for handling large models. Streaming of partial completions, token by token, is also supported.

**To follow along with this example, view and pull the code on CoreWeave's GitHub:**

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/fastertransformer" %}

## Prerequisites

The following tools must be installed prior to running the demo:

* [kubectl](https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools)
* [Docker](https://docs.docker.com/get-docker/) and a [Docker Hub](https://hub.docker.com/) account
* An active CoreWeave account (with [kubeconfig configured for access credentials](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials))

## Overview

No modifications are needed to any of the files to follow along. The general procedure for this example is:

1. Build and push the Docker image to a container registry (in this case, [Docker Hub](https://hub.docker.com/)).
2. Deploy the Kubernetes resources:
   1. a PVC in which to store the model.
   2. a Batch Job used to download the model. **The model is quite large at roughly 45Gi, and will take around 15-20 minutes to complete the download.**
   3. the CoreWeave InferenceService.
3. Perform Text Generation using the model by sending HTTP requests to the InferenceService.

## Procedure

### Building and pushing the Docker image

Once the example code is cloned to your local machine, enter the `build` directory. From here, `build` and `push` the Docker image to your Docker Hub repository.

Ensure you are logged in to Docker, and make sure the `DOCKER_USER` environment variable is set:

```bash
$ docker login
$ export DOCKER_USER=coreweave
```

{% hint style="warning" %}
**Important**

The default Docker tag is `latest`. We strongly **discourage** you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack.

Once you have pushed to a tag, **do not push to that tag again**. Below, we use simple versioning, using tag `1` for the first iteration of the image, and so on.
{% endhint %}

From the `kubernetes-cloud/online-inference/fastertransformer/build` directory, build and push the image:

```bash
$ docker build -t $DOCKER_USER/fastertransformer-triton:1
$ docker push $DOCKER_USER/fastertransformer-triton:1
```

{% hint style="info" %}
**Note**

This example assumes a public docker registry. To use a private registry, an [imagePullSecret ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)needs to be defined.

Be sure to configure any usernames in the following examples with your actual Docker Hub username.
{% endhint %}

### Deploying the Kubernetes resources

#### PVC

{% hint style="info" %}
**Note**

Before continuing, you may either point the `image: $DOCKER_USER/fastertransformer-triton:1`in the following manifests to the image we just built in the previous steps, or you may use the publicly-available image found in the following manifest:

* `ft-inference-service-gptj.yml`
* `ft-inference-service-neox.yml`
{% endhint %}

To create a PVC in which to store the model, navigate to the `kubernetes-cloud/online-inference/fastertransformer/` directory, then run:

```bash
$ kubectl apply -f model-storage-pvc.yml
```

{% tabs %}
{% tab title="GPT-J" %}
### Model job download

To deploy the job to download the model to the PVC, navigate to the `kubernetes-cloud/online-inference/fastertransformer/` directory, then run:

```bash
$ kubectl apply -f download-weights-job-gptj.yml
```



This job performs the following:

* downloads the GPT-J weights into the PVC at `/mnt/pvc/models/gptj-store`
* installs the required packages to convert them to FasterTransformer format
* converts the packages to the FasterTransformer format, then stores them in the PVC at `/mnt/pvc/gptj-store/triton-model-store/fastertransformer/1/`
* passes the `config.pbtxt` file to set important parameters such as `tensor_para_size=1`, `pipeline_para_size=1, (1 GPU x 1 Pod)` and `model_transaction_policy { decoupled: False }`, which allows for streaming if set to `True`.\


{% hint style="info" %}
**Note**

The model is quite large at \~23Gi, and may take around 15-20 minutes for the download job to complete.
{% endhint %}



To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```bash
$ kubectl get jobs

NAME                        COMPLETIONS   DURATION      AGE
gptj-download                 1/1            24m        1h
```



Or, follow the job logs to monitor progress:

```bash
kubectl logs -l job-name=gptj-download --follow
```



### InferenceService

Once the model is downloaded, the `InferenceService` can be deployed by invoking:

```bash
$ kubectl apply -f ft-inference-service-gptj.yml
```

\
Due to the size of the model, loading into GPU memory can take around 5-10 minutes. To monitor the progress of this, you can wait to see the KServe workers start in the pod logs by invoking:

```bash
$ kubectl logs -f -l serving.kubeflow.org/inferenceservice=fastertransformer-triton-gptj kfserving-container
```

\
Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL:

```bash
$ kubectl get isvc

NAME                             URL                                                                                                          READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                                      AGE
fastertransformer-triton-gptj     http://fastertransformer-triton-gptj.tenant-demo.knative.chi.coreweave.com     True           100                              fastertransformer-triton-gptj-predictor-default-00001     2d5h
```
{% endtab %}

{% tab title="GPT-NeoX" %}
### Model job download

To deploy the job to download the model to the PVC, navigate to the `kubernetes-cloud/online-inference/fastertransformer/` directory, then run:

```
$ kubectl apply -f download-weights-job-gpt-neox.yml
```

\
This job performs the following:

* downloads the GPT-NeoX weights into the PVC at `/mnt/pvc/models/gpt-neox`
* installs the required packages to convert them to FasterTransformer format
* converts the packages to the FasterTransformer format, then stores them in the PVC at `/mnt/pvc/gptj-store/triton-model-store/fastertransformer/1/`
* passes the `config.pbtxt` file to set important parameters such as `tensor_para_size=1`, `pipeline_para_size=1, (1 GPU x 1 Pod)` and `model_transaction_policy { decoupled: False }`, which allows for streaming if set to `True`.



{% hint style="info" %}
**Note**

The model is quite large at \~39Gi (mirror to pull from Europe), and may take around 3-5 hours for the download and conversion job to complete.
{% endhint %}



To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```bash
$ kubectl get jobs

NAME                           COMPLETIONS   DURATION      AGE
gpt-neox-download                 1/1            24m        1h
```



Or, follow the job logs to monitor progress:

```bash
$ kubectl logs -l job-name=gpt-neox-download --follow
```



### InferenceService

Once the model is downloaded, the `InferenceService` can be deployed by invoking:

```bash
$ kubectl apply -f ft-inference-service-neox.yml
```

\
Due to the size of the model, loading into GPU memory can take around 5-10 minutes. To monitor the progress of this, you can wait to see the KServe workers start in the pod logs by invoking:

```bash
$ kubectl logs -f -l serving.kubeflow.org/inferenceservice=fastertransformer-triton-neox kfserving-container
```

\
Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL:

```bash
$ kubectl get isvc

NAME                             URL                                                                                                          READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                                      AGE
fastertransformer-triton-neox     http://fastertransformer-triton-neox.tenant-demo.knative.chi.coreweave.com     True           100                              fastertransformer-triton-neox-predictor-default-00001     5h54m
```
{% endtab %}
{% endtabs %}

### Using the Python Inference Client

Once you have the `InferenceService` up and running, you should be able to query FasterTransformer via the HTTP API to generate text based on a conditional prompt.

From the `kubernetes-cloud/online-inference/fastertransformer/client` directory, login to Docker:

```bash
$ docker build -t $DOCKER_USER/fastertransformer-triton-client:1
```

Set the value for the `SERVICE` variable:

{% hint style="info" %}
**Note:**

* **DO NOT** append `http://` to `SERVICE` below.
* Use either GPTJ (or) GPT-Neox Inference Service URL for `--url`
* Use `gptj or gpt-neox` for `--model`
{% endhint %}

```bash
$ export SERVICE=fastertransformer-triton-gptj.tenant-demo.knative.chi.coreweave.com
```

Then `run` the image:

```bash
$ docker run $DOCKER_USER/fastertransformer-client:1 --url=$SERVICE --model=gptj (or) gpt-neox  --prompt="Mary has a little lamb."
```

The resulting output should resemble the following:

```bash
$ docker run $DOCKER_USER/fastertransformer-client:1 --url=$SERVICE --model=gptj --prompt="Mary has a little lamb."

Mary has a little lamb. Its fleece is white as snow, and everywhere that Mary walks, the lamb is sure to be sure-footed behind her. It loves the little lambs.
```

{% hint style="info" %}
**Note**

To set and change parameters, view the `sample_request.json` file.

`example.py` provides simple methods to use the Python Triton client with FasterTransformer via HTTP.
{% endhint %}

## Hardware and performance

### GPT-J

This example is set to use one NVIDIA RTX A5000 PCIe GPU. CoreWeave has performed [prior benchmarking](https://docs.google.com/spreadsheets/d/1HGQKoYgO0H2y7-DmIiIZhLmGU8vZPH8FoojXG7zj6-o/edit#gid=0) to analyze performance of Triton with FasterTransformer against the vanilla Hugging Face version of GPTJ-6B.

### **Key observations**

* `tokens_per_second` using FasterTransformer GPTJ vs. Hugging Face on one A5000 GPU is about **30%** **faster** in general.
* Using multiple (four) GPUS, we have observed average speedups for GPTJ of **2X** vs. 1 GPU on Hugging Face.

### GPT-NeoX 20B

This example is set to use one NVIDIA RTX A6000 PCIe GPU. On a single A6000 GPU, the average tokens per second for a 1024 token input context is **15.6 tokens/second.** For additional performance, FasterTransformer supports running over multiple GPUs.

### Autoscaling

Scaling is controlled in the `InferenceService` configuration. This example is set to always run one replica, regardless of number of requests.

Increasing the number of `maxReplicas` will allow the CoreWeave infrastructure to automatically scale up replicas when there are multiple outstanding requests to your endpoints. Replicas will automatically be scaled down as demand decreases.

#### Example

```yaml
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 1
```

By setting `minReplicas` to `0`, Scale-to-Zero can be enabled, which will completely scale down the `InferenceService` when there have been no requests for a period of time.

{% hint style="info" %}
**Note**

When a service is scaled to zero, no cost is incurred.

Please note that due to the size of the GPT-J model, Scale to Zero will lead to long request completion times if the model has to be scaled from zero. This can take around 5-10 minutes.
{% endhint %}

For more information on autoscaling, refer to [the official Kubernetes documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
