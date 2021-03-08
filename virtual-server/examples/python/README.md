# Python example

An example Python implementation of a kubernetes client that interacts with the Coreweave VirtualServer resource as well as the kubevirt subresource api.

The python example illustrates the following:
1. Removal of an existing Virtual Server.
2. Creation of a new Virtual Server based on the `my_virtualserver` example configuration
3. Waiting for a Virtual Server ready status.
4. Stop the Virtual Server instance and wait until it is stopped.
5. Delete the Virtual Server instance.

In order to workaround unresolved issue with resource paths in the native python client for kubevirt https://github.com/kubevirt/client-python, we introduced class `KubeVirtClient` for basic operations on kubevirt VirtualMachine resources.

Class `VSClient` does the basic operation on Vitrual Server controller.

## Install

```
virtualenv -p python3 .venv && source ./.venv/bin/activate
pip install kubernetes
```

## Run

```
NAMESPACE=<my_namespace> KUBECONFIG=$HOME/.kube/config python3 main.py
```
