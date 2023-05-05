---
description: Get faster pull times with Nydus on CoreWeave
---

# Nydus

{% hint style="info" %}
**Note**

Nydus on CoreWeave Cloud is currently in **alpha** with limited availability. In order to make use of Nydus, Workloads must be [scheduled onto Nydus-enabled nodes using anti-affinity](nydus.md#schedule-the-workloads).
{% endhint %}

Embedding machine learning models directly into images has become a popular ease-of-use technique, but it has made image pull times slower due to the increased size of container images. As a result, pulling images is often the most time-consuming aspect of spinning up new containers, and for those who rely on fast autoscaling to respond to changes in demand, the time it takes to create new containers can pose as a major hurdle.

It's for this reason that CoreWeave Cloud supports [Nydus](https://github.com/containerd/nydus-snapshotter), for dramatically shorter container image pull times.

## What is Nydus?

[Nydus](https://github.com/containerd/nydus-snapshotter) is an external plugin for [containerd](https://containerd.io/) leveraging the [Nydus container image service](https://github.com/dragonflyoss/image-service#nydus-dragonfly-container-image-service), which implements a content-addressable filesystem on top of a RAFS format for container images. This formatting allows for major improvements to the current [OCI image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md#open-container-initiative) in terms of container launching speed, image space, network bandwidth efficiency, and data integrity.

Some of [Nydus' key features](https://github.com/dragonflyoss/image-service#nydus-dragonfly-container-image-service) include:

* a method called "lazy pulling," container images are downloaded on-demand in "chunks," which [significantly boosts container startup times](https://github.com/dragonflyoss/image-service/blob/master/misc/perf.jpg),
* content-addressable data deduplication, which minimizes storage, transmission, and memory footprints,
* a merged filesystem tree, which allows all intermediate layers to be removed,
* compatibility with [the OCI artifacts and distribution specs](https://github.com/opencontainers/artifacts#project-introduction-and-scope), so Nydus images may be stored in any regular container registry

For clients who would like to bake machine learning models directly into their images, or who otherwise have very large container images, Nydus provides a solution that significantly shortens pull times of hefty container images.

{% hint style="info" %}
**Additional Resources**

For a list of additional features and official benchmarks, refer to [the Nydus project's GitHub](https://github.com/dragonflyoss/image-service#introduction).
{% endhint %}

## Setup

Nydus configures the container runtime (conatinerd), to inspect the given container image at runtime. If Nydus recognizes the image as a Nydus-formatted image, then it will pull it using the Nydus image service.

Nydus is also backwards-compatible - if Nydus recognizes that the image being pulled is a standard OCI image, then it will pull it normally; just as a normal configuration of the containerd runtime would.

To use Nydus on CoreWeave Cloud, **you do not need to change your Kubernetes manifests**, but you will need to **reformat your base images** to the Nydus format.

### Convert images to Nydus format

To convert your images to Nydus format, use the [Nydusify conversion tool](https://github.com/dragonflyoss/image-service/blob/master/docs/nydusify.md#nydusify). Converting base images is as easy as either targeting an OCI image in a repository:

```bash
nydusify convert \
  --source myregistry/repo:tag \
  --target myregistry/repo:tag-nydus
```

Or, a local dictionary may be packed as a Nydus-formatted image:

```bash
nydusify pack \
  --bootstrap target.bootstrap \
  --target-dir /path/to/target \
  --output-dir /path/to/output
```

{% hint style="warning" %}
**Important**

At this time, using Nydus images on CoreWeave **requires** that:

* base images are converted manually using **Nydusify**
* images **must** be stored in a **public repository**
{% endhint %}

### Schedule Workloads onto Nydus-enabled nodes

Nydus is only available on some nodes on CoreWeave Cloud. To use Nydus, Workloads must be scheduled on Nydus-enabled nodes using [a Kubernetes anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) that explicitly prevents Workloads from being scheduled onto nodes running Cloud version `1.20.0`, `1.19.1`, or `1.18.0`:

```yaml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.coreweave.cloud/version
            operator: NotIn
            values:
            - 1.20.0
            - 1.19.1
            - 1.18.0
```

A more complete example of this same manifest might look like:

```yaml
kind: Pod
apiVersion: v1
metadata:
  name: nydus-image
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.coreweave.cloud/version
            operator: NotIn
            values:
            - 1.20.0
            - 1.19.1
            - 1.18.0   
  containers:
  - name: nydus-image
    image: {registry}:{tag}
    ports:
    - containerPort: 80
```
