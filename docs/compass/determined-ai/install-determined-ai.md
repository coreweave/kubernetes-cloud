---
description: How to install via the Applications Catalog on CoreWeave Cloud
---

# Install Determined AI

To install Determined AI on CoreWeave Cloud, follow these steps:

## Step 1: Create a Shared File System Volume

Create a Shared File System Volume by selecting [Storage Volumes](https://cloud.coreweave.com/storage) in the Cloud UI.

You'll use this volume to store the model weights and training data for fine-tuning. CoreWeave's Shared File System Volumes can be accessed by many Nodes simultaneously, allowing massive amounts of compute power to access the same dataset.

<figure><img src="../../.gitbook/assets/Screen Shot 2022-07-26 at 4.14.13 PM.png" alt="Create a New Volume on the Storage menu from the Cloud UI"><figcaption><p>Create a New Volume on the Storage menu from the Cloud UI</p></figcaption></figure>

This tutorial uses the following values when creating the Shared File System Volume. If needed, it is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a storage volume later.

| Field name       | Demo value          |
| ---------------- | ------------------- |
| **Volume Name**  | `finetune-gpt-neox` |
| **Region**       | `LAS1`              |
| **Disk Class**   | `HDD`               |
| **Storage Type** | Shared Filesystem   |
| **Size (Gi)**    | `1,000`             |
| **Labels**       | \[none]             |

## **Step 2: Install the filebrowser application**

{% hint style="info" %}
**Filebrowser is optional**\
We recommend that you install the filebrowser application, but it's also possible to use a Virtual Server or Kubernetes Pod to interact with the Shared File System Volume through SSH or another mechanism. Those steps are beyond the scope of this tutorial.
{% endhint %}

Find the **filebrowser** application in the [Applications Catalog](https://apps.coreweave.com/). This app allows you to transfer files to and from your Shared File System Volume through a web interface.

![The filebrowser application in the Cloud UI application Catalog](<../../.gitbook/assets/Screen Shot 2022-07-26 at 4.10.34 PM.png>)

Give the filebrowser application a name. Use a short name to avoid [SSL CNAME](#user-content-fn-1)[^1] issues. This tutorial uses the name `finetune`.&#x20;

Select the `finetune-gpt-neox` volume you created earlier, then click the `+` icon to move it to the attached list.

Verify the Volume is added to the lists of attached volumes as shown below, then click **Deploy**.

<figure><img src="../../.gitbook/assets/filebrowser2.png" alt="Deploy the filebrowser application."><figcaption><p>Deploy the filebrowser application.</p></figcaption></figure>

## Step 3: Create an Object Storage bucket

Most Determined AI applications require Object Storage buckets to store model checkpoints, while a few, such as Jupiter Notebooks, can run without a bucket.&#x20;

Unless you are sure your application will not require one, [create an Object Storage bucket](../../storage/object-storage.md) and make note of the access key and secret key in the generated configuration file.

## Step 4: Install the Determined AI application

Search for `determined` in the [Application Catalog](https://apps.coreweave.com/) to locate the Determined AI (`determined`) application.&#x20;

![Determined AI in the Cloud UI Applications Catalog](<../../.gitbook/assets/Screen Shot 2022-07-26 at 4.06.24 PM.png>)

Select the application, then click **Deploy** to continue.

Give the application a memorable name.&#x20;

In the **Default Resources** section, this tutorial uses the following values:

| Field name     | Demo value |
| -------------- | ---------- |
| vCPU Request   | 8          |
| Memory Request | 256        |
| GPU Type       | A40        |

In the **Object Storage Configuration** section, set your [Object Storage](../../storage/object-storage.md) bucket values, including the`ACCESS_KEY` and `SECRET_KEY`. Object storage is required if you store model checkpoints.

Some values, such as link to the cluster, may be important for certain applications. Those details can be found in the post-deployment notes after the application is running. If you need to access these notes, navigate to the **Applications** tab, then click the Determined application tile.

Make sure to attach the Shared File System Volume you created in Step 1.&#x20;

<figure><img src="../../.gitbook/assets/image5.png" alt=""><figcaption><p>Add Object Storage and the Shared File System Volume</p></figcaption></figure>

Finally, click **Deploy** to launch the application.

## Step 5: Access Determined AI

After the application is in a **Ready** state, navigate to the Ingress URL provided in the post-launch notes and use the login information provided.&#x20;

{% hint style="info" %}
**Note**

The client is configured to communicate with the server via the environment variable `$DET_MASTER`.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (5) (5).png" alt="The Web UI access info in the post-launch notes"><figcaption><p>The Web UI access info in the post-launch notes</p></figcaption></figure>

At the Determined AI home screen, you can [launch a JupyterLab and subsequent Jupyter Notebooks](../../machine-learning-and-ai/training/determined-ai/launch-jupyter-notebook-on-coreweave-via-determined-ai.md), or perform model fine-tuning with [GPT DeepSpeed](../../machine-learning-and-ai/training/determined-ai/launch-gpt-deepspeed-models-using-determinedai.md), [GPT-NeoX](gpt-neox.md), or [Hugging Face](../../machine-learning-and-ai/training/determined-ai/finetuning-huggingface-llms-with-determined-ai-and-deepspeed.md).

<figure><img src="../../.gitbook/assets/image (3) (1) (2).png" alt="The Determined AI Web UI"><figcaption><p>The Determined AI Web UI</p></figcaption></figure>

## More Resources

For more information about Determined AI, see:

* [Official documentation](https://docs.determined.ai/latest/)
* [Intro to Determined: A First Time User's Guide](https://www.determined.ai/blog/intro-to-determined)
* [Determined AI Blog](https://www.determined.ai/blog)

[^1]: A domain alias that allows multiple URLs to use the same SSL certificate.
