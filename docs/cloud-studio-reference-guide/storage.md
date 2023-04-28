---
description: Learn how to configure and use storage for your VFX Cloud Studio
---

# Storage

Storage is, of course, an essential part of any VFX studio. In this section, we will walk through the most basic storage configuration appropriate for a VFX studio by deploying a filesystem volume for asset storage and then exposing the storage volume externally.

{% hint style="success" %}
**Tip**

If your studio configuration requires a more custom solution, [reach out to your CoreWeave Support Specialist](https://cloud.coreweave.com/contact).
{% endhint %}

## Setup

First, [log in to your CoreWeave Cloud account](https://cloud.coreweave.com). Navigate to [the application Catalog](https://apps.coreweave.com) by clicking **Applications** in the right-hand menu. From there, search for `filesystem-volume`, then select the **filesystem-volume** application.

<figure><img src="../.gitbook/assets/image (120).png" alt="The filesystem-volume application in the application Catalog"><figcaption><p>The filesystem-volume application displayed in the application Catalog</p></figcaption></figure>

Click the **Deploy** button in the upper right-hand corner to open the configuration screen. Set a name for the filesystem, then set the [data center region](../data-center-regions.md), [storage type](broken-reference), and storage size.

{% hint style="info" %}
**Note**

This application will create a **shared filesystem**. If you require a **block filesystem** instead, [please refer to the Storage documentation](broken-reference).&#x20;
{% endhint %}

<figure><img src="../.gitbook/assets/image (125).png" alt="Storage configuration for the filesystem-volume application"><figcaption><p>Storage configuration for the filesystem-volume application</p></figcaption></figure>

In this example, we create a filesystem volume for render outputs. This way, all of our virtual desktops can access the same shared storage as our rendering nodes.

When rendering on CoreWeave Cloud, ensuring that applications don't attempt to write over the Internet to on-premise storage is essential. It is typically recommended that large amounts of data accessed infrequently - such as render outputs - be allocated to our HDD tier.

{% hint style="info" %}
**Note**

For this example, everything is provisioned to the Chicago datacenter (`ORD1`), however if you are following along, it is recommended to select the datacenter closest to you. [Read more about CoreWeave's data center regions](../data-center-regions.md).
{% endhint %}

<figure><img src="../../.gitbook/assets/image (66) (1).png" alt="The filesystem storage application configuration screen"><figcaption><p>The filesystem storage application configuration screen</p></figcaption></figure>

After clicking on the **Deploy** button, the status screen will inform you that the volume has been created.

![The post-deployment status screen, including a status message](<../../.gitbook/assets/image (58).png>)

From the **Applications** tab, you will also be able to see the filesystem volume with the name you've assigned it.

![The filesystem volume application](<../../.gitbook/assets/image (76).png>)

If you would like to use Kubernetes to view the new storage volume, you may use `kubectl` to list the existing Persistent Volume Claims (PVCs) in the namespace.

```bash
$ kubectl get pvc
```

To get more details on the storage volume, invoke:

```bash
$ kubectl describe pvc <name of pvc>
```

{% hint style="info" %}
**Note**

If you installed Helm on your local machine, you can also use `helm list` to see the full list of all applications deployed in your namespace.
{% endhint %}

With this new storage volume deployed, the shared volume can be mounted onto any Kubernetes Pod or onto a [CoreWeave Virtual Server](broken-reference).

## Exposing storage

{% hint style="info" %}
**Note**

The following guides recommend deploying storage sharing solutions in the same data center region into which the storage volume created earlier was provisioned. While it is _possible_ to deploy the server in a region different to the one in which the storage volume was deployed, it is not recommended due to resulting storage latency, which will degrade overall performance.
{% endhint %}

CoreWeave provides many methods out of the box for exposing your storage volumes to external workstations or on-premise services. Storage volumes can also be exposed in custom ways using your own containerized images.

There are two primary methods of connecting storage for render outputs to a Virtual Server:

* (Linux and macOS) Using [an NFS server](storage.md#exposing-storage-via-nfs)
* (Windows) Mount exported storage from[ Samba to the workstation after initialization](storage.md#using-samba)
* (Any OS) Use [the FileBrowser application](storage.md#filebrowser)

{% hint style="info" %}
**Note**

If you prefer to associate storage volumes with mount points by designating them in the YAML manifest for the application, navigate to the **YAML tab** at the top of the application configuration screen, then edit the manifest:

```yaml
mounts:
  - name: render-output
    pvc: render-output
```
{% endhint %}

### Exposing storage externally using Samba

Both the standard flavor of Samba as well as the Active Directory version may be installed into CoreWeave Cloud from [the Cloud UI application Catalog](https://apps.coreweave.com).

<div>

<figure><img src="../../.gitbook/assets/image (62) (1) (1).png" alt="The standard Samba icon in the application Catalog"><figcaption><p>The standard Samba icon in the application Catalog</p></figcaption></figure>

 

<figure><img src="../.gitbook/assets/image (133).png" alt="The Active Directory Samba icon in the application Catalog"><figcaption><p>The Active Directory Samba icon in the application Catalog</p></figcaption></figure>

</div>

{% hint style="info" %}
**Note**

The Active Directory flavor of the Samba application will require a domain controller to be set up in your namespace with an address specified during deployment.
{% endhint %}

To deploy either, first search for **Samba** in the application Catalog, then select the desired application from the Catalog results. Click the **Deploy** button in the lower right-hand area to begin configuring the instance.

From the following configuration screen, be sure to specify the same data center region into which you deployed your filesystem volume earlier.

{% hint style="info" %}
**Note**

If you require more advanced access permissions for your Samba volume, consider pairing our **samba-ad** option with your on-premise Active Directory domain services.&#x20;
{% endhint %}

Next, create a user for the volume share. Finally, from the volumes section at the bottom of the configuration menu, highlight the name of the storage volume created earlier, then click the blue plus sign to the right of its name. This will add the volume to the **Attach Volume** list.

If you would like to edit the YAML manifest for this application directly, navigate to the YAML tab from within the application's configuration screen. In this manifest example, the name of the mounted volume is specified, as is the related storage volume (PVC):

{% hint style="warning" %}
**Important**

If you would like the service to be accessible from other places on the Internet, ensure the **Expose on public IP** slider is in the "true" position (green, with the slider on the right).
{% endhint %}

The following examples demonstrate different configuration settings per Samba type.

{% tabs %}
{% tab title="Standard Samba configuration" %}
## Standard Samba configuration

To install a standard Samba instance, navigate to the application Catalog and search for **Samba**. Select the Samba application, then click the **Deploy** button in the lower right-hand corner to open the configuration options.

<figure><img src="../.gitbook/assets/image (30) (3).png" alt="The standard Samba configuration options"><figcaption><p>The standard Samba configuration options</p></figcaption></figure>

Under the **Form** tab, within the **Samba Server** box, select the same region into which your storage volume was provisioned earlier.

Next, select the number of replicas you'd like the Pod to have. Then, choose whether you'd like to expose the instance publicly by altering the **Expose on Public IP** toggle, which allows, enables or disables public networking accordingly.

The following box, **User Information**, is for configuring the Samba user account. Input the **Username, Password, User ID, Group name,** and **Group ID** to use for the Samba share.

Configure associated storage volumes from the volumes panes at the bottom of the menu. Highlight the desired storage volume from the **Available Volumes** list, then click the blue plus sign to the right of the volume's name to add it to the **Attach Volume** list.

Finally, click the **Deploy** button in the lower left-hand corner.
{% endtab %}

{% tab title="Samba-AD configuration" %}
## Samba Active Directory configuration

To install a Samba-AD instance, navigate to the application Catalog and search for **Samba**. Select the **samba-ad** application, then click the **Deploy** button in the lower right-hand corner to open the configuration options.

<figure><img src="../.gitbook/assets/image (38).png" alt="The Samba-AD configuration options"><figcaption><p>The Samba-AD configuration options</p></figcaption></figure>

First, select the same data region into which your storage volume was provisioned earlier. Then, complete the Samba Server Domain information, and whether or not to specify a custom DNS suffix.



{% hint style="info" %}
**Note**

Custom DNS suffixes are usually for on-premise domains connected via VPN.
{% endhint %}



Configure associated storage volumes from the volumes panes at the bottom of the menu. Highlight the desired storage volume from the **Available Volumes** list, then click the blue plus sign to the right of the volume's name to add it to the **Attach Volume** list.

Finally, click the **Deploy** button in the lower left-hand corner.
{% endtab %}
{% endtabs %}

Once you are finished configuring your Samba instance, click the **Deploy** button in the lower left corner. After the application has finished deploying, you'll see a success message like the one below, which will provide you with your initial login information.

<figure><img src="../../.gitbook/assets/image (72).png" alt="A successful post-installation message"><figcaption><p>A successful post-installation message</p></figcaption></figure>

Additionally, now from the **Applications** tab, both the shared filesystem volume as well as the new Samba instance should be listed as exemplified below.

![Both the render-output storage volume (PVC) and the render-outputs-samba Samba instance are listed in the Applications page](<../.gitbook/assets/image (152).png>)

### Connecting to Samba (Windows)

After deploying your Samba instance, the **Installation Notes** section will provide the `.coreweave.cloud` domain name for the instance. You can connect to this drive by utilizing Windows "Map network drive" option.

![The DNS name listed in the success message of the Samba deployment](<../../.gitbook/assets/image (73) (1).png>)

Navigate to the Start menu and right-click the name of your local machine. Select **Map network drive...** from the drop-down.

<figure><img src="../../.gitbook/assets/image (70).png" alt="Screenshot of Map network drive..."><figcaption></figcaption></figure>

Map the network drive by providing the given Samba domain name to the **Folder** input field. Then click the **Browse...** button.

![Mapping the network drive using the provided DNS name](<../.gitbook/assets/image (139).png>)

![The mapped drive, listed in the Browse for Folder listing](<../../.gitbook/assets/image (65) (1).png>)

Select the mount, click the OK button, then enter your credentials.

![A successful mount](<../../.gitbook/assets/image (74) (1).png>)

## Exposing storage via NFS

To expose the same storage over NFS, search for the NFS application in the application Catalog. Click the **Deploy** button to configure the NFS settings.

<figure><img src="../.gitbook/assets/image (29) (1).png" alt="The NFS application in the application Catalog"><figcaption><p>The NFS application in the application Catalog</p></figcaption></figure>

{% hint style="warning" %}
**Important**

One major difference between an NFS deployment and a Samba deployment on CoreWeave is that the one-click NFS solution **does not include any authentication.** For added security, consider integrating with Active Directory directly, or use network policies to ensure access to the NFS service is only accessible to the correct endpoints.
{% endhint %}

<figure><img src="../.gitbook/assets/image (27) (1).png" alt="The NFS configuration screen"><figcaption><p>The NFS configuration screen</p></figcaption></figure>

First, give the NFS volume a name. Then, select the same data region into which the storage volume was provisioned earlier.

Select an [NFS squash option](https://docs.qnap.com/operating-system/qts/4.5.x/en-us/GUID-4A850D3A-5293-4B13-ABEF-8B66D1384BFC.html) from the drop-down menu, as well as what kind of access type you'd like the NFS server to have. In most cases, `RW` makes sense.

Toggle the **Expose on Public IP** toggle depending on whether or not you'd like to expose the service publicly. Next, highlight the associated storage volume from the **Available Volumes** list, then click the blue plus sign that appears to the right of its name to add it to the **Attach Volume** list.

Finally, click the **Deploy** button in the lower left-hand corner.

<figure><img src="../.gitbook/assets/Screenshot 2021-10-18 170110.jpg" alt="The updated applications listing page"><figcaption><p>The updated applications listing page, including both Samba and NFS</p></figcaption></figure>

## Exposing storage via FileBrowser

A final option for accessing your Cloud storage remotely is by using the FileBrowser application from the applications Catalog. Once installed, FileBrowser will provide a Web interface from which files can be uploaded and downloaded files easily from your Cloud storage.

To install FileBrowser, first navigate to the applications Catalog, then search for **filebrowser**.

<figure><img src="../.gitbook/assets/image (24) (1).png" alt=""><figcaption><p>The filebrowser application</p></figcaption></figure>

Navigate to the application Catalog through the CoreWeave Cloud UI, then search for `filebrowser`.  Select the application, then click the **Deploy** button in the lower right-hand corne

Under **Node Selection**, select the same data center region into which the storage volume was provisioned earlier.

Under the "Attach existing volumes to your FileBrowser" list, highlight the associated storage volume, then click the blue plus sign to the right of its name.

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption><p>The FileBrowser configuration screen, including a list of "Available Volumes"</p></figcaption></figure>

Configure how you'd like the Volume to appear once mounted, then click the **Deploy** button.

{% hint style="info" %}
**Note**

It is recommended that the name you give this FileBrowser application be very short, or you will run into SSL CNAME issues.
{% endhint %}

During the deployment of the application, you'll be redirected to a status page, which will update when the Pod running the FileBrowser application is ready. This status page also provides default login credentials for the FileBrowser application.

In the **Access URLs** box on the status page, you will find an Ingress URL (such as `https://filebrowser-name.tenant-sta-coreweave-clientname.ord1.ingress.coreweave.cloud/`). This Ingress URL may be used to access the FileBrowser application in a browser.

{% hint style="warning" %}
**Important**

After the first login, it is strongly recommended to change the password of your FileBrowser user account. Log in, then navigate to **Settings -> User Management** to configure new users.
{% endhint %}

<figure><img src="../.gitbook/assets/filebrowser-screen.png" alt="A successful FileBrowser post-installation screen"><figcaption><p>A successful FileBrowser post-installation screen</p></figcaption></figure>

## Media Shuttle

[Media Shuttle](https://www.signiant.com/products/media-shuttle/) makes it easy to share and receive media from outside parties. The MediaShuttle service may be used with your own subscription, or you may acquire a license via CoreWeave. If you'd like to license Media Shuttle via CoreWeave's licensing, [contact your CoreWeave Support Specialist](https://cloud.coreweave.com/contact).

### Setup

Once you have a working Media Shuttle license, locate your Media Shuttle registration key by opening Media Shuttle. Click "Add" beside Storage.

<figure><img src="../.gitbook/assets/image (48) (1) (1).png" alt="Screenshot of the &#x22;Add&#x22; link located on the Media Shuttle menu"><figcaption><p>The "Add" link located on the Media Shuttle menu</p></figcaption></figure>

Then, select the checkbox to agree to the license agreement terms.

<figure><img src="../.gitbook/assets/image (39) (1).png" alt="Screenshot of the license agreement checkbox in Media Shuttle"><figcaption><p>License agreement checkbox</p></figcaption></figure>

Once you have completed the wizard, the storage server registration key will be presented to you. Retain this for the next few setup steps.

Return to the applications Catalog from CoreWeave Cloud, and search for `media-shuttle`. Find the **media-shuttle** application, select it, then click the **Deploy** button in the bottom right corner of the screen to begin configuring the application.

<figure><img src="../../.gitbook/assets/image (64) (1) (1).png" alt="The Media Shuttle application icon"><figcaption><p>The Media Shuttle application icon displayed in the applications Catalog</p></figcaption></figure>

Clicking the **Deploy** button will open the application configuration screen.

![After pressing Media Shuttle](<../.gitbook/assets/image (131).png>)

Update the name, registry key, and add a [Persistent Volume Claim](https://docs.coreweave.com/coreweave-kubernetes/storage) to the `mounts` list by navigating to the **YAML** tab and locating the `mounts` block. In the example below, the PVC that has been added is defined with a mountpoint `name` of `render-output-mnt` and passed the PVC title, `pvc: render-output`.

<figure><img src="../.gitbook/assets/image (47) (1).png" alt="A defined mount in the mounts block"><figcaption><p>A defined mount in the <code>mounts</code> block</p></figcaption></figure>

Finally, click the **Deploy** button at the bottom of the screen to launch the deployment.

Once the deployment has completed, you will be automatically redirected to the Media Shuttle deployment status page. Once this status page shows that the Media Shuttle Pod is ready, you are ready to use the deployment.

<figure><img src="../.gitbook/assets/image (150).png" alt="Media Shuttle deployment status page, showing the Pod is ready"><figcaption><p>Media Shuttle deployment status page, showing the Pod is ready</p></figcaption></figure>
