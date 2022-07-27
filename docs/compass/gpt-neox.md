---
description: >-
  This page details the setup and process to train or fine-tune a GPT-NeoX 20B
  parameter model on CoreWeave cloud.
---

# Finetuning GPT-NeoX 20B using Determined.A

## Introduction

[GPT-NeoX](https://blog.eleuther.ai/announcing-20b/) is a 20B parameter autoregressive model that is trained on the Pile dataset. It generates text based on context or unconditionally for use cases such as story generation, chat bots, summarization etc. You can read the paper [here](https://arxiv.org/abs/2204.06745) and access the code [here](https://github.com/EleutherAI/gpt-neox). This model is trained on CoreWeave infrastructure and the [weights](https://github.com/EleutherAI/gpt-neox#pretrained-models) are made available via a permissive license. Based on your requirements and use case, this model is capable of high quality text generation. The model is trained on The Pile. Many customers have seen dastrically improved results by fine-tuning the model with data specific to their use-case. This guide will use the Determined.AI MLOpls platform to run distributed fine-tuning jobs on the model.

## Setup

{% hint style="info" %}
**Note**\
****This guide assumes that you have [set up the CoreWeave Kubernetes environment.](../../coreweave-kubernetes/getting-started.md) It also assumes that you have experience launching and using [determined.ai on CoreWeave Cloud](https://www.determined.ai). If you have not done so already, it is recommended to [deploy determined.ai via the application Catalog](https://apps.coreweave.com/) to familiarize yourself with it.
{% endhint %}

## Install Determined.ai on CoreWeave

* Create a Shared Filesystem storage volume from [the Storage menu on the CoreWeave Cloud UI](https://cloud.coreweave.com/storage). You can use the values in the image below for this tutorial. This volume will be used to store the model weights as well as training data for the finetune. Shared storage volumes can be accessed by many nodes at once in CoreWeave, allowing for massive amounts of compute power to access the same dataset.

![](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.14.13 PM.png>)

* It should be noted that it is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a storage volume as needed.&#x20;

**\[Optional] filebrowser**

![](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.10.34 PM.png>)

* Filebrowser allows you to access your storage volumes via a web interface to upload and download files and folders.
* You can deploy the filebrowser in the [Application Catalog](https://apps.coreweave.com/).
* It is recommended that the name you give this filebrowser application be very short, or you will run into SSL CNAME issues. We recommend `finetune`.
* Simply select the `finetune-gpt-neox` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**
* Some people may prefer to use a Virtual Server or Kubernetes Pod and interact with their PVC via SSH or other mechanism.

Please install determined.ai from the [Application Catalog](https://apps.coreweave.com/).&#x20;

![](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.06.24 PM.png>)

Your installation values should look similar to these. You will need to create a object storage bucket which will be used to store checkpoints. Object storage is currently in beta, please[ contact support](https://cloud.coreweave.com/contact). You will then have access to `<YOUR_ACCESS_KEY> and <YOUR_SECRET_KEY>.`

![](<../.gitbook/assets/Screen Shot 2022-07-26 at 3.04.11 PM.png>)

You can click on the `+` to attach the `finetune-gpt-neox` volume as shown below in your determined.ai deployment with the mount path `/mnt/finetune-gpt-neox.`

![](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.26.14 PM.png>)

## Training

* You can use the following command to get the source code for the Determined.AI examples (assuming you have `git` installed on your terminal):\
  `git clone`[`https://github.com/determined-ai/determined.git`](https://github.com/determined-ai/determined.git)
* You will find the experiment deployment configurations and source code to run the finetuning job in [GPT-NeoX example](https://github.com/determined-ai/determined/tree/master/examples/deepspeed/gpt\_neox). The path in the repository above is `examples/deepspeed/gpt_neox`
* You should be able to [download](https://github.com/EleutherAI/gpt-neox) the "Slim" weights by running the following commands in your terminal. Please run the `export DET_MASTER=...ord1.ingress.coreweave.cloud:80` (should be in post-installation notes from the Determined.AI deployment) prior to running the below command:

```
det cmd run 'wget --cut-dirs=5 -nH -r --no-parent --reject "index.html*" https://the-eye.eu/public/AI/models/GPT-NeoX-20B/slim_weights/ -P /mnt/finetune-gpt-neox/20B_checkpoints'
```

* You should ensure that the above command completes executing. Downloading weights can take an hour or two depending on your network bandwidth for 39GB of data. You can monitor the logs of the above command using: `det task logs -f <TASK_NAME_FROM_ABOVE>`
* Please go through and use the below configuration for `determined-cluster.yml`.You are free to configure or change any of the optimizer values or training configurations. Please use [this](https://github.com/EleutherAI/gpt-neox) as reference when doing so. You should replace the original file with the content below:

{% code title="determined-cluster.yml" %}
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
{% endcode %}

* Once you replace the above and the weights have been downloaded, you can navigate from the source code you cloned to `examples/deepspeed/gpt_neox`(if you have not already here)
* You should copy the below configuration into a file called `finetune-gpt-neox.yml`

{% code title="finetune-gpt-neox.yml" %}
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
{% endcode %}

* Note that many of the parameters in the above configuration can be changed such as `batches`, `slots_per_trail.` We use default values of `100` batches to finetune on with `50` batches before validation (or) early stopping and `96 A40 GPUs` .
* You can run the following command:

```
det experiment create finetune-gpt-neox.yml .
```

* Now you have it, you can see the status of your experiment using the Web UI and monitor logs as well. Once training is completed, you will have access to the checkpoint in your S3 bucket for downstream tasks such as inference or model ensembles.&#x20;

