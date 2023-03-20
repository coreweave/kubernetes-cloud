---
description: Install a filesystem browser to use with storage volumes
---

# FileBrowser

Many use cases on CoreWeave Cloud require files to be uploaded to or downloaded from CoreWeave storage volumes. Using [the FileBrowser application](https://filebrowser.org/), deployable from the applications Catalog, can make this process much easier.

{% hint style="info" %}
**Note**

You will want to ensure that the storage volume you want to use with FileBrowser is already created before deploying the FileBrowser. See [Storage](broken-reference) for more information.
{% endhint %}

## Deploy the application

<figure><img src="../.gitbook/assets/image (24).png" alt=""><figcaption><p>The filebrowser application</p></figcaption></figure>

To deploy FileBrowser, first log in to your CoreWeave Cloud account. Then, navigate to [the Applications Catalog](../coreweave-kubernetes/applications-catalog.md). Once in the Catalog, use the search bar to search for `filebrowser`.

When the **filebrowser** application appears, click on it. This will open the application's about page. At the bottom or top right-hand corner of the screen, click the **Deploy** button to open the deployment page for the application. From this page, set a **Name** for the application. Then, under **Node Selection**, select your [data center region](../data-center-regions.md).

{% hint style="info" %}
**Note**

It is recommended that the name you give the FileBrowser application be very short, or else you may run into SSL CNAME issues.
{% endhint %}

<figure><img src="../.gitbook/assets/image (54).png" alt="Screenshot: Select your data center region"><figcaption><p>Select your data center region</p></figcaption></figure>

### Attach volumes

Under the "Attach existing volumes to your FileBrowser" list, under the "Available Volumes" menu, find the volume you'd like to attach to FileBrowser. In the example shown below, the volume named `shared-data-pvc` is being attached.

Click the small blue plus sign to the right of the Volume name to move it to the list on the right.

<figure><img src="../.gitbook/assets/image (73).png" alt="Screenshot: Click the blue plus sign beside the volume you wish to attach"><figcaption><p>Click the blue plus sign beside the volume you wish to attach</p></figcaption></figure>

Configure how you'd like the volume to appear once mounted. In the example shown here, the `shared-data-pvc` volume retains its same name for the mount path.

<figure><img src="../.gitbook/assets/image (69) (1).png" alt=""><figcaption></figcaption></figure>

Once you are ready, click the **Deploy** button.

During the deployment of the application, you will be redirected to the application's status page, which will let you know when the FileBrowser application is ready. This status page also provides the default login credentials for the FileBrowser application.

<figure><img src="../.gitbook/assets/image (65).png" alt="Screenshot: For this example, the default login credentials have been removed, but in a real scenario, will be shown here"><figcaption><p>For this example, the default login credentials have been removed, but in a real scenario, will be shown here</p></figcaption></figure>

****

## Access FileBrowser

In the **Access URLs** box on the status page, you will find an Ingress URL (for example, `https://filebrowser-name.tenant-sta-coreweave-clientname.ord1.ingress.coreweave.cloud/`).

This Ingress URL may be used to access the FileBrowser application in a browser.

![The FileBrowser login screen](<../../.gitbook/assets/image (3) (1) (1) (2).png>)

**It is strongly recommended to change the password for your FileBrowser instance as soon as possible.** Do this by logging into your new FileBrowser instance, navigating to **Settings** on the left-hand side, and changing the password from that page.

<figure><img src="../.gitbook/assets/image (76).png" alt="Screenshot: Change the default password for your FileBrowser instance"><figcaption><p>Change the default password for your FileBrowser instance</p></figcaption></figure>

Congratulations! You have successfully deployed FileBrowser onto CoreWeave Cloud, and now have an easy-to-use interface for file management. To learn more about the application itself, check out [the official FileBrowser documentation](https://filebrowser.org/features).
