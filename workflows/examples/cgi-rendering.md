---
description: Creating your own Blender render farm using thousands of GPUs
---

# CGI Rendering Using Workflows

This example walks through the setup of a complete Cloud rendering solution for GPU rendering using Blender on CoreWeave Cloud. The example uses node affinity rules to select the type and quantity of hardware we use for our render, and even passes in a custom `artifact` to the container.

If you are following along with this example, by the end of it you will have a Web-based file management solution for uploading assets and downloading render output, as well as a highly parallel workflow template with which to launch your render jobs.

<figure><img src="../../docs/.gitbook/assets/image (23) (1).png" alt=""><figcaption><p>Image of a CGI-rendered car</p></figcaption></figure>

## Procedure

### Configure the Persistent Volume Claim

First, we will need a place for all of our render assets and outputs to reside that is accessible to multiple workers and other services in our namespace. To do this, we will create a shared filesystem [Persistent Volume Claim](https://docs.coreweave.com/coreweave-kubernetes/storage#shared-filesystem).

In this example, the resource storage request is `100Gi` in this example; you may adjust as necessary.

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
      storage: 100Gi # 100GB total volume size
```
{% endcode %}

Once the PVC is created and saved in a clearly-named file (we named ours `pvc.yaml`), run `kubectl apply` to create the claim:

```bash
$ kubectl apply -f pvc.yaml

persistentvolumeclaim/shared-data-pvc created
```

We now have a shared filesystem of `100GB`, named `shared-data-pvc`, which we can utilize throughout this rendering example.

### Install the FileBrowser application

Because we are attempting to create an easy-to-use service to render our Blender animation, we will also quickly setup a Web-based file management platform to upload and download any assets and render output we have. To accomplish this, we will be using the open-source utility [FileBrowser](http://www.filebrowser.xyz), available through [the CoreWeave Cloud application Catalog](https://apps.coreweave.com) as **filebrowser**.

<figure><img src="../../docs/.gitbook/assets/image (24).png" alt=""><figcaption><p>The filebrowser application</p></figcaption></figure>

To install and configure the FileBrowser application:

1. Navigate to the application Catalog through the CoreWeave Cloud UI, then search for `filebrowser`.
2. Select the application, which will open the first configuration screen.
3. Under **Node Selection**, select your datacenter region.
4. As we want our new PVC to act as the storage for FileBrowser, under the "Attach existing volumes to your FileBrowser" list, select the newly created PVC (in this case, `shared-data-pvc`) by clicking the small blue plus sign to the right of the Volume name:

<figure><img src="../../docs/.gitbook/assets/image (21).png" alt=""><figcaption><p>The FileBrowser configuration screen, including a list of "Available Volumes"</p></figcaption></figure>

Configure how you'd like the Volume to appear once mounted, then click the **Deploy** button.

{% hint style="info" %}
**Note**

It is recommended that the name you give this FileBrowser application be very short, or you will run into SSL CNAME issues.
{% endhint %}

During the deployment of the application, you'll be redirected to a status page, which will let you know when the Pod running the FileBrowser application is ready.

This status page also provides default login credentials for the FileBrowser application.

{% hint style="warning" %}
**Important**

It is **strongly recommended** to change the default login credentials for FileBrowser.
{% endhint %}

In the **Access URLs** box on the status page, you will find an Ingress URL (such as `https://filebrowser-name.tenant-sta-coreweave-clientname.ord1.ingress.coreweave.cloud/`). This Ingress URL may be used to access the FileBrowser application in a browser.

![The FileBrowser login screen](<../../.gitbook/assets/image (3) (1) (1).png>)

#### **Rendering example**

For this example, we want to render something that quickly in order to showcase the power of CoreWeave Cloud, so we're going to take one of the typical Blender benchmarks, [BMW\_27](https://download.blender.org/demo/test/BMW27\_2.blend.zip), and upload the unpacked file `bmw27_gpu.blend` to our root path in the FileBrowser application.

![The FileBrowser UI, displaying the uploaded bmw27\_gpu.blend file](<../../.gitbook/assets/image (2) (1) (1).png>)

### Create the render workflow

{% hint style="info" %}
**Note**

This portion of the example assumes that you've already set up [Argo CLI tools](../argo.md) on CoreWeave Cloud.
{% endhint %}

The following [Argo workflow file](https://argoproj.github.io/argo-workflows/workflow-concepts/) allows us to:

* define the parameters of the overall job, including the name of the file to render, the frame range, how many frames to render per Pod, and the maximum number of parallel Pods.
* auto-generate "slices" to render in parallel on each Pod
* define the type of hardware on which we would like our job to be executed
* supply Blender commands, and
* pass in a custom python script to ensure we render on GPU.

Some of the workflow steps detailed in this file are a little advanced; we've commented them where possible to clarify their purpose:

{% code title="blender-gpu-render.yaml" %}
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
{% endcode %}

{% hint style="info" %}
**Note**

[Retry logic](https://argoproj.github.io/argo-workflows/retries/) is considered a best practice when running rendering in parallel. Due to the constant advancements in CGI rendering platforms and GPU compute, sometimes these things break "for no reason." Retries as defined in your Argo Workflow template will ensure you aren't hunting for frames lost due to some unknown cause.
{% endhint %}

Our completed Workflow file, which we will save as `blender-gpu-render.yaml`, is now set up to render in parallel using 10 Pods of `4x NV_Pascal` GPUs.

To begin rendering, invoke `argo submit` and specify the Workflow file:

```
$ argo submit --watch blender-gpu-render.yaml
```

Immediately after this command is invoked, you should see the Argo command line begin processing, showing the inputs and the status of your Workflow.

{% hint style="info" %}
**Note**

You may see some `Unschedulable` warnings at first; this is just because Kubernetes is evicting idle containers in order to get your systems ready to run.
{% endhint %}

After about 1 minute, you should see output similar to the following:

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

This output shows the status of the 10 frames you've specified being rendered on 10 different GPU instances with `4x NV_Pascal GPUs` each. You can now browse to your FileBrowser site via the Ingress URL provided in the application status page, where you should see a new folder named `outputs` with a sub-directory - in this example named `bmw27_gpu`. This directory should now contain the 10 newly rendered frames!

![](<../../.gitbook/assets/image (1) (1).png>)

With just some small changes to the Argo workflow we just built and used, you can now run your Blender GPU rendering on thousands of GPUs simultaneously!
