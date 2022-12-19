---
description: Set up Determined AI via the applications Catalog on CoreWeave Cloud
---

# Install Determined AI

## Create an Object Storage bucket

Before installing the Determined AI application, you may first need to create an Object Storage bucket. [Follow the steps to create a bucket](../../storage/object-storage.md), making sure to retain the given values for your **access key** and **secret key**. Then, continue with this guide.

{% hint style="info" %}
**Note**

Most but not all applications of Determined AI require Object Storage buckets - they are used to store model checkpoints. It is possible to create a Jupyter Notebook without first creating an Object Storage bucket.
{% endhint %}

## Install the Determined application

From the [application Catalog](https://apps.coreweave.com/), search for `determined`. This will bring up the Determined AI (`determined`) application, which you will deploy into your cluster.

![The DeterminedAI application in the Cloud UI application Catalog](<../../.gitbook/assets/Screen Shot 2022-07-26 at 4.06.24 PM.png>)

Click on the application when it appears, then click the **Deploy** button at the very bottom right-hand corner of the screen to continue to the configuration screen.

<figure><img src="../../.gitbook/assets/Screen Shot 2022-08-01 at 4.46.55 PM.png" alt="Screenshot of the default values for launching Determined AI"><figcaption><p>Default values for launching Determined AI</p></figcaption></figure>

Under the **Object Storage Configuration** section, set the values you'd like to use for the [Object Storage](../../storage/object-storage.md) bucket, including your previously generated `ACCESS_KEY` and `SECRET_KEY` , which will be used to store model checkpoints.

{% hint style="info" %}
**Note**

Some values, such as link to the cluster, may be important for certain applications. Those details can be found in the post-deployment notes after the application is running. If you need to access these notes, navigate to the **Applications** tab, then click the Determined application tile.
{% endhint %}

Finally, click the **Deploy** button at the bottom of the configuration screen to launch the application.
