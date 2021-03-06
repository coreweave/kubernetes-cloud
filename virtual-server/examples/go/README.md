# Go example

An example Go implementation of a kubernetes client that interacts with the CoreWeave VirtualServer resource as well as the kubevirt subresource api.

The Go example illustrates the following:
1. Build VirtualServer definition based on API https://github.com/coreweave/virtual-server.
2. Builds a Service and PVC to be used as a FloatingIP and Additional Filesystem respectively. 
3. Removal of an existing VirtualServer.
4. Creation of a new VirtualServer. The instance is started automatically.
5. Waiting for VirtualServer ready status. 
6. Stop the instance and wait until it is fully stopped.
7. Delete the VirtualServer.

## Run

The first run takes more time until all necessary packages are downloaded.

```
Be sure to use secure credentials for USERNAME and PASSWORD as they will be used to create a user in your Virtual Server
USERNAME=<my_username> PASSWORD=<my_password> KUBECONFIG=/home/<user>/.kubeconfig NAMESPACE=<namespace> make
```
