---
description: >-
  CoreWeave has the standard Kubernetes resource monitoring metrics along other
  useful metrics.
---

# Useful Metrics

## Billing Metrics

All billing metrics return values in USD.&#x20;

| PromQL Metric                 | Description                                                   |
| ----------------------------- | ------------------------------------------------------------- |
| `billing_pod_cost`            | Returns the total cost for each Pod that is currently running |
| `billing_pod_cpu_cost`        | Returns the CPU usage cost for each CPU Pod running           |
| `billing_pod_gpu_cost`        | Returns the GPU usage cost for each GPU Pod running           |
| `billing_pod_mem_cost`        | Returns the Memory usage cost for each Pod running            |
| `billing_pod_cpu_cost_hourly` | Returns the average CPU usage cost per hour                   |
| `billing_pod_gpu_cost_hourly` | Returns the average GPU usage cost per hour                   |
| `billing_pod_mem_cost_hourly` | Returns the average Memory usage cost per hour                |
| `billing_pod_cost_hourly`     | Returns the average cost for each Pod per hour                |

{% hint style="warning" %}
Billing metrics should be used to monitor usage cost estimates. For billed usage, go to **Usage & Billing** page on the [CoreWeave Dashboard](https://cloud.coreweave.com).
{% endhint %}

## Container Metrics

We've implemented [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) in our infrastructure so you can monitor the resource usage for all of your Kubernetes services, deployments, jobs, and more. Review the full list of [exposed metrics](https://github.com/kubernetes/kube-state-metrics/tree/master/docs#exposed-metrics) for more details.
