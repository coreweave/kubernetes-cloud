---
description: Use the power of the command line to control Argo Workflows
---

# Use the Argo Workflows CLI

The Argo Command Line Interface (CLI) is a powerful tool used to create, submit, manage, and monitor workflows directly from the command line. The CLI also allows creating reusable templates, making it easier to define and share common workflow patterns. Many of [CoreWeave's example projects](./#practical-examples) use Argo CLI as the primary way to demonstrate different techniques.

## Use Argo CLI

To submit a job with the CLI, first verify the [CoreWeave Kubernetes environment](../../coreweave-kubernetes/getting-started.md#setup-kubernetes-config) is set up.

Next, download the latest Argo CLI from [the GitHub releases](https://github.com/argoproj/argo-workflows/releases) page and follow their Quick Start installation instructions.&#x20;

To test the installation, run:

```bash
argo version
```

The result should be similar to:

```
argo: v3.4.7
  BuildDate: 2023-04-11T17:19:48Z
  GitCommit: f2292647c5a6be2f888447a1fef71445cc05b8fd
  GitTreeState: clean
  GitTag: v3.4.7
  GoVersion: go1.19.7
  Compiler: gc
  Platform: linux/amd64
```

Next, create a working folder and a file named `workflow.yaml`.

```
$ mkdir example
$ cd example
$ nano workflow.yaml
```

Expand the section below, and copy/paste the contents into the file.&#x20;

<details>

<summary>Click to expand - <code>workflow.yaml</code></summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: gpu-say
spec:
  entrypoint: main
  activeDeadlineSeconds: 300 # Cancel operation if not finished in 5 minutes
  ttlStrategy:
    secondsAfterCompletion: 86400 # Clean out old workflows after a day
  # Parameters can be passed/overridden via the argo CLI.
  # To override the printed message, run `argo submit` with the -p option:
  # $ argo submit examples/arguments-parameters.yaml -p messages='["CoreWeave", "Is", "Fun"]'
  arguments:
    parameters:
    - name: messages
      value: '["Argo", "Is", "Awesome"]'
    - name: foo
      value: "bar"

  templates:
  - name: main
    steps:
      - - name: echo
          template: gpu-echo
          arguments:
            parameters:
            - name: message
              value: "{{item}}"
          withParam: "{{workflow.parameters.messages}}"

  - name: gpu-echo
    inputs:
      parameters:
      - name: message
    retryStrategy:
      limit: 1
    script:
      image: nvidia/cuda:11.4.1-runtime-ubuntu20.04
      command: [bash]
      source: |
        nvidia-smi
        echo "Input was: {{inputs.parameters.message}}"        

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
```



</details>

Then, submit the workflow file.

```bash
argo submit workflow.yaml
```

Here's the output.

```bash
ame:                gpu-say64d9m
Namespace:           tenant-96362f-dev
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Pending
Created:             Thu May 04 17:38:04 -0400 (now)
Progress:            
Parameters:          
  messages:          ["Argo", "Is", "Awesome"]
  foo:               bar
```

This workflow uses the JSON array as parameters to spin up three Pods, with one GPU allocated for each, in parallel.&#x20;

There are two parameters in this file:

* `messages`, which is an array of strings
* `foo`, which has the value `bar`

## How to override parameters

One technique used often in [CoreWeave examples](./#practical-examples) is setting default values in the workflow YAML, and then overriding a few of them on the command line or with a parameters file.&#x20;

### Override parameters on the command line

Override workflow parameters on the command line with the `-p` option:

```bash
argo submit workflow.yaml \
-p messages='["CoreWeave", "Is", "Fun"]' \
-p foo='Something Else'
```

In this case, the output shows the overridden parameters:

```
Name:                gpu-sayxgsrv
Namespace:           tenant-96362f-dev
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Pending
Created:             Thu May 04 17:40:30 -0400 (now)
Progress:            
Parameters:          
  messages:          ["CoreWeave", "Is", "Fun"]
  foo:               Something Else
```

### Override parameters with a YAML file

Another technique is using a [YAML file](https://argoproj.github.io/argo-workflows/walk-through/parameters/) to override parameters. To do that, create `params.yaml` in the example folder and paste this into it.

```yaml
messages: ["Use", "Anything", "Here"]
foo: "Another new string"
```

Then, use the `--parameter-file` option to pass `params.yaml` to the workflow.

```bash
argo submit workflow.yaml --parameter-file params.yaml
```

The output shows the new parameters:

```
Name:                gpu-saygppcq
Namespace:           tenant-96362f-dev
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Pending
Created:             Thu May 04 17:43:57 -0400 (now)
Progress:            
Parameters:          
  foo:               Another new string
  messages:          ["Use","Anything","Here"]
```

## List workflows

After submitting a job, use the `argo` command to interact with it.&#x20;

To find a job's name, use the `list` command.

```bash
argo list
```

The output shows the name, `gpu-sayn5p6w` in this case.

```
NAME             STATUS      AGE   DURATION   PRIORITY   MESSAGE
gpu-sayn5p6w     Succeeded   41m   37s        0          
```

## View Argo logs

To see the logs for a workflow job, use the `logs` command with workflow name we fetched earlier. It looks like this:

```bash
argo logs gpu-sayn5p6w
```

Expand the log output below to see the result:

<details>

<summary>Click to expand - Argo log output</summary>

```
gpu-sayn5p6w-gpu-echo-1273146457: Wed May  3 21:30:56 2023       
gpu-sayn5p6w-gpu-echo-1273146457: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-1273146457: | NVIDIA-SMI 510.60.02    Driver Version: 510.60.02    CUDA Version: 11.6     |
gpu-sayn5p6w-gpu-echo-1273146457: |-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-1273146457: | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
gpu-sayn5p6w-gpu-echo-1273146457: | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
gpu-sayn5p6w-gpu-echo-1273146457: |                               |                      |               MIG M. |
gpu-sayn5p6w-gpu-echo-1273146457: |===============================+======================+======================|
gpu-sayn5p6w-gpu-echo-1273146457: |   0  NVIDIA RTX A4000    On   | 00000000:02:00.0 Off |                  Off |
gpu-sayn5p6w-gpu-echo-1273146457: | 46%   33C    P8    17W / 140W |     65MiB / 16376MiB |      0%      Default |
gpu-sayn5p6w-gpu-echo-1273146457: |                               |                      |                  N/A |
gpu-sayn5p6w-gpu-echo-1273146457: +-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-1273146457:                                                                                
gpu-sayn5p6w-gpu-echo-1273146457: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-1273146457: | Processes:                                                                  |
gpu-sayn5p6w-gpu-echo-1273146457: |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
gpu-sayn5p6w-gpu-echo-1273146457: |        ID   ID                                                   Usage      |
gpu-sayn5p6w-gpu-echo-1273146457: |=============================================================================|
gpu-sayn5p6w-gpu-echo-1273146457: |    0   N/A  N/A      2181      G                                      63MiB |
gpu-sayn5p6w-gpu-echo-1273146457: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-1273146457: Input was: Is
gpu-sayn5p6w-gpu-echo-1273146457: time="2023-05-03T21:30:57.804Z" level=info msg="sub-process exited" argo=true error="<nil>"
gpu-sayn5p6w-gpu-echo-3614462693: Wed May  3 21:31:16 2023       
gpu-sayn5p6w-gpu-echo-3614462693: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-3614462693: | NVIDIA-SMI 510.60.02    Driver Version: 510.60.02    CUDA Version: 11.6     |
gpu-sayn5p6w-gpu-echo-3614462693: |-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-3614462693: | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
gpu-sayn5p6w-gpu-echo-3614462693: | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
gpu-sayn5p6w-gpu-echo-3614462693: |                               |                      |               MIG M. |
gpu-sayn5p6w-gpu-echo-3614462693: |===============================+======================+======================|
gpu-sayn5p6w-gpu-echo-3614462693: |   0  NVIDIA RTX A4000    On   | 00000000:01:00.0 Off |                  Off |
gpu-sayn5p6w-gpu-echo-3614462693: | 47%   33C    P8    15W / 140W |     65MiB / 16376MiB |      0%      Default |
gpu-sayn5p6w-gpu-echo-3614462693: |                               |                      |                  N/A |
gpu-sayn5p6w-gpu-echo-3614462693: +-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-3614462693:                                                                                
gpu-sayn5p6w-gpu-echo-3614462693: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-3614462693: | Processes:                                                                  |
gpu-sayn5p6w-gpu-echo-3614462693: |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
gpu-sayn5p6w-gpu-echo-3614462693: |        ID   ID                                                   Usage      |
gpu-sayn5p6w-gpu-echo-3614462693: |=============================================================================|
gpu-sayn5p6w-gpu-echo-3614462693: |    0   N/A  N/A      2290      G                                      63MiB |
gpu-sayn5p6w-gpu-echo-3614462693: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-3614462693: Input was: Awesome
gpu-sayn5p6w-gpu-echo-3614462693: time="2023-05-03T21:31:17.624Z" level=info msg="sub-process exited" argo=true error="<nil>"
gpu-sayn5p6w-gpu-echo-2418828045: Wed May  3 21:31:22 2023       
gpu-sayn5p6w-gpu-echo-2418828045: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-2418828045: | NVIDIA-SMI 510.60.02    Driver Version: 510.60.02    CUDA Version: 11.6     |
gpu-sayn5p6w-gpu-echo-2418828045: |-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-2418828045: | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
gpu-sayn5p6w-gpu-echo-2418828045: | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
gpu-sayn5p6w-gpu-echo-2418828045: |                               |                      |               MIG M. |
gpu-sayn5p6w-gpu-echo-2418828045: |===============================+======================+======================|
gpu-sayn5p6w-gpu-echo-2418828045: |   0  NVIDIA RTX A4000    On   | 00000000:C1:00.0 Off |                  Off |
gpu-sayn5p6w-gpu-echo-2418828045: | 42%   31C    P8    13W / 140W |     94MiB / 16376MiB |      0%      Default |
gpu-sayn5p6w-gpu-echo-2418828045: |                               |                      |                  N/A |
gpu-sayn5p6w-gpu-echo-2418828045: +-------------------------------+----------------------+----------------------+
gpu-sayn5p6w-gpu-echo-2418828045:                                                                                
gpu-sayn5p6w-gpu-echo-2418828045: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-2418828045: | Processes:                                                                  |
gpu-sayn5p6w-gpu-echo-2418828045: |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
gpu-sayn5p6w-gpu-echo-2418828045: |        ID   ID                                                   Usage      |
gpu-sayn5p6w-gpu-echo-2418828045: |=============================================================================|
gpu-sayn5p6w-gpu-echo-2418828045: |    0   N/A  N/A      2218      G                                      92MiB |
gpu-sayn5p6w-gpu-echo-2418828045: +-----------------------------------------------------------------------------+
gpu-sayn5p6w-gpu-echo-2418828045: Input was: Argo
gpu-sayn5p6w-gpu-echo-2418828045: time="2023-05-03T21:31:23.231Z" level=info msg="sub-process exited" argo=true error="<nil>"
```

</details>

## Watch the submission

Use the `--watch` option to observe the workflow in progress.

```
argo submit workflow.yaml --watch
```

If the `--watch` option wasn't used when submitting the workflow, the `watch` command is used with the workflow name to observe it.

```bash
argo watch gpu-sayn5p6w
```

In either case, the output looks the same.

```
Name:                gpu-sayn5p6w
Namespace:           tenant-d0b59f-dfinst
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Running
Conditions:          
 PodRunning          False
Created:             Wed May 03 17:30:50 -0400 (26 seconds ago)
Started:             Wed May 03 17:30:50 -0400 (26 seconds ago)
Duration:            26 seconds
Progress:            1/3
ResourcesDuration:   3s*(100Mi memory),1s*(1 nvidia.com/gpu),3s*(1 cpu)
Parameters:          
  messages:          ["Argo", "Is", "Awesome"]

STEP                       TEMPLATE  PODNAME                           DURATION  MESSAGE
 ● gpu-sayn5p6w            main                                                                   
 └─┬─◷ echo(0:Argo)(0)     gpu-echo  gpu-sayn5p6w-gpu-echo-2418828045  26s       PodInitializing  
   ├─✔ echo(1:Is)(0)       gpu-echo  gpu-sayn5p6w-gpu-echo-1273146457  6s                         
   └─◷ echo(2:Awesome)(0)  gpu-echo  gpu-sayn5p6w-gpu-echo-3614462693  25s       PodInitializing  

```

## Use a specific ServiceAccount

In the previous example, notice that the third line says:

```
ServiceAccount:      unset (will run with the default ServiceAccount)
```

If no specific Kubernetes ServiceAccount was declared, the workflow uses the default one for the namespace. To use a specific ServiceAccount, create one and then use the `--serviceaccount` option by following the steps that follow. The [security best practices guide](security-best-practices-for-argo-workflows.md) has more details.

First, define a ServiceAccount and assign it some defined Roles. Then, define a RoleBinding to bind them together.&#x20;

This can be done in a single YAML file. Create `my-example-sa.yaml` and paste the contents below.

<details>

<summary>Click to expand - <code>my-example-sa.yaml</code></summary>

{% code title="my-example-sa.yaml" %}
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-example
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-example-role
rules:
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - 'patch'
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
  name: my-example-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: my-example-role
subjects:
  - kind: ServiceAccount
    name: my-example
```
{% endcode %}

</details>

There are three sections in this file, separated with `---`.&#x20;

* First, it creates a new ServiceAccount named `my-example`.&#x20;
* Next, it creates a Role named `my-example-role` with several permissions.&#x20;
* Finally, it creates a RoleBinding named `my-example-rolebinding` which binds the ServiceAccount to the Role.&#x20;

### Create the ServiceAccount

Apply the YAML to the cluster with `kubectl`.

```
kubectl apply -f my-example-sa.yaml
```

The output looks like this:

```bash
serviceaccount/my-example created
role.rbac.authorization.k8s.io/my-example-role created
rolebinding.rbac.authorization.k8s.io/my-example-rolebinding created
```

### Use the ServiceAccount

Now, use the new ServiceAccount with Argo, like this:

```bash
argo submit workflow.yaml --serviceaccount my-example
```

The output looks like this:

```
Name:                gpu-say72dm5
Namespace:           tenant-96362f-dev
ServiceAccount:      my-example
Status:              Pending
Created:             Thu May 04 18:24:58 -0400 (now)
Progress:            
Parameters:          
  messages:          ["Argo", "Is", "Awesome"]
  foo:               bar
```

Notice that the third line now shows the new ServiceAccount name. Using a specific ServiceAccount with limited permissions is a [security best practice](security-best-practices-for-argo-workflows.md).

## More information

These are only a few of the most common Argo CLI commands used in CoreWeave's examples and demonstrations. For a full list, please see the [Argo documentation](https://argoproj.github.io/argo-workflows/cli/argo/) or see these Argo Workflows resources:

* [Examples on GitHub](https://github.com/argoproj/argo-workflows/tree/master/examples)
* [Slack](https://argoproj.github.io/community/join-slack/)
* [Training on YouTube](https://www.youtube.com/playlist?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo)
* [Argo Blog](https://blog.argoproj.io/)
