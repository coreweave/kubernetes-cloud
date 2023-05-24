---
description: Try out Inference on CoreWeave by following our in-depth walkthrough guides
---

# Examples and Tutorials

## Inference tutorial directory

Each tutorial page includes a link to the source code for the provided example. In most cases, it will be required to clone the repository in order to follow along directly with the tutorial's walkthrough.

### One-Click models

<table><thead><tr><th width="370">Title</th><th>Description</th></tr></thead><tbody><tr><td><a href="models/gpt-j-6b.md">GPT-J-6B</a></td><td>Deploy popular open source model GPT-J-6B with the click of a button</td></tr></tbody></table>

### PyTorch

<table><thead><tr><th width="371">Title</th><th>Description</th></tr></thead><tbody><tr><td><a href="pytorch-jax/hugging-face/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md">Hugging Face: Stable Diffusion Text to Image</a></td><td>Input a text prompt to generate high-quality images with photorealistic capabilities</td></tr><tr><td><a href="pytorch-jax/hugging-face/pytorch-hugging-face-transformers-bigscience-bloom.md">Hugging Face: Transformers Accelerate - BigScience BLOOM</a></td><td>Deploy <a href="https://huggingface.co/bigscience/bloom">BLOOM</a> as an <a href="https://kserve.github.io/website/0.8/get_started/first_isvc/">InferenceService</a> with a simple HTTP API to perform Text Generation using Transformers Accelerate</td></tr><tr><td><a href="pytorch-jax/hugging-face/pytorch-hugging-face-transformers-bigscience-bloom-1.md">Hugging Face: Transformers DeepSpeed: BigScience BLOOM</a></td><td>Deploy <a href="https://huggingface.co/bigscience/bloom">BLOOM</a> as an <a href="https://kserve.github.io/website/0.8/get_started/first_isvc/">InferenceService</a> with a simple HTTP API to perform Text Generation using Transformers DeepSpeed</td></tr><tr><td><a href="pytorch-jax/custom-pytorch-aitextgen.md">GPT-2 for AITextgen</a></td><td>Deploy the new text generation toolchain for GPT-2, <a href="https://docs.aitextgen.io">aitextgen</a>, using a custom predictor</td></tr><tr><td><a href="pytorch-jax/custom-sentiment.md">FastAI Sentiment</a></td><td>Deploying a sentiment analyzer built with <a href="https://docs.fast.ai/text.html">FastAI</a>, using a custom predictor</td></tr></tbody></table>

### TensorFlow

|                                                                             |                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Open AI GPT-2](tensorflow/gpt-2/)                                          | Serve and use the [OpenAI GPT-2 text generation model](https://github.com/openai/gpt-2) with this multi-part guide                                                                                               |
| [Tensorflow2: Image Classifier](tensorflow/tensorflow2-image-classifier.md) | Step-by-step instructions are **not published** for this example - the deployment process is identical to the steps used in the [GPT-2 Tensorflow](tensorflow/gpt-2/) example, save for the provided source code |

### Triton Inference

|                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [FasterTransformer GPT-J and GPT: NeoX 20B](triton-inference/triton-inference-server-fastertransformer.md) | Deploy EleutherAI GPT-J and GPT-NeoX on [NVIDIA Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server) with the [FasterTransformer](https://github.com/NVIDIA/FasterTransformer) backend via an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) using an HTTP API to perform Text Generation |

### JAX

|                                                                 |                                                                                                                             |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [DALL-E Mega](pytorch-jax/hugging-face/jax-dall-e-mini-mega.md) | Use a text prompt as input to generate an image as output using [DALL-E Mega](https://huggingface.co/dalle-mini/dalle-mega) |

### Custom

|                                       |                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------- |
| [BASNET](tensorflow/custom-basnet.md) | Deploy an auto-scaling Inference service from a pre-existing Docker image |

{% hint style="info" %}
**Note**

For PyTorch, use `pip` to install PyTorch bundled with CUDA. Do not install CUDA separately, as doing so may result in dependency mismatches. For more information, refer to the[ PyTorch installation guide](https://pytorch.org/get-started/locally/).
{% endhint %}
