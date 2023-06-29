---
description: Build a feature-rich VFX studio on CoreWeave Cloud
---

# Get Started with VFX Studios

CoreWeave Cloud makes it easy to deploy an end-to-end VFX production pipeline in the Cloud. Solutions can be either hosted entirely on CoreWeave Cloud, or integrated with pipelines hosted elsewhere.

* :earth\_africa: With [data center locations](../coreweave-kubernetes/data-center-regions.md) in New York City, Chicago and Las Vegas, CoreWeave guarantees a low-latency Virtual Workstation experience for remote employees.
* :zap:The industry's fastest autoscale starts your tasks on hundreds of GPUs or thousands of CPUs in 30 seconds, and scales them down once finished to avoid incurring charges while idle.

<figure><img src="../.gitbook/assets/110822001-a1eafa00-825e-11eb-9f67-66411d3ad641.png" alt="Diagram displaying various configuration options and applications for Virtual Workstations on CoreWeave Cloud"><figcaption><p>Configuration possibilities are endless with CoreWeave Virtual Workstations</p></figcaption></figure>

## Components of CoreWeave VFX Studios

Like any VFX studio, CoreWeave Cloud studios are comprised of multiple parts. The diagram below offers a visual example of how each part works together within the Cloud.

### :desktop: Virtual Workstations

Linux and Windows high performance workstations with NVIDIA GPUs for editing, compositing and modeling work with direct access to storage and render capacity. Workstations come pre-loaded with [Teradici](https://www.teradici.com) or Parsec for multi monitor 4K support. New workstations can be instantiated in a minute, and stopped when the work-day is over.

### :brain: Managed Thinkbox Deadline

With a one-click deployment of a fully managed [Thinkbox Deadline](https://docs.thinkboxsoftware.com/products/deadline/10.1/1\_User%20Manual/manual/overview.html) instance, you can connect local artists via Remote Connection Server.

### :file\_cabinet: High-performance storage

Shared file systems optimized for VFX feeding render workers and virtual workstations at wire speed. All storage is replicated to prevent data loss, and both ultra high performance NVMe and HDD storage is available.

### :globe\_with\_meridians: Low-latency networking

Each CoreWeave data center features redundant, 200Gbps+ public Internet connectivity from Tier 1 global carriers, and are connected to each other with 400Gbps+ of dark fiber transport, allowing for easy, free data transfers within CoreWeave Cloud.

### :link: On-premise integrations with CoreWeave CloudLink



## Authentication with Active Directory

The examples in these guides assume that user authentication is desired. Many examples in this guide use Active Directory for user management and authentication.

Therefore, it is assumed that [an Active Directory domain](../virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/) - required to use Active Directory for user authentication - has already been provisioned.

{% hint style="success" %}
**Tip**

[Setting up an Active Directory domain](../virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/) may be a good place to start when setting up your Cloud studio, but you can also come back later to configure Active Directory after other components are deployed.
{% endhint %}
