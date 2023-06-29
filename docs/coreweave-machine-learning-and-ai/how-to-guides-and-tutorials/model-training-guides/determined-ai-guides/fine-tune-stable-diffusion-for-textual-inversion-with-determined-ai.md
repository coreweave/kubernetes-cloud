# Fine-tune Stable Diffusion for Textual Inversion with Determined AI

This guide, based on Determined AI's article [Personalizing Stable Diffusion with Determined](https://www.determined.ai/blog/stable-diffusion-core-api),   explains how fine-tune a Stable Diffusion model on CoreWeave Cloud to do Textual Inversion, generating personalized images.

[Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release) is the latest deep learning model to generate brilliant, eye-catching art based on simple input text. Built upon the ideas behind models such as [DALL·E 2](https://openai.com/dall-e-2/), [Imagen](https://imagen.research.google/), and [LDM](https://arxiv.org/abs/2112.10752), Stable Diffusion is the first architecture in this class which is small enough to run on typical consumer-grade GPUs.

## Prerequisites

This guide assumes that the following are completed in advance.

* You have [set up your CoreWeave Kubernetes environment](../../../../welcome-to-coreweave/getting-started.md) locally
* `git` is locally installed
* [Determined AI is installed in your namespace](install-determined-ai.md)

## Configure the experiment

In a text editor, open the files in `/examples/diffusion/textual_inversion_stable_diffusion/`.  Change the values in `finetune_const.yaml` [config file](https://github.com/determined-ai/determined/blob/master/examples/diffusion/textual\_inversion\_stable\_diffusion/finetune\_const.yaml), as needed.

```yaml
environment:
   environment_variables:   
    - HF_AUTH_TOKEN=YOUR_HF_AUTH_TOKEN_HERE
hyperparameters:
   concepts:
      learnable_properties:  
          - object
      concept_strs:    
          - det-logo
      initializer_strs:  
          - brain logo, sharp lines, connected circles, concept art
      img_dirs:
          - det_logos
```

These values may be broken down as follows:

<table><thead><tr><th width="305">Value name</th><th>Description</th></tr></thead><tbody><tr><td><code>YOUR_HF_AUTH_TOKEN_HERE</code></td><td>Your Hugging Face User Access Token</td></tr><tr><td><code>learnable_properties</code></td><td>Either <code>object</code> or <code>style</code>, depending on whether you want to capture the object itself, or only its style</td></tr></tbody></table>

More than one concept at a time may be fine-tuned by appending relevant information to the lists:

* `concept_strs` - the string used to refer to new concept in prompts
* `initializer_strs` - a short phrase which roughly describes the concept of interest and provides a warm-start for fine-tuning

### Clone the repository

To fine-tune images, first [clone the Determined repository](https://github.com/determined-ai/determined).

### Acquire a Hugging Face User Access Token

Create a Hugging Face account if necessary, then generate a  [User Access Token](https://huggingface.co/docs/hub/security-tokens). Accept the Stable Diffusion license at `CompVis/stable-diffusion-v1-4` by [clicking "Access repository](https://huggingface.co/CompVis/stable-diffusion-v1-4)".

### Place images

In a new directory at the root of the repository, place the training images.

## Submit the experiment

Submit the fine-tuning experiment by navigating to the root of the repository, then create the experiment by running `det e create`:

<pre class="language-bash"><code class="lang-bash"><strong>$ det e create finetune_const.yaml
</strong></code></pre>

To quickly test your configuration, add the `HF_AUTH_TOKEN` value. Leave all other values at their defaults, then submit the experiment without any further changes. A fine-tuning experiment using the Determined AI logo is set up in the repository by default.

After launching the experiment, navigate to the Web UI. Click the **Logs** tab to view training progress.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-29-15.png" alt="Stable Diffusion with Textual Inversion running on CoreWeave infrastructure using Determined AI"><figcaption><p>Stable Diffusion with Textual Inversion running on CoreWeave infrastructure using Determined AI</p></figcaption></figure>

When the experiment completes, the checkpoints are exported to Object Storage (shown as `s3`).

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-30-42 (1).png" alt="Showcases all steps completed in the fine-tuning job"><figcaption><p>Showcases all steps completed in the fine-tuning job</p></figcaption></figure>

You can view Loss on the **Overview** tab. Here, you can choose **Fork** or **Continue Trial** if required to get better results.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-30-02.png" alt="Loss going down as more batches are iterated upon"><figcaption><p>Loss going down as more batches are iterated upon</p></figcaption></figure>

Use the **Checkpoints** tab to view them.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-30-20.png" alt="All listed Checkpoints for the experiment"><figcaption><p>All listed Checkpoints for the experiment</p></figcaption></figure>

Use the **Hyperparameters** tab to see the values passed to the experiment.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-32-55 (1).png" alt="Hyperparameters for the fine-tuning experiment"><figcaption><p>HyperParameters for the fine-tuning experiment</p></figcaption></figure>

You can visualize the results via TensorBoard.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-33-24 (1).png" alt="TensorBoard showing inference prompts"><figcaption><p>TensorBoard showing inference prompts</p></figcaption></figure>

## Generate Images

After the fine-tuning experiment is complete, you can generate art with the newly-trained concept using Jupyter notebook or with large-scale generation through a Determined experiment. The former is useful for quick interactive experimentation, while the latter is useful for pure performance.

The Jupyter notebook workflow only requires three steps:

1. Copy the User Access Token into the `detsd-notebook.yaml` [config file](https://github.com/determined-ai/determined/blob/master/examples/diffusion/textual\_inversion\_stable\_diffusion/detsd-notebook.yaml), similar to the step in the previous section.
2. Get the `uuid` of the desired Checkpoint by navigating to the Experiment page in the Web UI and either clicking on the Checkpoint’s flag icon or inspecting the Checkpoints tab.
3. Launch the `textual_inversion.ipynb` [notebook](https://github.com/determined-ai/determined/blob/master/examples/diffusion/textual\_inversion\_stable\_diffusion/textual\_inversion.ipynb) and copy the Checkpoint `uuid` into the `uuids` list in the appropriate cell. You can also do this by executing the following command in the root of the repository:

<pre class="language-bash"><code class="lang-bash"><strong>$ det notebook start --config-file detsd-notebook.yaml --context .
</strong></code></pre>

The `--context .` argument loads the full contents of the repository into the JupyterLab instance, including the `textual_inversion.ipynb` repo itself and various supporting files.&#x20;

In particular, these include a demonstration concept stored in `learned_embeddings_dict_demo.pt` which was extensively trained on Determined AI logos, which you can use instead of, or in addition to, one specified by `uuid`.

After you've prepared the `textual_inversion.ipynb` notebook, it can be run from top to bottom and the generated images will appear at the end.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-35-17.png" alt="Notebook open to run and download dependencies"><figcaption><p>Notebook open to run and download dependencies</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-36-07.png" alt="Fetching the concept to generate images"><figcaption><p>Fetching the concept to generate images</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-36-34.png" alt="Generate images from the concept"><figcaption><p>Generate images from the concept</p></figcaption></figure>

Here are some example images generated from the fine-tuning experiment:

<div align="left">

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-37-52.png" alt="Example 1"><figcaption><p>Example 1</p></figcaption></figure>

</div>

<div align="left">

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-38-18.png" alt="Example 2"><figcaption><p>Example 2</p></figcaption></figure>

</div>

<div align="left">

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-03-13 12-38-33.png" alt="Example 3"><figcaption><p>Example 3</p></figcaption></figure>

</div>

After you've found promising prompts and parameter settings with Jupyter notebook, images can be generated at scale by submitting a full-fledged experiment.&#x20;

The `generate_grid.yaml` file loads pretrained concepts by `uuid` or local path and controls the generation process by specifying the prompts and parameter settings to scan over. All generated images are logged to Tensorboard for easy access, as shown previously.

By default, you can submit a two-GPU experiment that creates nearly 500 total images with the pre-trained demonstration in `learned_embeddings_dict_demo.pt` by inserting your authorization token, without other changes, then executing:

```bash
det e create generate_grid.yaml .
```

## References

To learn more, see these resources:

* [Personalizing Stable Diffusion with Determined](https://www.determined.ai/blog/stable-diffusion-core-api)
* [Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release)
* [Determined repository](https://github.com/determined-ai/determined/tree/master/examples/diffusion/textual\_inversion\_stable\_diffusion)
