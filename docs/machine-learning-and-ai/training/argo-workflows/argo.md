---
description: Use Argo Workflows to run jobs in parallel
---

# Get Started with Workflows

Workflows on CoreWeave Cloud run on [Argo Workflows](https://argoproj.github.io/workflows), which is a great tool to orchestrate parallel execution of GPU and CPU jobs. With Workflows, you can manage retries and parallelism automatically. Workflows can also be submitted via CLI, [Rest API](https://argoproj.github.io/argo-workflows/rest-api/) and the [Kubernetes API](https://argoproj.github.io/argo-workflows/walk-through/kubernetes-resources/).

<figure><img src="../../../.gitbook/assets/screen-shot-2020-07-29-at-10.04.26-pm.png" alt="Screenshot showing the Argo Web UI"><figcaption><p>A view of the Argo Web UI</p></figcaption></figure>

## Get Started

After logging into [CoreWeave Cloud](https://cloud.coreweave.com), navigate to the CoreWeave application **Catalog**.

![The Catalog link on the Cloud UI](<../../../../.gitbook/assets/image (17) (2) (1) (2).png>)

A new window will open onto the Catalog, where you can browse all available applications. In the search field, type `argo-workflows`. Then, select the **argo-workflows** application once it appears:

<figure><img src="../../../../.gitbook/assets/image (14).png" alt="argo-workflows application in the Catalog"><figcaption><p>argo-workflows application in the Catalog</p></figcaption></figure>

In the upper right-hand corner of the following screen, select the latest version of the Helm chart under **Chart Version**, then click the **Deploy** button.

<figure><img src="../../../../.gitbook/assets/image (25) (1).png" alt="Chart version selection and deploy button"><figcaption><p>Chart version selection and deploy button</p></figcaption></figure>

The following deployment form will prompt you to enter a name for the application. The remaining parameters will be set to CoreWeave's suggested defaults, but can be changed to suit your requirements. When ready to deploy, click the **Deploy** button at the bottom of the page.

{% hint style="warning" %}
**Important**

`The server` authentication mode does not require credentials and is **strongly discouraged**. We suggest using [the`client` mode](https://argoproj.github.io/argo-workflows/argo-server-auth-mode) for better security.

[See the **Security** section below for more information](argo.md#security).
{% endhint %}

![The Argo Workflows configuration screen](<../../../.gitbook/assets/image (1) (6) (1) (1).png>)

After a few minutes, the deployment will be ready. If you selected `Expose UI via public Ingress`, Argo Workflows will be accessible outside the cluster.

Click the **ingress** link to open the Argo Workflows UI in a new window.

![](<../../../../.gitbook/assets/image (23) (1).png>)

{% hint style="warning" %}
**Important**

It can take up to five minutes for a TLS certificate to be issued. Prior to this, you may encounter a TLS certificate error, but once the certificate is issued, this error should disappear on its own.
{% endhint %}

To run a sample workflow:

1. Click **+SUBMIT NEW WORKFLOW**, then **Edit using workflow options.**
2. Click **+CREATE**. After a few minutes, once successful, the workflow indication color will change to green.

## Installing Argo CLI

{% hint style="info" %}
**Note**

The following assumes you have already obtained CoreWeave Cloud access credentials and [set up your kubeconfig file](../../../coreweave-kubernetes/getting-started.md#setup-kubernetes-config).
{% endhint %}

The Argo CLI tool can be obtained from [the Argo Project's website](https://argoproj.github.io/argo-workflows/quick-start/#install-the-argo-workflows-cli). Then, to run an example workflow, save an example workflow into the file `gpu-say-workflow.yaml`.

**Example**

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

Submit the new workflow file (`gpu-say-workflow.yaml`). According to the specifications above, this workflow takes a JSON array to spin up Pods with one GPU allocated for each, in parallel. The `nvidia-smi` output, as well as the parameter entry assigned for that Pod, is outputted to the log:

```
$ argo submit --watch gpu-say-workflow.yaml -p messages='["Argo", "Is", "Awesome"]'

  Name:                gpu-sayzfwxc
  Namespace:           tenant-test
  ServiceAccount:      default
  Status:              Running
  Created:             Mon Feb 10 19:31:17 -0500 (15 seconds ago)
  Started:             Mon Feb 10 19:31:17 -0500 (15 seconds ago)
  Duration:            15 seconds
  Parameters:
    messages:          ["Argo", "Is", "Awesome"]

  STEP                                  PODNAME                  DURATION  MESSAGE
   ● gpu-sayzfwxc (main)
   └-·-✔ echo(0:Argo)(0) (gpu-echo)     gpu-sayzfwxc-391007373   10s
     ├-● echo(1:Is)(0) (gpu-echo)       gpu-sayzfwxc-3501791705  15s
     └-✔ echo(2:Awesome)(0) (gpu-echo)  gpu-sayzfwxc-3986963301  12s
```

To print the log output from all parallel containers, use the `logs` command:

```
$ argo logs -w gpu-sayrbr6z

echo(0:Argo)(0):    Tue Feb 11 00:25:30 2020
echo(0:Argo)(0):    +-----------------------------------------------------------------------------+
echo(0:Argo)(0):    | NVIDIA-SMI 440.44       Driver Version: 440.44       CUDA Version: 10.2     |
echo(0:Argo)(0):    |-------------------------------+----------------------+----------------------+
echo(0:Argo)(0):    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
echo(0:Argo)(0):    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
echo(0:Argo)(0):    |===============================+======================+======================|
echo(0:Argo)(0):    |   0  NVIDIA Graphics...  Off  | 00000000:08:00.0 Off |                  N/A |
echo(0:Argo)(0):    | 28%   51C    P5    16W / 180W |     18MiB /  8119MiB |      0%      Default |
echo(0:Argo)(0):    +-------------------------------+----------------------+----------------------+
echo(0:Argo)(0):
echo(0:Argo)(0):    +-----------------------------------------------------------------------------+
echo(0:Argo)(0):    | Processes:                                                       GPU Memory |
echo(0:Argo)(0):    |  GPU       PID   Type   Process name                             Usage      |
echo(0:Argo)(0):    |=============================================================================|
echo(0:Argo)(0):    +-----------------------------------------------------------------------------+
echo(0:Argo)(0):    Input was: Argo
echo(1:Is)(0):    Tue Feb 11 00:25:30 2020
echo(1:Is)(0):    +-----------------------------------------------------------------------------+
echo(1:Is)(0):    | NVIDIA-SMI 440.44       Driver Version: 440.44       CUDA Version: 10.2     |
echo(1:Is)(0):    |-------------------------------+----------------------+----------------------+
...
```

## Security

Argo requires a Service Account token for authentication. The following steps are best practices based on [Argo's access token creation](https://argoproj.github.io/argo-workflows/access-token/#token-creation).

{% hint style="danger" %}
**Warning**

`server` auth mode is strongly discouraged, as it opens up Argo Workflows to public access, and is therefore a security risk. ​
{% endhint %}

### Tailored permissions

To tailor permissions more granularly, first create a role with minimal permissions:

```bash
$ kubectl create role argo-role --verb=list,update --resource=workflows.argoproj.io
```

​ To get full list of resources, issue the `api-resources` command:

```bash
$ kubectl api-resources --api-group=argoproj.io --namespaced=true -o wide
```

with the following parameters:

| Name                    | Shortnames   | Kind                 | Verbs                                                          |
| ----------------------- | ------------ | -------------------- | -------------------------------------------------------------- |
| `cronworkflows`         | `cwf,cronwf` | CronWorkflow         | `[delete deletecollection get list patch create update watch]` |
| `workfloweventbindings` | `wfeb`       | WorkflowEventBinding | `[delete deletecollection get list patch create update watch]` |
| `workflows`             | `wf`         | Workflow             | `[delete deletecollection get list patch create update watch]` |
| `workflowtaskresults`   |              | WorkflowTaskResult   | `[delete deletecollection get list patch create update watch]` |
| `workflowtasksets`      | `wfts`       | WorkflowTaskSet      | `[delete deletecollection get list patch create update watch]` |
| `workflowtemplates`     | `wftmpl`     | WorkflowTemplate     | `[delete deletecollection get list patch create update watch]` |

Using the command line to create a tailored role with the many resources and verbs can be inefficient. It's also possible to set permissions using a YAML manifest instead:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-role
rules:
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  verbs:
  - list
  - update
```

Then, apply the manifest using `kubectl apply`:

```bash
$ kubectl apply -f <manifest_roles.yaml>
```

### **Service account** ​

To create a unique Service Account, use `kubectl create sa`.

For example, here we create a Service Account with the name `argo-sa`:

```bash
$ kubectl create sa argo-sa
```

Then, create a rolebinding for the new Service Account, bound to the argo-role created:

```bash
$ kubectl create rolebinding argo-role-binding --role=argo-role --serviceaccount=<namespace>:argo-sa 
```

​ ​where `namespace` is the namespace in which Argo is running.

### **Generate the token**

Generate the token to be used with the Service Account:

{% tabs %}
{% tab title="Linux" %}
{% code overflow="wrap" %}
```bash
$ export SECRET=$(kubectl get sa argo-sa -o=jsonpath='{.secrets[0].name}') && export ARGO_TOKEN="Bearer $(kubectl get secret $SECRET -o=jsonpath='{.data.token}' | base64 --decode)" && echo $ARGO_TOKEN
```
{% endcode %}
{% endtab %}

{% tab title="Powershell" %}
{% code overflow="wrap" %}
```powershell
Write-Host "Bearer $([Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($(kubectl get secret $(kubectl get sa {{ .Release.Name }}-argo-client -o=jsonpath='{.secrets[0].name}') -o=jsonpath='{.data.token}'))))"
```
{% endcode %}
{% endtab %}
{% endtabs %}

Then, inside the box for **client authentication**, copy and paste the newly generated token into the Argo UI:

![The Argo Workflow UI with a Bearer token pasted into the client authentication box](<../../../.gitbook/assets/image (2) (2) (1).png>)

Finally, to log in, click the **Login** button after adding the token.

## Recommendations

We recommend the following retry strategy on your workflow / steps.

```yaml
 retryStrategy:
   limit: 2
   retryPolicy: Always
   backoff:
     duration: "15s"
     factor: 2
   affinity:
     nodeAntiAffinity: {}
```

We also recommend setting an `activeDeadlineSeconds` on each `step`, but not on the entire workflow. This allows a step to retry but prevents it from taking unreasonably long time to finish.
