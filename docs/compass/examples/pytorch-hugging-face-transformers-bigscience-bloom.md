---
description: >-
  An example of a Hugging Face Transformers implementation of the BigScience
  Bloom 176B parameter model
---

# PyTorch Hugging Face Transformers Accelerate - BigScience BLOOM

## Introduction

This example demonstrates how to deploy [BLOOM](https://huggingface.co/bigscience/bloom) as an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) with a simple HTTP API to perform Text Generation. The deployment will run on CoreWeave Cloud NVIDIA A100 GPUs with autoscaling and Scale To Zero.

![](<../../.gitbook/assets/image (2).png>)

### What is BLOOM?

> BLOOM is an autoregressive Large Language Model (LLM), trained to continue text from a prompt on vast amounts of text data using industrial-scale computational resources. As such, it is able to output coherent text in 46 languages and 13 programming languages that is hardly distinguishable from text written by humans. BLOOM can also be instructed to perform text tasks it hasn't been explicitly trained for, by casting them as text generation tasks.

#### View the example code on GitHub:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/bloom-176b" %}
To follow along, please clone the manifests from GitHub
{% endembed %}

## Pre-requisites

The following pieces must be installed and configured prior to running the example.

* [kubectl](https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools)
* [docker](https://docs.docker.com/get-docker/)
* A Coreweave Account ([with Kubectl configured to use your Coreweave Kubeconfig](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials))
* A [Docker Hub](https://hub.docker.com/) Account

## Overview

&#x20;No modifications are needed to any of the files to follow along. The general procedure for this example is:

1. [Build and push the Docker image](pytorch-hugging-face-transformers-bigscience-bloom.md#docker-image) to a container registry, in this case [Docker Hub](https://hub.docker.com/).
2. [Deploy the Kubernetes resources](pytorch-hugging-face-transformers-bigscience-bloom.md#kubernetes-resources):
   1. [A PVC](pytorch-hugging-face-transformers-bigscience-bloom.md#undefined) in which to store the model.
   2. A [Batch Job to download the model](pytorch-hugging-face-transformers-bigscience-bloom.md#undefined). **The model is quite large at roughly 329Gi, and will take around 30 minutes to complete the download.**
   3. Deploy the [CoreWeave InferenceService](pytorch-hugging-face-transformers-bigscience-bloom.md#undefined).
3. Perform Text Generation using the model by sending HTTP requests to the InferenceService.

## Procedure

### Build and push the Docker image

First, enter the `model` directory. From here, build and push the Docker image.

{% hint style="warning" %}
**Important**\
The default Docker tag is `latest`. We strongly **discourage** you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack.
{% endhint %}

Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image.

{% hint style="info" %}
**Note**\
****In the following commands, be sure to replace the example `username` with your Docker Hub `username`.
{% endhint %}

From the `kubernetes-cloud/online-inference/bloom-176b/model` directory, run the following commands:

```bash
$ docker login
$ export DOCKER_USER=coreweave
$ docker build -t $DOCKER_USER/bloom-176b:1
$ docker push $DOCKER_USER/bloom-176b:1
```

{% hint style="info" %}
**Note**\
This example assumes a public docker registry. To use a private registry, an [imagePullSecret ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)needs to be defined.
{% endhint %}

### Deploy the Kubernetes resources

#### PVC

{% hint style="info" %}
**Note**\
Before continuing, you may either point the `image:` in the following manifests to the image we just built in the previous steps, or you may use the publicly-available image found in the following manifests:

* `bloom-176b-download-job.yaml`
* `bloom-176b-inferenceservice.yaml`
{% endhint %}

To create a PVC to store the model, from the `kubernetes-cloud/online-inference/bloom-176b/` directory, run:

```bash
$ kubectl apply -f 00-bloom-176b-pvc.yaml
```

#### Model job download

To deploy the job to download the model to the PVC, from the `kubernetes-cloud/online-inference/bloom-176b/` directory, run:

```
$ kubectl apply -f 01-bloom-176b-download-job.yaml
```

{% hint style="info" %}
**Note**\
****The model is quite large at 329Gi, and may take around 30 minutes for the download job to complete.
{% endhint %}

To check if the model has finished downloading, wait for the job to be in a `Completed` state:

```
$ kubectl get pods

NAME                        READY   STATUS      RESTARTS   AGE
bloom-176b-download-hkws6   0/1     Completed   0          1h
```

Or, follow the job logs to monitor progress:

```
kubectl logs -l job-name=bloom-176b-download --follow
```

#### InferenceService

Once the model is downloaded, the `InferenceService` can be deployed by invoking:

```
kubectl apply -f 02-bloom-176b-inferenceservice.yaml
```

Due to the size of the model, loading into GPU memory can take around 5 minutes. To monitor the progress of this, you can wait to see the KServe workers start in the pod logs by invoking:

```
kubectl logs -f -l serving.kubeflow.org/inferenceservice=bloom-176b kfserving-container
```

Alternatively, you can wait for the `InferenceService` to show that `READY` is `True`, and that it has a URL:

```bash
$ kubectl get inferenceservices
                
NAME         URL                                                                        READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                  AGE
bloom-176b   http://bloom-176b.tenant-sta-tweldon-workbench.knative.chi.coreweave.com   True           100                              bloom-176b-predictor-default-00001   9m2s
```

Using the provided URL, you can make an HTTP request via your preferred means.

Here is a simple cURL example:

```bash
curl http://bloom-176b.tenant-sta-tweldon-workbench.knative.chi.coreweave.com/v1/models/bigscience-bloom:predict -d '{"instances": ["That was fun"]}' | jq
{
  "predictions": [
    [
      {
        "generated_text": "That was fun.\n- Yeah, it was good to see you guys again.\nYeah, you too.\nYou know what?\nI think I'm gonna go home and get some sleep.\nI'm beat.\n-"
      }
    ]
  ]
}
```

The following parameters are supported:

```
- min_length
- max_length
- temperature
- top_k
- top_p
- repetition_penalty
```

You can modify the model parameters by invoking `curl` as follows:

```bash
$ curl http://bloom-176b.tenant-sta-tweldon-workbench.knative.chi.coreweave.com/v1/models/bigscience-bloom:predict -d '{"instances": ["This will generate some text"], "parameters":{"max_length": 20, "min_length": 20}}'
```

### Hardware and Performance

This example is set to use five NVIDIA A100 PCIe GPUs. Generation performance with the current codebase is suboptimal. We are actively working to integrate optimizations into the BLOOM example.

{% hint style="info" %}
**Note**\
The highest performing GPU combination for production grade deployment of BLOOM is 8x A100 NVLINK 80GB GPUs. Please [contact support](https://cloud.coreweave.com/contact) to access these.
{% endhint %}

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

When a service is scaled to zero, no cost is incurred. Please note that due to the size of the BLOOM model, Scale to Zero will lead to very long request completion times if the model has to be scaled from zero. This can take around 5 minutes.
