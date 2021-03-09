// Validates is a quantity is a valid k8s resource.Quantity
const k8sValidateQuantity = (size) => /^(\+|-)?(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(([KMGTPE]i)|[numkMGTPE]|([eE](\+|-)?(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))))?$/.test(size)
// Create a new blank VirtualServer Manifest object
const newVirtualServerManifest = ({name, namespace}) => ({
  apiVersion: "virtualservers.coreweave.com/v1alpha1",
  kind: "VirtualServer",
  metadata: {
    name,
    namespace
  },
  spec: {
    affinity: {},
    region: "",
    os: {
      definition: "a",
      type: ""
    },
    resources: {
      definition: "a",
      gpu: {
        type: null,
        count: null,
      },
      cpu: {
        type: null,
        count: null,
      },
      memory: ""
    },
    storage: {
      root: {
        size: "",
        source: {
          pvc: {
            namespace: "",
            name: ""
          },
          storageClassName: "",
          volumeMode: null,
          accessMode: null
        }
      },
      additionalDisks: [
        
      ],
      filesystems: [

      ],
      swap: null
    },
    users: [

    ],
    network: {
      tcp: [],
      udp: [],
      directAttachLoadBalancerIP: false,
      floatingIPs: []
    },
    initializeRunning: false
  }
})

module.exports = {
  k8sValidateQuantity,
  newVirtualServerManifest
}