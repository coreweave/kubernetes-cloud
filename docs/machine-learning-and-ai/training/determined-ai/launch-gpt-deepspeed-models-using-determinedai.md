---
description: Launch a GPT DeepSpeed model using Determined AI on CoreWeave Cloud
---

# Launch GPT DeepSpeed Models using Determined AI

DeepSpeed is an [open-source](https://en.wikipedia.org/wiki/Open\_source) [deep learning](https://en.wikipedia.org/wiki/Deep\_learning) library for [PyTorch](https://en.wikipedia.org/wiki/PyTorch) optimized for low latency and high throughput training, designed to reduce compute power and memory required to train large distributed models.

In the example below, a minimal GPT-NeoX DeepSpeed distributed training job is launched without the additional features such as tracking, metrics, and visualization that Determined AI offers.&#x20;

## Prerequisites

Before following this guide, you should have some experience with [Determined AI on CoreWeave Cloud](https://www.determined.ai) and:

* a [CoreWeave Kubernetes environment](../../../coreweave-kubernetes/getting-started.md)
* deployed the [Determined AI application](https://apps.coreweave.com/)
* `git` installed on your terminal

If you are new to Determined, see the [Quickstart guide](https://docs.determined.ai/latest/quickstart-mdldev.html).

## Setup

### Clone the repository

To follow along with this example, first clone the [the CoreWeave GPT DeepSpeed repository](https://github.com/coreweave/gpt-det-deepseed) to your workstation:

```bash
$ git clone --recurse-submodules https://github.com/coreweave/gpt-det-deepseed.git
```

### Install Determined AI

[Follow the steps to install the Determined AI application](../../../compass/determined-ai/install-determined-ai.md).

Then, in `gpt_neox_config/small.yml`, change these values to the appropriate paths:

* `vocab_path`
* `data_path`&#x20;
* `load`
* `save`&#x20;

### The launcher configuration file

The `launcher.yml` configuration file provided in this demo exposes the overall configuration parameters for the experiment**.**

{% hint style="info" %}
**Note**

Determined AI uses its own fork of DeepSpeed, so using [that image](https://github.com/determined-ai/environments/blob/master/Makefile#L322) is recommended.
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

The Dockerfile provided in this experiment is used to build the Docker image needed to run the experiment in the cluster. The image may be manually built if customizations are desired.

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

You can track logs for this experiment using the Determined AI web UI, and visualize metrics using [Weights & Biases (WandB)](https://wandb.ai/site). To use WandB, pass your WandB API key to an environment variable called `WANDB_API_KEY`, or modify the function `get_wandb_api_key()` in `deepy.py` to return your API Token.

{% hint style="warning" %}
**Important**

To configure your DeepSpeed experiment to run on multiple nodes, change the `slots_per_trail` option to the number of GPUs you require. The maximum number of GPUs per node on CoreWeave is `8`, so the experiment will become multi-node once it reaches this threshold.
{% endhint %}
