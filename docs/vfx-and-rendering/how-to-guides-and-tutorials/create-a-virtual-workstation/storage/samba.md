---
description: Expose storage volumes using Samba
---

# Samba

## Samba

Both the standard flavor of Samba as well as the Active Directory version of Samba may be installed into CoreWeave Cloud from [the Cloud UI Applications Catalog](https://apps.coreweave.com).

To deploy either, navigate to the Applications Catalog, then search for **Samba**. Select the desired application from the listed results, then click the **Deploy** button in the lower right-hand corner to configure the instance.

{% hint style="info" %}
**Note**

The Active Directory flavor of the Samba application will require a domain controller to be set up in your namespace with an address specified during deployment.
{% endhint %}

<div>

<figure><img src="../../../../../.gitbook/assets/image (62) (1) (1) (1).png" alt="The standard Samba icon in the application Catalog"><figcaption><p>The standard Samba icon in the application Catalog</p></figcaption></figure>

 

<figure><img src="../../../../.gitbook/assets/image (133).png" alt="The Active Directory Samba icon in the application Catalog"><figcaption><p>The Active Directory Samba icon in the application Catalog</p></figcaption></figure>

</div>

The Samba instance and the filesystem volume to expose should be deployed in the same data center region. When selecting a region for the Samba instance, ensure it matches the one chosen for the filesystem volume.

<figure><img src="../../../../.gitbook/assets/image (12) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

If you require more advanced access permissions for your Samba volume, consider pairing our **samba-ad** option with your on-premise Active Directory domain services.&#x20;
{% endhint %}

The following examples demonstrate different configuration settings per Samba type.

{% tabs %}
{% tab title="Standard Samba configuration" %}
## Standard Samba configuration

To install a standard Samba instance, navigate to the application Catalog and search for **Samba**. Select the Samba application, then click the **Deploy** button in the lower right-hand corner to open the configuration options.

<figure><img src="../../../../.gitbook/assets/image (30) (3).png" alt="The standard Samba configuration options"><figcaption><p>The standard Samba configuration options</p></figcaption></figure>

Under the **Form** tab, within the **Samba Server** box, select the same region into which your storage volume was provisioned earlier.

Next, select the number of replicas you'd like the Pod to have. Then, choose whether you'd like to expose the instance publicly by altering the **Expose on Public IP** toggle, which allows, enables or disables public networking accordingly.

The following box, **User Information**, is for configuring the Samba user account. Input the **Username, Password, User ID, Group name,** and **Group ID** to use for the Samba share.

Configure associated storage volumes from the volumes panes at the bottom of the menu. Highlight the desired storage volume from the **Available Volumes** list, then click the blue plus sign to the right of the volume's name to add it to the **Attach Volume** list.

Finally, click the **Deploy** button in the lower left-hand corner.
{% endtab %}

{% tab title="Samba-AD configuration" %}
## Samba Active Directory configuration

To install a Samba-AD instance, navigate to the application Catalog and search for **Samba**. Select the **samba-ad** application, then click the **Deploy** button in the lower right-hand corner to open the configuration options.

<figure><img src="../../../../.gitbook/assets/image (38) (2).png" alt="The Samba-AD configuration options"><figcaption><p>The Samba-AD configuration options</p></figcaption></figure>

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

<figure><img src="../../../../../.gitbook/assets/image (72).png" alt="A successful post-installation message"><figcaption><p>A successful post-installation message</p></figcaption></figure>

## Connect to Samba

After deploying your Samba instance, the **Installation Notes** section will provide the `.coreweave.cloud` domain name for the instance.&#x20;

![The DNS name listed in the success message of the Samba deployment](<../../../../../.gitbook/assets/image (73) (1) (1) (1).png>)

Connect to this drive by mapping the network drive. Navigate to the Start menu and right-click the name of your local machine. Select **Map network drive...** from the drop-down.

<figure><img src="../../../../../.gitbook/assets/image (70).png" alt="Screenshot of Map network drive..."><figcaption></figcaption></figure>

Provide the Samba domain name to the **Folder** input field. Then click the **Browse...** button.

![Mapping the network drive using the provided DNS name](<../../../../.gitbook/assets/image (139).png>)

![The mapped drive, listed in the Browse for Folder listing](<../../../../../.gitbook/assets/image (65) (1).png>)

Select the mount, click the **OK** button, then enter your credentials when prompted. A successful mount will display the full path of the mounted drive in your filesystem browser.

![A successful mount](<../../../../../.gitbook/assets/image (74) (1).png>)
