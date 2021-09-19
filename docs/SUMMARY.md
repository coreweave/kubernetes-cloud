# Table of contents

* [CoreWeave Cloud](README.md)

## CoreWeave Kubernetes

* [Getting Started](coreweave-kubernetes/getting-started.md)
* [Useful Commands](coreweave-kubernetes/useful-commands.md)
* [Node Types](coreweave-kubernetes/node-types.md)
* [Advanced Label Selectors](coreweave-kubernetes/label-selectors.md)
* [Storage](coreweave-kubernetes/storage.md)
* [Exposing Applications](coreweave-kubernetes/exposing-applications.md)
* [Serverless](coreweave-kubernetes/serverless.md)
* [Metrics](coreweave-kubernetes/prometheus/README.md)
  * [Grafana](coreweave-kubernetes/prometheus/grafana.md)
  * [Useful Metrics](coreweave-kubernetes/prometheus/useful-metrics.md)
* [Examples](coreweave-kubernetes/examples/README.md)
  * [Jupyter Notebook with TensorFlow](coreweave-kubernetes/examples/tensorflow-jupyter.md)
  * [Ethereum Miner](coreweave-kubernetes/examples/miner.md)
  * [SSH Server with CUDA](coreweave-kubernetes/examples/cuda-ssh.md)

## Inference <a id="compass"></a>

* [Online Inference Serving](compass/online-inference.md)
* [Examples](compass/examples/README.md)
  * [TensorFlow - Open AI GPT-2](compass/examples/gpt-2/README.md)
    * [Transformer](compass/examples/gpt-2/transformer.md)
    * [Exporting with Jupyter](compass/examples/gpt-2/jupyter-pvc.md)
    * [S3 Model Serving](compass/examples/gpt-2/service-s3.md)
    * [PVC Model Serving](compass/examples/gpt-2/service-pvc.md)
  * [TensorFlow2 - Image Classifier](compass/examples/tensorflow2-image-classifier.md)
  * [PyTorch - GPT-2 AITextgen](compass/examples/custom-pytorch-aitextgen.md)
  * [PyTorch - FastAI Sentiment](compass/examples/custom-sentiment.md)
  * [Custom - BASNET](compass/examples/custom-basnet.md)

## Workflows

* [Getting Started](workflows/argo.md)
* [Examples](workflows/examples/README.md)
  * [CGI Rendering](workflows/examples/cgi-rendering.md)

## Virtual Servers

* [Getting Started](virtual-servers/getting-started.md)
* [Deployment Methods](virtual-servers/deployment-methods/README.md)
  * [CLI](virtual-servers/deployment-methods/kubectl.md)
  * [Terraform](virtual-servers/deployment-methods/terraform.md)
  * [Programmatically](virtual-servers/deployment-methods/programmatically/README.md)
    * [Python](virtual-servers/deployment-methods/programmatically/python.md)
    * [NodeJS](virtual-servers/deployment-methods/programmatically/nodejs.md)
    * [Golang](virtual-servers/deployment-methods/programmatically/golang.md)
* [Remote Access and Control](virtual-servers/remote-access-and-control.md)
* [Root Disk Lifecycle Management](virtual-servers/root-disk-lifecycle-management/README.md)
  * [Manually creating a Virtual Server base image](virtual-servers/root-disk-lifecycle-management/creating-a-virtual-server-base-image.md)
  * [Copying CoreWeave Images to a Writable PVC](virtual-servers/root-disk-lifecycle-management/exporting-coreweave-images-to-a-writable-pvc.md)
  * [Using Hashicorp Packer to create and update OS Images](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/README.md)
    * [Creating a Packer Worker Virtual Server](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/creating-a-packer-worker-virtual-server.md)
    * [Configuring a Windows Image sourced from CoreWeave Cloud](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-windows-image-sourced-from-coreweave-cloud.md)
    * [Configuring a Linux image sourced from CoreWeave Cloud](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-linux-image-sourced-from-coreweave-cloud.md)
    * [Configuring an externally sourced cloud Linux image](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-an-externally-sourced-cloud-linux-image.md)
  * [Exporting images to QCOW2](virtual-servers/root-disk-lifecycle-management/exporting-images-to-qcow2.md)
* [Examples](virtual-servers/examples/README.md)
  * [Provision an Active Directory Domain Controller](virtual-servers/examples/provision-an-active-directory-domain-controller.md)

## Solutions

* [VFX](solutions/vfx/README.md)
  * [Deadline](solutions/vfx/deadline.md)
  * [On-Premise Integration](solutions/vfx/on-premise-integration/README.md)
    * [CloudLink on Linux](solutions/vfx/on-premise-integration/linux.md)
    * [Synology NAS](solutions/vfx/on-premise-integration/synology-nas.md)
* [Virtual Workstations](solutions/virtual-workstations.md)

## Resources

* [Resource Based Pricing](resources/resource-based-pricing.md)
* [Terms of Service](resources/terms-of-service.md)

