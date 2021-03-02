const VSClient = require("./client.js")

// A sample VirtualServer manifest
const virtualServerManifest = `
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: sample-virtual-server
  namespace: my-namespace
spec:
  region: ORD1
  affinity: {}
  os:
    type: "linux"
  resources:
    definition: "a"
    gpu:
      type: "Quadro_RTX_4000"
      count: 4
    cpu:
      count: 2
    memory: 16Gi
  storage:
    root:
      size: 40Gi
      volumeMode: Block
      accessMode: ReadWriteOnce
      storageClassName: ceph-ssd-2-replica
      source:
        pvc:
          namespace: vd-images
          name: ubuntu2004-docker-master-20210210-ord1
  users:
    - username: user
      password: pass
  network:
    tcp:
      ports:
      - 22
      - 443
      - 60443
      - 4172
      - 3389
    udp:
      ports:
      - 4172
      - 3389
`

const main = async() => {
  // Create and initialize a new VirtualServer client
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

  // Increase the memory resource request to 32Gi and update the VirtualServer
  vs.spec.resources.memory = "32Gi"
  await client.virtualServer.update(JSON.stringify(vs))
    .then(o => o.statusCode === 200 && console.log("VS patched"))
    .catch(err => console.log(err))

  // Stop the VirtualServer
  await client.virtualServer.stop({name: "sample-virtual-server", namespace: "my-namespace"})
  .then(o => o.statusCode === 202 && console.log("VS stopped"))
  .catch(err => console.log(err.toString()))
}
  
main()