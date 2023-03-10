---
description: Try out Inference on CoreWeave by following our in-depth walkthrough guides
---

# Examples and Tutorials

## Inference tutorial directory

Each tutorial page includes a link to the source code for the provided example. In most cases, it will be required to clone the repository in order to follow along directly with the tutorial's walkthrough.

### One-Click models

| Title                          | Description                                                          |
| ------------------------------ | -------------------------------------------------------------------- |
| [GPT-J-6B](models/gpt-j-6b.md) | Deploy popular open source model GPT-J-6B with the click of a button |

### PyTorch

| Title                                                                                                                                  | Description                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Hugging Face: Stable Diffusion Text to Image](pytorch/hugging-face/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md)  | Input a text prompt to generate high-quality images with photorealistic capabilities                                                                                                                                             |
| [Hugging Face: Transformers Accelerate - BigScience BLOOM](pytorch/hugging-face/pytorch-hugging-face-transformers-bigscience-bloom.md) | Deploy [BLOOM](https://huggingface.co/bigscience/bloom) as an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) with a simple HTTP API to perform Text Generation using Transformers Accelerate |
| [Hugging Face: Transformers DeepSpeed: BigScience BLOOM](pytorch/hugging-face/pytorch-hugging-face-transformers-bigscience-bloom-1.md) | Deploy [BLOOM](https://huggingface.co/bigscience/bloom) as an [InferenceService](https://kserve.github.io/website/0.8/get\_started/first\_isvc/) with a simple HTTP API to perform Text Generation using Transformers DeepSpeed  |
| [GPT-2 for AITextgen](pytorch/custom-pytorch-aitextgen.md)                                                                             | Deploy the new text generation toolchain for GPT-2, [aitextgen](https://docs.aitextgen.io), using a custom predictor                                                                                                             |
| [FastAI Sentiment](pytorch/custom-sentiment.md)                                                                                        | Deploying a sentiment analyzer built with [FastAI](https://docs.fast.ai/text.html), using a custom predictor                                                                                                                     |

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

|                                                                                                                                 |                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [DALL-E Mega](../../training/kubeflow-training-operators/finetune-gpt-neox-20b-with-argo-workflows/jax/jax-dall-e-mini-mega.md) | Use a text prompt as input to generate an image as output using [DALL-E Mega](https://huggingface.co/dalle-mini/dalle-mega) |

### Custom

|                                                                                                                        |                                                                           |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [BASNET](../../training/kubeflow-training-operators/finetune-gpt-neox-20b-with-argo-workflows/custom/custom-basnet.md) | Deploy an auto-scaling Inference service from a pre-existing Docker image |

{% hint style="info" %}
**Note**

For PyTorch, use `pip` to install PyTorch bundled with CUDA. Do not install CUDA separately, as doing so may result in dependency mismatches. For more information, refer to the[ PyTorch installation guide](https://pytorch.org/get-started/locally/).
{% endhint %}
