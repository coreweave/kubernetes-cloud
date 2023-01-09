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

## Accessing Determined

Once the application is in a **Ready** state, the Determined AI Web UI may be accessed by visiting the Ingress URL provided in the post-launch notes. The default URL and default login information for the instance will be listed after the text `To access the Web UI, please visit:`. Navigate to the given URL using your Web browser to access the Determined UI.

{% hint style="info" %}
**Note**

The client is configured to communicate with the server via the environment variable `$DET_MASTER`.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (5).png" alt="The Web UI access info in the post-launch notes"><figcaption><p>The Web UI access info in the post-launch notes</p></figcaption></figure>

### The Web UI

Navigating to the generated URL will lead you to the Determined AI home screen. From here you can do things like [launch a JupyterLab and subsequent Jupyter Notebooks](launch-jupyter-notebook-on-coreweave-via-determined-ai.md), or perform model finetuning using [GPT DeepSpeed](launch-gpt-deepspeed-models-using-determinedai.md), [GPT-NeoX](gpt-neox.md), or [HuggingFace](finetuning-huggingface-llms-with-determined-ai-and-deepspeed.md).

<figure><img src="../../.gitbook/assets/image (3) (5).png" alt="The Determined AI Web UI"><figcaption><p>The Determined AI Web UI</p></figcaption></figure>

For more information on using Determined AI, refer to the [official Determined AI documentation](https://docs.determined.ai/latest/).
