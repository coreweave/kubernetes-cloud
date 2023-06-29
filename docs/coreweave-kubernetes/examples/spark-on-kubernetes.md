---
description: >-
  Run Spark workloads on CoreWeave using spark-submit, or interactively from
  JupyterLab.
---

# Spark on Kubernetes

[Apache Spark ](https://spark.apache.org/)is a popular multi-language engine designed for executing distributed workloads. It is often used for data processing tasks, such as preparing data for training machine learning models.

This guide demonstrates how to use Spark in cluster mode and interactively in client mode through a Jupyter notebook, with PySpark serving as the backend for the [`img2dataset`](https://github.com/rom1504/img2dataset) tool. This tool will be used to download and process large, publicly available image datasets. For an in-depth explanation of all the features available, please visit Sparks's [Running on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html) documentation.

## Prerequisite steps

Before proceeding with this guide, complete the following two steps: first, verify that your Kubernetes configuration is set up correctly, and second, clone the source code repository from GitHub.

### 1. Configure Kubernetes

Complete account creation details are found in [Cloud Account and Access](../../welcome-to-coreweave/getting-started.md).

1. Install `kubectl`.
2. [Create an API token](https://cloud.coreweave.com/api-access), and download the Kubeconfig.
3. [Install](../../welcome-to-coreweave/getting-started.md#i-do-not-have-a-.kube-config-file) the new Kubeconfig, or [merge it with your existing one](../../welcome-to-coreweave/getting-started.md#i-have-an-existing-kubeconfig-file).
4.  Set your Kubernetes context to `coreweave.`

    ```
    $ kubectl config set-context coreweave
    ```
5.  Verify your configuration by checking your Kubernetes secrets.

    ```
    $ kubectl get secret
    ```

If the `kubectl` command returns any security tokens, your configuration is ready to go.&#x20;

### 2. Clone the source code repository

Clone the `coreweave/kubernetes-cloud` repository to your local workstation, then change to the `spark` [directory](https://github.com/coreweave/kubernetes-cloud/tree/master/spark).

{% hint style="info" %}
**Important**

If you've previously cloned this repository when working on other CoreWeave projects, make sure to pull the latest version of the `master` branch.&#x20;
{% endhint %}

<pre class="language-bash"><code class="lang-bash"><strong>git clone https://github.com/coreweave/kubernetes-cloud.git
</strong>cd kubernetes-cloud/spark
</code></pre>

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/spark" %}
See the `spark` directory in `kubernetes-cloud`
{% endembed %}

## Get started

Before running the Spark jobs, you need to:&#x20;

* Create a shared filesystem called a PVC (Persistent Volume Claim)
* Deploy your Weights and Biases Secret
* Create a ServiceAccount

### Create the PVC

The PVC is a shared, 400Gi NVMe drive used to store the downloaded datasets. Create it by applying the `spark-pvc.yaml` manifest, found in the `spark` project folder.&#x20;

```bash
kubectl apply -f spark-pvc.yaml
```

### Deploy the Weights and Biases Secret

The `img2dataset` code will log metrics to Weights and Biases. To enable this, you must deploy a WandB auth token as a Kubernetes secret.&#x20;

First, find your token by [logging in to your Weights and Biases account](https://wandb.auth0.com/login?state=hKFo2SByMEtYV3JMMFY3ekpWSFlrRXNOX3lKTDhpMWFJRzh1NaFupWxvZ2luo3RpZNkgQlNFYV9vUXZoVEU5Z1ZSRlRKNmhxMXhIUkhUU2hGbXijY2lk2SBWU001N1VDd1Q5d2JHU3hLdEVER1FISUtBQkhwcHpJdw\&client=VSM57UCwT9wbGSxKtEDGQHIKABHppzIw\&protocol=oauth2\&nonce=VG9EN21BWUlleVhwUWVnUQ%3D%3D\&redirect\_uri=https%3A%2F%2Fapi.wandb.ai%2Foidc%2Fcallback\&response\_mode=form\_post\&response\_type=id\_token\&scope=openid%20profile%20email) and navigating to [https://wandb.ai/authorize](https://wandb.ai/authorize).

Then, encode your token with `base64`:

```bash
$ echo -n "example-wanbd-token" | base64
ZXhhbXBsZS13YW5kYi10b2tlbg==
```

Next, copy the token into `wandb-secret.yaml`. When complete, it should look similar to this:

```yaml
apiVersion: v1
data:
  token: ZXhhbXBsZS13YW5kYi10b2tlbg==
kind: Secret
metadata:
  name: wandb-token-secret
type: Opaque
```

Finally, apply the updated manifest to the cluster with `kubectl`:

```bash
kubectl apply -f wandb-secret.yaml
```

### Create the ServiceAccount

Because Spark runs on Kubernetes, it needs permission to manage its resources. For instance, Spark uses Pods as executors, so it needs the necessary permissions to deploy and delete them.&#x20;

The required ServiceAccount, Role, and RoleBinding are defined in the `spark-role.yaml` manifest. Apply it to your namespace with `kubectl`:

```
kubectl apply -f spark-role.yaml
```

## About the different modes

You can launch your Spark job in cluster mode, or in client mode.&#x20;

* Cluster mode requires Spark installed locally on your workstation. If you don't already have Apache Spark installed, follow the instructions on the [download page](https://spark.apache.org/downloads.html) to install the latest version pre-built for Apache Hadoop.
* Client mode does not require Spark installed locally.

We'll explain both methods.

## Use cluster mode

In cluster mode the Spark driver is deployed as a Pod alongside the executors. You'll use `spark-submit`, located in `$SPARK_HOME/bin`, to launch the job. We've provided an example submit command in the project directory as `example-spark-submit.sh`.&#x20;

### Spark Configuration

Spark jobs use many configuration parameters.&#x20;

In the example script, the configuration is defined on the command line. However, there are two other ways you can set Spark configuration parameters.&#x20;

* You can use a Kubernetes Pod template to set default parameters. Any variables defined in the template can be overridden by the `spark-submit` command line.
* You can set parameters in the Python script when creating the Spark context. Anything set here will override parameters in the Pod template or the command line.&#x20;

The full parameter list is published at [spark.apache.org](https://spark.apache.org/docs/latest/running-on-kubernetes.html#pod-template-properties).

The example script uses a template YAML file, `cpu-pod-template.yaml`, which contains specific Kubernetes configurations that Spark does not override. It also specifies the Docker files for the driver and executors, the ServiceAccount, and the Kubernetes namespace. The script deploys a total of two Pods - one executor and one driver - with each Pod allocated 16 cores and 64GB of memory.

### Run the job

To launch the job, run the example script:

```
./example-spark-submit.sh
```

The job will download the [MSCOCO](https://academictorrents.com/details/74dec1dd21ae4994dfd9069f9cb0443eb960c962) dataset to the `msoco/` folder in the PVC you created. It should take approximately 10 minutes to run, then the compute resources will be deleted when the job is finished. The driver Pod won't be deleted so you can view the logs after the job is complete.

While the script runs, you can watch the job status in the terminal. You can see the logs for the driver and executor Pods with the `kubectl logs` command.

## Use client mode

In client mode, the Spark driver is the machine from which the jobs are launched, and the driver needs to communicate with the executor pods running on the cluster. Although there are multiple ways to achieve this, we'll deploy a JupyterLab service on Kubernetes to serve as the driver for this example. You do not need to install Spark locally in client mode.

### Deploy JupyterLab

JupyterLab runs in a pod specified by a Kubernetes deployment, which is connected to a headless service that exposes ports for both JupyterLab and Spark. This setup is detailed in the [Client Mode Networking](https://spark.apache.org/docs/latest/running-on-kubernetes.html#client-mode-networking) section of Spark on Kubernetes.&#x20;

The deployment and service configurations can be found in `jupyter/jupyter-service.yaml`. To deploy, execute the following command:

```
kubectl apply -f jupyter/jupyter-service.yaml
```

This setup does not expose the service over the open internet. Therefore, you need create two port forwards for JupyterLab and Spark UI:

```
kubectl port-forward service/spark-jupyter 8888:8888 4040:4040
```

When the port forward is running, you can connect to JupyterLab at `https://localhost:8888` and the Spark UI at `https://localhost:4040`.

### Running the Job

An example Jupyter notebook (`jupyter/interactive-example.ipynb`) is provided, which creates a Spark session in client mode using dynamic executors. This setup allows the Spark session to run concurrently with the Jupyter notebook, with executors spinning up as needed for jobs and shutting down once the jobs are completed. By default, the example notebook configures the Spark session to use a maximum of five executors. The remaining Spark configuration parameters are identical to those of the previous job.

In this notebook, the main job uses `img2dataset` to download the [Conceptual 12M dataset](https://github.com/google-research-datasets/conceptual-12m) to the `cc12m-jupyter/` folder within the PVC you created during setup.&#x20;

The `img2dataset` documentation states that the dataset was downloaded in approximately five hours using a single machine with 16 CPU cores and 64GB memory. The [Weights and Biases report for that run can be found here](https://wandb.ai/rom1504/img2dataset/reports/Download-cc12m-with-img2dataset--VmlldzoxMjIxMTY0). By using five executors with the same resource configuration, the notebook can download the dataset in about one hour, demonstrating the scalability and efficiency of batch processing with Spark.

{% hint style="info" %}
**Note**

Many of the images in this run failed to download, as did the run shown in the `img2dataset` documentation. This is an issue with timeouts for the CC12M dataset, not a Spark error.
{% endhint %}

