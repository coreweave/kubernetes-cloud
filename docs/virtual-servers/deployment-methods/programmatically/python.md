---
description: >-
  An example Python implementation of a kubernetes client that interacts with
  the CoreWeave VirtualServer resource as well as the kubevirt subresource api.
---

# Python

The python example illustrates the following:

1. Removal of an existing Virtual Server.
2. Creation of a new Virtual Server based on the `my_virtualserver` example configuration
3. Waiting for a Virtual Server ready status.
4. Stop the Virtual Server instance and wait until it is stopped.
5. Delete the Virtual Server instance.

{% embed url="https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/python" %}

{% hint style="info" %}
In order to workaround unresolved issue with resource paths in the native python client for [kubevirt](https://github.com/kubevirt/client-python), we introduced class `KubeVirtClient` for basic operations on kubevirt VirtualMachine resources.
{% endhint %}

### Implementation

The python example consists of the [vsclient](../../../../virtual-server/examples/python/vsclient.py) and the [kubevirtclient](../../../../virtual-server/examples/python/kubevirtclient.py). The vsclient provides an interface in the form of helper functions to interact with the Virtual Server resource, while the kubevirtclient provides an interface to interact with the kubevirt subresource API in order to stop and start a Virtual Server. Both clients can be edited and used as drop in clients for a simple Virtual Server controller built in python.

### Installation

```
virtualenv -p python3 .venv && source ./.venv/bin/activate
pip install kubernetes
```

### Run

```
Be sure to set secure credentials for your USERNAME and PASSWORD, as they will be used to create a user in your Virtual Server
USERNAME=<my_username> PASSWORD=<my_password> NAMESPACE=<my_namespace> KUBECONFIG=$HOME/.kube/config python3 main.py
```
