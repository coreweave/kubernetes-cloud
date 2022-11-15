---
description: Launch a GPT DeepSpeed model using DeterminedAI on CoreWeave Cloud
---

# Launching GPT DeepSpeed Models using DeterminedAI

DeepSpeed is an [open source](https://en.wikipedia.org/wiki/Open\_source) [deep learning](https://en.wikipedia.org/wiki/Deep\_learning) optimization library for [PyTorch](https://en.wikipedia.org/wiki/PyTorch) optimized for low latency, high throughput training, and is designed to reduce compute power and memory use for the purpose of training large distributed models.

In the example below, a minimal GPT-NeoX DeepSpeed distributed training job is launched without the additional features such as tracking, metrics, and visualization that DeterminedAI offers.&#x20;

{% hint style="info" %}
**Note**

This guide makes several assumptions:\
\
• You have [set up the CoreWeave Kubernetes environment](../../coreweave-kubernetes/getting-started.md).\
• You have some experience launching and using [DeterminedAI on CoreWeave Cloud](https://www.determined.ai). (If you have not done so already, it is recommended to [deploy DeterminedAI via the application Catalog](https://apps.coreweave.com/) to familiarize yourself with it).\
• You have `git` installed on your terminal.
{% endhint %}

## Setup

### Clone the files

To follow along with this example, first clone the [the CoreWeave GPT DeepSpeed repository](https://github.com/coreweave/gpt-det-deepseed) locally:

```bash
$ git clone --recurse-submodules https://github.com/coreweave/gpt-det-deepseed.git
```

### Install DeterminedAI

To install DeterminedAI, log in to your CoreWeave Cloud account and navigate to the applications Catalog. From here, search for and locate the DeterminedAI application. Click into it to configure the instance from the deployment screen, then deploy the instance into your cluster by clicking the **Deploy** button.

Once the instance is shown as `Ready`, you may proceed with the experiment.

In the configuration file `gpt_neox_config/small.yml`, change the `vocab_path`, `data_path` `load`, and `save` parameters to the appropriate paths.

### The launcher configuration file

The launcher configuration file provided in this demo (`launcher.yml`) exposes the overall configuration parameters for the experiment**.**

{% hint style="info" %}
**Note**

DeterminedAI uses its own fork of DeepSpeed, so using [that image](https://github.com/determined-ai/environments/blob/master/Makefile#L322) is recommended.
{% endhint %}

```yaml
   image:
      gpu: liamdetermined/gpt-neox
```

&#x20;In this example, we're using a wrapper around DeepSpeed called `determined.launch.deepspeed` in order to allow for safe handling of note failure and shutdown.

```yaml
entrypoint:
   - python3
   - -m
   - determined.launch.deepspeed
```

### Mount path for host file

In `train_deepspeed_launcher.py` , the default mount path is defined as:

```
shared_hostfile = "/mnt/finetune-gpt-neox/hostfile.txt"
```

Configure this hostfile path to your mount path.

### Dockerfile

The Dockerfile provided in this experiment is used to build the Docker image used to run the experiment in the cluster. The image may be manually built if customizations are desired.

The Dockerfile uses the following:

* Python 3.8&#x20;
* PyTorch 1.12.1
* CUDA 11.6

<details>

<summary>Click to Expand - Example Dockerfile</summary>

{% code overflow="wrap" %}
```docker
FROM coreweave/nccl-tests:2022-09-28_16-34-19.392_EDT

ENV DET_PYTHON_EXECUTABLE="/usr/bin/python3.8"
ENV DET_SKIP_PIP_INSTALL="SKIP"

# Run updates and install packages for build
RUN echo "Dpkg::Options { "--force-confdef"; "--force-confnew"; };" > /etc/apt/apt.conf.d/local
RUN apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    add-apt-repository universe && \
    apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl tzdata build-essential daemontools && \
    apt-get install -y --no-install-recommends \
       python3.8 \
       python3.8-distutils \
       python3.8-dev \
       python3.8-venv \
       git && \
    apt-get clean

# python3.8 -m ensurepip --default-pip && \
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install --no-cache-dir --upgrade pip

ARG PYTORCH_VERSION=1.12.1
ARG TORCHVISION_VERSION=0.13.1
ARG TORCHAUDIO_VERSION=0.12.1
ARG TORCH_CUDA=116
ARG TORCH_INDEX=whl

RUN python3.8 -m pip install --no-cache-dir install torch==${PYTORCH_VERSION}+cu${TORCH_CUDA} \ 
        torchvision==${TORCHVISION_VERSION}+cu${TORCH_CUDA} \
        torchaudio==${TORCHAUDIO_VERSION}+cu${TORCH_CUDA} \
        --extra-index-url https://download.pytorch.org/${TORCH_INDEX}/cu${TORCH_CUDA}

RUN python3.8 -m pip install --no-cache-dir install packaging

RUN mkdir -p /tmp/build && \
        cd /tmp/build && \
        git clone https://github.com/NVIDIA/apex && \
        cd apex && \
        python3.8 -m pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./ && \
        cd /tmp && \
        rm -r /tmp/build

#### Python packages
RUN python3.8 -m pip install --no-cache-dir determined==0.19.2
COPY requirements/requirements.txt .
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt
COPY requirements/requirements-onebitadam.txt .
RUN python3.8 -m pip install --no-cache-dir -r requirements-onebitadam.txt
COPY requirements/requirements-sparseattention.txt .
RUN python3.8 -m pip install -r requirements-sparseattention.txt
RUN python3.8 -m pip install --no-cache-dir pybind11
RUN python3.8 -m pip install --no-cache-dir protobuf==3.19.4
RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 2
RUN echo 2 | update-alternatives --config python
```
{% endcode %}

</details>

### Launch the experiment

To run the experiment, invoke `det experiment create` from the root of the cloned repository.

```bash
$ det experiment create core_api.yml . 
```

### Logging

Logs for this experiment may be tracked using the DeterminedAI Web UI, but metrics may also be visualized using [Weights & Biases (WandB)](https://wandb.ai/site). To use WandB, pass your WandB API key to an environment variable called `WANDB_API_KEY`, or else modify the function `get_wandb_api_key()` in `deepy.py` to return your API Token.

{% hint style="warning" %}
**Important**

To configure your DeepSpeed experiment to run on multiple nodes, you can change the `slots_per_trail` option with the number of GPUs you require. The maximum number of GPUs per node on CoreWeave is `8`, so the experiment will become multi-node once it reaches this threshold.
{% endhint %}
