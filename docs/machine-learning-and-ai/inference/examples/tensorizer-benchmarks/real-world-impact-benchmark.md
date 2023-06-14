---
description: Compare Tensorizer using a real-world scenario
---

# Real World Impact Benchmark

This benchmark tutorial constructs two identical services, one leveraging [Tensorizer](../../tensorizer.md) and the other leveraging a Hugging Face transformer to serve GPT-J-6B.

Serving traffic using machine learning models for inference requires a trade-off between cost, accuracy and latency. The illustration below showcases how one can optimize these metrics by using Tensorizer.

<figure><img src="../../../../.gitbook/assets/Screenshot from 2023-06-14 10-29-11.png" alt="Venn diagram illustrating various trade-offs when optimizing metrics using Tensorizer"><figcaption></figcaption></figure>

{% hint style="success" %}
**Additional Resources**

To learn more about Tensorizer before embarking on this tutorial, check out our blog post, ["Decrease PyTorch Model Load Times with CoreWeave’s Tensorizer,"](https://coreweave.com/blog/coreweaves-tensorizer-decrease-pytorch-model-load-times) or [our slideshow presentation](https://docs.google.com/presentation/d/1o67YkRchVEszAesU\_xFFtNChwp9GWfGIJ6aIzi7cEOI/edit?usp=sharing) of the same title.
{% endhint %}

## Prerequisites

This guide presumes that `kubectl` and `python` are installed on the host system, and that the user has some basic familiarity with Kubernetes.

### Example source code

To follow along with this tutorial, first clone the source code from the CoreWeave GitHub repository:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/tensorizer-isvc" %}

## Deploy all resources

After cloning the source code, change directories to `tensorizer-isvc`. From this directory, provision the [Persistent Volume Claim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) defined in `pvc.yaml`:

```bash
$ kubectl apply -f pvc.yaml
```

Next, download the model to the newly deployed PVC by deploying the model download job located at `model-download/model-download-job.yaml`.

```bash
$ kubectl apply -f model-download/model-download-job.yaml
```

Now, run the Hugging Face `InferenceService` by deploying its manifest at `tensorizer_hf_isvc/kserve/hf-isvc.yaml`. In this example, [`kserve`](https://github.com/kserve/kserve) is used as the server.

```bash
$ kubectl apply -f tensorizer_hf_isvc/kserve/hf-isvc.yaml
```

Next, run the Tensorizer `InferenceService` by deploying the manifest at `tensorizer_hf_isvc/kserve/tensorizer-isvc.yaml`. In this example, `kserve` is once again used as the server.

```bash
$ kubectl apply -f tensorizer_hf_isvc/kserve/tensorizer-isvc.yaml
```

### Acquire the Inference Service's URL

View the `InferenceService` deployment's information to acquire its URL under the `URL` field using `kubectl get`:

```bash
$ kubectl get isvc
```

{% hint style="info" %}
**Note**

`http://` may be required instead of `https://` when connecting to the given URL.
{% endhint %}

## Test the `InferenceService`

The KServe services use [KServe's V1 protocol](https://kserve.github.io/website/0.10/modelserving/data\_plane/v1\_protocol/). The basic `POST` command below may be used to test the Service when served with KServe:

{% code overflow="wrap" %}
```bash
$ curl http://<URL>/v1/models/gptj:predict -X POST -H 'Content-Type: application/json' -d '{"instances": ["Hello!"]}'
```
{% endcode %}

The Flask services simply encode queries into the URL path component. The basic `curl` command below may be used to test the Service when served with Flask:

```bash
$ curl http://<URL>/predict/Hello%21
```

## Run the benchmark

Use `python` to run the benchmark test. The `load_test.py` test defaults to running async requests with [`aiohttp`](https://pypi.org/project/aiohttp/). In this case, KServe is used as the server:

{% code overflow="wrap" %}
```bash
$ python benchmark/load_test.py --kserve --url=<ISVC_URL> --requests=<NUMBER_OF_REQUESTS>
```
{% endcode %}

As an alternative to using [`requests`](https://pypi.org/project/requests/), the `--sync` option may be added to the command line to send requests sequentially.

## Delete the `InferenceService`

To remove the `InferenceService`, use `kubectl delete` to target the same manifest file applied earlier. For example:

```bash
$ kubectl delete -f tensorizer_hf_isvc/<...>/<...>-isvc.yaml
```

## `InferenceServer` containers

It is worth noting that each `InferenceService` manifest (those whose filenames end in `-isvc.yaml`) runs a container defined in a Dockerfile located in the same directory. For example, `tensorizer_hf_isvc/kserve/Dockerfile`.

These containers may be changed and rebuilt to customize the behavior of the `InferenceService`. The `build` context for each Dockerfile is its parent directory. Build commands are subsequently structured as follows:

```bash
$ docker build ./tensorizer_hf_isvc -f ./tensorizer_hf_isvc/kserve/Dockerfile
$ docker build ./tensorizer_hf_isvc -f ./tensorizer_hf_isvc/flask/Dockerfile
```

## Results

### RAM Usage

Tensorizer uses only enough RAM that is equal to the **size of the largest tensor** to load the model directly into GPU in 'Plaid' mode. As models get larger, the cost-effectiveness of using tensorizer becomes more prevalent since you do not have to load the entire model into CPU RAM before transferring it to the GPU. Therefore, scaling inference services during bursts of traffic minimizing cost for RAM.&#x20;

### Model load times

CoreWeave’s Tensorizer outperforms SafeTensors and Hugging Face for model load times on OPT-30B with [NVIDIA A100s](../../../../../coreweave-kubernetes/node-types.md).

Here, "model load times" refers to completely initializing the model from a checkpoint - not swapping in weights from a checkpoint to an already initialized model.

#### Smaller model metrics

CoreWeave’s Tensorizer outperforms SafeTensors and HuggingFace for model load times on GPT-J-6B with NVIDIA A40s.

<figure><img src="../../../../.gitbook/assets/image (6).png" alt="Graph displaying Tensorizer smaller model load times compared to SafeTensors and Hugging Face."><figcaption></figcaption></figure>

#### Larger model metrics

CoreWeave’s Tensorizer outperforms SafeTensors and HuggingFace for model load times on OPT-30B with NVIDIA A100s.

<figure><img src="../../../../.gitbook/assets/image.png" alt="Graph displaying Tensorizer larger model load times compared to SafeTensors and Hugging Face."><figcaption></figcaption></figure>

### Handling burst requests

In CoreWeave's tests of Tensorizer's performance, CoreWeave’s Tensorizer presented **approximately five times faster** average latency over the burst in requests, and required fewer Pod spin-ups compared to Hugging Face.&#x20;

The burst involved 100 concurrent requests on GPT-J using NVIDIA A40s.

In these results, the data shown reflects how the `InferenceService` scaled from `1` idle GPU with zero requests to `100` requests sent at once. the `InferenceService` ran on [NVIDIA A40s](../../../../../coreweave-kubernetes/node-types.md).

<figure><img src="../../../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

The average latency per request is `0.43s` for Tensorizer end-to-end inference on GPT-Jm, as compared to `2.45` seconds. Tensorizer provides cost effectiveness, lower latency and minimal RAM usage as model size gets larger.
