# Python example

An example Python implementation of a kubernetes client that interacts with the Coreweave VirtualServer resource as well as the kubevirt subresource api.

The python example illustrates the following:
1. Removal of an existing Virtual Server.
2. Creation of a new Virtual Server based on the `my_virtualserver` example configuration
3. Waiting for a Virtual Server ready status.
4. Stop the Virtual Server instance and wait until it is stopped.
5. Delete the Virtual Server instance.

In order to workaround unresolved issues with resource paths in the native python client for kubevirt https://github.com/kubevirt/client-python, we introduced the class `KubeVirtClient` for basic operations on kubevirt VirtualMachine resources.

Class VSClient performs basic operations on the Vitrual Server resource.

## Install

```
virtualenv -p python3 .venv && source ./.venv/bin/activate
pip install kubernetes
```

## Run

```
Be sure to set secure credentials for your USERNAME and PASSWORD, as they will be used to create a user in your Virtual Server
USERNAME=<my_username> PASSWORD=<my_password> NAMESPACE=<my_namespace> KUBECONFIG=$HOME/.kube/config python3 main.py
```
