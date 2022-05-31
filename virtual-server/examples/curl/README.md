## Virtual Server curl Example

An example implementation in bash of a Kubernetes client to interact with a Virtual Server resource on CoreWeave Cloud.



## Quickstart

The script creates, lists and deletes simple Ubuntu 20.04 with 2 cores and 2Gi of memory.

To run the script, `jq` and `curl` commands must be installed and available from the `PATH`.

```bash
TOKEN=<token> NAMESPACE=<namespace> ./run.sh
```

Replace `<token>` with the value of 'token:' from `kubeconfig` file. [This chapter](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials) describes how to generate the `kubeconfig`.


Replace `<namespace>` with the namespace.


## Implementation Breakdown

The implementation consists of a few simple `curl` calls. The API can be divided into two main groups:
- **Kubevirt** - an open-source project that allows running virtual systems on the Kubernetes cluster.
- **Virtual Server** - a Kubernetes custom resource that allows deploying a virtual system and interacting with Kubevirt with ease.


> The latest resource details like statuses and conditions are available on [Virtual Servers reference API](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1#VirtualServerConditionType)

> The general description of Kubernetes RESTful API and its concept is available in the official documentation [API Overview](https://kubernetes.io/docs/reference/using-api/) and [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/)

## Virtual Server

- `create_vs()` - creates Virtual Server
- `delete_vs()` - deletes Virtual Server
- `list_vs()` - lists of all Virtual Servers in namespace
- `get_vs()` - prints formatted JSON details about Virtual Server
- `wait_until_vs_status()` - loops until expected condition is met. 

> The most efficient way to detect changes in the Kubernetes object is to use [watch feature](https://kubernetes.io/docs/reference/using-api/api-concepts/#efficient-detection-of-changes). The API reponses with stream of notification when any object changed. Curl is not best suited for the `watch` feature - it does not add new line after each notification and the last change does not pass to bash pipe. That's the reason we used `wait_until_vs_status()` with simple loop, to be sure we get the latest status of the Virtual Server.

### Kubevirt

**VM**
- `start_vm()` - starts Virtual Machine and creates Virtual Machine Instance
- `stop_vm()` - stops Virtual Machine and deletes Virtual Machine Instance
- `list_vm()` - lists of all Virtual Machines in namespace
- `get_vm()` - prints formatted JSON details about Virtual Machine

**VMI**
- `list_vmi()` - lists of all Virtual Machine Instances in namespace
- `get_vmi()` - prints formatted JSON details about Virtual Machine Instance

> [Kubevirt Python client](https://github.com/kubevirt/client-python#documentation-for-api-endpoints) list all Kubevirt RESTful API, both for VM and VMI.