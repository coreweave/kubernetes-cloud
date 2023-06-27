---
description: Welcome to Inference on CoreWeave
---

# Inference

**Machine learning** is one of the most popular applications of CoreWeave Cloud's state-of-the-art infrastructure. Models are easily hosted on CoreWeave, and can be sourced from a range of storage backends including [S3-compatible object storage](../../storage/object-storage.md), HTTP, or persistent [Storage Volumes](../../storage/storage/#storage-volumes).

CoreWeave Cloud's Inference engine autoscales containers based on demand in order to to swiftly fulfill user requests, then scales down according to load so as to preserve GPU resources. Allocating new resources and scaling up new containers can be as fast as 15 seconds for the 6B GPT-J model.

Allocating new resources and scaling up a container can be **as fast as fifteen seconds** for the 6B GPT-J model. This quick autoscale allows for a significantly more responsive service than that of other Cloud providers.

## The CoreWeave inference stack

<figure><img src="../../.gitbook/assets/image (48) (2).png" alt=""><figcaption><p>The flow of a request in the Inference engine</p></figcaption></figure>

CoreWeave Cloud's inference stack is backed by well-supported Open Source tools.

* [**Knative Serving**](https://knative.dev/docs/serving/) acts as the serverless runtime, which manages autoscaling, revision control, and canary deployments.
* [**KServe**](https://www.kubeflow.org/docs/components/serving/kfserving/) provides an easy to use interface via [Kubernetes resource definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) for deploying models without the fuss of correctly configuring the underlying framework (i.e., Tensorflow).

### Knative default parameters

The table below lists the global Knative defaults that have been adjusted by CoreWeave, though there are additional Knative settings that have not been altered.

**Refer to the** [**Knative documentation**](https://knative.dev/docs/serving/configuring-autoscaling/) **for more information.**

<table><thead><tr><th width="289.3333333333333">KNative Parameter</th><th width="126">Value</th><th>Description</th></tr></thead><tbody><tr><td><code>stable-window</code></td><td>180s</td><td>The time period average concurrency is measured over in stable mode</td></tr><tr><td><code>panic-window-percentage</code></td><td>13.0</td><td>Indicates how the window over which historical data is evaluated will shrink upon entering panic mode - for example, a value of 13.0 means that in panic mode, the window will be 13% of the stable window size</td></tr><tr><td><code>container-concurrency-target-percentage</code></td><td>85%</td><td>Scale to keep an average headroom of 15% of available concurrent request to accommodate for bursts</td></tr><tr><td><code>max-scale-up-rate</code></td><td>20</td><td>Scale up at a maximum of 20x of current capacity or 1 container (whichever is larger) per 15 seconds</td></tr><tr><td><code>max-scale-down-rate</code></td><td>1.1</td><td>Scale down at a maximum of 10% of current capacity or 1 container (whichever is larger) per 15 seconds</td></tr><tr><td><code>scale-to-zero-pod-retention-period</code></td><td>30m</td><td>If no requests have been received for 30 minutes, a service will be scaled to zero and not use any resources. This behavior can be disabled by setting minReplicas to 1 in the service spec</td></tr><tr><td><code>scale-to-zero-grace-period</code></td><td>60s</td><td>The upper bound time limit that the system will internally wait for scale-from-zero machinery to be in place, before the last replica is removed</td></tr><tr><td><code>scale-down-delay</code></td><td>60s</td><td>Containers are only scaled down if scaled-down has been requested over a 60s period. This is to avoid thrashing.</td></tr></tbody></table>

If concurrent request exceeds the current scaled-for request volume by 200% during a period of 24 seconds, the autoscaler enters "panic mode," and starts scaling containers faster than the normal 180-second stable window. Some of these settings, such as stable window, can be modified using [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) on the `InferenceService`.

## Autoscaling

Autoscaling is enabled by default for all Inference Services.

Autoscaling parameters have been pre-configured for GPU-based workloads, where a large dataset usually needs to be loaded into GPU VRAM before serving can begin. Autoscaling is enabled any time the value of `minReplicas` differs from the value of `maxReplicas` in the `InferenceService` spec. For example:

```yaml
spec:
  predictor:
    minReplicas: 0 
    maxReplicas: 10
```

### Scale-to-Zero

Inference Services with long periods of idle time can automatically be scaled to zero. When scaled down, the Inference Service will consume no resources and incur no billing. As soon as a new request comes in, a Pod will be instantiated and the request will be served. For small models, this can be as quick as five seconds. For larger models, spin up times can be 30 to 60 seconds. Model loading times are highly dependent on the code responsible of loading the model into the GPU. Many popular PyTorch frameworks do not optimize for optimal loading times.

To enable Scale To Zero, simply set `minReplicas` to `0`. By default, scale-down will happen in 0 to 30 minutes after the last request was served.

To set the max scale down delay lower, add the annotation:

```yaml
 autoscaling.knative.dev/scale-to-zero-pod-retention-period: "10m"
```

&#x20;to the `InferenceService` block. By default, this is set to 30 minutes.

## Model storage

Models can be served directly from [CoreWeave's S3-compatible Object Storage](../../storage/object-storage.md). For faster container launch times in a production environment, it is recommended to cache the model in a `ReadWriteMany` [persistent volume on CoreWeave storage](../../storage/storage/#storage-volumes).

The model can be written to a PVC from any container deployed via [CoreWeave Apps](https://apps.coreweave.com) such as SSH, Jupyter, or [FileBrowser](../../storage/filebrowser.md). The Determined AI MLOps platform can also write models directly to a PVC for usage by an `InferenceService`. Determined AI can also be deployed via the applications Catalog.

For best performance results, avoid including models over `1GB` in size in a Docker container. For larger models, loading from a storage PVC is strongly recommended. For optimal loading speeds, [NVMe-backed storage volumes](../../storage/storage/#volume-types) are recommended.

## Compute selectors and affinities

{% hint style="info" %}
**Additional Resources**

All values for all available node types may be found on the [Node Types](../../../coreweave-kubernetes/node-types.md) page.
{% endhint %}

GPU and CPU types are specified using [Kubernetes affinities](../../../coreweave-kubernetes/label-selectors.md). For example:

```yaml
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

## Billing

For on-demand customers, billing is done on a per-minute basis when containers are running. Scale-to-Zero allows rarely used models to incur no costs, while still making the models available to receive requests.

{% hint style="warning" %}
**Important**

When an `InferenceService` is scaled to zero due to being idle, it usually takes 15-60 seconds depending on the model size until the first API request is answered. If this is unacceptable, it is recommended to set `minReplicas` to `1`.
{% endhint %}

## How-to guides and tutorials

The provided [inference how-to guides and tutorials](../how-to-guides-and-tutorials/examples/) are tailored specifically for common use cases with popular models, such as GPT-J and Stable Diffusion. Additionally, there are many more examples in the [KServe repository](https://github.com/kubeflow/kfserving/tree/master/docs/samples), which can be used directly in your namespace.
