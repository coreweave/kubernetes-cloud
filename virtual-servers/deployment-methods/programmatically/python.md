---
description: >-
  An example Python implementation of a kubernetes client that interacts with
  the CoreWeave VirtualServer resource as well as the kubevirt subresource api.
---

# Python

In [this example](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/python), Python is used to perform the following actions via the Kubernetes REST API using Bash:

1. **Remove** an existing Virtual Server.
2. **Create** of a new Virtual Server based on the `my_virtualserver` example configuration
3. **Wait** for a Virtual Server `Ready` status.
4. **Stop** the Virtual Server instance and wait until it is stopped.
5. **Delete** the Virtual Server instance.

{% hint style="info" %}
**Note**

In order to work around an unresolved issue with resource paths in the native Python client for [kubevirt](https://github.com/kubevirt/client-python), we introduced the class `KubeVirtClient` for basic operations on kubevirt VirtualMachine resources.
{% endhint %}

## Implementation

Follow along by cloning the example script:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/python" %}

The Python example consists of two pieces of code: [vsclient](../../../virtual-server/examples/python/vsclient.py) and [kubevirtclient](../../../virtual-server/examples/python/kubevirtclient.py).

The vsclient provides an interface in the form of helper functions to interact with the Virtual Server resource, while the kubevirtclient provides an interface to interact with the kubevirt subresource API in order to stop and start a Virtual Server.

Both clients can be edited and used as drop-in clients for a simple Virtual Server controller built in Python.

## Installation

```
virtualenv -p python3 .venv && source ./.venv/bin/activate
pip install kubernetes
```

## Run

Be sure to set secure credentials for your `USERNAME` and `PASSWORD`, as they will be used to create a user in your Virtual Server.

```
USERNAME=<my_username> PASSWORD=<my_password> NAMESPACE=<my_namespace> KUBECONFIG=$HOME/.kube/config python3 main.py
```
