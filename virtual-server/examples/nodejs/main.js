const VSClient = require("./client.js")
const { newVirtualServerManifest } = require("./util.js")

// Create a blank VirtualServer manifest
const virtualServerManifest = newVirtualServerManifest({
  name: "sample-virtual-server",
  namespace: "my-namespace"
})
// Configure a sample spec
virtualServerManifest.spec = {
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

const main = async() => {
  // Create and initialize a new VirtualServer client
  // Path to kube config may be null, in which case the default ~/.kube kubeconfig location will be used
  const client = new VSClient('/path/to/kube/config')
  await client.init()

  // Delete the existing VirtualServer: my-namespace/sample-virtual-server
  await client.virtualServer.delete({name: "sample-virtual-server", namespace: "my-namespace"})
    .then(o => o.statusCode === 200 && console.log("VS deleted"))
    .catch(err => console.log(err.toString()))

  // Create a new VirtualServer with the sample manifest
  await client.virtualServer.create(virtualServerManifest)
    .then(o => o.statusCode === 201 && console.log("VS created"))
    .catch(err => console.log(err.toString()))
  
  // Wait until the VirtualServer is ready
  await client.virtualServer.ready({name: "sample-virtual-server", namespace: "my-namespace"})
  .then(o => console.log("VS ready"))
  .catch(err => console.log(err.toString()))

  // Start the VirtualServer
  // After a VirtualServer is created, there may be a slight delay before the subresource API is available for the VirtualServer
  let started = false
  while(!started) {
    await client.virtualServer.start({name: "sample-virtual-server", namespace: "my-namespace"})
    .then(o => {
      if(o.statusCode === 202) {
        started = true
        console.log("VS started")
      }
    })
    .catch(err => err.statusCode === 404 ? console.log("Waiting for subresource API") : console.log(err.toString())) 
  }
  
  // Get the VirtualServer we created
  const vs = await client.virtualServer.get({name: "sample-virtual-server", namespace: "my-namespace"})
  .then(o => {
    console.log(`Found VS: ${o.body.metadata.name}`)
    return o.body
  })
  .catch(err => console.log(err.toString()))

  // Log the network status of the VirtualServer to the console
  const externalIP = vs.status.network.externalIP || ""
  const floatingIPs = vs.status.network.floatingIPs || {}
  const internalIP = vs.status.network.internalIP || ""
  console.log(`Virtual Server network status: 
    InternalIP: ${internalIP}
    ExternalIP: ${externalIP}
    FloatingIPs:
    \t${Object.entries(floatingIPs).map(([svc, ip]) => `${svc}: ${ip}`).join("\n\t")}
  `)
  /* 
  Sample Output:
    InternalIP: 1.2.3.4
    ExternalIP: 0.0.0.0
    FloatingIPs:
        sample-floating-ip-service: 1.1.1.1
  */

  // Stop the VirtualServer
  await client.virtualServer.stop({name: "sample-virtual-server", namespace: "my-namespace"})
  .then(o => o.statusCode === 202 && console.log("VS stopped"))
  .catch(err => console.log(err.toString()))
}
  
main()