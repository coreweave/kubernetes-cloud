const { KubeConfig, Client } = require('kubernetes-client')
const Request = require('kubernetes-client/backends/request')
const YAML = require('yaml')

// Request to the kubevirt subresource api
const VMBackendRequest = (kubeclient, namespace, name, command) =>
  kubeclient.apis['kubevirt.io'].v1.namespace(namespace).virtualmachines(name).get().then(r => {
    const vm = r.body
    const apiStorageVersion = vm.metadata.annotations["kubevirt.io/storage-observed-api-version"]
    const vmSubresourceCommandURL = `/apis/subresources.kubevirt.io/${apiStorageVersion}/namespaces/${namespace}/virtualmachines/${name}/${command}`
    const options = {
      method: 'PUT',
      pathname: vmSubresourceCommandURL,
      headers: {
        "Accept": "*/*" 
      }
    }
    return kubeclient.backend.http(options)
  })

// A kubernetes client for creating and managing VirtualServers
class VSClient {
  // Create a new VSClient. 
  // kubeconfig is a path to a local kubeconfig file. 
  // kubeconfig may be null, in which case the environment variable KUBECONFIG will be used, ~/.kube/config will be used, and lastly an in cluster service account will be used
  constructor(kubeconfig) {
    this.initialized = false
    let backend = null
    if(kubeconfig) {
      const config = new KubeConfig()
      config.loadFromFile(kubeconfig)
      backend = new Request({kubeconfig: config})
    }  
    this.kubeclient = new Client({version: '1.13', backend})
    const initCheck = () => this.initialized === true ? Promise.resolve() : Promise.reject(new Error("Client not yet initialized. Call init before using the client."))
    for(let k in this.virtualServer) {
      const f = this.virtualServer[k]
      if(typeof f === 'function') {
        this.virtualServer[k] = (...args) => initCheck().then(() => f(...args))
      }
    }
  }
  // init will initialize the client for use. init must be run before any VirtualServer function is called
  init = async() => {
    const virtualServerCRD = await this.kubeclient.apis['apiextensions.k8s.io'].v1beta1.customresourcedefinitions("virtualservers.virtualservers.coreweave.com").get().then(r => r.body)
    this.kubeclient.addCustomResourceDefinition(virtualServerCRD)
    this.initialized = true
  }
  
  // functions to interface with VirtualServers
  virtualServer = {
    // Stop an already running VirtualServer
    stop: ({namespace, name}) => {
      if(!namespace || !name) {
        return Promise.reject(new Error("Virtual Server namespace and name are required"))
      }
      return VMBackendRequest(this.kubeclient, namespace, name, "stop")
    },
    // Start a stopped VirtualServer
    start: ({namespace, name}) => {
      if(!namespace || !name) {
        return Promise.reject(new Error("Virtual Server namespace and name are required"))
      }
      return VMBackendRequest(this.kubeclient, namespace, name, "start")
    },
    // Get a VirtualServer deployed
    get: ({namespace, name}) => {
      if(!namespace || !name) {
        return Promise.reject(new Error("Virtual Server namespace and name are required"))
      }
      return this.kubeclient.apis['virtualservers.coreweave.com'].v1alpha1.namespaces(namespace).virtualservers(name).get()
    },
    // Create a new VirtualServer
    // manifest is a yaml string
    create: (manifest) => {
      const manifestObj = YAML.parse(manifest)
      if(!manifestObj.metadata.namespace) {
        return Promise.reject(new Error("VirtualServer metadata.namespace is required"))
      }
      return this.kubeclient.apis['virtualservers.coreweave.com'].v1alpha1.namespaces(manifestObj.metadata.namespace).virtualservers.post({body: manifestObj})
    },
    // Delete a VirtualServer
    delete: ({namespace, name}) => {
      if(!namespace || !name) {
        return Promise.reject(new Error("Virtual Server namespace and name are required"))
      }
      return this.kubeclient.apis['virtualservers.coreweave.com'].v1alpha1.namespaces(namespace).virtualservers(name).delete()
    },
    // Update a new VirtualServer
    // manifest is a yaml string
    update: async (manifest) => {
      const manifestObj = YAML.parse(manifest)
      if(!manifestObj.metadata.namespace || !manifestObj.metadata.name) {
        return Promise.reject(new Error("VirtualServer metadata.namespace and metadata.name is required"))
      }
      if(!manifestObj.metadata.resourceVersion) {
        await this.virtualServer.get({namespace: manifestObj.metadata.namespace, name: manifestObj.metadata.name}).then(o => manifestObj.metadata.resourceVersion = o.body.metadata.resourceVersion)
      }
      return this.kubeclient.apis['virtualservers.coreweave.com'].v1alpha1.namespaces(manifestObj.metadata.namespace).virtualservers(manifestObj.metadata.name).put({body: manifestObj})
    },
    // Ready will resolve when the VirtualServer is ready (determined by the status field of the Ready Condition)
    ready: async({namespace, name}) => {
      if(!namespace || !name) {
        return Promise.reject(new Error("Virtual Server namespace and name are required"))
      }
      const stream = await this.kubeclient.apis['virtualservers.coreweave.com'].v1alpha1.watch.namespaces(namespace).virtualservers(name).getObjectStream()
      return new Promise((resolve, reject) => {
        stream.on('data', async e => {
          if(e.type === 'DELETED') {
            stream.end()
            return reject(new Error(`VirtualServer ${namespace}/${name} was deleted`))
          }
          else {
            if(!!e.object.status) {
              const readyCondition = e.object.status.conditions.filter(c => c.type === 'Ready')[0] || {}
              if(readyCondition.status === 'True') {
                stream.end()
                return resolve('Ready')
              }
            }
          }
        })
      })
    }
  }
}

module.exports = VSClient