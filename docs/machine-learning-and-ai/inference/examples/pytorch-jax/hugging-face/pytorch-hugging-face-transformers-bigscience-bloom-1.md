---
description: >-
  An example of a Hugging Face Transformers implementation of the BigScience
  Bloom 176B parameter model, optimized by Microsoft's DeepSpeed and pre-sharded
  model weights.
---

# Transformers DeepSpeed: BigScience BLOOM

This example demonstrates how to deploy [BLOOM](https://huggingface.co/bigscience/bloom) as an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) with a simple HTTP API to perform Text Generation, while leveraging [Hugging Face's Transformers Accelerate library](https://huggingface.co/docs/accelerate/index) including [the DeepSpeed plugin](https://huggingface.co/docs/accelerate/usage\_guides/deepspeed) for Accelerate.

The deployment will run a DeepSpeed-optimized, pre-sharded version of the model on CoreWeave Cloud NVIDIA A100 80GB GPUs networked by NVLink with autoscaling and Scale To Zero. This example uses the [Hugging Face BLOOM Inference Serve](https://github.com/huggingface/transformers-bloom-inference)r under the hood, wrapping it as a Inference Service on CoreWeave.

{% hint style="info" %}
**Note**

Please [contact CoreWeave Support](https://cloud.coreweave.com/contact) to access NVIDIA A100 80GB GPUs.
{% endhint %}

![To follow along, please clone the manifests from GitHub](<../../../../../.gitbook/assets/image (1) (2) (2) (2) (1).png>)

### What is BLOOM?

> _BLOOM is an autoregressive Large Language Model (LLM), trained to continue text from a prompt on vast amounts of text data using industrial-scale computational resources._

– [Hugging Face BigScience BLOOM](https://huggingface.co/bigscience/bloom)

BigScience BLOOM is able to output coherent text in 46 human languages and 13 programming languages. BLOOM can also be instructed to perform text tasks that it hasn't been explicitly trained for by casting them as text generation tasks.

### What is DeepSpeed?

> _DeepSpeed is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective._

– [Microsoft DeepSpeed](https://github.com/microsoft/DeepSpeed)

#### View the example code on GitHub:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/bloom-176b-deepspeed" %}

## Pre-requisites

If you'd like to follow along with this demo, [clone the manifests provided on GitHub](https://github.com/coreweave/kubernetes-cloud/tree/tweldon/bloom-deepspeed).

The following pieces must be installed and configured prior to running the example.

* [kubectl](https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools)
* [docker](https://docs.docker.com/get-docker/)
* A Coreweave Account ([with Kubectl configured to use your Coreweave Kubeconfig](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials))
* A [Docker Hub](https://hub.docker.com/) Account

## Overview

No modifications are needed to any of the files to follow along with this demo. The general procedure for this example is:

1. [Build and push the Docker images](pytorch-hugging-face-transformers-bigscience-bloom-1.md#docker-image) to a container registry, in this case [Docker Hub](https://hub.docker.com/).
2. [Deploy the Kubernetes resources](pytorch-hugging-face-transformers-bigscience-bloom-1.md#kubernetes-resources):
   1. [A PVC](pytorch-hugging-face-transformers-bigscience-bloom-1.md#undefined) in which to store the model.
   2. A [Batch Job to download the model](pytorch-hugging-face-transformers-bigscience-bloom-1.md#undefined). **The model is quite large at roughly 329Gi, and will take around 30 minutes to complete the download.**
   3. Deploy the [CoreWeave InferenceService](pytorch-hugging-face-transformers-bigscience-bloom-1.md#undefined).
3. Perform Text Generation using the model by sending HTTP requests to the InferenceService.

## Procedure

### Build and push the Docker images

First, enter the `kubernetes-cloud/online-inference/bloom-deepspeed` directory. From here, build and push the Docker images; we need one for the model downloader, and one to run the model.

{% hint style="warning" %}
**Important**\
The default Docker tag is `latest`. We strongly **discourage** you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack.
{% endhint %}

Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image.

{% hint style="info" %}
**Note**\
\*\*\*\*In the following commands, be sure to replace the example `username` with your Docker Hub `username`.
{% endhint %}

From the `kubernetes-cloud/online-inference/bloom-deepspeed` directory, run the following commands:

```bash
$ docker login
$ export DOCKER_USER=coreweave
$ docker build -t $DOCKER_USER/huggingface-hub-downloader:1 -f Dockerfile.downloader .
$ docker push $DOCKER_USER/huggingface-hub-downloader:1
$ docker build -t $DOCKER_USER/microsoft-bloom-deepspeed-inference-fp16:1 -f Dockerfile .
$ docker push $DOCKER_USER/microsoft-bloom-deepspeed-inference-fp16:1
```

{% hint style="info" %}
**Note**\
This example assumes a public docker registry. To use a private registry, an [imagePullSecret ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)needs to be defined.
{% endhint %}

### Deploy the Kubernetes resources

#### PVC

{% hint style="info" %}
**Note**\
Before continuing, you may either point the `image:` in the following manifests to the images we just built in the previous steps, or you may use the publicly-available image found in the following manifests:

* `01-download-job.yaml`
* `02-inference-service.yaml`
{% endhint %}

To create a PVC to store the model, from the `kubernetes-cloud/online-inference/bloom-deepspeed/` directory, run:

```bash
$ kubectl apply -f 00-pvc.yaml
```

#### Model job download

To deploy the job to download the model to the PVC, from the `kubernetes-cloud/online-inference/bloom-deepspeed/` directory, run:

```
$ kubectl apply -f 01-download-job.yaml
```

{% hint style="info" %}
**Note**\
\*\*\*\*The model is quite large at 329Gi, and may take around 30 minutes for the download job to complete.
{% endhint %}

To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```
$ kubectl get po -l job-name=microsoft-bloom-deepspeed-inference-fp16-download                                                                                                                                   
NAME                                                      READY   STATUS    RESTARTS   AGE                                                                                                                        
microsoft-bloom-deepspeed-inference-fp16-download-5mdd2   0/1     Pending   0          48s        
```

Or, follow the job logs to monitor progress:

```
kubectl logs -l job-name=microsoft-bloom-deepspeed-inference-fp16-download --follow
```

#### InferenceService

Once the model is downloaded, the `InferenceService` can be deployed by invoking:

```
kubectl apply -f 02-inference-service.yaml
```

Due to the size of the model, loading into GPU memory can take around 5 minutes. To monitor the progress of this, you can wait to see the KServe workers start in the pod logs by invoking:

```
kubectl logs -f -l serving.kubeflow.org/inferenceservice=microsoft-bloom-deepspeed-inference-fp16 kfserving-container
```

Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL:

```bash
$ kubectl get inferenceservices
NAME                                       URL                                                                                                      READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                                               AGE
microsoft-bloom-deepspeed-inference-fp16   http://microsoft-bloom-deepspeed-inference-fp16.tenant-demo.knative.chi.coreweave.com   True           100                              microsoft-bloom-deepspeeda7e1fc0ba9c8977d6db7956f04d85acf-00001   16m
```

Using the provided URL, you can make an HTTP request via your preferred means.

Here is a simple cURL example:

```bash
$ curl http://microsoft-bloom-deepspeed-inference-fp16.tenant-demo.coreweave.com/generate/ -H 'Content-Type: application/json' -d '{"text": ["Deepspeed is"], "repetition_penalty": 10.0}'
{"method":"generate","num_generated_tokens":[75],"query_id":1,"text":["Deepspeed is a leading provider of high-performance, low-latency data center connectivity. We offer the fastest and most reliable Internet access available in North America.\nWe are committed to providing our customers with unmatched performance at an affordable price point through innovative technology solutions that deliver exceptional value for their business needs\nOur network consists entirely on dark fiber routes between major metropolitan areas across Canada & USA"],"total_time_taken":"4.86 secs"}
```

A complete list of available request parameters can be found here:

{% embed url="https://github.com/huggingface/transformers-bloom-inference/blob/main/bloom-inference-server/utils/requests.py#L11" %}

Parameters may be modified with each request by supplying the parameters found at the above link as keys, along with the desired value in your request data:

```bash
curl http://microsoft-bloom-deepspeed-inference-fp16.tenant-demo.knative.chi.coreweave.com/generate/ -H 'Content-Type: application/json' -d '{"text": ["Deepspeed is"], "repetition_penalty": 10.0, "top_k": 10, "do_sample": true}'
```

### Autoscaling

Scaling is controlled in the `InferenceService` configuration. This example is set to always run one replica, regardless of number of requests.

Increasing the number of `maxReplicas` will allow the CoreWeave infrastructure to automatically scale up replicas when there are multiple outstanding requests to your endpoints. Replicas will automatically be scaled down as demand decreases.

#### Example

```yaml
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 5
```

By setting `minReplicas` to `0`, Scale To Zero can be enabled, which will completely scale down the `InferenceService` when there have been no requests for a period of time.

When a service is scaled to zero, no cost is incurred. Please note that due to the size of the BLOOM model, Scale to Zero will lead to very long request completion times if the model has to be scaled from zero. This can take around 5 minutes.

### Hardware and Performance

This example is set to use eight NVIDIA A100 80GB NVLink GPUs, as required by Microsoft's pre-sharded weights. This combination offers the highest available throughput for a production grade deployment.

DeepSpeed offers a dramatic speedup to the model over vanilla `transformers` accelerate as indicated by benchmark testing. The benchmarks below were run on CoreWeave Cloud [using BLOOM's inference scripts](https://github.com/huggingface/transformers-bloom-inference/tree/main/bloom-inference-scripts).

#### DeepSpeed benchmarks

```bash
*** Running benchmark

*** Performance stats:
Throughput per token including tokenize: 62.73 msecs
Start to ready to generate: 129.698 secs
Tokenize and generate 500 (bs=1) tokens: 6.280 secs
Start to finish: 135.978 secs

*** Running benchmark

*** Performance stats:
Throughput per token including tokenize: 7.58 msecs
Start to ready to generate: 122.540 secs
Tokenize and generate 4000 (bs=8) tokens: 6.088 secs
Start to finish: 128.628 secs
```

#### HuggingFace transformers with accelerate benchmarks

<pre class="language-bash"><code class="lang-bash">*** Running benchmark
<strong>
</strong>*** Performance stats:
Throughput per token including tokenize: 318.38 msecs
Start to ready to generate: 338.782 secs
Tokenize and generate 500 (bs=1) tokens: 39.511 secs
Start to finish: 378.292 secs

*** Running benchmark

*** Performance stats:
Throughput per token including tokenize: 57.81 msecs
Start to ready to generate: 353.200 secs
Tokenize and generate 4000 (bs=8) tokens: 56.108 secs
Start to finish: 409.308 secs
</code></pre>
