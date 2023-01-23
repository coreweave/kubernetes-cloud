const VSClient = require("./client.js")
const { newVirtualServerManifest } = require("./util.js")

const namespace = process.env.NAMESPACE
const kubeconfig = process.env.KUBECONFIG
const username = process.env.USERNAME
const password = process.env.PASSWORD

if (!namespace || !kubeconfig) {
  throw Error ('NAMESPACE and KUBECONFIG variables are required.')
}

if (!username || !password) {
  throw Error ('USERNAME and PASSWORD variables are required.')
}

// Create a blank VirtualServer manifest
const virtualServerManifest = newVirtualServerManifest({
  name: "sample-virtual-server",
  namespace,
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
      storageClassName: "block-nvme-ord1",
      source: {
        pvc: {
          namespace: "vd-images",
          name: "ubuntu2004-nvidia-515-86-01-1-docker-master-20221205-ord1"
        }
      }
    }
  },
	// Add user
	// SSH public key is optional and allows to login without a password
	// Public key is located in $HOME/.ssh/id_rsa.pub
	// publicKey = `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEQCQpab6UWuA ... user@hostname`
  users: [
    {
      username,
      password
	  	// SSHPublicKey: publicKey
    }
  ],
	// Add cloud config
	// more examples on https://cloudinit.readthedocs.io/en/latest/topics/examples.html
  cloudInit: `
# Update packages
package_update: true
# Install packages
packages:
  - curl
  - git
# Run additional commands
runcmd:
  - [df, -h]
  - [git, version]
  - [curl, --version ]
`,
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
  }
}

const main = async() => {
  // Create and initialize a new VirtualServer client
  // Path to kube config may be null, in which case the default ~/.kube kubeconfig location will be used
  const client = new VSClient(kubeconfig)
  await client.init()

  // Delete the existing VirtualServer: my-namespace/sample-virtual-server
  await client.virtualServer.delete({name: "sample-virtual-server", namespace})
    .then(o => o.statusCode === 200 && console.log("VS deleted"))
    .catch(err => console.log(err.toString()))

  // Create a new VirtualServer with the sample manifest
  await client.virtualServer.create(virtualServerManifest)
    .then(o => o.statusCode === 201 && console.log("VS created"))
    .catch(err => console.log(err.toString()))
  
  console.log("Waiting for VS ready state")

  // Wait until the VirtualServer is ready
  await client.virtualServer.ready({name: "sample-virtual-server", namespace})
  .then(o => console.log("VS ready"))
  .catch(err => console.log(err.toString()))

  // Start the VirtualServer
  // After a VirtualServer is created, there may be a slight delay before the subresource API is available for the VirtualServer
  let started = false
  while(!started) {
    await client.virtualServer.start({name: "sample-virtual-server", namespace})
    .then(o => {
      if(o.statusCode === 202) {
        started = true
        console.log("VS started")
      }
    })
    .catch(err => err.statusCode === 404 ? console.log("Waiting for subresource API") : console.log(err.toString())) 
  }
  
  // Get the VirtualServer we created
  const vs = await client.virtualServer.get({name: "sample-virtual-server", namespace})
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
  await client.virtualServer.stop({name: "sample-virtual-server", namespace})
  .then(o => o.statusCode === 202 && console.log("VS stopped"))
  .catch(err => console.log(err.toString()))
}
  
main()
