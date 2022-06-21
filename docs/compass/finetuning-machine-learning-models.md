# Finetuning Machine Learning Models

## Introduction

Finetuning and training machine learning models can be computationally expensive. CoreWeave Cloud allows for easy on-demand compute resources to train models along with the infrastructure to support it. This guide is intended to be a reference example of [how to use Argo Workflows](broken-reference) to set up a machine learning pipeline on CoreWeave.

The reference example utilizes GPT-type transformer models with the HuggingFace Transformers library, and assumes that the model's tokenization format is BPE. The reference example is not intended to be a production application; rather it is a guide to how to utilize CoreWeave resources to set up a pipeline.

The base model being trained on can be provided directly in a [PVC (PersistentVolumeClaim)](../../coreweave-kubernetes/storage.md), or a model identifier from [HuggingFace's model repository](https://huggingface.co/models). The dataset trained upon needs to be in the same PVC, and in pure text format. It is recommended that you partition your data into separate files for easy addition and removal of subsets.

Presently, the reference example uses the following container configuration to train models on:

* 8 vCPU (AMD EPYC usually)
* 128GB RAM
* Nvidia A40/A6000 (48GB VRAM)

The above configuration has been found to be pretty optimal for training a variety of GPT models from 155m to 6b parameter size on a single GPU. The above configuration is billed at $2.00/hr through CoreWeave's [resource based pricing](../../resources/resource-based-pricing.md) model.

There is an optional test [Inference endpoint](broken-reference) that can be enabled and deployed automatically when the model completes finetuning. The Inference container defaults to the following configuration:

* 4 vCPU
* 8GB RAM
* Nvidia RTX A5000 (24GB VRAM)&#x20;

This configuration will be able to do 6b models comfortably, and is less expensive than the finetuner as it requires less resources at $0.85/hr.

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/finetuner-workflow" %}
Check out the code on GitHub
{% endembed %}

## Setup

**NOTE:** It is also assumed that you have [followed the process to get set up in the CoreWeave Kubernetes environment.](../../coreweave-kubernetes/getting-started.md)

The following Kubernetes-based components are required to be setup:

* [Argo Workflows](broken-reference)
  * You can deploy Argo Workflows using the [Application Catalog](https://apps.coreweave.com). Click on the `Catalog` tab, and find the `argo-workflows` application to deploy it.

![Argo Workflows](<../.gitbook/assets/image (82) (1) (1).png>)

* [PVC](../../coreweave-kubernetes/storage.md)
  * You can create a `ReadWriteMany` PVC storage volume at [Storage](https://cloud.coreweave.com/storage).
  * `1TB` to `2TB` is recommended as the model checkpoints take up a lot of space! These PVCs can be shared between multiple finetune runs. We recommend using HDD type storage, as the finetuner does not require high random I/O performance.
  * It should be noted that it is easy to [increase the size](https://docs.coreweave.com/coreweave-kubernetes/storage#resizing) of a PVC as needed.
  * The workflow expects a default PVC name of `finetune-data`. This name can be changed once you are more comfortable with the workflow and configure it.
  * The below YAML file can be used to setup the PVC with `kubectl apply -f` if you prefer:

{% code title="finetune-data.yaml" %}
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

![Example finetune-data PVC configuration](<../.gitbook/assets/Screen Shot 2022-04-22 at 12.06.50 PM.png>)

The following components are optional, but may make your interaction easier:

* filebrowser
  * This allows you to share out and access your PVC using an easy application that lets you upload and download files and folders.
  * You can deploy the filebrowser over at the same[ Application Catalog](https://apps.coreweave.com/) that you used to deploy Argo Workflows.&#x20;
  * It is recommended that the name you give this filebrowser application be very short, or you will run into SSL CNAME issues. We recommend `finetune`.
  * Simply select the `finetune-data` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**
  * Some people may prefer to use a Virtual Server and interact with their PVC via ssh or other mechanism. This flexibility is one of the key advantages of CoreWeave.

![filebrowser application](<../.gitbook/assets/image (77) (1).png>)

## Dataset Setup

At this point, you should have a PVC set up that you can access via `filebrowser` or some other mechanism. For each dataset you want to use, you should create a directory or folder and give it a meaningful name. The workflow will however default to `dataset` as the directory to read the finetune dataset from.

The data should be individual **plaintext** files in the precise format that you want the prompt and responses to come in.

For example, we have a `western-romance` with novels in cleaned up and normalized plaintext format, with all extra whitespace cleaned up.

![western-romance dataset with text files for each novel.](<../.gitbook/assets/Screen Shot 2022-04-22 at 12.20.38 PM.png>)

The dataset will automatically be tokenized by a [`dataset_tokenizer`](https://github.com/wbrown/gpt\_bpe/blob/main/cmd/dataset\_tokenizer/dataset\_tokenizer.go) component written in `golang` as a step in the Argo Workflow. It is quite fast, and has different options for how to partition the data.

## Permissions Setup

To automatically create an `InferenceService`, the Argo Workflow job you submit needs special permissions. The below code block shows an example `ServiceAccount` and the corresponding permissions required. Copy the below into a file, `inference-role.yaml`.

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

Apply the permissions above by invoking `kubectl apply -f inference-role.yaml.`

## Getting and Running the Workflow

The [example code is available at GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/finetuner-workflow), and it is recommended that you use `git checkout` to pull down the latest copy of the code.

It includes the following files:

* `finetune-workflow.yaml` - the Argo Workflow itself
* `inference-role.yaml` - the role you set up earlier in this document
* `finetune-pvc.yaml` - Model storage volume as set up earlier in this document
* `finetuner/Dockerfile` - if you modify the `finetuner.py` code, you can use this Dockerfile to build your own finetuner image
* `finetuner/finetuner.py` - the simple reference example finetune training code
* `finetuner/ds_config.json` - the deepspeed configuration placed in the container. It is recommended that you not modify this.
* `finetuner/requirements.txt` - the Python requirements and versions; you can create a venv, but this is mainly for the `Dockerfile` build

For reference, a copy of the `finetune-workflow.yaml` is at the [bottom of this document](finetuning-machine-learning-models.md#undefined), but the GitHub repository has the authoritative version.

Assuming that you have grabbed the copy of `finetune-workflow.yaml`, we invoke Argo Workflows with:

{% code title="argo-submit-example" %}
```bash
$ argo submit finetune-workflow.yaml \
        -p run_name=example-gpt-j-6b \
        -p dataset=dataset \
        -p run_inference=true \
        -p model=EleutherAI/gpt-j-6B \
        --serviceaccount inference
```
{% endcode %}

Walking through the parameters given:

* `run_name` -- The only absolutely required parameter is `run_name`. It is strongly recommended that it be unique, as it is what is used to name the `InferenceService`. Consequentially, the `run_name` is required to meet DNS standards.
* `dataset` -- the name of the dataset directory on the PVC
* `run_inference` -- this explicitly tells the Workflow that we want to run a test inference service when this is done. It is not intended to be a production service, but to demonstrate end to end and to allow you to kick the tires on the finetuned model.
* `model` -- this example uses a Huggingface model identifier to pull down `gpt-j-6B`. This will be cached on subsequent runs on your PVC under `cache`.
* `--serviceaccount inference` is required for `run_inference` to work correctly

**NOTE:** There are easier ways to parameterize your jobs than the command line such as:

* Parameters file (`argo submit -f`, and use `-p` to customized further)
* Templating using [Helm Charts](https://helm.sh)
* Programmatically using the Argo Workflows API
* Using the Argo web UI

When you submit your job, you should see a screen that looks very much like the following:

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

At this point, we can observe the job via several mechanisms, now that we have our `Name` of `finetune-wtd2k`:

* `argo watch finetune-wtd2k`
  * this tells Argo that we want to watch the job as it goes through the stages of:
    * model-tokenization
    * model-finetune
    * model-inference

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

* `argo logs -f finetune-wtd2k` to watch the logs in real time. Pleae note that if it appears to hang on `Loading the model`, this is due to a bug in the terminal display code when it downloads and caches the model for the first time. You can simply kill the pod in question or the job, and resubmit it and it will display progress correctly.

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

During the finetuning, it will give you the time elapsed, and expected time to complete. It will also report checkpointing and loss reporting.

{% hint style="info" %}
You can instnatly watch a submitted workflow by using `argo submit --watch` when submitting
{% endhint %}

* Access your Argo Workflow application via HTTPS to see all the finetuner jobs and check on the status.&#x20;

![Argo Workflows HTTPS Request](<../.gitbook/assets/image (63) (1).png>)

## Workflow Options

This section covers what the author believes to be some of the more useful parametes. It is not intended to be a complete and exhaustive reference on all exposed parameters, as this is documented via comments in the workflow YAML file itself.

| Parameter        | Description                                                                                                                                                  | Default Value               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `run_name`       | The run name used to name artifacts and report metrics. Should be unique.                                                                                    | required option, no default |
| `pvc`            | The PVC to use for dataset and model artifacts                                                                                                               | `finetune-data`             |
| `region`         | The region to run the Argo jobs in. This generally should be `ORD1`.                                                                                         | `ORD1`                      |
| `dataset`        | The dataset folder relative to the `pvc` root.                                                                                                               | `dataset`                   |
| `model`          | The model to train on. It can be a relative path to the `pvc` root; if it can't be found, the finetuner will attempt to download the model from Huggingface. | `EleutherAI/gpt-neo-2.7B`   |
| `context`        | Training context size in tokens. Affects the tokenization proces as well.                                                                                    | `2048`                      |
| `epochs`         | The number of times the finetuner should train on the dataset.                                                                                               | `1`                         |
| `learn_rate`     | How quickly the model should learn the finetune data. Too high a learn rate can be counterproductive and replace the base model's training.                  | `5e-5`                      |
| `wandb_key`      | Strongly recommended. Use an API key from [http://wandb.ai](http://wandb.ai) to report on finetuning metrics with nice charts.                               |                             |
| `run_inference`  | Whether to run the example `InferenceService` on the finetuned model.                                                                                        | `false`                     |
| `inference_only` | Do **not** run the tokenization or finetune. Intended to quickly run only the `InferenceService` on a previously trained model.                              | `false`                     |

## Artifacts and Inference

When the model completes finetuning, you should find the model artifacts under a `{{pvc}}/{{run_name}}/final` directory. You can download the model at this point, or you can run the `InferenceService` on the model.

If you followed the directions for Inference Service, and[ installed the KNative client](https://github.com/knative/client/blob/main/docs/README.md), you should be able to get an URL by invoking `kn service list`.  Services can also be listed without the KNative Client by executing `kubectl get ksvc`

```
NAME                                              URL                                                                                                  LATEST                                      AGE     CONDITIONS   READY   REASON
inference-western-predictor-default               http://inference-western-predictor-default.tenant-goosewes-1.knative.chi.coreweave.com  
             inference-western-predictor-default-00007   2d21h   3 OK / 3     True
```

We can run CURL to do a test query (note that [this assumes you have `jq` installed](https://stedolan.github.io/jq/)):

```shell
curl http://inference-western-predictor-default.tenant-goosewes-1.knative.chi.coreweave.com/v1/models/final:predict \
     -H 'Content-Type: application/json; charset=utf-8' \
     --data-binary @- << EOF | jq .
{"parameters": {"min_length":150,
                "max_length":200},
 "instances": ["She danced with him in the honky-tonk"]}
EOF
```

This should yield a result similar to:

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

And now we have it -- taking a model and dataset through the tokenization and finetuning process to doing test inferences against the new model. This barely scratches the surface of finetuning, but CoreWeave hopes that this helps you get started.
