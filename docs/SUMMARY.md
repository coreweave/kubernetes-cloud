# Table of contents

* [CoreWeave Cloud](README.md)
* [Data Center Regions](data-center-regions.md)
* [Release Notes](release-notes.md)

## CoreWeave Kubernetes

* [Getting Started](../coreweave-kubernetes/getting-started.md)
* [Useful Commands](../coreweave-kubernetes/useful-commands.md)
* [Node Types](../coreweave-kubernetes/node-types.md)
* [Advanced Label Selectors](../coreweave-kubernetes/label-selectors.md)
* [Networking](../coreweave-kubernetes/networking/README.md)
* [Serverless](../coreweave-kubernetes/serverless.md)
* [Metrics](../coreweave-kubernetes/prometheus/README.md)
  * [Grafana](../coreweave-kubernetes/prometheus/grafana.md)
  * [Useful Metrics](../coreweave-kubernetes/prometheus/useful-metrics.md)
  * [Logging](coreweave-kubernetes/prometheus/logging.md)
* [Examples](../coreweave-kubernetes/examples/README.md)
  * [Jupyter Notebook with TensorFlow](../coreweave-kubernetes/examples/tensorflow-jupyter.md)
  * [SSH Server with CUDA](../coreweave-kubernetes/examples/cuda-ssh.md)

## Networking

* [Getting Started with Networking](networking/getting-started-with-networking.md)
* [CoreWeave Cloud Native Networking (CCNN)](coreweave-kubernetes/networking/coreweave-cloud-native-networking-ccnn.md)
  * [Exposing Applications](networking/layer-2-vpc-l2vpc/exposing-applications.md)
* [Layer 2 VPC (L2VPC)](coreweave-kubernetes/networking/layer-2-vpc-l2vpc/README.md)
  * [L2VPC Usage](networking/layer-2-vpc-l2vpc/l2vpc-usage.md)
  * [DHCP on L2VPC](coreweave-kubernetes/networking/layer-2-vpc-l2vpc/dhcp-on-l2vpc.md)
  * [Virtual Firewalls](networking/layer-2-vpc-l2vpc/virtual-firewalls/README.md)
    * [Fortinet](networking/layer-2-vpc-l2vpc/virtual-firewalls/fortinet.md)
* [Site-to-Site Connections](coreweave-kubernetes/networking/site-to-site-connections/README.md)
  * [Site-to-Site VPN](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/README.md)
    * [VPN Setup](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/vpn-setup.md)
    * [Examples](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/examples/README.md)
      * [AWS](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/examples/aws.md)
      * [Fortinet](coreweave-kubernetes/networking/site-to-site-connections/site-to-site-vpn/examples/fortinet.md)
  * [Direct Connect](coreweave-kubernetes/networking/site-to-site-connections/direct-connections.md)
* [HPC Interconnect](coreweave-kubernetes/networking/hpc-interconnect.md)
* [Bring Your Own IP](coreweave-kubernetes/networking/bring-your-own-ip.md)

## Storage

* [Getting Started with Storage](storage/storage.md)
* [Object Storage](storage/object-storage.md)

## Virtual Servers

* [Getting Started with Virtual Servers](../virtual-servers/getting-started.md)
* [Virtual Server Deployment Methods](../virtual-servers/deployment-methods/README.md)
  * [CoreWeave Cloud UI](../virtual-servers/deployment-methods/coreweave-apps.md)
  * [Kubernetes CLI](virtual-servers/deployment-methods/kubectl.md)
  * [Terraform](../virtual-servers/deployment-methods/terraform.md)
  * [Programmatic Deployment](../virtual-servers/deployment-methods/programmatically/README.md)
    * [Bash](virtual-servers/deployment-methods/programmatically/bash.md)
    * [Python](../virtual-servers/deployment-methods/programmatically/python.md)
    * [NodeJS](../virtual-servers/deployment-methods/programmatically/nodejs.md)
    * [Golang](../virtual-servers/deployment-methods/programmatically/golang.md)
* [Virtual Server Configuration Options](virtual-servers/virtual-server-configuration-options/README.md)
  * [Region, Hardware & Firmware](virtual-servers/virtual-server-configuration-options/region-hardware-and-firmware.md)
  * [Operating System & Root Disk](virtual-servers/virtual-server-configuration-options/operating-system-and-root-disk.md)
  * [Storage](virtual-servers/virtual-server-configuration-options/storage.md)
  * [User Accounts](virtual-servers/virtual-server-configuration-options/user-accounts.md)
  * [Networking](virtual-servers/virtual-server-configuration-options/networking.md)
  * [Cloud-init](virtual-servers/virtual-server-configuration-options/cloud-init.md)
  * [Node Affinity](virtual-servers/virtual-server-configuration-options/node-affinity.md)
  * [Additional Features](virtual-servers/virtual-server-configuration-options/additional-features.md)
* [Remote Access and Control](../virtual-servers/remote-access-and-control.md)
* [Root Disk Lifecycle Management](../virtual-servers/root-disk-lifecycle-management/README.md)
  * [Expanding Disks](../virtual-servers/root-disk-lifecycle-management/expanding-disks.md)
  * [Manually creating a Virtual Server base image](../virtual-servers/root-disk-lifecycle-management/creating-a-virtual-server-base-image.md)
  * [Copying CoreWeave Images to a Writable PVC](../virtual-servers/root-disk-lifecycle-management/exporting-coreweave-images-to-a-writable-pvc.md)
  * [Using Hashicorp Packer to create and update OS Images](../virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/README.md)
    * [Creating a Packer Worker Virtual Server](../virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/creating-a-packer-worker-virtual-server.md)
    * [Configuring a Windows Image sourced from CoreWeave Cloud](../virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-windows-image-sourced-from-coreweave-cloud.md)
    * [Configuring a Linux image sourced from CoreWeave Cloud](../virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-a-linux-image-sourced-from-coreweave-cloud.md)
    * [Configuring an externally sourced cloud Linux image](../virtual-servers/root-disk-lifecycle-management/using-packer-to-create-and-update-os-images/configuring-an-externally-sourced-cloud-linux-image.md)
  * [Exporting images to QCOW2](../virtual-servers/root-disk-lifecycle-management/exporting-images-to-qcow2.md)
  * [Importing a QCOW2 image](virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md)
  * [Cloning block volumes](virtual-servers/root-disk-lifecycle-management/cloning-block-volumes.md)
* [CoreWeave System Images](virtual-servers/coreweave-system-images/README.md)
  * [Windows Images](virtual-servers/coreweave-system-images/windows-images.md)
  * [Linux Images](virtual-servers/coreweave-system-images/linux-images.md)
* [Examples](../virtual-servers/examples/README.md)
  * [Active Directory Environment hosted on CoreWeave Cloud](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/README.md)
    * [Provision an Active Directory Domain](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/provision-an-active-directory-domain-controller.md)
    * [Highly Available Storage using Samba-AD and AD DFS](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/highly-available-storage-using-samba-ad-and-ad-dfs.md)
  * [CentOS 7 Virtual Server with LUKS Encryption](virtual-servers/examples/centos-7-virtual-server-with-luks-encryption.md)

## Inference <a href="#compass" id="compass"></a>

* [Inference on the Cloud](../compass/online-inference.md)
* [One-Click Models](../compass/models/README.md)
  * [GPT-J-6B](../compass/models/gpt-j-6b.md)
* [Finetuning Machine Learning Models](compass/finetuning-machine-learning-models.md)
* [Finetuning GPT-NeoX 20B using DeterminedAI](compass/gpt-neox.md)
* [Inference Examples](../compass/examples/README.md)
  * [PyTorch Hugging Face Diffusers - Stable Diffusion Text to Image](compass/examples/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md)
  * [PyTorch Hugging Face Transformers Accelerate - BigScience BLOOM](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom.md)
  * [PyTorch Hugging Face Transformers DeepSpeed - BigScience BLOOM](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1.md)
  * [JAX - DALL-E Mini / Mega](compass/examples/jax-dall-e-mini-mega.md)
  * [Triton Inference Server - FasterTransformer GPT-J](compass/examples/triton-inference-server-fastertransformer.md)
  * [TensorFlow - Open AI GPT-2](../compass/examples/gpt-2/README.md)
    * [Transformer](../compass/examples/gpt-2/transformer.md)
    * [Exporting with Jupyter](../compass/examples/gpt-2/jupyter-pvc.md)
    * [S3 Model Serving](../compass/examples/gpt-2/service-s3.md)
    * [PVC Model Serving](../compass/examples/gpt-2/service-pvc.md)
  * [TensorFlow2 - Image Classifier](../compass/examples/tensorflow2-image-classifier.md)
  * [PyTorch - GPT-2 AITextgen](../compass/examples/custom-pytorch-aitextgen.md)
  * [PyTorch - FastAI Sentiment](../compass/examples/custom-sentiment.md)
  * [Custom - BASNET](../compass/examples/custom-basnet.md)

## Workflows

* [Getting Started](../workflows/argo.md)
* [Examples](workflows/examples/README.md)
  * [CGI Rendering Using Workflows](../workflows/examples/cgi-rendering.md)

## Solutions

* [VFX](../solutions/vfx/README.md)
  * [Deploying Managed Deadline](../solutions/vfx/deadline.md)
  * [On-Premise Integration](../solutions/vfx/on-premise-integration/README.md)
    * [CloudLink on Linux](../solutions/vfx/on-premise-integration/linux.md)
    * [Synology NAS](../solutions/vfx/on-premise-integration/synology-nas.md)
  * [VFX Studio Components Guide](../solutions/vfx/vfx-studio-components-guide.md)
  * [Cloud Studio Reference Guide](../solutions/vfx/cloud-studio-reference-guide.md)

## Cloud Account Management

* [Organizations](cloud-account-management/organizations.md)
* [Billing Portal](cloud-account-management/billing-portal.md)

## Resources

* [Resource Based Pricing](../resources/resource-based-pricing.md)
* [Terms of Service](../resources/terms-of-service/README.md)
  * [Data Processing Agreement](../resources/terms-of-service/data-protection-agreement.md)
  * [Acceptable Use Policy](../resources/terms-of-service/acceptable-use-policy.md)
  * [Privacy Policy](../resources/terms-of-service/privacy-policy.md)
  * [Security & Compliance](../resources/terms-of-service/security-and-compliance.md)
  * [Maintenance Policy](../resources/terms-of-service/maintenance-policy.md)
