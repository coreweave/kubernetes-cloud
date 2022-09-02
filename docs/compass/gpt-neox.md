---
description: >-
  This page details the setup and process to train or fine-tune a GPT-NeoX 20B
  parameter model on CoreWeave cloud.
---

# Finetuning GPT-NeoX 20B using DeterminedAI

[GPT-NeoX](https://blog.eleuther.ai/announcing-20b/) is a 20B parameter autoregressive model trained on [the Pile dataset](https://arxiv.org/abs/2101.00027).

It generates text based on context or unconditionally for use cases such as story generation, chat bots, summarization, and so on.

{% hint style="info" %}
**Additional Resources**

Learn more in the [GPT-NeoX-20B: An Open-Source Autoregressive Language Model](https://arxiv.org/abs/2204.06745) whitepaper, and [view the GPT-NeoX source code on GitHub](https://github.com/EleutherAI/gpt-neox).
{% endhint %}

This model is trained on CoreWeave infrastructure and the [weights](https://github.com/EleutherAI/gpt-neox#pretrained-models) are made available via a permissive license. Based on your requirements and use case, this model is capable of high quality text generation. Many customers have seen drastically improved results by finetuning the model with data specific to their use case.

This guide will use [the DeterminedAI MLOps platform](https://www.determined.ai/blog/determined-algorithmia-integration) to run distributed finetuning jobs on the model.

## Procedure

{% hint style="info" %}
**Note**

This guide makes several assumptions:\
\
• You have [set up the CoreWeave Kubernetes environment](../../coreweave-kubernetes/getting-started.md).\
• You have some experience launching and using [DeterminedAI on CoreWeave Cloud](https://www.determined.ai). (If you have not done so already, it is recommended to [deploy DeterminedAI via the application Catalog](https://apps.coreweave.com/) to familiarize yourself with it).\
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
| **Region**       | LAS1              |
| **Disk Class**   | HDD               |
| **Storage Type** | Shared Filesystem |
| **Size (Gi)**    | 1,000             |

{% hint style="info" %}
**Note**\
****If needed, it is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a storage volume later.
{% endhint %}

### **Install the Filebrowser application**

The **filebrowser** application, available through the [application Catalog](https://apps.coreweave.com/), allows you to access your storage volumes via a Web interface that allows you to upload and download files and folders.

It is recommended that the name you give this filebrowser application be very short, or you will run into SSL CNAME issues. We recommend `finetune`.

Simply select the `finetune-gpt-neox` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**

![The filebrowser application in the Cloud UI application Catalog](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.10.34 PM.png>)

{% hint style="info" %}
**Note**\
Installing the filebrowser application is **very helpful** to this process. As an alternative, it may be preferable to you to launch a Virtual Server or Kubernetes Pod to interact with their PVC via SSH or other mechanism.
{% endhint %}

### Install the Determined application

From the [application Catalog](https://apps.coreweave.com/), search for `determined`. This will bring up the Determined.ai (**determined**) application, which you can then deploy into your cluster.

![The DeterminedAI application in the Cloud UI application Catalog](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.06.24 PM.png>)

The installation values should look similar to the ones shown and described below.

![](<../.gitbook/assets/Screen Shot 2022-08-01 at 4.46.55 PM.png>)

First, create an object storage bucket, which will be used to store checkpoints. You will then have access to `<YOUR_ACCESS_KEY>` and `<YOUR_SECRET_KEY>`.

{% hint style="info" %}
**Note**

Object storage is currently in beta. Please[ contact support](https://cloud.coreweave.com/contact) for access.
{% endhint %}

The values used for this demonstration are as follows:

#### Region

`LAS1 (Las Vegas)`

#### Default Resources

| Field                 | Demo Value |
| --------------------- | ---------- |
| **Default resources** | 8 vCPUs    |
| **Memory request**    | 256Gi      |
| **GPU Type**          | A40        |

#### Object Storage Configuration

| Field           | Demo Value                                                                             |
| --------------- | -------------------------------------------------------------------------------------- |
| **Bucket Name** | model-checkpoints                                                                      |
| **Access Key**  | `<YOUR_ACCESS_KEY>` - this should be replaced by your actual Object Storage access key |
| **Secret Key**  | `<YOUR_SECRET_KEY>` - this should be replaced by your actual Object Storage secret key |

{% hint style="info" %}
**Note**

You will acquire the `ACCESS_KEY` and `SECRET_KEY` once object storage has been configured for you. [Contact support for more information.](https://cloud.coreweave.com/contact)
{% endhint %}

#### Attaching the volume

Click  `+` to attach the `finetune-gpt-neox` volume.

![The attachment configuration screen for the DeterminedAI application](<../.gitbook/assets/Screen Shot 2022-07-26 at 4.26.14 PM.png>)

As shown above, for this tutorial we are attaching the `finetune-gpt-neox` volume on the mount path `/mnt/finetune-gpt-neox`.

### Determined Web UI

After deploying the DeterminedAI application, a URL to the Web UI will be provided to you. You can use this UI to monitor experiments and check logs.

![The DeterminedAI Web UI](<../.gitbook/assets/image (17).png>)

As an example, here is what a live experiment looks like when viewed from the Web UI:

![A live experiment running in the DeterminedAI Web UI](<../.gitbook/assets/image (20).png>)

Navigating to the **Logs** tab will give you a full output of the experiment's logs:

![Log output from the DeterminedAI Web UI](<../.gitbook/assets/image (19).png>)

Navigating to **Overview** will give you access to a metrics visualization of the experiment and checkpoint reference.

![Metrics visualization in the DeterminedAI Web UI](<../.gitbook/assets/image (16) (1).png>)

## Training

### Configure your dataset

{% hint style="warning" %}
**Important**

Run the`export DET_MASTER=...ord1.ingress.coreweave.cloud:80` command, found in the post-installation notes from the DeterminedAI deployment, prior to running the next command.
{% endhint %}

Clone [the GPT-NeoX repository](https://github.com/EleutherAI/) to your CoreWeave Cloud Storage in a terminal:

```bash
det cmd run 'git clone https://github.com/EleutherAI/gpt-neox.git /mnt/finetune-gpt-neox/gpt-neox'
```

Then, download the [Vocab](https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-vocab.json) and [Merge](https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-merges.txt) files to your CoreWeave Cloud Storage in a terminal:

```bash
det cmd run 'wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-vocab.json
-O /mnt/finetune-gpt-neox/gpt2-vocab.json'

det cmd run 'wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-merges.txt
-O /mnt/finetune-gpt-neox/gpt2-merges.txt'
```

### Dataset Format&#x20;

Datasets for GPT-NeoX should be one large document in [**JSONL format**](https://jsonlines.org/). To prepare your own dataset for training with custom data, format it as one large JSONL-formatted file, where each item in the list of dictionaries is a separate document.

The document text should be grouped under one JSON key, i.e `"text"`.

#### Example

```
{"text": "We have received the water well survey for the N. Crawar site. The Crane \nCounty Water District owns 11 water wells within a one mile radius of the \nsite. The nearest well is located about 1000 feet east of the site. It \nappears that all of the wells are completed into the uppermost aquifer and, \nin general, are screened from 50' bgs to total depth at about 140' bgs. The \nshallow water table at the site and in the nearby wells is at about 50' bgs. \nThe groundwater flow direction at the site has consistently been toward due \nsouth. There are no water supply wells within one mile due south of the site. \nThere are two monitor wells at the east side of the site which have always \nproduced clean samples. The remediation system for this site should be \noperational by April 1, 2001. We will also have more current groundwater \nsampling information for the site within the next few weeks.", "meta": {}}
{"text": "Roger-\nWe will require off-site access for the installation of 10 remediation wells \nat the North Crawar facility (formerly owned by TW but now owned by Duke). I \nwill drop off in your office a site diagram that indicates the location of \nthe wells relative to the facility and the existing wells. I believe that the \nadjacent property owner had been contacted prior to well installations in \nAugust 1997, but I am not familiar with the details of the access agreement \nor even who within ET&S made the arrangements. We are shooting for \nearly-October for the well installations. We may also want to address \ncontinued access to the wells in an agreement with the landowner (a 5-10 year \nterm should be sufficient). Give me a call at x67327 if you have any \nquestions.\nThanks,\nGeorge", "meta": {}}
{"text": "Larry, the attached file contains a scanned image of a story that was \npublished in The Monahans News, a weekly paper, on Thursday, April 20, 2000. \nI've shown the story to Bill, and he suggested that you let Rich Jolly know \nabout the story.\n\nThanks, George\n\n\n---------------------- Forwarded by George Robinson/OTS/Enron on 04/24/2000 \n03:29 PM ---------------------------\n\n04/24/2000 03:21 PM\nMichelle Muniz\nMichelle Muniz\nMichelle Muniz\n04/24/2000 03:21 PM\n04/24/2000 03:21 PM\nTo: George Robinson/OTS/Enron@ENRON\ncc:  \n\nSubject: Newspaper\n\nI hope this works.  MM", "meta": {}}
```

{% hint style="info" %}
There are [several standard datasets](https://github.com/EleutherAI/gpt-neox/blob/e7a2fd25e4133fe570c7a8648c7b12b60c415a4b/tools/corpora.py#L298-L319) that you can leverage for testing.&#x20;
{% endhint %}

### Pre-processing your dataset

Upload your data as a single JSONL file called `data.jsonl` to filebrowser under `finetune-gpt-neox`:

![](<../.gitbook/assets/Screen Shot 2022-08-01 at 5.43.47 PM.png>)

Using the filebrowser app, create a new folder called `gpt_finetune` under the `finetune-gpt-neox` folder.

![Creating the gpt\_finetune directory in filebrowser](<../.gitbook/assets/image (5) (3).png>)

You can now pre-tokenize your data using `tools/preprocess_data.py`. The arguments for this utility are listed below.

<details>

<summary>preprocess_data.py Arguments</summary>

```
usage: preprocess_data.py [-h] --input INPUT [--jsonl-keys JSONL_KEYS [JSONL_KEYS ...]] [--num-docs NUM_DOCS] --tokenizer-type {HFGPT2Tokenizer,HFTokenizer,GPT2BPETokenizer,CharLevelTokenizer} [--vocab-file VOCAB_FILE] [--merge-file MERGE_FILE] [--append-eod] [--ftfy] --output-prefix OUTPUT_PREFIX
                          [--dataset-impl {lazy,cached,mmap}] [--workers WORKERS] [--log-interval LOG_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit

input data:
  --input INPUT         Path to input jsonl files or lmd archive(s) - if using multiple archives, put them in a comma separated list
  --jsonl-keys JSONL_KEYS [JSONL_KEYS ...]
                        space separate listed of keys to extract from jsonl. Defa
  --num-docs NUM_DOCS   Optional: Number of documents in the input data (if known) for an accurate progress bar.

tokenizer:
  --tokenizer-type {HFGPT2Tokenizer,HFTokenizer,GPT2BPETokenizer,CharLevelTokenizer}
                        What type of tokenizer to use.
  --vocab-file VOCAB_FILE
                        Path to the vocab file
  --merge-file MERGE_FILE
                        Path to the BPE merge file (if necessary).
  --append-eod          Append an <eod> token to the end of a document.
  --ftfy                Use ftfy to clean text

output data:
  --output-prefix OUTPUT_PREFIX
                        Path to binary output file without suffix
  --dataset-impl {lazy,cached,mmap}
                        Dataset implementation to use. Default: mmap

runtime:
  --workers WORKERS     Number of worker processes to launch
  --log-interval LOG_INTERVAL
                        Interval between progress updates
```

</details>

The command to tokenize your data and output it to `gpt_finetune` is below:

```shell
python tools/preprocess_data.py \
            --input /mnt/finetune-gpt-neox/data.jsonl \
            --output-prefix ./gpt_finetune/mydataset \
            --vocab /mnt/finetune-gpt-neox/gpt2-vocab.json \
            --merge-file /mnt/finetune-gpt-neox/gpt2-merges.txt \
            --dataset-impl mmap \
            --tokenizer-type GPT2BPETokenizer \
            --append-eod
```

&#x20;**Run** this command to pre-process and tokenize your data:

```shell
det cmd run 'apt-get -y install libopenmpi-dev; pip install -r /mnt/finetune-gpt-neox/gpt-neox/requirements/requirements.txt; pip install protobuf==3.20; python /mnt/finetune-gpt-neox/gpt-neox/tools/preprocess_data.py --input /mnt/finetune-gpt-neox/data.jsonl --output-prefix /mnt/finetune-gpt-neox/gpt_finetune/mydataset --vocab /mnt/finetune-gpt-neox/gpt2-vocab.json --merge-file /mnt/finetune-gpt-neox/gpt2-merges.txt --dataset-impl mmap --tokenizer-type GPT2BPETokenizer --append-eod'
```

{% hint style="warning" %}
**Important**

Tokenized data will be saved out to two files:

`<data-dir>/<dataset-name>/<dataset-name>_text_document.bin`and `<data-dir>/<dataset-name>/<dataset-name>_text_document.idx`.

You will need to add the prefix that both these files share to your training configuration file under the `data-path` field.
{% endhint %}

You should see the data here similar to below:

![](<../.gitbook/assets/Screen Shot 2022-08-02 at 5.54.33 PM.png>)

### Finetuning

{% hint style="warning" %}
**Important**

Run the`export DET_MASTER=...ord1.ingress.coreweave.cloud:80` command, found in the post-installation notes from the DeterminedAI deployment, prior to running the next command.
{% endhint %}

[Download the "Slim" weights](https://github.com/EleutherAI/gpt-neox) by running the following commands in a terminal:

```
det cmd run 'wget --cut-dirs=5 -nH -r --no-parent --reject "index.html*" https://the-eye.eu/public/AI/models/GPT-NeoX-20B/slim_weights/ -P /mnt/finetune-gpt-neox/20B_checkpoints'
```

{% hint style="warning" %}
**Important**

Ensure that the above command completes executing. Depending on your network bandwidth, downloading weights can take up to an hour or two for 39GB of data. You can monitor the logs of the above command using the `logs` command:\
\
`det task logs -f <TASK_NAME_FROM_ABOVE>`
{% endhint %}

#### Download the training examples

DeterminedAI provides training examples on GitHub. Clone the source code for the DeterminedAI from their repository in a terminal in an acccesible path:

```bash
$ git clone https://github.com/determined-ai/determined.git
```

The deployment configurations for the experiments and the source code to run the finetuning job are located in the [GPT-NeoX example](https://github.com/determined-ai/determined/tree/master/examples/deepspeed/gpt\_neox) directory under `examples/deepspeed/gpt_neox`.

{% hint style="info" %}
**Additional Resources**

EleutherAI provides [a lot of useful information](https://github.com/EleutherAI/gpt-neox/tree/e7a2fd25e4133fe570c7a8648c7b12b60c415a4b#datasets) on their provided datasets, which may be helpful when configuring datasets and training parameters for tensor and pipeline parallelism for finetuning using GPT-NeoX.
{% endhint %}

Navigate from the root of the `determined.ai` source code you cloned previously to the `examples/deepspeed/gpt_neox` directory.

Review and replace the contents of the original `determined-cluster.yml` file with the content below to configure the cluster for 96 GPUs in `examples/deepspeed/gpt_neox/gpt_neox_config/determined-cluster.yml`. You may configure or change any of the optimizer values or training configurations to your needs. It is recommended to use [the NeoX source code](https://github.com/EleutherAI/gpt-neox) as reference when doing so.

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
  "data-path": "/mnt/finetune-gpt-neox/gpt_finetune/mydataset_text_document",

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

**(Optional)** You can customize the deployment to 8 GPUs as well using the below configuration. Ensure you set `slots_per_trial: 8` in the following (next section) experiment configuration file `finetune-gpt-neox.yml`:

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
   "data-path": "/mnt/finetune-gpt-neox/gpt_finetune/mydataset_text_document",

   # parallelism settings ( you will want to change these based on your cluster setup, ideally scheduling pipeline stages
   # across the node boundaries )
   "pipe-parallel-size": 2,
   "model-parallel-size": 2,

   # model settings
   "num-layers": 24,
   "hidden-size": 1024,
   "num-attention-heads": 16,
   "seq-length": 2048,
   "max-position-embeddings": 2048,
   "norm": "layernorm",
   "pos-emb": "rotary",
   "no-weight-tying": true,

   # these should provide some speedup but takes a while to build, set to true if desired
   "scaled-upper-triang-masked-softmax-fusion": false,
   "bias-gelu-fusion": false,



   # optimizer settings
   "optimizer": {
     "type": "Adam",
     "params": {
       "lr": 0.0003,
       "betas": [0.9, 0.999],
       "eps": 1.0e-8,
     }
   },
   "zero_optimization": {
    "stage": 1,
    "allgather_partitions": True,
    "allgather_bucket_size": 500000000,
    "overlap_comm": True,
    "reduce_scatter": True,
    "reduce_bucket_size": 500000000,
    "contiguous_gradients": True,
    "cpu_offload": False
  },
   # batch / data settings
   "train_micro_batch_size_per_gpu": 4,
   "train_batch_size" : 32, 
   "data-impl": "mmap",
   "split": "949,50,1",

   # activation checkpointing
   "checkpoint-activations": true,
   "checkpoint-num-layers": 1,
   "partition-activations": false,
   "synchronize-each-layer": true,

   # regularization
   "gradient_clipping": 1.0,
   "weight-decay": 0,
   "hidden-dropout": 0,
   "attention-dropout": 0,

   # precision settings
   "fp16": {
     "fp16": true,
     "enabled": true,
     "loss_scale": 0,
     "loss_scale_window": 1000,
     "hysteresis": 2,
     "min_loss_scale": 1
   },

   # misc. training settings
   "train-iters": 320000,
   "lr-decay-iters": 320000,
   "distributed-backend": "nccl",
   "lr-decay-style": "cosine",
   "warmup": 0.01,
   "save-interval": 10000,
   "eval-interval": 1000,
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

### Create the experiment

{% hint style="info" %}
**Note**

You will need to be in the `examples/deepspeed/gpt_neox` directory
{% endhint %}

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

You should see an "Active" status for your experiment:

![](<../.gitbook/assets/Screen Shot 2022-08-01 at 12.44.15 PM.png>)

You can visualize and monitor logs:

![](<../.gitbook/assets/Screen Shot 2022-08-01 at 12.46.41 PM (1).png>)

Once training is completed, you will have access to the checkpoint in your S3 bucket for downstream tasks such as inference, transfer learning or model ensembles.

![](<../.gitbook/assets/Screen Shot 2022-08-02 at 5.47.43 PM.png>)

### **(Optional) Wandb.ai visualization of training graphs**

[Weights & Biases AI](https://wandb.ai/site) (Wandb.ai) can be installed and configured to visualize training graphs.

Pass in the  `<WANDB_GROUP>` and `<WANDB_TEAM>` variables to your configuration file.

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
  wandb_group: <WANDB_GROUP>
  wandb_team: <WANDB_TEAM>
environment:
  environment_variables:
      - NCCL_DEBUG=INFO
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
    batches: 1000
min_validation_period:
    batches: 500
max_restarts: 0
entrypoint:
  - python3
  - -m
  - determined.launch.deepspeed
  - --trial
  - gpt2_trial:GPT2Trial
```

{% hint style="info" %}
**Additional Resources**

* [GPT-NeoX ](https://github.com/EleutherAI/gpt-neox#using-custom-data)
* [Determined.ai Documentation](https://docs.determined.ai/latest/)
* [Determined.ai Github](https://github.com/determined-ai/determined)
{% endhint %}
