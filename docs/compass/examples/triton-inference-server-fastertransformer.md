---
description: >-
  Deploy GPT-J using NVIDIA Triton Inference Server with the FasterTransformer
  backend
---

# Triton Inference Server - FasterTransformer

### Introduction

This example demonstrates how to deploy [NVIDIA Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server) with the [FasterTransformer](https://github.com/NVIDIA/FasterTransformer) backend via an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) with a HTTP API to perform Text Generation. The deployment will run on CoreWeave Cloud NVIDIA RTX A5000 GPUs with Autoscaling and Scale To Zero.

![](<../../.gitbook/assets/Screen Shot 2022-08-10 at 2.25.16 PM.png>)

### What is Fastertransformer?

> In NLP, encoder and decoder are two important components, with the transformer layer becoming a popular architecture for both components. FasterTransformer implements a highly optimized transformer layer for both the encoder and decoder for inference. On Volta, Turing and Ampere GPUs, the computing power of Tensor Cores are used automatically when the precision of the data and weights are FP16.
>
> FasterTransformer is built on top of CUDA, cuBLAS, cuBLASLt and C++. We provide at least one API of the following frameworks: TensorFlow, PyTorch and Triton backend. Users can integrate FasterTransformer into these frameworks directly. For supporting frameworks, we also provide example codes to demonstrate how to use, and show the performance on these frameworks.

FasterTransformer provides up to 40% faster GPT-J inference over a vanilla Hugging Face Transformers based implementation. FasterTransformer also supports multi GPU inference for additional speed and to handle large models. Streaming of partial completions, token by token, is supported.

#### View the example code on GitHub:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/fastertransformer" %}

## Pre-requisites

The following pieces must be installed and configured prior to running the example.

* [kubectl](https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools)
* [docker](https://docs.docker.com/get-docker/)
* A Coreweave Account ([with Kubectl configured to use your Coreweave Kubeconfig](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials))
* A [Docker Hub](https://hub.docker.com/) Account

## Overview

No modifications are needed to any of the files to follow along. The general procedure for this example is:

1. Build and push the Docker image to a container registry, in this case [Docker Hub](https://hub.docker.com/).
2. Deploy the Kubernetes resources:
   1. A PVC in which to store the model.
   2. A Batch Job to download the model. **The model is quite large at roughly 45Gi, and will take around 15-20 minutes to complete the download.**
   3. Deploy the CoreWeave InferenceService.
3. Perform Text Generation using the model by sending HTTP requests to the InferenceService.

## Procedure

### Build and push the Docker image

First, enter the `build` directory. From here, build and push the Docker image.

{% hint style="warning" %}
**Important**\
The default Docker tag is `latest`. We strongly **discourage** you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack.
{% endhint %}

Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image.

{% hint style="info" %}
**Note**\
****In the following commands, be sure to replace the example `username` with your Docker Hub `username`.
{% endhint %}

From the `kubernetes-cloud/online-inference/fastertransformer/build` directory, run the following commands:

```bash
$ docker login
$ export DOCKER_USER=coreweave
$ docker build -t $DOCKER_USER/fastertransformer-triton:1
$ docker push $DOCKER_USER/fastertransformer-triton:1
```

{% hint style="info" %}
**Note**\
This example assumes a public docker registry. To use a private registry, an [imagePullSecret ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)needs to be defined.
{% endhint %}

### Deploy the Kubernetes resources

#### PVC

{% hint style="info" %}
**Note**\
Before continuing, you may either point the `image: $DOCKER_USER/fastertransformer-triton:1`in the following manifests to the image we just built in the previous steps, or you may use the publicly-available image found in the following manifest:

* `gptj-ft-inference-service.yml`
{% endhint %}

To create a PVC to store the model, from the `kubernetes-cloud/online-inference/fastertransformer/` directory, run:

```bash
$ kubectl apply -f model-storage-pvc.yml
```

#### Model job download

To deploy the job to download the model to the PVC, from the `kubernetes-cloud/online-inference/fastertransformer/` directory, run:

```
$ kubectl apply -f download-weights-job-gptj.yml
```

This job performs the following:

* Downloads the GPT-J weights into the PVC at `/mnt/pvc/models`
* Installs the required packages to convert them to FasterTransformer format
* Converts them to FasterTransformer format and stores them in the PVC at `/mnt/pvc/triton-model-store/fastertransformer/1/`
* Passes the `config.pbtxt` file that sets important parameters such as `tensor_para_size=1`, `pipeline_para_size=1, (1 GPU x 1 Pod)` and `model_transaction_policy { decoupled: False }` which allows for streaming if set to `True`.&#x20;

{% hint style="info" %}
**Note**\
****The model is quite large at \~45Gi, and may take around 15-20 minutes for the download job to complete.
{% endhint %}

To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```
$ kubectl get jobs

NAME                        COMPLETIONS   DURATION      AGE
gptj-download                 1/1            24m        1h
```

Or, follow the job logs to monitor progress:

```
kubectl logs -l job-name=gptj-download --follow
```

#### InferenceService

Once the model is downloaded, the `InferenceService` can be deployed by invoking:

```
kubectl apply -f gptj-ft-inference-service.yml
```

Due to the size of the model, loading into GPU memory can take around 5-10 minutes. To monitor the progress of this, you can wait to see the KServe workers start in the pod logs by invoking:

```
kubectl logs -f -l serving.kubeflow.org/inferenceservice=fastertransformer-triton kfserving-container
```

Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL:

```bash
$ kubectl get isvc                                                                                     
NAME                             URL                                                                                                          READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                                      AGE
fastertransformer-triton         http://fastertransformer-triton.tenant-sta-coreweavertalari-rahultalaridev.knative.chi.coreweave.com         True           100                              fastertransformer-triton-predictor-default-00001         2d3h
```

### Python Inference Client

Once you have the `InferenceService` up and running, you should be able to query fastertransformer via the HTTP API to generate text based on a conditional prompt.&#x20;

From the `kubernetes-cloud/online-inference/fastertransformer/client` directory, run the following commands:

```bash
$ docker login
$ export DOCKER_USER=coreweave
$ docker build -t $DOCKER_USER/fastertransformer-triton-client:1
Once you build and push your image above, you should be able to query the InferenceService  to generate text by running the following commands:
```

{% hint style="info" %}
**`Note`**

`$ kubectl get isvc` (will give you the URL required for the below `SERVICE` variable). Note that you should NOT pass `http://`, just the URL like below. ``&#x20;
{% endhint %}

<pre><code><strong>cd client/;
</strong>export SERVICE=fastertransformer-triton.tenant-sta-coreweavertalari-rahultalaridev.knative.chi.coreweave.com
docker run $DOCKER_USER/fastertransformer-client:1 --url=$SERVICE  --prompt="Mary has a little lamb."</code></pre>

You should see output like below:

```
$ docker run $DOCKER_USER/fastertransformer-client:1 --url=$SERVICE --prompt="Mary has a little lamb."      
Ouput: Mary has a little lamb. Its fleece is white as snow, and everywhere that Mary walks, the lamb is sure to be sure-footed behind her. It loves the little lambs
```

You can find how to set and change parameters in the `sample_request.json` . The file `example.py` provides simple methods to use the Python Triton client with fastertransformer via HTTP.

### Hardware and Performance

This example is set to use one NVIDIA RTX A5000 PCIe GPU. We have done prior benchmarking to analyze performance of Triton with fastertransformer against our current Hugging Face version of GPTJ-6B.&#x20;

**Benchmark results** are available [here](https://docs.google.com/spreadsheets/d/1HGQKoYgO0H2y7-DmIiIZhLmGU8vZPH8FoojXG7zj6-o/edit#gid=0).

**Key Observations:**

* `tokens_per_second` using fastertransformer v/s Hugging Face on 1 A5000 GPU is about **30%** faster in general.
* Using multiple (4) GPUS, we have observed average speedups of **2X** v/s 1 GPU on Hugging Face.

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

By setting `minReplicas` to `0`, Scale To Zero can be enabled, which will completely scale down the `InferenceService` when there have been no requests for a period of time.

When a service is scaled to zero, no cost is incurred. Please note that due to the size of the GPT-J model, Scale to Zero will lead to long request completion times if the model has to be scaled from zero. This can take around 5-10 minutes.&#x20;
