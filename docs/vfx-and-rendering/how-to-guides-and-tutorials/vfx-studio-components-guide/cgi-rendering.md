---
description: >-
  Create your own Blender render farm with thousands of GPUs using Argo
  Workflows
---

# CGI Rendering with Argo Workflows

In this example, a complete Cloud rendering solution is deployed onto a CoreWeave Virtual Workstation. This tutorial uses [Argo Workflows](../../../cloud-tools/argo/) for GPU-rendering jobs with [Blender](https://www.blender.org/).

By following along with this example, at the end you will have:

* a Web-based file management solution for uploading assets and downloading render output, and
* a highly parallel workflow template with which to launch your render jobs.

In this tutorial, all resources are deployed using [the Kubernetes command line (Kubectl)](../../../virtual-servers/deployment-methods/kubectl.md).

## Prerequisites

This guide assumes that the [Argo CLI tools](../../../cloud-tools/argo/) have already been configured in your CoreWeave Cloud namespace.

## Overview

This tutorial covers the following procedure:

1. [Create a storage volume f](cgi-rendering.md#create-a-storage-volume)or assets
2. [Install FileBrowser](cgi-rendering.md#install-filebrowser)
3. [Create the render Workflow](cgi-rendering.md#create-the-render-workflow)

<figure><img src="../../../.gitbook/assets/cars.png" alt=""><figcaption><p>Image of a CGI-rendered car</p></figcaption></figure>

## Create a storage volume

Render assets and outputs must be stored somewhere that is accessible to multiple workers and to other services in our namespace. For this purpose, a shared filesystem is created by way of a [Persistent Volume Claim](https://docs.coreweave.com/coreweave-kubernetes/storage#shared-filesystem).

In the example manifest below, the resource storage request is set to create a storage volume with a size of `100Gi`.

{% code title="pvc.yaml" %}
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data-pvc
spec:
  storageClassName: shared-hdd-ord1
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi # 100Gi total volume size
```
{% endcode %}

Once the PVC is created and saved in a clearly-named file, such as `pvc.yaml`, run `kubectl apply` to deploy it:

```bash
$ kubectl apply -f pvc.yaml

persistentvolumeclaim/shared-data-pvc created
```

A shared filesystem of `100Gi` is now deployed in the namespace with the name `shared-data-pvc`. This volume is utilized throughout this rendering example.

## Install FileBrowser

The end goal of this tutorial is to create an easy-to-use service for rendering a Blender animation. The simplest solution for accessing output assets is to use the open-source utility [FileBrowser](http://www.filebrowser.xyz), which is available through [the Applications Catalog](../../../welcome-to-coreweave/coreweave-cloud-ui/applications-catalog.md) by searching for **filebrowser**.

For more information on installing and using FileBrowser, see [the FileBrowser installation guide](../../../storage/filebrowser.md).

{% hint style="info" %}
**Note**

It is recommended that the name of the FileBrowser application be kept short. Names that are too long may run into SSL CNAME issues.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (24) (1) (1) (1).png" alt=""><figcaption><p>The filebrowser application in the Applications Catalog</p></figcaption></figure>

The newly-created storage volume (PVC) is used as the backend for FileBrowser. Under the "Attach existing volumes to your FileBrowser," select the new volume (here, `shared-data-pvc`) by clicking the small blue plus sign to the right of the Volume name.

<figure><img src="../../../.gitbook/assets/image (21) (1) (1) (1) (1).png" alt=""><figcaption><p>The FileBrowser configuration screen, including a list of "Available Volumes"</p></figcaption></figure>

Configure how you'd like the volume to appear once mounted, then click the **Deploy** button.

During the deployment of the application, you'll be redirected to the application's status page. This status page also provides the default login credentials for the FileBrowser application.

{% hint style="warning" %}
**Important**

It is **strongly recommended** to change the default login credentials for FileBrowser.
{% endhint %}

Navigate to the **Access URLs** box on the status page to find the Ingress URL (for example, `https://filebrowser-name.tenant-coreweave-clientname.ord1.ingress.coreweave.cloud/`).

This Ingress URL is used to access the FileBrowser application in using a Web browser.

![The FileBrowser login screen](<../../../../.gitbook/assets/image (3) (1) (1) (1).png>)

In this example, one of the typical Blender benchmarks, [BMW\_27](https://download.blender.org/demo/test/BMW27\_2.blend.zip), is uploaded as the unpacked file `bmw27_gpu.blend` to the root path in the FileBrowser application. Once logged into FileBrowser, the file may be uploaded using its Web UI.

![The FileBrowser UI displaying the uploaded bmw27\_gpu.blend file](<../../../../.gitbook/assets/image (2) (1) (1).png>)

## Create the render workflow

The [Argo workflow file](https://argoproj.github.io/argo-workflows/workflow-concepts/) provided below does a number of things. First, it defines the parameters of the overall job, including the name of the file to render, the frame range, how many frames to render per Pod, and the maximum number of parallel Pods.

Next, it auto-generates "slices" to render in parallel on each Pod, defines the type of hardware on which we would like our job to be executed, supplies Blender commands, and finally passes in a custom Python script to ensure we render on GPU.

Some of the workflow steps included in this file may be considered advanced. Comments are included where possible to clarify their purpose.

The complete Workflow file is saved as `blender-gpu-render.yaml`, and is now set up to render in parallel using `10` Pods using four `NV_Pascal GPUs` per instance.

<details>

<summary>Click to expand - <code>blender-gpu-render.yaml</code></summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: render-
spec:
  entrypoint: main
  parallelism: 10 # Maximum number of parallel pods to run (pods x gpu limit = total GPUs)
  activeDeadlineSeconds: 864000 # Cancel operation if not finished in 24 hours
  ttlSecondsAfterFinished: 86400 
  arguments:
    parameters: # These parameters are available as variables throughout our template.
    - name: filename # The location of our blend file, /data/ is the root directory of our Filebrowser app
      value: '/data/bmw27_gpu.blend'
    - name: sliceSize # How many frames to render per pod, let's set it to 1
      value: 1
    - name: start # Start frame of entire sequence to render
      value: 1
    - name: stop # Stop frame of entire sequence to render, let's render 10
      value: 10
    - name: outputLocation # Location to write the output to
      value: "/data/output/bmw27_gpu/"

  volumes:
  - name: data-storage
    persistentVolumeClaim:
      claimName: shared-data-pvc # Mounting in our shared data PVC

  tolerations: # This is here so that our generate slices script only runs on a CPU node.
  - key: is_cpu_compute
    operator: Exists

  templates: # This defines the steps in our workflow.
  - name: main
    steps:
    - - name: slice # Step to generate frame ranges "slices" to run on each pod.
        template: gen-slices
    - - name: render
        template: render-blender
        arguments:
          parameters:
          - name: start
            value: "{{item.start}}"
          - name: stop
            value: "{{item.stop}}"
        withParam: "{{steps.slice.outputs.result}}"

  - name: gen-slices # This is our custom slicing script that runs as bare code in a python container.
    script:
      image: python:alpine3.6
      command: [python]
      source: |
        import json
        import sys
        frames = range({{workflow.parameters.start}}, {{workflow.parameters.stop}}+1)
        n = {{workflow.parameters.sliceSize}}
        slices = [frames[i * n:(i + 1) * n] for i in range((len(frames) + n - 1) // n )]
        intervals = map(lambda x: {'start': min(x), 'stop': max(x)}, slices)
        json.dump(list(intervals), sys.stdout)
  - name: render-blender
    metadata:
      labels:
        coreweave.com/role: render
    inputs:
      parameters:
      - name: start
      - name: stop
      artifacts: # Artifacts are directly mounted inside the container for use by our program.
      - name: blender_gpu # We are mounting a python script that ensures all GPUs are used for our render.
        path: /blender_gpu.py # The python script will be mounted at /blender_gpu.py and accessible by Blender.
        raw:
          data: |

            import bpy

            # Set GPU rendering
            bpy.context.scene.cycles.device = 'GPU'
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
            # Force turn off progressive refine, since we are not in viewport
            bpy.context.scene.cycles.use_progressive_refine = False
            # Enable all available GPUs
            for devices in bpy.context.preferences.addons['cycles'].preferences.get_devices():
                for d in devices:
                    d.use = True
                    if d.type == 'CPU':
                        d.use = False
            # Disable placeholder frame files
            bpy.context.scene.render.use_placeholder = False
            # Force process to over-write existing files
            bpy.context.scene.render.use_overwrite = True

    retryStrategy: # It is important that we define retry logic, in case Blender fails. It fails sometimes. Out of nowhere.
      limit: 1
    container:
      image: nytimes/blender:2.82-gpu-ubuntu18.04 # We are using the Docker container graciously provided by NYT.
      command: ["blender"]
      workingDir: /
      # These are the command line arguments that will be supplied to our Blender process, including the python script above.
      args: [ 
            "-b",
            "{{workflow.parameters.filename}}",
            "--engine", "CYCLES",
            "--factory-startup", "-noaudio",
            "--use-extension", "1",
            "-o", "{{workflow.parameters.outputLocation}}",
            "--python", "blender_gpu.py",
            "-s", "{{inputs.parameters.start}}",
            "-e", "{{inputs.parameters.stop}}",
            "-a"
      ]
      resources: # This is where we request our pod resources.
        requests:
          memory: 8Gi # Requesting a minimum of 8GB system ram
          cpu: 1 # Requesting a minimum of 1 vCPU
        limits:
          cpu: 2 # Requesting a maximum of 2 vCPU
          nvidia.com/gpu: 4 # Requesting 4 GPUs
      volumeMounts:
      - name: data-storage # Mounting in our PVC as /data so it's accessible to our pod.
        mountPath: /data
    affinity: 
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
          - matchExpressions:
            - key: gpu.nvidia.com/model
              operator: In
              values: # This is where we identify what GPU type we want to run on.
              - Quadro_RTX_4000
```

</details>

{% hint style="info" %}
**Note**

Argo's [retry logic](https://argoproj.github.io/argo-workflows/retries/) is considered a best practice when running rendering in parallel. Due to the constant advancements in CGI rendering platforms and GPU compute, sometimes these things break "for no reason." Retries as defined in the Argo Workflow template will ensure frames are lost due to an unknown cause.
{% endhint %}

To begin rendering, pass this Workflow file to `argo submit`:

```bash
$ argo submit --watch blender-gpu-render.yaml
```

Immediately after the command is invoked, the Argo command line will begin processing, while displaying the inputs and the status of the Workflow.

{% hint style="info" %}
**Note**

You may see some `Unschedulable` warnings at first; this is due to Kubernetes evicting idle containers in order to prepare the specified systems to run.
{% endhint %}

After about a minute, output similar to the following should be generated:

```bash
Name:                render-sjf6t
Namespace:           tenant-test
ServiceAccount:      default
Status:              Succeeded
Created:             Fri May 29 22:26:01 -0400 (2 minutes ago)
Started:             Fri May 29 22:26:01 -0400 (2 minutes ago)
Finished:            Fri May 29 22:28:12 -0400 (now)
Duration:            2 minutes 11 seconds
Parameters:          
  filename:          /data/bmw27_gpu.blend
  sliceSize:         1
  start:             1
  stop:              10
  outputLocation:    /data/output/bmw27_gpu/

STEP                                                   PODNAME                  DURATION  MESSAGE
 ✔ render-sjf6t (main)                                                                    
 ├---✔ slice (gen-slices)                              render-sjf6t-2863198607  3s        
 └-·-✔ render(0:start:1,stop:1)(0) (render-blender)    render-sjf6t-1206241518  1m        
   ├-✔ render(1:start:2,stop:2)(0) (render-blender)    render-sjf6t-2071804633  1m        
   ├-✔ render(2:start:3,stop:3)(0) (render-blender)    render-sjf6t-2756225068  1m        
   ├-✔ render(3:start:4,stop:4)(0) (render-blender)    render-sjf6t-2726811839  1m        
   ├-✔ render(4:start:5,stop:5)(0) (render-blender)    render-sjf6t-3220888738  1m        
   ├-✔ render(5:start:6,stop:6)(0) (render-blender)    render-sjf6t-3319286957  1m        
   ├-✔ render(6:start:7,stop:7)(0) (render-blender)    render-sjf6t-577269840   1m        
   ├-✔ render(7:start:8,stop:8)(0) (render-blender)    render-sjf6t-3336690355  1m        
   ├-✔ render(8:start:9,stop:9)(0) (render-blender)    render-sjf6t-3980468470  2m        
   └-✔ render(9:start:10,stop:10)(0) (render-blender)  render-sjf6t-2756728893  1m
```

This output shows the status of the 10 frames specified being rendered on 10 different GPU instances with four `NV_Pascal GPUs` per instance.

Now, using FileBrowser via the provided Ingress URL, a new folder named `outputs` has been generated, along with a subdirectory inside of it that contains the newly rendered frames. In this example, the subdirectory is named `bmw27_gpu`.

<figure><img src="../../../../.gitbook/assets/image (1) (1).png" alt="Newly rendered frames in the file browser"><figcaption><p>Newly rendered frames viewed in FileBrowser</p></figcaption></figure>

Using this Argo Workflow as a template or starting point, it is easy to run Blender GPU rendering on thousands of GPUs simultaneously!
