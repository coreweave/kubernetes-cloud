---
description: Expose storage volumes using NFS server
---

# NFS

To expose storage using NFS, find the **nfs-server** application in [the Applications Catalog](../../../../welcome-to-coreweave/coreweave-cloud-ui/applications-catalog.md). Click the **Deploy** button to configure the NFS settings.

<figure><img src="../../../../.gitbook/assets/image (29) (2) (1).png" alt="The NFS application in the application Catalog"><figcaption><p>The NFS application in the application Catalog</p></figcaption></figure>

{% hint style="warning" %}
**Important**

One major difference between an NFS deployment and a Samba deployment on CoreWeave is that the one-click NFS solution **does not include any authentication.** For added security, consider integrating with Active Directory directly, or use network policies to ensure access to the NFS service is only accessible to the correct endpoints.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (27) (1).png" alt="The NFS configuration screen"><figcaption><p>The NFS configuration screen</p></figcaption></figure>

Give the NFS volume a name, then select a data center region. This region should be the same one in which the storage volume is deployed.

Select an [NFS squash option](https://docs.qnap.com/operating-system/qts/4.5.x/en-us/GUID-4A850D3A-5293-4B13-ABEF-8B66D1384BFC.html) from the drop-down menu, as well as what kind of access type you'd like the NFS server to have. In most cases, `RW` makes sense.

Toggle the **Expose on Public IP** toggle depending on whether or not you'd like to expose the service publicly. Next, highlight the associated storage volume from the **Available Volumes** list, then click the blue plus sign that appears to the right of its name to add it to the **Attach Volume** list.

Finally, click the **Deploy** button in the lower left-hand corner to deploy the NFS server.
