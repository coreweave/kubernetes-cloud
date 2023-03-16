---
description: Welcome to Training on CoreWeave Cloud
---

# Get Started with Training

## Training tutorial directory

This section contains a series of tutorials for training machine learning models on CoreWeave Cloud. They are organized by distributed training platform.

### Determined AI

| Example                                                                                                                                       | Description                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [Fine-tune Hugging Face LLMs with Determined AI and DeepSpeed](determined-ai/finetuning-huggingface-llms-with-determined-ai-and-deepspeed.md) | Deploy Determined AI on CoreWeave Cloud to perform distributed training of the OPT-125m model |

### Argo Workflows

| Example                                                                                                                | Description                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fine-tune GPT-NeoX-20B with Argo Workflows](argo-workflows/fine-tuning/fine-tune-gpt-neox-20b-with-argo-workflows.md) | Use Argo Workflows to fine-tune a smaller model (GPT-J) on a smaller dataset                                                                                                                                                       |
| [Train ResNet-50 with ImageNet](kubeflow-training-operators-pytorch-mpi/train-resnet-50-with-imagenet.md)              | Use the [`torchvision` library](https://pytorch.org/vision/stable/index.html) along with multiple [Kubeflow training operators ](kubeflow-training-operators-pytorch-mpi/)to perform distributed training of ResNet-50 on ImageNet |
| [Fine-tune Stable Diffusion Models with CoreWeave](argo-workflows/fine-tuning/finetuning-image-generation-models.md)   | Use Argo Workflows to set up a pipeline on CoreWeave for fine-tuning and training Stable Diffusion models                                                                                                                          |
| [Fine-tune GPT Models with CoreWeave](argo-workflows/fine-tuning/finetuning-machine-learning-models.md)                | Fine-tune GPT models using Argo Workflows on CoreWeave Cloud                                                                                                                                                                       |

