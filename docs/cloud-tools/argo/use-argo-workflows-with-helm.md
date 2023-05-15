# Use Argo Workflows with Helm

[Helm](https://helm.sh/) is a popular package manager for Kubernetes that streamlines the deployment and management of applications on Kubernetes clusters. A Helm-based workflow can submit Argo Workflows with ease, enabling users to focus on building and running workflows rather than dealing with the complexities of manual deployment.

{% hint style="info" %}
**Tip**

It's helpful to know how to use parameters with Argo Workflows before adding the Helm abstraction layer. [Read the introductory guide](./) to learn more.
{% endhint %}

This guide assumes the client workstation is Linux and [already has Helm installed](https://helm.sh/docs/intro/install/).&#x20;

## Submit an Argo workflow with a Helm chart

This example uses is a basic Helm chart to submit an Argo workflow with parameters supplied by Helm.

First, create a new project directory and change into it.&#x20;

```bash
$ mkdir ~/my-helm-projects
$ cd ~/my-helm-projects
```

Then, create a new example chart.

```bash
$ helm create helm-example
Creating helm-example
```

Next, change to the `example/templates` directory and create an Argo workflow file.

```bash
$ cd ~/my-helm-projects/helm-example/templates/
$ nano workflow.yaml
```

Expand the section below and copy/paste the contents into the `workflow.yaml` file.&#x20;

<details>

<summary>Click to expand - <code>workflow.yaml</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: gpu-say
spec:
  entrypoint: main
  activeDeadlineSeconds: 300 # Cancel operation if not finished in 5 minutes
  ttlStrategy:
    secondsAfterCompletion: 86400 # Clean out old workflows after a day
  arguments:
    parameters:
    - name: message
      value: "{{ .Values.helmmessage }}"
    - name: foo
      value: "{{ .Values.helmfoo }}"

  templates:
  - name: main
    inputs:
      parameters:
      - name: message
      - name: foo
    retryStrategy:
      limit: 1
    script:
      image: nvidia/cuda:11.4.1-runtime-ubuntu20.04
      command: [bash]
      source: |
        nvidia-smi
        echo "Message was: {{`{{inputs.parameters.message}}`}}"
<strong>        echo "Foo was: {{`{{inputs.parameters.foo}}`}}"
</strong>
      resources:
        requests:
          memory: 128Mi
          cpu: 500m # Half a core
        limits:
          nvidia.com/gpu: 1 # Allocate one GPU
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
            # This will REQUIRE the Pod to be run on a system with a GPU with 8 or 16GB VRAM
              nodeSelectorTerms:
              - matchExpressions:
                - key: gpu.nvidia.com/vram
                  operator: In
                  values:
                    - "8"
                    - "16"

</code></pre>



</details>

### About the workflow

Let's take a closer look at lines 10 through 15 of `workflow.yaml`:

```
  arguments:
    parameters:
    - name: message
      value: "{{ .Values.helmmessage }}"
    - name: foo
      value: "{{ .Values.helmfoo }}"
```

The Argo workflow has two parameters:&#x20;

* Argo parameter `message` receives its value from Helm variable `helmmessages`
* Argo parameter `foo` receives its value from Helm variable `helmfoo`

There's no requirement that the Helm variable be named differently than the Argo parameter. In fact, it's common for them to be named the same in production code, but this illustrates that they are two different things.&#x20;

Lines 21 and 22 define the inputs in the template, which are used in lines 30 and 31, like this:

```
echo "Message was: {{`{{inputs.parameters.message}}`}}"
echo "Foo was: {{`{{inputs.parameters.foo}}`}}"
```

Notice the funky syntax with two sets of double braces and backticks. This wraps the Argo template syntax with Helm syntax. See [this answer on Stack Overflow](https://stackoverflow.com/a/64805238) for more details.&#x20;

### Create the Helm values

Now, we'll create a Helm value file to supply those values to Argo.&#x20;

Go up one level to the `example` directory and open the existing `values.yaml`.

```bash
$ cd ~/my-helm-projects/helm-example
$ nano values.yaml
```

Add these Helm values to the end of the file:

{% code title="values.yaml" %}
```yaml
helmmessage: "Hello World!"
helmfoo: "Hello from Helm!"
```
{% endcode %}

Go to the Helm project folder and install the chart as `my-deployment`.

```bash
$ cd ~/my-helm-projects
$ helm install my-deployment helm-example
```

This submits the Argo workflow with the values pulled from `values.yaml`.

Let's see the result:

```
NAME: my-deployment
LAST DEPLOYED: Fri May  5 15:08:50 2023
NAMESPACE: tenant-12345a-example
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace tenant-12345a-example -l "app.kubernetes.io/name=helm-example,app.kubernetes.io/instance=my-deployment" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace tenant-12345a-example $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace tenant-12345a-example port-forward $POD_NAME 8080:$CONTAINER_PORT
```

Here is the log file:

```
$ argo logs gpu-say
...
gpu-say-main-2758790358: Message was: Hello World!
gpu-say-main-2758790358: Foo was: Hello from Helm!
...
```

### How to pass Helm options on the command line

An Argo workflow can receive values from a Helm `values.yaml` file. But, sometimes it's better to supply the values on the command line. This is demonstrated with the `helmfoo` value in this example.

In Helm, values passed on the command line do not override the `values.yaml` file, so remove this value from the file before proceeding:

```
helmfoo: "Hello from Helm!"
```

Then, use the `--set` command line option to pass the value, like this:

```bash
$ helm install my-deployment helm-example \
     --set helmfoo="Command lines are fun!"
```

Remember, the Helm value, `helmfoo`  is received by Argo as `foo`, as shown in the Argo log:

```
$ argo logs gpu-say
...
gpu-say-main-2758790358: Message was: Hello World!
gpu-say-main-2758790358: Foo was: Command lines are fun!
...
```

With the power of Helm and the versatility of Argo Workflows combine to streamline application deployment, and improve the efficiency of the development process.

## More information

For more information, please see these Argo Workflows resources:

* [Examples on GitHub](https://github.com/argoproj/argo-workflows/tree/master/examples)
* [Slack](https://argoproj.github.io/community/join-slack/)
* [Training on YouTube](https://www.youtube.com/playlist?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo)
* [Argo Blog](https://blog.argoproj.io/)
