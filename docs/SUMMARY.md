# Table of contents

* [CoreWeave Cloud](README.md)
* [Data Center Regions](data-center-regions.md)
* [Release Notes](release-notes.md)

## CoreWeave Kubernetes

* [Get Started with CoreWeave](coreweave-kubernetes/getting-started/README.md)
  * [Applications Catalog](coreweave-kubernetes/getting-started/applications-catalog.md)
* [Serverless](coreweave-kubernetes/serverless.md)
* [Exposing Applications](coreweave-kubernetes/exposing-applications.md)
* [Useful Commands](../coreweave-kubernetes/useful-commands.md)
* [Node Types](../coreweave-kubernetes/node-types.md)
* [Advanced Label Selectors](../coreweave-kubernetes/label-selectors.md)
* [CoSchedulers](coreweave-kubernetes/coschedulers.md)
* [Metrics](../coreweave-kubernetes/prometheus/README.md)
  * [Grafana](../coreweave-kubernetes/prometheus/grafana.md)
  * [Useful Metrics](../coreweave-kubernetes/prometheus/useful-metrics.md)
  * [Logging](coreweave-kubernetes/prometheus/logging.md)
* [Examples](../coreweave-kubernetes/examples/README.md)
  * [Jupyter Notebook with TensorFlow](../coreweave-kubernetes/examples/tensorflow-jupyter.md)
  * [SSH Server with CUDA](../coreweave-kubernetes/examples/cuda-ssh.md)

## Networking

* [Get Started with Networking](networking/getting-started-with-networking.md)
* [CoreWeave Cloud Native Networking (CCNN)](networking/coreweave-cloud-native-networking-ccnn.md)
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

* [Get Started with Storage](storage/storage/README.md)
  * [Using Storage - Cloud UI](storage/storage/using-storage-cloud-ui.md)
  * [Using Storage - Kubectl](storage/storage/using-storage-kubectl.md)
* [FileBrowser](storage/filebrowser.md)
* [Object Storage](storage/object-storage.md)

## Virtual Servers

* [Get Started with Virtual Servers](../virtual-servers/getting-started.md)
* [Deployment Methods](../virtual-servers/deployment-methods/README.md)
  * [CoreWeave Cloud UI](../virtual-servers/deployment-methods/coreweave-apps.md)
  * [Kubernetes CLI](virtual-servers/deployment-methods/kubectl.md)
  * [Terraform](../virtual-servers/deployment-methods/terraform.md)
  * [Programmatic Deployment](../virtual-servers/deployment-methods/programmatically/README.md)
    * [Bash](virtual-servers/deployment-methods/programmatically/bash.md)
    * [Python](../virtual-servers/deployment-methods/programmatically/python.md)
    * [NodeJS](../virtual-servers/deployment-methods/programmatically/nodejs.md)
    * [Golang](../virtual-servers/deployment-methods/programmatically/golang.md)
* [Configuration Options](virtual-servers/virtual-server-configuration-options/README.md)
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
  * [Importing Disk Images](virtual-servers/root-disk-lifecycle-management/importing-a-qcow2-image.md)
  * [Cloning block volumes](virtual-servers/root-disk-lifecycle-management/cloning-block-volumes.md)
* [CoreWeave System Images](virtual-servers/coreweave-system-images/README.md)
  * [Windows Images](virtual-servers/coreweave-system-images/windows-images.md)
  * [Linux Images](virtual-servers/coreweave-system-images/linux-images.md)
* [Tips and Tricks for VDIs](virtual-servers/tips-and-tricks-for-vdis.md)
* [Examples](../virtual-servers/examples/README.md)
  * [Active Directory Environment hosted on CoreWeave Cloud](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/README.md)
    * [Provision an Active Directory Domain](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/provision-an-active-directory-domain-controller.md)
    * [Highly Available Storage using Samba-AD and AD DFS](virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/highly-available-storage-using-samba-ad-and-ad-dfs.md)
  * [CentOS 7 Virtual Server with LUKS Encryption](virtual-servers/examples/centos-7-virtual-server-with-luks-encryption.md)

## Inference <a href="#compass" id="compass"></a>

* [Get Started with Inference](../compass/online-inference.md)
* [NVIDIA HGX H100](compass/nvidia-hgx-h100.md)
* [Inference Examples](../compass/examples/README.md)
  * [PyTorch Hugging Face Diffusers - Stable Diffusion Text to Image](compass/examples/pytorch-hugging-face-diffusers-stable-diffusion-text-to-image.md)
  * [PyTorch Hugging Face Transformers Accelerate - BigScience BLOOM](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom.md)
  * [PyTorch Hugging Face Transformers DeepSpeed - BigScience BLOOM](compass/examples/pytorch-hugging-face-transformers-bigscience-bloom-1.md)
  * [JAX - DALL-E Mini / Mega](compass/examples/jax-dall-e-mini-mega.md)
  * [Triton Inference Server - FasterTransformer GPT-J and GPT-NeoX 20B](compass/examples/triton-inference-server-fastertransformer.md)
  * [TensorFlow - Open AI GPT-2](../compass/examples/gpt-2/README.md)
    * [Exporting with Jupyter](compass/examples/gpt-2/jupyter-pvc.md)
    * [PVC Model Serving](compass/examples/gpt-2/service-pvc.md)
    * [Transformer](../compass/examples/gpt-2/transformer.md)
    * [S3 Model Serving](compass/examples/gpt-2/service-s3.md)
  * [TensorFlow2 - Image Classifier](../compass/examples/tensorflow2-image-classifier.md)
  * [PyTorch - GPT-2 AITextgen](../compass/examples/custom-pytorch-aitextgen.md)
  * [PyTorch - FastAI Sentiment](../compass/examples/custom-sentiment.md)
  * [Custom - BASNET](../compass/examples/custom-basnet.md)
* [One-Click Models](../compass/models/README.md)
  * [GPT-J-6B](../compass/models/gpt-j-6b.md)
* [Finetuning Machine Learning Models](compass/finetuning-machine-learning-models.md)
* [Finetuning Image Generation Models](compass/finetuning-image-generation-models.md)
* [Determined AI](compass/determined-ai/README.md)
  * [Install Determined AI](compass/determined-ai/install-determined-ai.md)
  * [Shell for Machine Learning on Determined AI](compass/determined-ai/shell-for-machine-learning-on-determined-ai.md)
  * [Launch Jupyter Notebook on CoreWeave via Determined AI](compass/determined-ai/launch-jupyter-notebook-on-coreweave-via-determined-ai.md)
  * [Finetune GPT-NeoX 20B using DeterminedAI](compass/determined-ai/gpt-neox.md)
  * [Launch GPT DeepSpeed Models using DeterminedAI](compass/determined-ai/launch-gpt-deepspeed-models-using-determinedai.md)
  * [Finetuning HuggingFace LLMs with Determined AI and DeepSpeed](compass/determined-ai/finetuning-huggingface-llms-with-determined-ai-and-deepspeed.md)

## Workflows

* [Get Started with Workflows](../workflows/argo.md)
* [Examples](workflows/examples/README.md)
  * [CGI Rendering Using Workflows](../workflows/examples/cgi-rendering.md)

## VFX & Rendering

* [Get Started with VFX Studios](vfx-and-rendering/vfx/README.md)
  * [Managed Thinkbox Deadline](vfx-and-rendering/vfx/deadline.md)
  * [On-Premise Integrations](vfx-and-rendering/vfx/on-premise-integration/README.md)
    * [CoreWeave CloudLink on Linux](vfx-and-rendering/vfx/on-premise-integration/linux.md)
    * [Synology NAS](vfx-and-rendering/vfx/on-premise-integration/synology-nas.md)

***

* [CoreWeave VFX Cloud Studio Reference Guide](cloud-studio-reference-guide/README.md)
  * [Virtual Workstations](cloud-studio-reference-guide/virtual-workstations.md)
  * [Rendering](cloud-studio-reference-guide/vfx-studio-components-guide.md)
  * [Storage](cloud-studio-reference-guide/storage.md)
  * [Networking](cloud-studio-reference-guide/networking.md)
  * [Management](cloud-studio-reference-guide/management.md)

## Cloud Account Management

* [Organizations](cloud-account-management/organizations.md)
* [Namespace Management](cloud-account-management/namespace-management.md)
* [Billing Portal](cloud-account-management/billing-portal.md)

## Security

* [CoreWeave Vulnerability Disclosure Policy](security/coreweave-vulnerability-disclosure-policy.md)
* [Information Security Advisories](security/information-security-advisories.md)

## Resources

* [Resource Based Pricing](../resources/resource-based-pricing.md)
* [Terms of Service](../resources/terms-of-service/README.md)
  * [Data Processing Agreement](../resources/terms-of-service/data-protection-agreement.md)
  * [Acceptable Use Policy](../resources/terms-of-service/acceptable-use-policy.md)
  * [Privacy Policy](../resources/terms-of-service/privacy-policy.md)
  * [Terms of Use](resources/terms-of-service/terms-of-use.md)
  * [Security & Compliance](../resources/terms-of-service/security-and-compliance.md)
  * [Maintenance Policy](../resources/terms-of-service/maintenance-policy.md)
