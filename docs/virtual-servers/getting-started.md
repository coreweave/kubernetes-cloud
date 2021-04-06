# Getting Started

![](../.gitbook/assets/virtualserver-6-.png)

CoreWeave supports both Linux and Windows Virtual Servers. Both GPU-enabled and CPU-only Virtual Servers are available for deployment, and can be configured from the variety of GPUs and CPUs in the CoreWeave fleet. CoreWeave storage can be mounted in automatically, providing high performance access to shared storage volumes accessible by other Kubernetes workloads including other Virtual Servers.

### Deployment Methods

Virtual Servers, being a Kubernetes custom-resource, can be be deployed onto CoreWeave Cloud easily using such conventional methods as application of a YAML manifest via `kubectl` and creation of a release via the Virtual Server helm chart. Additionally, CoreWeave provides a programmatic interface to create and manipulate Virtual Servers via the Kubernetes API server. These methods will be detailed in subsequent sections.

### Management & Control

Once a Virtual Server is deployed, tools such as `kubectl` and `virtctl` can be utilized to manage and control the resources, and state of a Virtual Server.

{% hint style="info" %}
The examples and demo files that will be used in the following sections are available in the CoreWeave [kubernetes-cloud](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples) repository.
{% endhint %}



