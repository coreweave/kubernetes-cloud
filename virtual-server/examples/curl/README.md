## Virtual Server `curl` Example

This is an example implementation in `bash` of a Kubernetes client interacting with a Virtual Server resource on CoreWeave Cloud using `curl`. The example script provided creates, lists, and deletes a simple Ubuntu 20.04 Virtual Server with 2 CPU cores and 2Gi of memory.

## Usage

### Dependencies
Before invoking the script, the `jq` and `curl` commands must be installed and available from the `PATH`.

### Environment variables
In invoking this script, `TOKEN` and `NAMESPACE` will be exported as environment variables. The value of `NAMESPACE` should be set to the desired namespace. The value of `TOKEN` should be replaced with the value of `'token:'` generated in the `kubeconfig` file.

> ℹ️ [See more about how to generate the kubeconfig file.](https://docs.coreweave.com/coreweave-kubernetes/getting-started#obtain-access-credentials)


### Running the script

The script is invoked like so:

```bash
TOKEN=<token> NAMESPACE=<namespace> ./run.sh
```

## Implementation Breakdown

The implementation consists of a few simple `curl` calls to two APIs:

1. **[Kubevirt](https://kubevirt.io/)** - An open-source project that allows running virtual systems on the Kubernetes cluster.
1. **[Virtual Server](https://docs.coreweave.com/virtual-servers/getting-started)** - A Kubernetes Custom Resource that allows deploying a virtual system and interacting with Kubevirt with ease.

> 💡 **Additional resources**
> 
> The latest resource details, such as statuses and conditions, are available on [Virtual Servers reference API](https://pkg.go.dev/github.com/coreweave/virtual-server/api/v1alpha1#VirtualServerConditionType)
> The general description of Kubernetes RESTful API is available in [the official documentation of the Kubernetes API Overview](https://kubernetes.io/docs/reference/using-api/). Basic concepts of the API are described in [the official documentation of the Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/).

## Virtual Server functions

- `create_vs()` - creates the Virtual Server
- `delete_vs()` - deletes the Virtual Server
- `list_vs()` - lists of all the Virtual Servers in the designated namespace
- `get_vs()` - prints formatted JSON details about the Virtual Server
- `wait_until_vs_status()` - loops until the expected condition is met. 

## Kubevirt functions

**VM**
- `start_vm()` - starts a Virtual Machine and creates a Virtual Machine Instance
- `stop_vm()` - stops the Virtual Machine, then the deletes Virtual Machine Instance
- `list_vm()` - lists all the Virtual Machines in namespace
- `get_vm()` - prints formatted JSON details about the Virtual Machine

**VMI**
- `list_vmi()` - lists all the Virtual Machine Instances in the designated namespace
- `get_vmi()` - prints formatted JSON details about Virtual Machine Instance

> 💡 **Additional resources**
> 
> The [Kubevirt Python client](https://github.com/kubevirt/client-python#documentation-for-api-endpoints) can list all of the Kubevirt RESTful API, both for VMs and VMIs.
