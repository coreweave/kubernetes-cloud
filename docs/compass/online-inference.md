# Online Inference Serving

## Introduction

![diagram](<../../.gitbook/assets/overview (1).png>)

CoreWeave Cloud allows for easy serving of machine learning models. The models can be sourced from a range of storage backends, including Amazon S3 and a [CoreWeave Storage Volume](../coreweave-kubernetes/storage.md). After deployment the inference engine auto scales the containers based on demand to swiftly fulfill user requests and scales down as load decreases to not waste GPU resources. Allocating new resources and scaling up a container usually takes 30 seconds for smaller models and 60 seconds for the full 11.5B parameter GPT-2 model. The quick autoscale allows a significantly more responsive service than depending on scaling of hypervisor backed instances of other cloud providers.

Well supported Open Source tools back the inference stack. [Knative Serving](https://knative.dev/docs/serving/) acts as the serverless runtime, managing auto scaling, revision control and canary deployments. [Kubeflow Serving](https://www.kubeflow.org/docs/components/serving/kfserving/) provides an easy to use interface, via Kubernetes resource definitions to deploy models without having to worry about correctly configuring the underlying framework (ie. Tensorflow). The examples in this repository are tailored specifically for common use cases, and there are many more examples in the [KFServing repostiory](https://github.com/kubeflow/kfserving/tree/master/docs/samples) that can be used directly in your namespace.

## Autoscaling

Autoscaling is enabled by default for all Inference Services. The autoscaling parameters have been pre-configured for GPU based workloads, where a large dataset usually needs to be loaded into GPU VRAM before serving can begin.

| KNative Parameter                       | Value | Description                                                                                                                                                                                 |
| --------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tick-interval                           | 15s   | Auto scaling decision are made every 10 seconds                                                                                                                                             |
| stable-window                           | 180s  | The time period average concurrency is measured over in stable mode                                                                                                                         |
| container-concurrency-target-percentage | 85%   | Scale to load all containers at 100% of their configured concurrency                                                                                                                        |
| max-scale-up-rate                       | 20    | Scale up at a maximum of 200% of current capacity or 1 container (whichever is larger) per 10 seconds                                                                                       |
| max-scale-down-rate                     | 2     | Scale down at a maximum of 50% of current capacity or 1 container (whichever is larger) per 10 seconds                                                                                      |
| scale-to-zero-grace-period              | 30m   | If no requests have been received for 30 minutes, a service will be scaled to zero and not use any resources. This behavior can be disabled by setting minReplicas to 1 in the service spec |

If concurrent requests exceeds the current scaled-for request volume by 200% during a period of 30 seconds, the autoscaler enters "panic mode" and starts scaling containers faster than the normal 120s stable window. Some of these settings, such as stable window can be modified using annotations on the `InferenceService`. Refer to the [KNative documentation](https://knative.dev/docs/serving/configuring-autoscaling/) for more information.

## Scale To Zero

Inference Services with long periods of idle time can automatically be scaled to zero. When scaled down, the Inference Service will consume no resources and incur no billing. As soon as a new request comes in, a Pod will be instantiated and the request will be served. For small models, this can be as quick as five seconds. For larger models, spin up times can be 30 to 60 seconds.

To enable Scale To Zero, simply set `minReplicas` to 0. By default, scale down will happen in 0 to 30 minutes after the last request was served. To set the max scale down delay lower, add the annotation `autoscaling.knative.dev/scaleToZeroPodRetentionPeriod: "10m"` to the `InferenceService`.

## Billing

For on demand customers, billing is done on a per minute basis when containers are running. Scale To Zero allows rarely used models to occur no costs, while still be available to receive requests. Please note that when an `InferenceService` is scaled to zero due to being idle, it usually takes 30-60 seconds depending on model size until the first API request is answered. If this is unacceptable, we recommend setting `minReplicas` to 1.

## Model Storage

Models can be served directly from Amazon S3, which is practical for testing and multi cloud deployment. For faster container launch times in a production environment it is recommended to cache the model in a `ReadWriteMany` persistent volume on CoreWeave storage. The model can be written to a PVC from any container, such as SSH, Jupyter or FileBrowser deployed via [CoreWeave Apps](https://apps.coreweave.com).

## GPU Selectors & Affinities

You will want to use [affinities](https://docs.coreweave.com/coreweave-kubernetes/node-types#requesting-compute-in-kubernetes), to specify what GPU type (or CPU, in case of CPU only Inference) your `InferenceService` should be scheduled on.

```yaml
spec:
  predictor:
    minReplicas: 0 
    maxReplicas: 3
    containerConcurrency: 1
    containers:
    ...
      resources:
        requests:
          cpu: 1
          memory: 6Gi
        limits:
          cpu: 3
          memory: 16Gi
          nvidia.com/gpu: 1
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
          - matchExpressions:
            - key: gpu.nvidia.com/class
              operator: In
              values:
              - Quadro_RTX_5000
```
