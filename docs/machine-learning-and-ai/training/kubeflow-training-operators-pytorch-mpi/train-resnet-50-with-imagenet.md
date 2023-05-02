---
description: >-
  Use Kubeflow training operators to perform distributing training of the
  popular ResNet-50 model.
---

# Train ResNet-50 with ImageNet

Originally published in 2015, [the ResNet model architecture](https://arxiv.org/abs/1512.03385) achieved state-of-the-art results on image classification datasets such as [ImageNet](https://en.wikipedia.org/wiki/ImageNet). Since then, both ResNet and ImageNet have been used in numerous papers to test the performance of large scale training techniques, such as the [Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour paper](https://arxiv.org/abs/1706.02677).

In this example, we'll use the [`torchvision` library](https://pytorch.org/vision/stable/index.html) along with multiple [Kubeflow training operators ](./)to perform distributed training of ResNet-50 on ImageNet.

## Source code

Throughout the rest of this document, referenced files may be found in CoreWeave's `kubernetes-cloud` repo in the `kubeflow/training-operator/resnet50` folder.

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/kubeflow/training-operator/resnet50" %}
Link to the source code referenced in this example
{% endembed %}

In this folder, there are two Python files, two Docker files, and one folder named `k8s/`.

The Python files implement the training scripts for [the PyTorch and MPI Operators](train-resnet-50-with-imagenet.md#kubeflow-training-operators). The Dockerfiles create the respective images used by the Training Operators. Finally, the `k8s/` folder contains all of the YAML files that define the Kubernetes resources needed to run this example on CoreWeave Cloud.

### Util script

Since both training operators are using PyTorch as the framework, the common functions are reused and located in `util.py`. This common functionality includes the training and test loops, along with loading the ImageNet dataset.

### PyTorch Operator Training script

The training script that will be used by the [PyTorch Operator](train-resnet-50-with-imagenet.md#pytorch-operator) is in `resnet50_pytorch.py`.

The model definition, train loop, and test loop are all standard for PyTorch. The important pieces that set up distributed training are found in the `main` function.

First, the distributed backend is initialized. This is where the distribution strategy is told which backend to use:

{% code overflow="wrap" %}
```python
if should_distribute():
    print('Using distributed PyTorch with {} backend'.format(args.backend))
    dist.init_process_group(backend=args.backend)
    print(f"Current rank: {dist.get_rank()}\tlocal rank: {LOCAL_RANK}\ttotal world size:  {dist.get_world_size()}")
```
{% endcode %}

{% hint style="info" %}
**Note**

This script is run by each device used in distributed training. A process's "rank" is a unique integer ranging from `0` to the world size. The world size is the total number of processes that are part of the distributed training. The local rank maps a process to the GPU on the device it's running on.
{% endhint %}

Next, the model is wrapped with a [Distributed Data Parallel](https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html#distributeddataparallel) object. This allows you to treat the model the same way as you would for non-distributed training within the training and test loops. Once the model is wrapped, it will distribute actions across all instances of the model like computing an output on a batch of data.

{% code overflow="wrap" %}
```python
if is_distributed():
    model = nn.parallel.DistributedDataParallel(model)
```
{% endcode %}

Following the [linear scaling rule](train-resnet-50-with-imagenet.md#data-parallelism), the learning rate is also scaled by the number of processes:

{% code overflow="wrap" %}
```python
lr_scaler = dist.get_world_size() if is_distributed() else 1
optimizer = optim.SGD(model.parameters(), lr=args.lr * lr_scaler, momentum=args.momentum)
```
{% endcode %}

When the training and test loops are completed, the model checkpoint needs to be saved. Since the script is being run synchronously across multiple devices, the saving of a checkpoint requires special logic. This prevents each process from trying to save a checkpoint into the same file. Saving the checkpoint is reserved for the "root" process, which will always have a rank of `0`.

{% code overflow="wrap" %}
```python
if args.model_dir and dist.get_rank() == 0:
    args.model_dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), args.model_dir / "mnist_cnn.pt")
```
{% endcode %}

### MPI Operator Training script

The training script that will be used by the [MPI Operator](train-resnet-50-with-imagenet.md#mpi-operator) is in `resnet50_horovod.py`.

This script also uses PyTorch as its framework, but utilizes [Horovod](https://horovod.ai/) to handle distribution.

{% hint style="info" %}
**Additional Resources**

Refer to the [Horovod with PyTorch](https://horovod.readthedocs.io/en/stable/pytorch.html) documentation for a general overview of adding Horovod to PyTorch scripts.
{% endhint %}

Like the PyTorch script, the model definition, train loop, and test loop are standard PyTorch implementations. The set up with Horovod is very similar to setting up PyTorch's `torch.distributed`.&#x20;

First, the distribution strategy is initialized:

{% code overflow="wrap" %}
```python
hvd.init()
```
{% endcode %}

Next, the optimizer is created with its learning rate scaled by the world size.

{% hint style="info" %}
**Note**

Horovod and this training script support using [AdaSum](https://horovod.readthedocs.io/en/stable/adasum\_user\_guide\_include.html), a novel algorithm for gradient reduction that eliminates the need to follow the Linear Scaling Rule.
{% endhint %}

After the model and optimizer are created, it must be broadcast to all the different processes. This is required to ensure that all of the workers have consistent initialization at the beginning of training.

```python
hvd.broadcast_parameters(model.state_dict(), root_rank=0)
hvd.broadcast_optimizer_state(optimizer, root_rank=0)
```

The last thing that must be created before starting the training loop is Horovod's `DistributedOptimizer`.

```python
optimizer = hvd.DistributedOptimizer(optimizer,
                                     named_parameters=model.named_parameters(),
                                     compression=compression,
                                     op=hvd.Adasum if args.use_adasum else hvd.Average,
                                     gradient_predivide_factor=args.gradient_predivide_factor)
```

### Dockerfiles

In order to run the training scripts from the Kubeflow Training Operators, the Operators must be containerized, for which we will use Docker. The Dockerfiles for the PyTorch and MPI Operators are found in the `Dockerfile.pytorch` and `Dockerfile.mpi` files, respectively.

Both Dockerfiles use [NVIDIA's PyTorch Docker image](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch). This Docker image comes with many of the necessary libraries preinstalled, including [NVIDIA NCCL](https://developer.nvidia.com/nccl), [CUDA](https://developer.nvidia.com/cuda-toolkit), and [OpenMPI](https://www.open-mpi.org/).&#x20;

### PyTorch Operator YAML

The `PyTorchJob` Kubernetes resource is defined in `k8s/imagenet-pytorchjob.yaml`.

Within this resource definition, there are two important `specs`: the `master` and the `worker`. The container defined by the `master` spec will be the process with a rank of `0`, also referred to as the `root`.

The PyTorch Job will also set up all the environment variables that are needed by `torchrun` and `dist` to set up distributed training. `MASTER_ADDR` and `MASTER_PORT` will point at the pod defined by the master spec.

In this example, the `master` and `worker` containers all run the same script using the same arguments. Both containers take the resources of an entire node, which includes 8 GPUs. The `torchrun` command is used to spawn one process per GPU on that container.

A shared PVC is also attached to all the containers, so that the dataset can be accessed by all the workers.

{% hint style="info" %}
**Note**

If you want to scale up the number of GPUs used for distributed training, all you would need to do is increase the number of worker replicas.
{% endhint %}

### MPI Operator YAML

The `MPIJob` Kubernetes resource is defined in `k8s/imagenet-mpijob.yaml`.

Similarly to the `PyTorchJob`, the `MPIJob` defines a `Launcher` and a `Worker` spec. However, there is one main difference between the specs found in `MPIJob` and those found in `PyTorchJob`.

`MPIJob` uses an `mpirun` command in the `launcher`, but no commands in the `worker` containers. This is because the `launcher` container is used to orchestrate the running of the workers, and will connect to the `worker` containers to run the training script.

{% hint style="info" %}
**Note**

The `launcher` container has low resource requests with no GPU, since it will not be running any of the actual training.
{% endhint %}

Like the `PyTorchJob`, scaling up the number of GPUs used with the `MPIJob` can be done by increasing the number of workers. When doing this, the value for the total number of processes will always need to be updated in the `mpirun` command used on the `launcher` container. This value is passed using the `-np` flag.

## Setup

{% hint style="info" %}
**Note**

This guide assumes that you have already followed the process to set up the CoreWeave Kubernetes environment. If you have not done so already, [follow our Getting Started guide](../../../coreweave-kubernetes/getting-started.md) before proceeding with this guide.
{% endhint %}

### PVC

A PVC storage volume will be used to store the dataset and model checkpoints. The PVC is defined in `k8s/pvc.yaml`. Use `kubectl` to deploy it:

```bash
kubectl apply -f k8s/pvc.yaml
```

#### FileBrowser (Optional)

This application allows you to share out and access your PVC using an easy application that lets you upload and download files and folders. You can find and deploy the Filebrowser application from the [application Catalog](https://apps.coreweave.com/?\_gl=1\*mundfp\*\_ga\*Nzk1MzkwNjE3LjE2NzEwNTA1OTk.\*\_ga\_XKNHS53VYL\*MTY3Mjc3NTc1Ni43NC4xLjE2NzI3NzU3NTcuMC4wLjA.) on CoreWeave Cloud.

It is recommended that the name you give the Filebrowser application be very short, or you will run into SSL CNAME issues. We recommend using the name `kubeflow`.

When configuring the application instance, select the `kubeflow-mnist` PVC that you created earlier. **Make sure that you actually add your PVC to the filebrowser list of mounts!**

<figure><img src="../../../.gitbook/assets/image (7) (3) (2).png" alt=""><figcaption><p>The filebrowser application</p></figcaption></figure>

### Docker images

Each of the training operators require their respective Docker image to be built and pushed.

{% hint style="warning" %}
**Important**

The default Docker tag is `latest`. Using this tag is **strongly** **discouraged**, as containers are cached on the nodes and in other parts of the CoreWeave stack. Always use a unique tag, and never push to the same tag twice. Once you have pushed to a tag, **do not** push to that tag again.
{% endhint %}

Below, we use simple versioning by using the tag `1` for the first iteration of the image.

{% hint style="info" %}
**Note**

When running the following commands, be sure to replace the example `username` with your Docker Hub `username.`
{% endhint %}

To build and push the two images, run the following commands:

```bash
docker login
export DOCKER_USER=<replace with your dockerhub username>
docker build -t $DOCKER_USER/pytorch_dist_resnet50:1 -f Dockerfile.pytorch .
docker build -t $DOCKER_USER/pytorch_mpi_resnet50:1 -f Dockerfile.mpi .
docker push $DOCKER_USER/pytorch_dist_resnet50:1
docker push $DOCKER_USER/pytorch_mpi_resnet50:1
```

{% hint style="info" %}
**Note**

This example assumes a public Docker registry. To use a private registry, an [`imagePullSecret` ](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)must be defined.
{% endhint %}

## Secrets

### Kaggle secret

The ImageNet dataset is publicly available via a [Kaggle Object Localization Challenge](https://www.kaggle.com/c/imagenet-object-localization-challenge). To download the dataset using the[ Kaggle CLI](https://github.com/Kaggle/kaggle-api), first [create a Kaggle account](https://www.kaggle.com/account/login?phase=startRegisterTab\&returnUrl=%2Fc%2Fimagenet-object-localization-challenge).

After you have signed in to your new account, navigate to the [Kaggle competition](https://www.kaggle.com/competitions/imagenet-object-localization-challenge/data) and accept the competition rules. When all of that is done, you should be be able to see a sample of the data in your browser:

<figure><img src="../../../.gitbook/assets/image (6) (5).png" alt="Preview of ImageNet data from Kaggle"><figcaption><p>Preview of ImageNet data from Kaggle</p></figcaption></figure>

Once your Kaggle account has access to the ImageNet dataset, create an API token by navigating to your profile page (`https://www.kaggle.com/<username>/account`). Click "Create API Token." This will trigger a download of a file named `kaggle.json`.

Next, retrieve the `key` value in `kaggle.json`, encode it using base64, then copy the encoded value into `k8s/kaggle-secret.yaml`.

```bash
$ cat kaggle.json
{"username":"navarreprattcw","key":"example-key-1234"}

$ echo -n "example-key-1234" | base64
ZXhhbXBsZS1rZXktMTIzNA==
```

When complete, your `k8s/kaggle-secret.yaml` should look similar to the following.

```yaml
apiVersion: v1
data:
  token: ZXhhbXBsZS1rZXktMTIzNA==
kind: Secret
metadata:
  name: kaggle-token-secret
type: Opaque
```

Apply the changed manifest to the cluster using `kubectl`:

```bash
kubectl apply -f k8s/kaggle-secret.yaml
```

### Weights and Biases secret

{% hint style="info" %}
**Note**

This is optional for this tutorial.
{% endhint %}

[Weights and Biases](https://wandb.ai/site) is a popular MLOps platform that helps track and visualize machine learning experiments.

If you would like to log metrics using Weights and Biases during this tutorial, then you will need to create a secret containing your wandb account token. To find your token, [log in to your Weights and Biases account](https://wandb.auth0.com/login?state=hKFo2SByMEtYV3JMMFY3ekpWSFlrRXNOX3lKTDhpMWFJRzh1NaFupWxvZ2luo3RpZNkgQlNFYV9vUXZoVEU5Z1ZSRlRKNmhxMXhIUkhUU2hGbXijY2lk2SBWU001N1VDd1Q5d2JHU3hLdEVER1FISUtBQkhwcHpJdw\&client=VSM57UCwT9wbGSxKtEDGQHIKABHppzIw\&protocol=oauth2\&nonce=VG9EN21BWUlleVhwUWVnUQ%3D%3D\&redirect\_uri=https%3A%2F%2Fapi.wandb.ai%2Foidc%2Fcallback\&response\_mode=form\_post\&response\_type=id\_token\&scope=openid%20profile%20email), then navigate to [https://wandb.ai/authorize](https://wandb.ai/authorize).

Encode your token using Base64, copy it into `k8s/wandb-secret.yaml` , and apply it to the cluster.

```bash
$ echo -n "example-wanbd-token" | base64
ZXhhbXBsZS13YW5kYi10b2tlbg==
```

When complete, your `k8s/kaggle-secret.yaml` should look similar to the following.

```yaml
apiVersion: v1
data:
  token: ZXhhbXBsZS13YW5kYi10b2tlbg==
kind: Secret
metadata:
  name: wandb-token-secret
type: Opaque
```

Apply the changed manifest to the cluster using `kubectl`:

```bash
kubectl apply -f k8s/wandb-secret.yaml
```

### Downloading the dataset

Downloading all of the required files for the ImageNet dataset is done by a Kubernetes job defined in `k8s/imagenet-download-job.yaml`.

This job uses the Kaggle secret to download the dataset via the Kaggle CLI directly into the PVC that was just created.

{% hint style="warning" %}
**Important**

The Kaggle token will be used from the secret, but the `username` needs to be updated in `k8s/imagenet-download-job.yaml`on line 29.
{% endhint %}

&#x20;Once the Kaggle username is updated, start the job using `kubectl`:

```bash
kubectl apply -f k8s/imagenet-download-job.yaml
```

## Running distributed training

Before running the Training Operators, replace the Docker image names in the YAML configuration files with the images that were just built and pushed.

You may either manually edit the files, or do so using `sed` by running the following commands:

{% code overflow="wrap" %}
```bash
sed -ri "s/^(\s*)(image\s*:\s*navarrepratt\/pytorch_dist_resnet50:1\s*$)/\1image: $DOCKER_USER\/pytorch_dist_resnet50:1/" k8s/imagenet-pytorchjob.yaml

sed -ri "s/^(\s*)(image\s*:\s*navarrepratt\/pytorch_mpi_resnet50:1\s*$)/\1image: $DOCKER_USER\/pytorch_mpi_resnet50:1/" k8s/imagenet-mpijob.yaml
```
{% endcode %}

{% hint style="info" %}
**Note**

If you are not using Weights and Biases, you must remove the two Weights and Biases flags in the command for all of the containers.
{% endhint %}

### PyTorch Operator

Deploy the `PyTorchJob` using `kubectl`:

```bash
kubectl apply -f k8s/imagenet-pytorchjob.yaml
```

Once it is created, you can view information about it using `kubectl get`:

```bash
$ kubectl get pytorchjob

NAME                      STATE     AGE
pytorch-dist-mnist-nccl   Created   52s
```

You can use `kubectl get pods` to watch the Pods start up and run:

```bash
$ kubectl get pods -w -l job-name=imagenet-pytorch

NAME                        READY   STATUS      RESTARTS   AGE
imagenet-pytorch-master-0   0/1     Completed   0          2m55s
imagenet-pytorch-worker-0   0/1     Completed   0          2m55s
```

Use `kubectl logs` to view logs for any of the Pods:

```bash
kubectl logs -f imagenet-pytorch-master-0
```

The model checkpoint will be saved to the PVC at the path `kubeflow-resnet50/pytorch/checkpoints/resnet50_imagenet.pt`.

### MPI Operator

Use `kubectl` to deploy the `MPIJob` resource:

```bash
kubectl apply -f k8s/imagenet-mpijob.yaml
```

Once it is created, you can view information about it using `kubectl get`:

```bash
$ kubectl get mpijob
                               
NAME                    AGE
imagenet-16gpu-mpijob   3s
```

You can use `kubectl get pods` to watch the Pods start up and run:

```bash
$ kubectl get pods -w -l training.kubeflow.org/job-name=imagenet-16gpu-mpijob

NAME                                   READY   STATUS              RESTARTS   AGE
imagenet-16gpu-mpijob-launcher-6cd4n   0/1     ContainerCreating   0          2m4s
imagenet-16gpu-mpijob-worker-0         1/1     Running             0          2m4s
```

{% hint style="info" %}
**Note**

You might see the `launcher` pod fail a couple of times if the `worker` pod is still starting up. This is an expected race condition which often happens if the Docker image is already cached on the launcher machine, causing it to start up much more quickly. Once the `worker` pod is fully created, the launcher will be able to communicate with it via SSH.
{% endhint %}

To follow the logs, run the following command:

```bash
$ kubectl logs -l job-name=imagenet-16gpu-mpijob-launcher -f
```

The model checkpoint will be saved to the PVC at the path `kubeflow-mnist/mpi/checkpoints/resnet50_imagenet.pt`.

## Performance Analysis

Using the chart's created on Weights and Biases we can analyze the scaling efficiencies of both of the training operators.

{% hint style="info" %}
**Note**

The hyperparameters used haven't been properly tuned to produce a "state of the art" version of ResNet-50. TorchVision publishes "training recipes" for their pretrained weights. You can see all the hyperparameters they used for ResNet-50 [here](https://pytorch.org/blog/how-to-train-state-of-the-art-models-using-torchvision-latest-primitives/#the-training-recipe).
{% endhint %}

The data in the chart below shows samples per second numbers throughout 3 epochs of training on **each** GPU. This means that the total samples per second is the value shown in the chart times the number of GPUs used. Each line represents a different combination of PytorchJob and MPIJob and half-full A40 nodes (8 and 16 GPUs).

<figure><img src="../../../.gitbook/assets/image (7) (1) (2).png" alt=""><figcaption><p>Training throughput for distributed training with the kubeflow training operators</p></figcaption></figure>

As you can see, the per-GPU throughput hardly drops when moving to two nodes. This means the total throughput is almost doubled when using twice as many GPUs. You can expect the scaling efficiency to decrease as you increase the model size and total number of GPUs.

[Horovod's own benchmarks](https://horovod.readthedocs.io/en/stable/benchmarks.html) report a 90% scaling efficiency when scaling up to 512 total GPUs when training ResNet-101.

{% hint style="info" %}
**Note**

Training with 8 GPUs has twice as many steps in the above chart because during each step only `8 * 256` images are processed. When training with 16 GPUs, two times as many images are processed in each batch.
{% endhint %}

## Clean up

Once you are finished with everything, you can delete all resources using the `kubectl delete` command:

```bash
kubectl delete -R -f k8s/
```

{% hint style="info" %}
**Note**

If you created the optional Filebrowser application, you will need to delete it via the CoreWeave Cloud Applications page **before** the PVC can be deleted.
{% endhint %}
