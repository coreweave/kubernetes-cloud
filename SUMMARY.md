# Table of contents

* [CoreWeave Cloud](README.md)

## CoreWeave Kubernetes

* [Getting Started](coreweave-kubernetes/getting-started.md)
* [Useful Commands](coreweave-kubernetes/useful-commands.md)
* [Node Types](coreweave-kubernetes/node-types.md)
* [Advanced Label Selectors](coreweave-kubernetes/label-selectors.md)
* [Storage](coreweave-kubernetes/storage.md)
* [Networking](coreweave-kubernetes/networking/README.md)
  * [Exposing Applications](coreweave-kubernetes/networking/exposing-applications.md)
  * [Bring Your Own IP](coreweave-kubernetes/networking/bring-your-own-ip.md)
* [Serverless](coreweave-kubernetes/serverless.md)
* [Metrics](coreweave-kubernetes/prometheus/README.md)
  * [Grafana](coreweave-kubernetes/prometheus/grafana.md)
  * [Useful Metrics](coreweave-kubernetes/prometheus/useful-metrics.md)
* [Examples](coreweave-kubernetes/examples/README.md)
  * [Jupyter Notebook with TensorFlow](coreweave-kubernetes/examples/tensorflow-jupyter.md)
  * [SSH Server with CUDA](coreweave-kubernetes/examples/cuda-ssh.md)

## Virtual Servers

* [Getting Started](virtual-servers/getting-started.md)
* [Deployment Methods](virtual-servers/deployment-methods/README.md)
  * [CoreWeave Apps Web UI](virtual-servers/deployment-methods/coreweave-apps.md)
  * [CLI](docs/virtual-servers/deployment-methods/kubectl.md)
  * [Terraform](virtual-servers/deployment-methods/terraform.md)
  * [Programmatically](virtual-servers/deployment-methods/programmatically/README.md)
    * [Python](virtual-servers/deployment-methods/programmatically/python.md)
    * [NodeJS](virtual-servers/deployment-methods/programmatically/nodejs.md)
    * [Golang](virtual-servers/deployment-methods/programmatically/golang.md)
* [Remote Access and Control](virtual-servers/remote-access-and-control.md)
* [Root Disk Lifecycle Management](virtual-servers/root-disk-lifecycle-management/README.md)
  * [Expanding Disks](virtual-servers/root-disk-lifecycle-management/expanding-disks.md)
  * [Manually creating a Virtual Server base image](virtual-servers/root-disk-lifecycle-management/creating-a-virtual-server-base-image.md)
  * [Copying CoreWeave Images to a Writable PVC](virtual-servers/root-disk-lifecycle-management/exporting-coreweave-images-to-a-writable-pvc.md)
  * [Using Hashicorp Packer to create and update OS Images](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/README.md)
    * [Creating a Packer Worker Virtual Server](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/creating-a-packer-worker-virtual-server.md)
    * [Configuring a Windows Image sourced from CoreWeave Cloud](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-windows-image-sourced-from-coreweave-cloud.md)
    * [Configuring a Linux image sourced from CoreWeave Cloud](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-linux-image-sourced-from-coreweave-cloud.md)
    * [Configuring an externally sourced cloud Linux image](virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-an-externally-sourced-cloud-linux-image.md)
  * [Exporting images to QCOW2](virtual-servers/root-disk-lifecycle-management/exporting-images-to-qcow2.md)
  * [Importing a QCOW2 image](virtual-servers/page-1.md)
* [CoreWeave System Images](virtual-servers/coreweave-system-images/README.md)
  * [Windows Images](virtual-servers/coreweave-system-images/windows-images.md)
* [Examples](virtual-servers/examples/README.md)
  * [Active Directory Environment hosted on CoreWeave Cloud](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/README.md)
    * [Provision an Active Directory Domain](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/provision-an-active-directory-domain-controller.md)
    * [Highly Available Storage using Samba-AD and AD DFS](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/highly-available-storage-using-samba-ad-and-ad-dfs.md)

## Inference <a href="#compass" id="compass"></a>

* [Online Inference Serving](compass/online-inference.md)
* [One Click Models](compass/models/README.md)
  * [GPT-J-6B](compass/models/gpt-j-6b.md)
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
* [Examples](docs/workflows/examples/README.md)
  * [CGI Rendering](workflows/examples/cgi-rendering.md)

## Solutions

* [VFX](solutions/vfx/README.md)
  * [Deploying Managed Deadline](solutions/vfx/deadline.md)
  * [On-Premise Integration](solutions/vfx/on-premise-integration/README.md)
    * [CloudLink on Linux](solutions/vfx/on-premise-integration/linux.md)
    * [Synology NAS](solutions/vfx/on-premise-integration/synology-nas.md)
    * [Direct Connections](solutions/vfx/on-premise-integration/direct-connections.md)
  * [VFX Studio Components Guide](solutions/vfx/vfx-studio-components-guide.md)
  * [Cloud Studio Reference Guide](solutions/vfx/cloud-studio-reference-guide.md)
* [Virtual Workstations](solutions/virtual-workstations.md)

## Cloud

* [Organization Management](cloud/organization-management.md)

## Resources

* [Resource Based Pricing](resources/resource-based-pricing.md)
* [Terms of Service](resources/terms-of-service/README.md)
  * [Data Protection Agreement](resources/terms-of-service/data-protection-agreement.md)
  * [Acceptable Use Policy](resources/terms-of-service/acceptable-use-policy.md)
  * [Privacy Policy](resources/terms-of-service/privacy-policy.md)
  * [Security & Compliance](resources/terms-of-service/security-and-compliance.md)
  * [Maintenance Policy](resources/terms-of-service/maintenance-policy.md)
