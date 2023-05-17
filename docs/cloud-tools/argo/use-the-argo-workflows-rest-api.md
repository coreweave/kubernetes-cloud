# Use the Argo Workflows REST API

The Argo Workflows [REST API](https://argoproj.github.io/argo-workflows/rest-api/) allows the workflow engine to work programmatically with other systems and applications to create, submit, and manage workflows, monitor their status, retrieve results, build custom applications, and integrating Argo Workflows into existing CI/CD pipelines and automation.

## Use the API

To demonstrate how to use the [Argo Workflows API](https://argoproj.github.io/argo-workflows/swagger/), we'll use `curl` to send an HTTP request to the Argo server.&#x20;

This guide assumed a workflow server has been deployed by following [Argo Workflows guide](./).

This uses the same workflow YAML as the [CLI guide](use-the-argo-workflows-cli.md).&#x20;

Create a file named `workflow.yaml`, expand the section below, and copy/paste the contents into the file.

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

The API needs the workflow to be converted from YAML to JSON. Assuming `yq` is installed:

```bash
yq eval -o=json workflow.yaml > workflow.json  
```

Retrieve the Bearer token for the deployment by running the commands below for the client OS.

{% tabs %}
{% tab title="macOS or Linux (bash or zsh)" %}
```bash
# Replace my-workflow with the deployment name.
export ARGO_NAME=my-workflow
# Use kubectl to find the name of the secret for the ${ARGO_NAME}-argo-client ServiceAccount.
export SECRET=$(kubectl get sa ${ARGO_NAME}-argo-client -o=jsonpath='{.secrets[0].name}')
# Extract the token (a Kubernetes Secret), base64 decode it, and prepend "Bearer " to the string. This is the Bearer token.
export ARGO_TOKEN="Bearer $(kubectl get secret $SECRET -o=jsonpath='{.data.token}' | base64 --decode)"
# Display the Bearer token on the screen.
echo $ARGO_TOKEN
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```powershell
# Replace "my-workflow" with the deployment name.
$ARGO_NAME="my-workflow"
# Use kubectl to find the name of the secret for the ${ARGO_NAME}-argo-client ServiceAccount.
$SECRET=$(kubectl get sa $ARGO_NAME-argo-client -o=jsonpath='{.secrets[0].name}')
# Extract the token (a Kubernetes Secret).
$DATA_TOKEN=$(kubectl get secret $SECRET -o=jsonpath='{.data.token}')
# base64 decode the token
$DECODE_64=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($DATA_TOKEN))
# Prepend "Bearer " to the string. This is the Bearer token.
$ARGO_TOKEN="Bearer $DECODE_64"
# Display the Bearer token on the screen.
Write-Output $ARGO_TOKEN
```
{% endtab %}
{% endtabs %}

Submit the workflow to the API with `curl`.

```bash
$ curl --request POST \
    --url http://<argo-server-address>/api/v1/workflows/<deployment-name>/submit \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer <the-token-here>" \
    --data @workflow.json
```

* Replace `<argo-server-address>` with the Access URL of the Argo server. This is available in [CoreWeave Applications](https://apps.coreweave.com/), see the [Argo Workflows guide](./) for more details.
* Replace `<deployment-name>` with the name.
* Replace `<the-token-here>` with the Bearer token.

Find the deployment name by running:

```bash
$ kubectl get deployments | grep argo-server
my-example-argo-server           1/1     1            1           3d20h
```

The deployment is `my-example-argo-server`.

More examples are available in the [Argo API documentation](https://argoproj.github.io/argo-workflows/rest-examples/).

## Override parameters with the API

Parameters can be overridden with the API, by passing JSON key-value pairs. To override `foo` with the value `curl is fun`, use this:

```bash
$ curl --request POST \
    --url http://<argo-server-address>/api/v1/workflows/<namespace>/submit \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer <the-token-here>" \
    --data @workflow.json \
    --data "{ \"foo\": \"curl is fun\" }"
```

## More information

For more information, please see these Argo Workflows resources:

* [API reference](https://argoproj.github.io/argo-workflows/swagger/)
* [Examples on GitHub](https://github.com/argoproj/argo-workflows/tree/master/examples)
* [Slack](https://argoproj.github.io/community/join-slack/)
* [Training on YouTube](https://www.youtube.com/playlist?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo)
* [Argo Blog](https://blog.argoproj.io/)
