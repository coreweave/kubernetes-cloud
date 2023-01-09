# Get Started with Inference

![diagram](../online-inference/overview.png)

CoreWeave Cloud allows for easy serving of machine learning models. The models can be sourced from a range of storage backends, including S3 compatible object storage, HTTP and a [CoreWeave Storage Volume](../docs/storage/storage/). After deployment the inference engine auto scales the containers based on demand to swiftly fulfill user requests and scales down as load decreases to not waste GPU resources. Allocating new resources and scaling up a container can be as fast as 15 seconds for the 6B GPT-J model. The quick autoscale allows a significantly more responsive service than depending on scaling of hypervisor backed instances of other cloud providers.

Well supported Open Source tools back the inference stack. [Knative Serving](https://knative.dev/docs/serving/) acts as the serverless runtime, managing auto scaling, revision control and canary deployments. [KServe](https://www.kubeflow.org/docs/components/serving/kfserving/) provides an easy to use interface, via Kubernetes resource definitions to deploy models without having to worry about correctly configuring the underlying framework (ie. Tensorflow). The examples in our documentation are tailored specifically for common use cases, and there are many more examples in the [KServe repostiory](https://github.com/kubeflow/kfserving/tree/master/docs/samples) that can be used directly in your namespace.

An extensive set of step by step guides are provided in the [Examples](examples/) section to show deployment of popular models such as GPT-J and Stable Diffusion.

## Autoscaling

Autoscaling is enabled by default for all Inference Services. The autoscaling parameters have been pre-configured for GPU based workloads, where a large dataset usually needs to be loaded into GPU VRAM before serving can begin. Autoscaling is enabled any time `minReplicas` differ from `maxReplicas` in the `InferenceService` spec:

```yaml
spec:
  predictor:
    minReplicas: 0 
    maxReplicas: 10
```

### Knative default parameters

The table below lists the global Knative defaults that have been adjusted by CoreWeave, though there are additional Knative settings that have not been altered. Refer to the [Knative documentation](https://knative.dev/docs/serving/configuring-autoscaling/) for more information.

| KNative Parameter                         | Value | Description                                                                                                                                                                                                     |
| ----------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stable-window`                           | 180s  | The time period average concurrency is measured over in stable mode                                                                                                                                             |
| `panic-window-percentage`                 | 13.0  | Indicates how the window over which historical data is evaluated will shrink upon entering panic mode - for example, a value of 13.0 means that in panic mode, the window will be 13% of the stable window size |
| `container-concurrency-target-percentage` | 85%   | Scale to keep an average headroom of 15% of available concurrent request to accommodate for bursts                                                                                                              |
| `max-scale-up-rate`                       | 20    | Scale up at a maximum of 20x of current capacity or 1 container (whichever is larger) per 15 seconds                                                                                                            |
| `max-scale-down-rate`                     | 1.1   | Scale down at a maximum of 10% of current capacity or 1 container (whichever is larger) per 15 seconds                                                                                                          |
| `scale-to-zero-pod-retention-period`      | 30m   | If no requests have been received for 30 minutes, a service will be scaled to zero and not use any resources. This behavior can be disabled by setting minReplicas to 1 in the service spec                     |
| `scale-to-zero-grace-period`              | 60s   | The upper bound time limit that the system will internally wait for scale-from-zero machinery to be in place, before the last replica is removed                                                                |
| `scale-down-delay`                        | 60s   | Containers are only scaled down if scaled-down has been requested over a 60s period. This is to avoid thrashing.                                                                                                |

If concurrent requests exceeds the current scaled-for request volume by 200% during a period of 24 seconds, the autoscaler enters "panic mode," and starts scaling containers faster than the normal 180-second stable window. Some of these settings, such as stable window, can be modified using annotations on the `InferenceService`.

## Scale To Zero

Inference Services with long periods of idle time can automatically be scaled to zero. When scaled down, the Inference Service will consume no resources and incur no billing. As soon as a new request comes in, a Pod will be instantiated and the request will be served. For small models, this can be as quick as five seconds. For larger models, spin up times can be 30 to 60 seconds. Model loading times are highly dependent on the code responsible of loading the model into the GPU. Many popular PyTorch frameworks do not optimize for optimal loading times.

To enable Scale To Zero, simply set `minReplicas` to 0. By default, scale down will happen in 0 to 30 minutes after the last request was served. To set the max scale down delay lower, add the annotation `autoscaling.knative.dev/scale-to-zero-pod-retention-period: "10m"` to the `InferenceService`. By default, this is set to 30 minutes.

## Billing

For on demand customers, billing is done on a per minute basis when containers are running. Scale To Zero allows rarely used models to occur no costs, while still be available to receive requests. Please note that when an `InferenceService` is scaled to zero due to being idle, it usually takes 15-60 seconds depending on model size until the first API request is answered. If this is unacceptable, we recommend setting `minReplicas` to 1.

## Model Storage

Models can be served directly from Amazon S3, which is practical for testing and multi cloud deployment. For faster container launch times in a production environment it is recommended to cache the model in a `ReadWriteMany` persistent volume on CoreWeave storage. The model can be written to a PVC from any container, such as SSH, Jupyter or FileBrowser deployed via [CoreWeave Apps](https://apps.coreweave.com). The Determined.AI MLOps platform can also write models directly to a PVC for usage by an InferenceService. Determined.AI can also be deployed via Apps.

For best performance, small models (less than 1GB) can safely be included in the docker image. For larger models, loading from a storage PVC is strongly recommended. Use NVMe backed storage volumes for optimal loading speeds.

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
