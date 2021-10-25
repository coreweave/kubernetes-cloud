# On-Premise Integration

Connecting the cloud to existing on-premise infrastructure allows customers to leverage powerful and elastic compute in CoreWeave Cloud without migrating their entire production pipeline. Three main areas of focus for a hybrid-cloud integration are:

* **On-Premise Storage** - Let Render Nodes and Virtual Workstations in CoreWeave Cloud seamlessly access storage hosted outside of CoreWeave
* **On-Premise Deadline **- Connect CoreWeave's auto-scaling render nodes to an existing on-premise deadline installation
* **Local Access to CoreWeave Storage **- Efficiently access CoreWeave storage from local workstations

Integration is achieved using one or a combination of multiple technologies.

* **CoreWeave CloudLink with Transparent Cache **- A small service running on an on-premise server forwarding access to local NFS, SMB file servers and Deadline services. A transparent cache running in CoreWeave Cloud minimizes the upstream bandwidth need even when rendering on hundreds of cloud nodes.
* **Site to Site VPN **- A site to site VPN is needed for more complex integration. It allows CoreWeave Cloud to act as a direct extension of an on-premise network. Storage in CoreWeave can be accessed by on-premise nodes over NFS and SMB, and storage on premise can be accessed directly from CoreWeave Cloud. Transparent Caching can optionally be employed to minimize upstream bandwidth requirement from the on-premise location. Deadline workers can run both on-premise and in the cloud, with the actual deadline installation also residing on either location.
* **Storage Synchronization **- In situations where direct storage access isn't performant, synchronizing all or partial on-premise storage to CoreWeave cloud is the best option. This is also a common choice when integrating Virtual Workstations over geographically dispersed location, providing the best user experience to all artists.

## Transparent Cache

![](../../../.gitbook/assets/111335067-772be780-864a-11eb-949c-56ece0902a9d.png)

A pull through transparent cache can be deployed in CoreWeave Cloud. Storage for the cache is backed by CoreWeave NVMe or HDD storage, and can be anywhere from 1GB to 500TB. The cache allows all on-premise storage to be efficiently accessed without first having to synchronize files. When an artists submits a render job, the first render worker to access an asset will cause that asset to be loaded from on-premise storage and stored in the cache. Subsequent access by other render nodes, or by subsequent render jobs will load the data directly from cache. When an artist makes a change to an asset, the cache is invalidated and the asset is pulled again on next render. As most assets, such as textures, don't change between iterations, high cache efficiency can be maintained, saving upstream bandwidth from the on-premise location.

## CoreWeave CloudLink

CoreWeave CloudLink consists if a small docker container running on a server in the on-premise environment. It can run on a physical Linux server or in a Virtual Machine, it can also run on certain docker capable storage solutions such as [Synology](https://www.synology.com/en-us) and [UNRAID](https://unraid.net). CoreWeave CloudLink exposes local SMB or NFS storage, as well as local Deadline services to your namespace in CoreWeave Cloud. CoreWeave CloudLink has a server component that is deployed via [Apps](https://apps.coreweave.com), running in your namespace. This server becomes the gateway to the on-premise resources and is protected by the same firewall and isolation as all other customer resources running in the CoreWeave Cloud namespace.

#### Requirements

* Linux server or Virtual Machine with good connectivity to the Storage Server
* One CPU core and 1GB of RAM
* Alternatively, CoreWeave CloudLink can run directly on Synology and UNRAID
* Upstream bandwidth of at least 500Mbps from the on-premise location is recommended
* If using NFS, the NFS share needs to be configured to allow connections from un-privileged ports



