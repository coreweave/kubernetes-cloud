---
description: >-
  Use the CoreWeave CoScheduler to deploy multiple Pods at the same time with
  predetermined resources
---

# CoSchedulers

With the **CoreWeave CoSchedulers,** Pods can be grouped together in order to be deployed all at once. This ability is particularly useful in Machine Learning environments, where it is often necessary for all pieces of a project to begin at the same time.

Traditional deployments via the default scheduler will try to provision all of the Pods it can, so long as the resources are available to do so. However, if the required resources run out, then the default scheduler will only create a partial deploy.

With the CoScheduler, you can define which resources you want to use prior to deployment. Then, the CoScheduler will _only_ provision all of the Pods if it can meet that predetermined request.

There are two CoSchedulers available on CoreWeave Cloud:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>CoreWeave CoScheduler</strong></td><td>The general use CoScheduler, which utilizes <code>PodGroups</code>. Best for most use cases.</td><td><code>schedulerName: cw-coscheduler</code></td><td><a href="coschedulers.md#coreweave-coscheduler">#coreweave-coscheduler</a></td></tr><tr><td><strong>CoScheduler for Determined AI</strong></td><td>CoScheduler exclusively for clients using Determined AI, or for other clients who require <code>label</code> support.</td><td><code>schedulerName: coscheduler</code></td><td><a href="coschedulers.md#coscheduler-for-determined-ai">#coscheduler-for-determined-ai</a></td></tr></tbody></table>

## CoreWeave CoScheduler

### Usage

**Use of the CoScheduler is optional.** To use it, apply a manifest similar to the following:

```yaml
apiVersion: scheduling.sigs.k8s.io/v1alpha1
kind: PodGroup
metadata:
  name: pg1
spec:
  scheduleTimeoutSeconds: 60
  # The minimum number of pods you need in order for this PodGroup to be deployed
  minMember: 4
---  
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pause
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pause
  template:
    metadata:
      labels:
        app: pause
        # Label value needs to match PodGroup name        
        pod-group.scheduling.sigs.k8s.io: pg1
    spec:
      # Define which scheduler to use
      schedulerName: cw-coscheduler
      containers:
      - name: pause
        image: k8s.gcr.io/pause:3.6          
```

In this manifest, note `kind: PodGroup`, the `PodGroup` name as specified via the `pod-group.scheduling.sigs.k8s.io` label, and that the `spec.schedulerName` is set to `cw-coscheduler`.

```
        # Label value needs to match PodGroup name        
        pod-group.scheduling.sigs.k8s.io: pg1
    spec:
      # Need to define which scheduler we want to use
      schedulerName: cw-coscheduler
```

The `pod-group.scheduling.sigs.k8s.io` label is used to match PodGroups by name, where as the `spec.schedulerName` value specifies which scheduler to use for the deployed Pods.

## CoScheduler for Determined AI

The CoScheduler for Determined AI is exclusively for clients using [Determined AI](https://www.determined.ai/), or for others who need `label` support in their coscheduler.

### Usage

When using the CoScheduler for Determined AI, the manifest kind will be a `Deployment` rather than a `PodGroup`. The `schedulerName` will be set to `coscheduler`, and the `labels` fields will be used to set scheduling specifications, as shown in this example:

{% code overflow="wrap" %}
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pause
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pause
  template:
    metadata:
      labels:
        app: pause
        pod-group.scheduling.sigs.k8s.io/min-available: <minimum number you require before starting all pods>
        pod-group.scheduling.sigs.k8s.io/name: <unique task name>
    spec:
      # Define which scheduler to use
      schedulerName: coscheduler
      containers:
      - name: pause
        image: k8s.gcr.io/pause:3.6
```
{% endcode %}
