---
description: View Kubernetes resources with kubectl
---

# Kubectl

The standard Kubernetes command line tool, `kubectl`, is a flexible way to inspect the active resources in your account. Here are some useful commands you can use to view your resources.&#x20;

## **View Pods**

### In the current namespace

```bash
kubectl get pods
```

### In a specific namespace

```bash
kubectl get pods --namespace your-namespace
```

### In all namespaces

```bash
kubectl get pods --all-namespaces
```

### More information

```bash
kubectl get pods -o wide
```

### Details about all Pods

```bash
kubectl describe pods
```

### Details about a specific Pod

```bash
kubectl describe pod your-pod
```

### YAML configuration of a specific Pod

```bash
kubectl get pod your-pod -o yaml
```

### **Resources requested by Pods**

List the number of CPUs, GPUs, and memory requested by each Pod. \
**Note**: This assumes you have installed `jq` .

{% code overflow="wrap" %}
```bash
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu, gpu: .spec.containers[].resources.requests."nvidia.com/gpu", memory: .spec.containers[].resources.requests.memory}'
```
{% endcode %}

## **Virtual servers**

### In the current namespace

```bash
kubectl get vs
```

## **Services**

### In the current namespace

```bash
kubectl get services
```

### In a specific namespace

```bash
kubectl get services --namespace your-namespace
```

### Services sorted by name

```bash
kubectl get services --sort-by=.metadata.name
```

## **Deployments**

### All deployments

```bash
kubectl get deployments
```

### Specific deployment

```bash
kubectl get deployment your-deployment
```
