---
description: >-
  An example of deploying and managing Virtual Servers using programmatic access
  to the Kubernetes REST API with Bash.
---

# Bash

## Using `curl` and `jq` to deploy a Virtual Server

{% hint style="info" %}
**Note**

Follow along with this example by pulling [the example script](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/curl).
{% endhint %}

In [this example](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/curl), the `curl` and [`jq`](https://stedolan.github.io/jq/) tools are used to perform the following actions via the Kubernetes REST API using Bash:

1. **Create a CoreWeave Virtual Server** with the following attributes:\
   \- Running the Ubuntu 20.04 Operating System\
   \- 2 CPUs\
   \- 2Gi of memory
2. **List** the created Virtual Server.
3. **Delete** the created Virtual Server.

### Dependencies

Before invoking the script, the [`jq`](https://stedolan.github.io/jq/) and `curl` commands must be installed, and available from the `PATH`.

#### Environment variables

In invoking this script, `TOKEN` and `NAMESPACE` will be exported as environment variables. The value of `NAMESPACE` should be set to the desired namespace. The value of `TOKEN` should be replaced with the value of `'token:'` generated in the `kubeconfig` file.

#### Running the script

The script is invoked using the following command and environment variable exports:

```bash
TOKEN=<token> NAMESPACE=<namespace> ./run.sh
```

### Breakdown

The way this script works is by making calls to two different API endpoints separately:

1. [**Kubevirt**](https://kubevirt.io/) - An open-source project that allows running virtual systems on the Kubernetes cluster.
2. [**Virtual Server**](https://docs.coreweave.com/virtual-servers/getting-started) - A Kubernetes Custom Resource that allows deploying a virtual system and interacting with Kubevirt with ease.

{% hint style="info" %}
**Additional resources**

The latest resource details, such as **statuses** and **conditions**, are available in the [Virtual Servers reference API](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1#VirtualServerConditionType).\
\
The general description of the Kubernetes RESTful API is available in [the official documentation of the Kubernetes API Overview](https://kubernetes.io/docs/reference/using-api/).\
\
The basic concepts of the API are described in [the official documentation of the Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/).
{% endhint %}

### Functions calling the Virtual Server API

The Bash **** script defines and leverages the following functions to call the Virtual Server API:

* `create_vs()` - Creates a Virtual Server (VS)
* `delete_vs()` - Deletes a Virtual Server (VS)
* `list_vs()` - Lists of all the Virtual Servers (VS) in the designated namespace
* `get_vs()` - Prints formatted JSON details about the Virtual Server (requires `jq`)
* `wait_until_vs_status()` - Loops until the expected condition of the Virtual Server (VS) is met

### Functions calling the Kubevirt API

The script defines and leverages the following functions to call to the Kubevirt API:

**VM**

* `start_vm()` - Starts a Virtual Machine and creates a Virtual Machine Instance (VMI)
* `stop_vm()` - Stops the Virtual Machine, then deletes the Virtual Machine Instance (VMI)
* `list_vm()` - Lists all the Virtual Machines (VMs) in the namespace
* `get_vm()` - Prints formatted JSON details about the Virtual Machine (requires `jq)`

**VMI**

* `list_vmi()` - Lists all the Virtual Machine Instances (VMIs) in the designated namespace
* `get_vmi()` - Prints formatted JSON details about the Virtual Machine Instance (VMI)

{% hint style="info" %}
**Additional resources**

The [Kubevirt Python client, **kubevirt-py**](https://github.com/kubevirt/client-python#documentation-for-api-endpoints), can list all of the Kubevirt RESTful API endpoints for both VMs and VMIs.
{% endhint %}
