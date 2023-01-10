---
description: Launch a Jupyter Notebook on CoreWeave using Determined AI
---

# Launch Jupyter Notebook on CoreWeave via Determined AI

## Prerequisites

Before continuing with this guide, first [install and configure the Determined AI application via the Cloud UI](install-determined-ai.md) into your namespace.

## Setup

Once the Determined application is launched, open the Determined AI Web UI. Click on the **Launch JupyterLab** button in the top-left corner to open the JupyterLab configuration window.

<figure><img src="../../.gitbook/assets/Screenshot from 2022-12-15 10-58-02.png" alt="Screenshot of &#x22;Launch Jupyter&#x22; button"><figcaption></figcaption></figure>

Choose a number of **Slots** (that is, the number of GPUs to use) and set a **Name** for your Notebook. The rest of the fields can be left as their default values.

<figure><img src="../../.gitbook/assets/Screenshot from 2022-12-15 10-59-08.png" alt="Screenshot of The Launch JupyterLab configuration modal"><figcaption><p>The Launch JupyterLab configuration modal</p></figcaption></figure>

Once configuration is complete, click the **Launch** button in the bottom right-hand corner of the modal. This will prompt Determined to prepare [the JupyterLab environment](https://towardsdatascience.com/how-to-setup-your-jupyterlab-project-environment-74909dade29b).

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt="Determined AI configuring the Jupyter-lab environment"><figcaption><p>Determined AI configuring the Jupyter-lab environment</p></figcaption></figure>

Once the environment is ready, you will be redirected to the JupyterLab home screen. From here, you may begin a Notebook, open a terminal, or create other kinds of files for your Notebook, such as Markdown text files.

{% hint style="info" %}
**Additional Resources**

To learn more about Jupyter and how to use Notebooks and JupyterLab, refer to [the Jupyter documentation](https://docs.jupyter.org/en/latest/).
{% endhint %}

<figure><img src="../../.gitbook/assets/image (12) (4).png" alt="The Jupyter-lab homescreen"><figcaption><p>The Jupyter-lab homescreen</p></figcaption></figure>

To shut down the notebook, navigate to the **File** menu, then select **Shut Down**.

![The file -> shutdown menu](<../../.gitbook/assets/image (11) (1).png>)

This will end the lab. In order to return to Jupyter Lab, you must re-launch the environment as described above.

## Video tutorial

{% embed url="https://youtu.be/pjkBSnInJ34" %}
Watch: How to launch a Jupyter Notebook on CoreWeave Cloud
{% endembed %}
