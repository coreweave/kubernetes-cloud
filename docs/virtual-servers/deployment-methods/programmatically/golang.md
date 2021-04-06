---
description: >-
  An example implementation in Golang of a kubernetes client to interact with a
  Virtual Server resource on CoreWeave Cloud.
---

# Golang

The Go example illustrates the following:

1. Building up a Virtual Server \([VirtualServer](https://github.com/coreweave/virtual-server/blob/13872bda37fadf2ea85bd2ac3a976c864548492d/api/v1alpha1/virtualserver_types.go#L64)\) struct.
2. Removal of an existing Virtual Server.
3. Creation of a new Virtual Server. \(The instance is started automatically\).
4. Waiting for Virtual Server ready status.
5. Stopping the instance and waiting until it is completely stopped.
6. Deletion of the Virtual Server.

### Build & Run

A `makefile` is provided within the [golang example](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/go) with the following directives:

| Directive | Description |
| :--- | :--- |
| install | Download the module dependencies |
| run | Build and run the example executable |
| clean | Remove the executable |

###   Implementation

The go [example](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/go/main.go) employs the [v1alpha1](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1) package of CoreWeave's VirtualServer in order to interface with the Virtual Server resource on CoreWeave Cloud. The Virtual Server struct is prepared using helper functions provided by package [v1alpha1](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1). Once prepared, a simple [sigs](https://github.com/kubernetes-sigs/controller-runtime) client is used to Create, Get, and Delete the Virtual Server. 

{% hint style="info" %}
For long-running, fine-grained and event-driven control of Virtual Servers, a [sigs controller](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/builder) can  be implemented for Virtual Servers.
{% endhint %}

