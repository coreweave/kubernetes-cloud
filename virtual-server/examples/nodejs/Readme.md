
## Virtual Server NodeJS Example

An example implementation in NodeJS of a kubernetes client to interact with a Virtual Server resource on Coreweave Cloud.

### Implementation Breakdown

The example is broken down into two parts, the [client](client.js), which is glue code layered on top of the godaddy implementation of a [kubernetes-client](https://github.com/godaddy/kubernetes-client), and the [application](main.js); both of which are described below.

### Client
The client ([client.js](client.js)) provides an interface to create a kubernetes client using your kubernetes credentials (token). Client.js may be dropped into any application and used to interface with Virtual Servers. A set of functions specific to creating, modifying, and checking the status of a Virtual Server are additionally provided and operate as follows:
> All functions below are within the client.virtualServer object

`init()`: Initialize the client
-- init must be called prior to using the Client
-- init will set up the client so that it is aware of Coreweave and Kubevirt CRDs as well as the kubevirt subresource api

`get({namespace, name})`: Retrieves a Virtual Server
* `namespace`: Namespace wherein the Virtual Server is deployed
* `name`: Name of the Virtual Server

`list({namespace})`: List all Virtual Servers
* `namespace`: Namespace wherein the Virtual Servers is deployed

`create(manifest)`: Retrieves a Virtual Server
* `manifest`: A Virtual Server manifest (JSON/Object)
	> Example manifests detailed in [Example Manifests](#example-manifests)

`delete({namespace, name})`: Delete a Virtual Server
* `namespace`: Namespace wherein the Virtual Server is deployed
* `name`: Name of the Virtual Server

`update(manifest)`: Update an existing Virtual Server
* `manifest`: An updated Virtual Server (JSON/Object)

`ready({namespace, name})`: Stopping function that waits for the VirtualMachineReady status condition of a Virtual Server
* `namespace`: Namespace wherein the Virtual Server is deployed
* `name`: Name of the Virtual Server


`start({namespace, name})`: Start a stopped Virtual Server
* `namespace`: Namespace wherein the Virtual Server is deployed
* `name`: Name of the Virtual Server

`stop({namespace, name})`: Stop a running Virtual Server
* `namespace`: Namespace wherein the Virtual Server is deployed
* `name`: Name of the Virtual Server

### Application
The application ([main.js](main.js)) implements client.js in order to create, watch, get, and update an example Virtual Server. The application serves as an example of how to implement client.js. Additionally, the application illustrates how one might retrieve status information from a running Virtual Server, retrieving it's run state and network information. Finally, the example shows how to simply interface with the subresource api, starting and stopping a Virtual Server.

### Example Manifests
```
{
  region: "ORD1",
  os: {
    type: "linux"
  },
  resources: {
    gpu: {
      type: "Quadro_RTX_4000",
      count: 4
    },
    cpu: {
      count: 2
    },
    memory: "16Gi"
  },
  storage: {
    root: {
      size: "40Gi",
      storageClassName: "ceph-ssd-2-replica",
      source: {
        pvc: {
          namespace: "vd-images",
          name: "ubuntu2004-docker-master-20210323-ord1"
        }
      }
    }
  },
  users: [
    {
      username: "user",
      password: "pass"
    }
  ],
  network: {
    public: true,
    tcp: {
      ports: [
        22,
        443,
        60443,
        4172,
        3389,
      ]
    },
    udp: {
      ports: [
        4172,
        3389
      ]
    }
  },
  initializeRunning: true
}
```
