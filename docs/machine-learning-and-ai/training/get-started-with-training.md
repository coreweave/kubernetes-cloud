---
description: Welcome to Training on CoreWeave Cloud
---

# Get Started with Training

## Training tutorial directory

This section contains a series of tutorials for training machine learning models on CoreWeave Cloud. They are organized by distributed training platform.

### Determined AI

| Example                                                                                                                                                                      | Description                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [Finetune Hugging Face LLMs with Determined AI and DeepSpeed](determined-ai/custom-images-for-determined-ai/finetuning-huggingface-llms-with-determined-ai-and-deepspeed.md) | Deploy Determined AI on CoreWeave Cloud to perform distributed training of the OPT-125m model |

### Argo Workflows

| Example                                                                                                              | Description                                                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Finetune GPT-NeoX-20B with Argo Workflows](kubeflow-training-operators/finetune-gpt-neox-20b-with-argo-workflows/)  | Use Argo Workflows to finetune a smaller model (GPT-J) on a smaller dataset                                                                                                                                            |
| [Train ResNet-50 with ImageNet](kubeflow-training-operators/train-resnet-50-with-imagenet.md)                        | Use the [`torchvision` library](https://pytorch.org/vision/stable/index.html) along with multiple [Kubeflow training operators ](kubeflow-training-operators/)to perform distributed training of ResNet-50 on ImageNet |
| [Finetune Stable Diffusion Models with CoreWeave](kubeflow-training-operators/finetuning-image-generation-models.md) | Use Argo Workflows to set up a pipeline on CoreWeave for finetuning and training Stable Diffusion models                                                                                                               |
| [Finetune GPT Models with CoreWeave](kubeflow-training-operators/finetuning-machine-learning-models.md)              | Finetune GPT models using Argo Workflows on CoreWeave Cloud                                                                                                                                                            |

