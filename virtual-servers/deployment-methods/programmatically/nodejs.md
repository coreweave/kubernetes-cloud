---
description: >-
  An example implementation in NodeJS of a kubernetes client to interact with a
  Virtual Server resource on CoreWeave Cloud.
---

# NodeJS

## Implementation

The example is broken down into two parts, the [client](../../../virtual-server/examples/nodejs/client.js), which is glue code layered on top of the godaddy implementation of a [kubernetes-client](https://github.com/godaddy/kubernetes-client), and the [application](../../../virtual-server/examples/nodejs/main.js); both of which are described below.

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/nodejs" %}

### Client

The client ([`client.js`](../../../virtual-server/examples/nodejs/client.js)) provides an interface to create a Kubernetes client using your Kubernetes credentials (token). `client.js` may be dropped into any application and used to interface with the Virtual Server resource.

A set of functions specific to creating, modifying, and checking the status of a Virtual Server are additionally provided, which operate as follows:

<table><thead><tr><th width="338.91081336596994">Function name</th><th>Description</th></tr></thead><tbody><tr><td><code>init()</code></td><td><p>Initializes the client</p><p><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong><code>init()</code> must be called prior to using the client</strong></p></td></tr><tr><td><code>namespace</code></td><td>Namespace in which the Virtual Server is deployed</td></tr><tr><td><code>name</code></td><td>Name of the Virtual Server</td></tr><tr><td><code>virtualServer.start({namespace, name})</code></td><td>Starts a stopped Virtual Server</td></tr><tr><td><code>virtualServer.stop({namespace, name})</code></td><td>Stops a running Virtual Server</td></tr><tr><td><code>virtualServer.get({namespace, name})</code></td><td>Retrieves a Virtual Server</td></tr><tr><td><code>virtualServer.ready({namespace, name})</code></td><td>Stopping function that waits for the <code>VirtualMachineReady</code> status condition of a Virtual Server</td></tr><tr><td><code>virtualServer.delete({namespace, name})</code></td><td>Deletes a Virtual Server</td></tr><tr><td><code>manifest</code></td><td>A Virtual Server manifest (JSON/Object) - <em>See</em> <a href="nodejs.md#example"><em>Examples</em></a></td></tr><tr><td><code>virtualServer.list({namespace})</code></td><td>Lists all Virtual Servers</td></tr><tr><td><code>virtualServer.create(manifest)</code></td><td>Creates a Virtual Server</td></tr><tr><td><code>virtualServer.update(manifest)</code></td><td>Update an existing Virtual Server</td></tr></tbody></table>

### Application

The application ([`main.js`](../../../virtual-server/examples/nodejs/main.js)) implements `client.js` in order to create, watch, get, and update an example Virtual Server.

The example application serves as an example of how to implement `client.js`. Additionally, the example application illustrates how one might retrieve status information from a running Virtual Server, retrieving its run state and network information.

Finally, the example shows how to simply interface with the `kubevirt __ subresource` API in order to start and stop a Virtual Server.

### Example

```
{
  apiVersion: "virtualservers.coreweave.com/v1alpha1",
  kind: "VirtualServer",
  metadata: {
    name: "example-vs",
    namespace: "my-namespace"
  },
  spec: {
    region: "ORD1",
    os: {
      type: "linux"
    },
    resources: {
      gpu: {
        type: "Quadro_RTX_4000",
        count: 1
      },
      cpu: {
        count: 3
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
        username, #Set from environment variable
        password #Set from environment variable
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
}
```
