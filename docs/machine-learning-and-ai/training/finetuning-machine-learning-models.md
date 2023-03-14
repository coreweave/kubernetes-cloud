---
description: Fine-tune machine learning models using Argo Workflows on CoreWeave Cloud
---

# Fine-tune GPT Models with CoreWeave

Finetuning and training machine learning models can be computationally expensive. CoreWeave Cloud allows for easy, on-demand compute resources to train models, along with the infrastructure to support it.

This guide is intended to be a reference example of [how to use Argo Workflows](../../compass/broken-reference/) to set up a machine learning pipeline on CoreWeave. While the following barely scratches the surface of finetuning, this is a great place to start.

The reference example utilizes GPT-type transformer models with the [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) library, and assumes that the model's tokenization format is BPE.

{% hint style="info" %}
**Note**

This reference example is not intended to be a production application; rather, it is a guide on how to utilize CoreWeave resources to set up a pipeline.
{% endhint %}

The base model being trained on can be provided directly in a [PVC (PersistentVolumeClaim)](../../storage/storage/), or in a model identifier from [Hugging Face's model repository](https://huggingface.co/models). The dataset trained upon needs to be in the same PVC, and in pure text format.

{% hint style="info" %}
**Note**

It is recommended that you partition your data into separate files for easy addition and removal of subsets.
{% endhint %}

Presently, the reference example uses the following container configuration to train models on:

* 8 vCPU (AMD EPYC, usually)
* 128GB RAM
* Nvidia A40/A6000 (48GB VRAM)

The above configuration has been found to be optimal for training a variety of GPT models from a 155m to a 6b parameter size on a single GPU. The above configuration is billed at $2.00/hr through CoreWeave's [resource based pricing](../../../resources/resource-based-pricing.md) model.

There is an optional test [Inference endpoint](../../compass/broken-reference/) that can be enabled and deployed automatically when the model completes finetuning. This Inference container defaults to the following configuration:

* 4 vCPU
* 8GB RAM
* Nvidia RTX A5000 (24GB VRAM)

This configuration is able to do 6b models comfortably, and is less expensive than the finetuner, as it requires less resources at $0.85/hr.

## Source code

The source code used for this tutorial can be found under the `finetuner-workflow` folder in the `coreweave/kubernetes-cloud` repository.

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/finetuner-workflow" %}
Check out the code on GitHub
{% endembed %}

## Setup

{% hint style="info" %}
**Note**

This guide assumes that you have already followed the process to set up the CoreWeave Kubernetes environment. If you have not done so already, [follow our Getting Started guide](../../coreweave-kubernetes/getting-started.md) before proceeding with this guide.
{% endhint %}

The following Kubernetes-based components are required:

### [Argo Workflows](https://docs.coreweave.com/workflows/argo)

You can deploy Argo Workflows using the [application Catalog](https://apps.coreweave.com). From the application deployment menu, click on the **Catalog** tab, then search for `argo-workflows` to find and deploy the application.

![Argo Workflows](<../../.gitbook/assets/image (138).png>)

The catalog deployment will create the underlying resources needed for client authentication. To fetch the authentication token run the following commands after filing in the name of your argo-workflows deployment.

```bash
export ARGO_NAME=<enter your deployment name>
export SECRET=$(kubectl get sa ${ARGO_NAME}-argo -o=jsonpath='{.secrets[0].name}')
export ARGO_TOKEN="Bearer $(kubectl get secret $SECRET -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN
```

Then, inside the box for **client authentication**, copy and paste the newly generated token into the Argo UI:

![The Argo Workflow UI with a Bearer token pasted into the client authentication box](<../../.gitbook/assets/image (2) (2) (1).png>)

Finally, to log in, click the **Login** button after adding the token.

### [PVC](../../storage/storage/)

Create a `ReadWriteMany` [PVC storage volume](../../storage/storage/#volume-types) from the [Storage](https://cloud.coreweave.com/storage) menu.

`1TB` to `2TB` is the recommended size for the volume, as the model checkpoints take up a lot of space! These PVCs can be shared between multiple finetune runs. We recommend using HDD type storage, as the finetuner does not require high random I/O performance.

![Configuring a PVC storage volume from the Cloud UI](<../../.gitbook/assets/image (3) (2) (1).png>)

{% hint style="info" %}
**Note**\
It is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a PVC as needed.
{% endhint %}

This workflow expects a default PVC name of `finetune-data`. This name can be changed once you are more comfortable with the workflow and configure it. If you prefer, the PVC can also be deployed using the YAML snippet below, applied using `kubectl apply -f finetune-pvc.yaml`:

{% code title="finetune-pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: finetune-data
spec:
  storageClassName: shared-hdd-ord1
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2000Gi
```
{% endcode %}

### Optional components

The following components are **optional**, but may make your interaction easier:

#### File Browser

This application allows you to share out and access your PVC using an easy application that lets you upload and download files and folders. You can find and deploy the filebrowser over at the same[ application Catalog](https://apps.coreweave.com/) that you used to deploy Argo Workflows.

It is recommended that the name you give the filebrowser application be very short, or you will run into SSL CNAME issues. We recommend using the name `finetune`.

Simply select the `finetune-data` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**

{% hint style="success" %}
**Tip**

Some people may prefer to use a [Virtual Server](../../compass/broken-reference/) to interact with their PVC via `ssh` or another mechanism. This flexibility is one of the key advantages of CoreWeave.
{% endhint %}

![The filebrowser application](<../../../.gitbook/assets/image (60) (2).png>)

## Dataset Setup

At this point, you should have a PVC set up that you can access via the [filebrowser application](finetuning-machine-learning-models.md#undefined) or some other mechanism. For each dataset you want to use, you should create a directory and give it a meaningful name. However, the workflow will read the finetune dataset from the `dataset` directory by default.

The data should be **individual plaintext files** (.txt) in the precise format that you want the prompt and responses to come in.

#### Example

Here we have a `western-romance` directory below with novels, in a clean and normalized plaintext format, with all extra whitespace removed.

![western-romance dataset with text files for each novel.](<../../.gitbook/assets/Screen Shot 2022-04-22 at 12.20.38 PM.png>)

The dataset will automatically be tokenized by a [`dataset_tokenizer`](https://github.com/wbrown/gpt\_bpe/blob/main/cmd/dataset\_tokenizer/dataset\_tokenizer.go) component written in `golang` as a step in the Argo Workflow. It is quite fast, and has different options for how to partition the data.

### Create a dataset

If you don't already have your own dataset, you can set the Argo Workflow to use CoreWeave's public [Dataset Downloader repository](https://github.com/coreweave/dataset-downloader). This script will download plain text files of Western Romance books available on [Smashworks](https://www.smashwords.com/). (This is the website that was scraped to create the [bookcorpus](https://huggingface.co/datasets/bookcorpus) dataset.)

## Permissions setup

To automatically create an `InferenceService`, the Argo Workflow job you submit needs special permissions. The below YAML snippet shows an example `ServiceAccount` with the corresponding required permissions.

Copy the below into a file titled `inference-role.yaml`:

{% code title="inference-role.yaml" %}
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: inference
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role:inference
rules:
  - apiGroups:
      - serving.kubeflow.org
    resources:
      - inferenceservices
    verbs:
      - '*'
  - apiGroups:
      - serving.knative.dev
    resources:
      - services
      - revisions
    verbs:
      - '*'
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rolebinding:inference-inference
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: role:inference
subjects:
  - kind: ServiceAccount
    name: inference
```
{% endcode %}

Invoking `kubectl apply -f inference-role.yaml` will apply the permissions detailed above.

## Clone and run the Workflow

The [example code is available on GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/finetuner-workflow). It is recommended that you use `git checkout` to pull down the latest copy of the code.

This repository includes the following files:

* `finetune-workflow.yaml` - The Argo Workflow itself.
* `inference-role.yaml` - The role you set up earlier in this document.
* `finetune-pvc.yaml` - A model storage volume, as described earlier in this document.
* `finetuner/Dockerfile` - A Dockerfile that can be used to build your own finetuner image, should you modify the `finetuner.py` code.
* `finetuner/finetuner.py` - The simple reference example finetune training code.
* `finetuner/ds_config.json` - The deepspeed configuration placed in the container. **It is recommended that you not modify this.**
* `finetuner/requirements.txt` - The Python requirements and versions. You can create a `venv`, but this is mainly for the `Dockerfile` build.

For reference, a copy of the `finetune-workflow.yaml` is at the [bottom of this document](finetuning-machine-learning-models.md#undefined), but the GitHub repository has the authoritative version.

Assuming that you have pulled a copy of `finetune-workflow.yaml`, the Argo Workflows are invoked using the following:

{% code title="Argo submit example" %}
```bash
$ argo submit finetune-workflow.yaml \
        -p run_name=example-gpt-j-6b \
        -p dataset=dataset \
        -p reorder=random \
        -p run_inference=true \
        -p inference_only=false \
        -p download_dataset=false \
        -p model=EleutherAI/gpt-j-6B \
        --serviceaccount inference
```
{% endcode %}

{% hint style="info" %}
**Note**

If you didn't upload your own dataset in the [Dataset Setup](finetuning-machine-learning-models.md#dataset-setup) section, set the `download_dataset` parameter to `true`:

`-p download_dataset=true`
{% endhint %}

The parameters included in the above are:

| Parameter name               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run_name`                   | <p><strong>The only absolutely required parameter.</strong><br><strong></strong><br><strong></strong>It is strongly recommended that the value of this parameter be unique, as it is what is used to name the <code>InferenceService</code>. Consequently, the <code>run_name</code> must meet DNS standards. Keep this parameter short in length.<br></p><p>Note also that the results of this exercise should be output to a folder in your PVC called <code>results-&#x3C;run_name></code>.</p> |
| `dataset`                    | The name of the dataset directory on the PVC.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `reorder`                    | <p>Determines how the tokenizer should order the dataset inputs.<br><br>Options are:  <code>size_ascending</code>, <code>size_descending</code>, <code>name_ascending</code>, <code>name_descending</code>,  <code>random</code>, and <code>none</code>.<br><br><code>shuffle</code> sorts the path using the <code>none</code> format, but also sorts tokens randomly. Useful for large sequential datasets, such as novels.</p>                                                                  |
| `run_inference`              | This parameter explicitly tells the Workflow that we want to run a test inference service when this exercise is done. It is not intended to be a production service, but to provide an end-to-end demonstration, allowing you to test the finetuned model.                                                                                                                                                                                                                                         |
| `--serviceaccount inference` | Required for `run_inference` to work correctly.                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `inference_only`             | <p>This parameter tells the Workflow whether or not you want to skip the finetuning portion of the training.<br><br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span>Set this to <code>false</code> in the first run, then to <code>true</code> in following runs once you have generated a model.</p>                                                                                                                                                                        |
| `download_dataset`           | This parameter tells the Workflow whether or not you need to download a dataset before tokenization.                                                                                                                                                                                                                                                                                                                                                                                               |
| `model`                      | This example uses a [Hugging Face model](https://github.com/huggingface) identifier to pull down the model `gpt-j-6B`. This model will be cached on subsequent runs on your PVC, under `cache`.                                                                                                                                                                                                                                                                                                    |

{% hint style="info" %}
**Note**

Other methods of passing parameters to your jobs may be preferred to inline definitions. These methods include:

* An [Argo parameters file](https://argoproj.github.io/argo-workflows/walk-through/parameters/) applied using `argo submit -f`, or, the `-p` option may be used to configure additional customizations
* Templating using [Helm Charts](https://helm.sh)
* Programmatically using the [Argo Workflows API](https://argoproj.github.io/argo-workflows/swagger/)
* Using the [Argo Web UI](finetuning-machine-learning-models.md#argo-workflows)
{% endhint %}

Once the job is submitted, you should see output that looks very much like the following:

```
Name:                finetune-wtd2k
Namespace:           tenant-goosewes-1
ServiceAccount:      inference
Status:              Pending
Created:             Fri Apr 22 12:50:34 -0400 (now)
Progress:
Parameters:
  dataset:           dataset
  run_name:          example-gpt-j-6b
  run_inference:     true
  model:             EleutherAI/gpt-j-6B
  pvc:               finetune-data
  retokenize:        false
  eot_token:
  pad_token:
  boundary_token:    \n
  context:           2048
  train_ratio:       0.9
  batch_size:        -1
  force_fp16:        false
  batch_size_divisor: 1.0
  random_seed:       42
  learn_rate:        5e-5
  epochs:            1
  gradients:         5
  zero_stage:        3
  no_resume:         false
  logs:              ./logs
  wandb_key:
  project_id:        huggingface
  inference_only:    false
  region:            ORD1
  tokenizer_image:   ghcr.io/wbrown/gpt_bpe/dataset_tokenizer:ed439c6
  finetuner_image:   docker.io/gooseai/finetuner:rc50
  inference_image:   coreweave/ml-images:pytorch-huggingface-81d5ce1
```

## Observing the Argo Workflow

At this point, we can observe the job via several mechanisms, now that we have the `Name` of `finetune-wtd2k`:

### Argo commands

#### `argo watch`

Invoking `argo watch finetune-wtd2k` tells Argo that we want to watch the job as it goes through the stages of:

* model-tokenization
* model-finetune\
  and
* model-inference

#### Example output

```
Name:                finetune-wtd2k
Namespace:           tenant-goosewes-1
ServiceAccount:      inference
Status:              Running
Conditions:
 PodRunning          True
Created:             Fri Apr 22 11:00:15 -0400 (1 hour ago)
Started:             Fri Apr 22 11:00:15 -0400 (1 hour ago)
Duration:            1 hour 54 minutes
Progress:            1/2
ResourcesDuration:   1s*(1 cpu),1s*(100Mi memory)
Parameters:
  dataset:           dataset
  run_name:          cassandra-gpt-j-6b-fp16
  run_inference:     true
  model:             EleutherAI/gpt-j-6B
  zero_stage:        3
  gradients:         5
  force_fp16:        true
  pvc:               finetune-data
  retokenize:        false
  eot_token:
  pad_token:
  boundary_token:    \n
  context:           2048
  train_ratio:       0.9
  batch_size:        -1
  batch_size_divisor: 1.0
  random_seed:       42
  learn_rate:        5e-5
  epochs:            1
  no_resume:         false
  logs:              logs
  project_id:        huggingface
  inference_only:    false
  region:            ORD1
  tokenizer_image:   ghcr.io/wbrown/gpt_bpe/dataset_tokenizer:ed439c6
  finetuner_image:   docker.io/gooseai/finetuner:rc50
  inference_image:   coreweave/ml-images:pytorch-huggingface-81d5ce11

STEP                 TEMPLATE         PODNAME                    DURATION  MESSAGE
 ● finetune-ckl8r    main
 ├───✔ tokenizer(0)  model-tokenizer  finetune-ckl8r-2169410118  7s
 └───● finetuner     model-finetuner  finetune-ckl8r-3837635091  1h
```

#### `argo logs`

Invoking `argo logs -f finetune-wtd2k kfserving-container` watches the logs in real time.

{% hint style="warning" %}
**Important**

If this process appears to hang while outputting the message `Loading the model`, this is due to a bug in the terminal display code which is exposed during initial model download and caching. To fix this, kill the relevant pod or job, then resubmit it. This should result in the proper progress display.
{% endhint %}

#### Example output

```
finetune-ckl8r-2169410118: 2022/04/22 15:00:21 Newest source `/finetune-data/dataset/Alastair Reynolds - [Revelation Space] Chasm City.txt` is older than `/finetune-data/dataset-EleutherAI_gpt_j_6B-2048.tokens`, not retokenizing. Use -retokenize to force retokenization.
finetune-ckl8r-3837635091: RUN_NAME: cassandra-gpt-j-6b-fp16
finetune-ckl8r-3837635091: HOST: finetune-ckl8r-3837635091
finetune-ckl8r-3837635091: CUDA: 11.3
finetune-ckl8r-3837635091: TORCH: 1.10.0a0+git302ee7b
finetune-ckl8r-3837635091: TRANSFORMERS: 4.17.0
finetune-ckl8r-3837635091: CPU: (maxrss: 297mb F: 811,255mb) GPU: (U: 19mb F: 51,033mb T: 51,052mb) TORCH: (R: 0mb/0mb, A: 0mb/0mb)
finetune-ckl8r-3837635091: DATASET: /finetune-data/dataset-EleutherAI_gpt_j_6B-2048.tokens
finetune-ckl8r-3837635091: DATASET SIZE: 194.27mb, 101,855,232 tokens, 49,734 contexts
finetune-ckl8r-3837635091: TRAIN_DATASET: 44,760 examples
finetune-ckl8r-3837635091: VALUE_DATASET: 4,974 examples
finetune-ckl8r-3837635091: LAST CHECKPOINT: None
finetune-ckl8r-3837635091: RANDOM SEED: 42
finetune-ckl8r-3837635091: FORCE FP16: True
finetune-ckl8r-3837635091: Loading EleutherAI/gpt-j-6B
finetune-ckl8r-3837635091: CPU: (maxrss: 48,240mb F: 761,345mb) GPU: (U: 13,117mb F: 37,935mb T: 51,052mb) TORCH: (R: 12,228mb/12,228mb, A: 12,219mb/12,219mb)
finetune-ckl8r-3837635091: CPU: (maxrss: 48,240mb F: 785,595mb) GPU: (U: 13,117mb F: 37,935mb T: 51,052mb) TORCH: (R: 12,228mb/12,228mb, A: 12,219mb/12,219mb)
finetune-ckl8r-3837635091: Setting batch size to 4
finetune-ckl8r-3837635091: [2022-04-22 15:03:12,856] [INFO] [distributed.py:46:init_distributed] Initializing torch distributed with backend: nccl
finetune-ckl8r-3837635091: Using amp half precision backend
finetune-ckl8r-3837635091: [2022-04-22 15:03:12,863] [INFO] [logging.py:69:log_dist] [Rank 0] DeepSpeed info: version=0.6.1, git-hash=unknown, git-branch=unknown
...
  4% 99/2238 [1:48:23<35:43:37, 60.13s/it]
finetune-ckl8r-3837635091: CPU: (maxrss: 114,754mb F: 674,206mb) GPU: (U: 37,289mb F: 13,763mb T: 51,052mb) TORCH: (R: 36,033mb/36,033mb, A: 22,016mb/23,665mb)
  4% 100/2238 [1:49:59<42:08:58, 70.97s/it]{'loss': 2.6446, 'learning_rate': 5e-05, 'epoch': 0.04}
  5% 101/2238 [1:51:00<40:18:00, 67.89s/it]
finetune-ckl8r-3837635091: CPU: (maxrss: 114,754mb F: 674,205mb) GPU: (U: 37,289mb F: 13,763mb T: 51,052mb) TORCH: (R: 36,033mb/36,033mb, A: 22,016mb/23,665mb)
  5% 103/2238 [1:53:00<37:54:38, 63.92s/it]
finetune-ckl8r-3837635091: CPU: (maxrss: 114,754mb F: 674,205mb) GPU: (U: 37,289mb F: 13,763mb T: 51,052mb) TORCH: (R: 36,033mb/36,033mb, A: 22,016mb/23,665mb)
  5% 105/2238 [1:55:01<36:50:48, 62.19s/it]
finetune-ckl8r-3837635091: CPU: (maxrss: 114,754mb F: 674,205mb) GPU: (U: 37,289mb F: 13,763mb T: 51,052mb) TORCH: (R: 36,033mb/36,033mb, A: 22,016mb/23,665mb)
```

During finetuning, the time elapsed is displayed, alongside the expected time to complete. Checkpointing and loss reporting is also reported.

{% hint style="info" %}
**Note**

You can instantly watch a submitted workflow by using the `--watch` option when running the `submit` command:\
`argo submit --watch`
{% endhint %}

#### Web UI

You can access your Argo Workflow application via HTTPS to see all the finetuner jobs, and to check their statuses.

![Argo Workflows HTTPS request, via the Web UI](<../../../.gitbook/assets/image (68).png>)

## Workflow options

The following section outlines some useful workflow parameters. This is not intended to be a complete or exhaustive reference on all exposed parameters.

| Parameter        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Default Value                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `run_name`       | The run name used to name artifacts and report metrics. Should be unique.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | The only required option; no default |
| `pvc`            | The PVC to use for dataset and model artifacts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `finetune-data`                      |
| `region`         | The region to run the Argo jobs in. Generally, this should be `ORD1`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `ORD1`                               |
| `dataset`        | The dataset folder relative to the `pvc` root.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `dataset`                            |
| `model`          | The model to train on. It can be a relative path to the `pvc` root; if it can't be found, the finetuner will attempt to download the model from Huggingface.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `EleutherAI/gpt-neo-2.7B`            |
| `context`        | Training context size in tokens. Affects the tokenization proces as well.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `2048`                               |
| `reorder`        | <p>Sort the input text files provided to the tokenizer according to one of the following selected criteria:<br>* <code>size_ascending</code><br>* <code>size_descending</code><br>* <code>name_ascending</code><br>* <code>name_descending</code><br>* <code>random</code></p><p>* <code>none</code><br>* <code>shuffle</code></p><p><br>This is different from the trainer shuffling, which selects contexts randomly. If you use one of the above options, you will most likely want to disable this behavior by passing <code>-no_shuffle</code> to the trainer. <code>shuffle</code> implements <code>none</code> while also shuffling the writing of tokens from the finetuner output.</p> | `none`                               |
| `epochs`         | The number of times the finetuner should train on the dataset.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `1`                                  |
| `learn_rate`     | How quickly the model should learn the finetune data. Too high a learn rate can be counterproductive and replace the base model's training.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `5e-5`                               |
| `wandb_key`      | Strongly recommended. Use an API key from [http://wandb.ai](http://wandb.ai) to report on finetuning metrics with nice charts.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                      |
| `run_inference`  | Whether to run the example `InferenceService` on the finetuned model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `false`                              |
| `inference_only` | When `true`, do **not** run the tokenization or finetune. Intended to quickly run only the `InferenceService` on a previously trained model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `false`                              |

## Artifacts and Inference

Once the model completes finetuning, the model artifacts should be found under a directory with a name patterned after`{{pvc}}/finetunes/{{run_name}}/final`.

You can download the model at this point, or you can run the `InferenceService` on the model.

If you followed the directions for Inference Service, and have installed the KNative client, you should be able to get an URL by invoking `kn service list`.

Services can also be listed without the KNative Client by executing `kubectl get ksvc`:

#### Example output

```
NAME                                              URL                                                                                                  LATEST                                      AGE     CONDITIONS   READY   REASON
inference-western-predictor-default               http://inference-western-predictor-default.tenant-goosewes-1.knative.chi.coreweave.com               inference-western-predictor-default-00007   2d21h   3 OK / 3     True
```

We can run `curl` to do a test query:

{% hint style="info" %}
**Note**

This assumes [`jq`](https://stedolan.github.io/jq/) is installed.
{% endhint %}

```shell
curl http://inference-western-predictor-default.tenant-goosewes-1.knative.chi.coreweave.com/v1/models/final:predict \
     -H 'Content-Type: application/json; charset=utf-8' \
     --data-binary @- << EOF | jq .
{"parameters": {"min_length":150,
                "max_length":200},
 "instances": ["She danced with him in the honky-tonk"]}
EOF
```

#### Example output

The above command should yield a result similar to the following:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   935  100   828  100   107    147     19  0:00:05  0:00:05 --:--:--   188
{
  "predictions": [
    [
      {
        "generated_text": "She danced with him in the honky-tonk hall as if to say, \"You got me into this mess. Now I'll get you out of it. Let's split it and go our separate ways. Maybe I'll get lucky and make you my partner.\"\nHe grinned. \"You never know. Don't let anyone stop you. But if someone tries to arrest you, let them worry about that.\"\n\"I'll do that. Now, about that money?\"\n\"Money? What money?\"\n\"The loan they paid to your uncle to buy your brother out of that mine. I'm not sure why they did that.\"\nHe grinned. \"That's what I've been trying to figure out myself. They want more power over the land they're buying so they can put up cattle. But they're not taking long to figure out that I'm onto them, so keep this money safe until we figure out the best way to handle it. Don't try"
      }
    ]
  ]
}
```

And there we have it - taking a model and dataset through the tokenization and finetuning process to do test inferences against the new model.

While this barely scratches the surface of finetuning, this is a good place to get started.
