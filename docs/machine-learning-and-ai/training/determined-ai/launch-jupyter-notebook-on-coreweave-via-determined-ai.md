---
description: Launch a Jupyter Notebook on CoreWeave using Determined AI
---

# Launch Jupyter Notebook on CoreWeave via Determined AI

## Prerequisites

This guide assumes that the following are completed in advance.

* You have [set up your CoreWeave Kubernetes environment](../../../coreweave-kubernetes/getting-started.md) locally
* `git` is locally installed
* [Determined AI is installed in your namespace](../../../compass/determined-ai/install-determined-ai.md)

## Setup

Once the Determined application is launched, open the Determined AI Web UI. Click on the **Launch JupyterLab** button in the top-left corner to open the JupyterLab configuration window.

<div align="left">

<figure><img src="../../../.gitbook/assets/Screenshot from 2022-12-15 10-58-02.png" alt="Screenshot of &#x22;Launch Jupyter&#x22; button"><figcaption></figcaption></figure>

</div>

Choose a number of **Slots** (that is, the number of GPUs to use) and set a **Name** for your Notebook, then [select a Resource Pool](../../../compass/determined-ai/install-determined-ai.md#resource-pools).

<figure><img src="../../../.gitbook/assets/image (1) (3) (1).png" alt="Screenshot of the JupyterLab configuration modal"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (13) (1).png" alt="Screenshot of Notebook configuration screen"><figcaption></figcaption></figure>



Once configuration is complete, click the **Launch** button in the bottom right-hand corner of the modal. This will prompt Determined to prepare [the JupyterLab environment](https://towardsdatascience.com/how-to-setup-your-jupyterlab-project-environment-74909dade29b).

<figure><img src="../../../.gitbook/assets/image (2) (3) (1).png" alt="Determined AI configuring the Jupyter-lab environment"><figcaption><p>Determined AI configuring the Jupyter-lab environment</p></figcaption></figure>

Once the environment is ready, you will be redirected to the JupyterLab home screen. From here, you may begin a Notebook, open a terminal, or create other kinds of files for your Notebook, such as Markdown text files.

{% hint style="info" %}
**Additional Resources**

To learn more about Jupyter and how to use Notebooks and JupyterLab, refer to [the Jupyter documentation](https://docs.jupyter.org/en/latest/).
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (12) (1) (3) (1).png" alt="The Jupyter-lab homescreen"><figcaption><p>The Jupyter-lab homescreen</p></figcaption></figure>

To shut down the notebook, navigate to the **File** menu, then select **Shut Down**.

![The file -> shutdown menu](<../../../.gitbook/assets/image (11) (6) (1).png>)

This will end the lab. In order to return to Jupyter Lab, you must re-launch the environment as described above.

## Video tutorial

{% embed url="https://youtu.be/pjkBSnInJ34" %}
Watch: How to launch a Jupyter Notebook on CoreWeave Cloud
{% endembed %}
