# Optimize Argo Workflows Performance and Resilience

When working with Argo Workflows, it's essential to ensure that your workflows are efficient, reliable, and make the best use of available resources. To achieve this, you need to consider a variety of performance-enhancing techniques and best practices, such as implementing proper time management with `activeDeadlineSeconds`, configuring retry strategies for error handling, and optimizing resource allocation, among others.

This documentation provides an overview of key concepts and strategies that will help you optimize your Argo Workflows. By incorporating them into your workflow design, you can ensure that your workflows run smoothly, recover from transient issues, and make the most of your resources.

## Use a retry strategy

To improve the reliability of your workflows or steps, we recommend implementing a retry strategy. This strategy helps handle transient errors or failures by automatically retrying the failed step. Here's our recommended retry strategy:

```yaml
 retryStrategy:
   limit: 2
   retryPolicy: Always
   backoff:
     duration: "15s"
     factor: 2
   affinity:
     nodeAntiAffinity: {}
```

**Explanation of the Retry Strategy Fields**

* `limit`: The maximum number of times to retry a failed step. In this example, the failed step will be retried up to 2 times.
* `retryPolicy`: Determines the conditions under which the step should be retried. In this example, the `Always` policy means that the step will be retried regardless of the failure reason.
* `backoff`: Configures the backoff strategy for retries, which determines the waiting time between retries.
  * `duration`: The initial duration to wait before retrying a failed step. In this example, the first retry will be attempted after 15 seconds.
  * `factor`: The multiplier applied to the duration for each subsequent retry. In this example, the factor is set to 2, which means that the waiting time will double with each retry (i.e., 15s, 30s, etc.).
* `affinity`: Configures the affinity rules for the pod during retries.
  * `nodeAntiAffinity`: Defines a node anti-affinity rule, which prevents the pod from being scheduled on the same node as the previous failed attempt. This can help avoid recurring issues caused by node-specific problems.

By incorporating this retry strategy in your workflows or steps, you can increase their resilience to failures and ensure that transient issues are automatically resolved.

In your documentation, you can include an explanation of using `activeDeadlineSeconds` like this:

## Set `activeDeadlineSeconds` for Workflow Steps

To improve the efficiency of your workflows and prevent steps from taking an unreasonably long time to finish, we recommend setting the `activeDeadlineSeconds` field for each step. This configuration should be applied to individual steps rather than the entire workflow, allowing steps to retry while still enforcing a time limit on their execution.

**Usage of `activeDeadlineSeconds`**

The `activeDeadlineSeconds` field sets a duration after which a step is considered to have failed and will be terminated. This helps to prevent steps from running indefinitely in case of issues or unexpected circumstances.

Here's an example of how to set `activeDeadlineSeconds` for a step:

```yaml
steps:
  - name: example-step
    template: example-template
    activeDeadlineSeconds: 300
```

In this example, the `example-step` has an `activeDeadlineSeconds` value of 300 seconds (5 minutes). If the step does not complete within this time, it will be terminated and considered as failed.

**Combining with Retry Strategy**

When combined with a retry strategy, `activeDeadlineSeconds` ensures that each retry attempt of a step has a time limit, preventing the step from taking too long to complete. This is particularly useful when handling external services or resources that may be temporarily unavailable or slow to respond.

By using `activeDeadlineSeconds` in conjunction with a retry strategy, you can efficiently manage the execution time of your workflow steps and ensure that they don't consume excessive resources due to unforeseen issues.

## Other recommendations

### Use Workflow Templates and ClusterWorkflowTemplates

Reusing common workflow steps across multiple workflows can reduce the complexity and resource usage. [Workflow Templates](https://argoproj.github.io/argo-workflows/workflow-templates/) and [ClusterWorkflowTemplates](https://argoproj.github.io/argo-workflows/cluster-workflow-templates/) allow you to define reusable workflow steps that can be easily referenced in other workflows.

### Use step level memoization and caching

Workflows often have outputs that are expensive to compute. [Step level memoization](https://argoproj.github.io/argo-workflows/memoization/) reduces cost and workflow execution time by memoizing previously run steps, storing the outputs of a template into a specified cache with a variable key.

### Use best practices for cost optimization

Follow the Argo Workflows [cost optimization recommendations](https://argoproj.github.io/argo-workflows/cost-optimisation/) for setting workflow pod resource requests, using node selectors to leverage more cost-effective instances, considering alternative storage solutions like Volume Claim Templates or Volumes instead of Artifacts, and limiting the total number of workflows and pods to manage resource usage. Also consider their best practices for Argo Workflows operators, such as setting appropriate resource requests and limits, and configuring executor resource requests to ensure efficient use of infrastructure resources. By following these guidelines, you can achieve a balance between performance and cost for your Argo Workflows deployments.

### Use a Time-to-Live (TTL) strategy

Configure the [TTL strategy](https://github.com/argoproj/argo-workflows/blob/master/examples/gc-ttl.yaml) for your workflows to automatically delete completed workflows and release resources after a specified amount of time. This helps prevent resource exhaustion and keeps the system running smoothly.

### Monitor and analyze performance

Use monitoring tools like Prometheus and [Grafana](../grafana.md) to analyze the performance of your Argo Workflows installation. This can help you identify bottlenecks and areas for improvement.

## More information

For more information, please see these Argo Workflows resources:

* [Examples on GitHub](https://github.com/argoproj/argo-workflows/tree/master/examples)
* [Slack](https://argoproj.github.io/community/join-slack/)
* [Training on YouTube](https://www.youtube.com/playlist?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo)
* [Argo Blog](https://blog.argoproj.io/)
