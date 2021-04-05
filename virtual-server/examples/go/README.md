# Go example

An example Go implementation of a kubernetes client that interacts with the CoreWeave VirtualServer resource as well as the kubevirt subresource api.

The Go example illustrates the following:
1. Build VirtualServer definition based on API https://github.com/coreweave/virtual-server.
2. Removal of an existing VirtualServer.
3. Creation of a new VirtualServer. The instance is started automatically.
4. Waiting for VirtualServer ready status. 
4. Stop the instance and wait until it is fully stopped.
5. Delete the VirtualServer.

## Run

The first run takes more time until all necessary packages are downloaded.

```
KUBECONFIG=/home/<user>/.kubeconfig NAMESPACE=<namespace> make
```
