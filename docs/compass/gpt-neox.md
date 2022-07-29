---
description: >-
  This page details the setup and process to train or fine-tune a GPT-NeoX 20B
  parameter model on CoreWeave cloud.
---

# Finetuning GPT-NeoX 20B using DeterminedAI

## Introduction

[GPT-NeoX](https://blog.eleuther.ai/announcing-20b/) is a 20B parameter autoregressive model trained on [the Pile dataset](https://arxiv.org/abs/2101.00027).

It generates text based on context or unconditionally for use cases such as story generation, chat bots, summarization, and so on.

{% hint style="info" %}
**Additional Resources**

Learn more in the [GPT-NeoX-20B: An Open-Source Autoregressive Language Model](https://arxiv.org/abs/2204.06745) whitepaper, and [view the GPT-NeoX source code on GitHub](https://github.com/EleutherAI/gpt-neox).
{% endhint %}

This model is trained on CoreWeave infrastructure and the [weights](https://github.com/EleutherAI/gpt-neox#pretrained-models) are made available via a permissive license. Based on your requirements and use case, this model is capable of high quality text generation. Many customers have seen drastically improved results by finetuning the model with data specific to their use case.

This guide will use [the DeterminedAI MLOps platform](https://www.determined.ai/blog/determined-algorithmia-integration) to run distributed finetuning jobs on the model.

## Setup

{% hint style="info" %}
**Note**

This guide makes several assumptions:\
\
• You have [set up the CoreWeave Kubernetes environment](../../coreweave-kubernetes/getting-started.md).\
• You have some experience launching and using [DeterminedAI on CoreWeave Cloud](https://www.determined.ai). (If you have not done so already, it is recommended to [deploy DeterminedAI via the application Catalog](https://apps.coreweave.com/) to familiarize yourself with it.)\
• You have `git` installed on your terminal.
{% endhint %}

### Create a Shared Filesystem storage volume

First, create a **Shared Filesystem storage volume** from [the Storage menu on the CoreWeave Cloud UI](https://cloud.coreweave.com/storage). This volume will be used to store the model weights as well as training data for finetuning. Shared storage volumes can be accessed by many nodes at once in CoreWeave, allowing for massive amounts of compute power to access the same dataset.

You can use the values shown and described below for this tutorial.

![Create a New Volume on the Storage menu from the Cloud UI](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.14.13 PM.png>)

The values used for this demo are as follows:

| Field name       | Demo value        |
| ---------------- | ----------------- |
| **Volume Name**  | finetune-gpt-neox |
| **Region**       | Chicago - ORD1    |
| **Disk Class**   | HDD               |
| **Storage Type** | Shared Filesystem |
| **Size (Gi)**    | 1000              |

{% hint style="info" %}
**Note**\
****If needed, it is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a storage volume later.
{% endhint %}

### &#x20;**(Optional) Install the Filebrowser application**

The **filebrowser** application, available through the [application Catalog](https://apps.coreweave.com/), allows you to access your storage volumes via a Web interface that allows you to upload and download files and folders.

It is recommended that the name you give this filebrowser application be very short, or you will run into SSL CNAME issues. We recommend `finetune`.

Simply select the `finetune-gpt-neox` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**

![The filebrowser application in the Cloud UI application Catalog](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.10.34 PM.png>)

{% hint style="info" %}
**Note**\
Installing the filebrowser application is optional to this process. As an alternative, it may be preferable to you to launch a Virtual Server or Kubernetes Pod to interact with their PVC via SSH or other mechanism.
{% endhint %}

### Install the DeterminedAI application

From the [application Catalog](https://apps.coreweave.com/), search for `determined`. This will bring up the DeterminedAI (**determined**) application, which you can then deploy into your cluster.

![The DeterminedAI application in the Cloud UI application Catalog](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.06.24 PM.png>)

The installation values should look similar to the ones shown and described below.

First, create an object storage bucket, which will be used to store checkpoints. You will then have access to `<YOUR_ACCESS_KEY> and <YOUR_SECRET_KEY>`.

{% hint style="info" %}
**Note**

Object storage is currently in beta. Please[ contact support](https://cloud.coreweave.com/contact) for more information.
{% endhint %}

![The DeterminedAI application configuration screen](<../.gitbook/assets/Screen Shot 2022-07-26 at 3.04.11 PM.png>)

The values used for this demonstration are as follows:

#### Default Resources

| Field                 | Demo value |
| --------------------- | ---------- |
| **Default resources** | 8 vCPUs    |
| **Memory request**    | 32Gi       |
| **GPU Type**          | A40        |

#### Object Storage Configuration

| Field           | Demo value                                                                             |
| --------------- | -------------------------------------------------------------------------------------- |
| **Bucket Name** | model-checkpoints                                                                      |
| **Access Key**  | `<YOUR_ACCESS_KEY>` - this should be replaced by your actual Object Storage access key |
| **Secret Key**  | `<YOUR_SECRET_KEY>` - this should be replaced by your actual Object Storage secret key |

#### Attaching the volume

Click  `+` to attach the `finetune-gpt-neox` volume.

![The attachment configuration screen for the DeterminedAI application](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.26.14 PM.png>)

As shown above, for this tutorial we are attaching the `finetune-gpt-neox` volume on the mount path `/mnt/finetune-gpt-neox`.

## Training

### Download the training examples

DeterminedAI provides training examples on GitHub. Clone the source code for the DeterminedAI from their repository.

```bash
$ git clone https://github.com/determined-ai/determined.git
```

The deployment configurations for the experiments and the source code to run the finetuning job are located in the [GPT-NeoX example](https://github.com/determined-ai/determined/tree/master/examples/deepspeed/gpt\_neox) directory under `examples/deepspeed/gpt_neox`.

### Download the "Slim" weights

{% hint style="warning" %}
**Important**

Run the`export DET_MASTER=...ord1.ingress.coreweave.cloud:80` command, found in the post-installation notes from the DeterminedAI deployment, prior to running the next command.
{% endhint %}

[Download the "Slim" weights](https://github.com/EleutherAI/gpt-neox) by running the following commands in your terminal:

```
det cmd run 'wget --cut-dirs=5 -nH -r --no-parent --reject "index.html*" https://the-eye.eu/public/AI/models/GPT-NeoX-20B/slim_weights/ -P /mnt/finetune-gpt-neox/20B_checkpoints'
```

Ensure that the above command completes executing. Depending on your network bandwidth, downloading weights can take up to an hour or two for 39GB of data. You can monitor the logs of the above command using the `logs` command:

```
det task logs -f <TASK_NAME_FROM_ABOVE>
```

### Deploy the DeterminedAI cluster

Review the below configuration for `determined-cluster.yml`. You may configure or change any of the optimizer values or training configurations to your needs. It is recommended to use [the NeoX source code](https://github.com/EleutherAI/gpt-neox) as reference when doing so.

Replace the contents of the original `determined-cluster.yml` file with the content below:

<details>

<summary>Click to expand - <code>determined-cluster.yml</code></summary>

```yaml
{
  # Tokenizer /  checkpoint settings - you will need to change these to the location you have them saved in
  "vocab-file": "/mnt/finetune-gpt-neox/20B_checkpoints/20B_tokenizer.json",
  
  # NOTE: You can make additional directories to load and save checkpoints
  "load": "/mnt/finetune-gpt-neox/20B_checkpoints",
  "save": "/mnt/finetune-gpt-neox/20B_checkpoints",

  # NOTE: This is the default dataset. Please change it to your dataset.
  "data-path": "/run/determined/workdir/shared_fs/data/enron/enron_text_document",

  # parallelism settings ( you will want to change these based on your cluster setup, ideally scheduling pipeline stages
  # across the node boundaries )
  "pipe-parallel-size": 4,
  "model-parallel-size": 2,

  # model settings
  "num-layers": 44,
  "hidden-size": 6144,
  "num-attention-heads": 64,
  "seq-length": 2048,
  "max-position-embeddings": 2048,
  "norm": "layernorm",
  "pos-emb": "rotary",
  "rotary_pct": 0.25,
  "no-weight-tying": true,
  "gpt_j_residual": true,
  "output_layer_parallelism": "column",
  "scaled-upper-triang-masked-softmax-fusion": true,
  "bias-gelu-fusion": true,

  # init methods
  "init_method": "small_init",
  "output_layer_init_method": "wang_init",

  # optimizer settings
  "optimizer": {
    "type": "Adam",
    "params": {
      "lr": 0.97e-4,
      "betas": [0.9, 0.95],
      "eps": 1.0e-8,
      }
      },

  "min_lr": 0.97e-5,
  "zero_optimization": {
  "stage": 1,
  "allgather_partitions": True,
  "allgather_bucket_size": 1260000000,
  "overlap_comm": True,
  "reduce_scatter": True,
  "reduce_bucket_size": 1260000000,
  "contiguous_gradients": True,
  "cpu_offload": False
  },

  # batch / data settings (assuming 96 GPUs)
  "train_micro_batch_size_per_gpu": 4,
  "gradient_accumulation_steps": 32,
  "data-impl": "mmap",
  "split": "995,4,1",

  # activation checkpointing
  "checkpoint-activations": true,
  "checkpoint-num-layers": 1,
  "partition-activations": false,
  "synchronize-each-layer": true,

  # regularization
  "gradient_clipping": 1.0,
  "weight-decay": 0.01,
  "hidden-dropout": 0,
  "attention-dropout": 0,

  # precision settings
  "fp16": {
    "fp16": true,
    "enabled": true,
    "loss_scale": 0,
    "loss_scale_window": 1000,
    "initial_scale_power": 12,
    "hysteresis": 2,
    "min_loss_scale": 1
    },

  # misc. training settings
  "train-iters": 150000,
  "lr-decay-iters": 150000,

  "distributed-backend": "nccl",
  "lr-decay-style": "cosine",
  "warmup": 0.01,
  "save-interval": 50,
  "eval-interval": 100,
  "eval-iters": 10,

  # logging
  "log-interval": 2,
  "steps_per_print": 2,
  "wall_clock_breakdown": false,

  ### NEW DATA: ####
  "tokenizer_type": "HFTokenizer",
  "tensorboard-dir": "./tensorboard",
  "log-dir": "./logs",

}
```

</details>

Once the above configuration has been replaced and the weights have been downloaded, you can navigate from the source code you cloned to the `examples/deepspeed/gpt_neox` directory if you have not already.

### Create the experiment

Copy the below configuration into a file called `finetune-gpt-neox.yml`

<details>

<summary>Click to expand - <code>finetune-gpt-neox.yml</code></summary>

```yaml
name: gpt-neox-zero1-3d-parallel
debug: false
profiling:
    enabled: true
    begin_on_batch: 1
    end_after_batch: 100
    sync_timings: true
hyperparameters:
  search_world_size: false
  conf_dir: /gpt-neox/configs
  conf_file:
      - determined_cluster.yml
  wandb_group: null
  wandb_team: null
  user_script: null
  eval_tasks: null
environment:
  environment_variables:
      - NCCL_SOCKET_IFNAME=ens,eth,ib
  force_pull_image: true
  image:
    gpu: liamdetermined/gpt-neox
resources:
  slots_per_trial: 96 # Utilize 96 GPUs for the finetune
searcher:
  name: single
  metric: lm_loss
  smaller_is_better: false
  max_length:
    batches: 100
min_validation_period:
    batches: 50
max_restarts: 0
entrypoint:
  - python3
  - -m
  - determined.launch.deepspeed
  - --trial
  - gpt2_trial:GPT2Trial

```

</details>

{% hint style="info" %}
**Note**

Many of the parameters in the above configuration can be changed, such as `batches`, and `slots_per_trail.` We use default values of `100` batches to finetune on with `50` batches before validation or early stopping, and `96 A40 GPUs` .
{% endhint %}

Run the following command to launch the experiment:

```
det experiment create finetune-gpt-neox.yml .
```

The experiment is now launched! You can see the status of your experiment and monitor logs as well using the Web UI.

Once training is completed, you will have access to the checkpoint in your S3 bucket for downstream tasks such as inference or model ensembles.
