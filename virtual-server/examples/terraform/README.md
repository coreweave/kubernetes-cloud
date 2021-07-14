# Deploying VirtualServers to Kubernetes with Terraform

This [terraform](terraform.io) module uses the [kubernetes provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) to deploy `VirtualServers` (Virtual Desktops) to [CoreWeave Cloud](coreweave.io).

## Setup

This module requires your `user_namespace`, `kubeconfig_path`, your desired desktop `vdi_username` (and you can optionally supply `vdi_password` or set `vdi_password_generate` to `true`), `vdi_image` (defaults to Ubuntu 20.04), `vdi_gpu_enable` (and `vdi_gpu_count`), and your desired `vdi_name` to set your system hostname.

## Installation

Run:

```bash
terraform plan
terraform apply -auto-approve
```

This module will output the network and credential information for the system, consumable by another module via the `network` and `password` attributes.

## Examples

In the `examples/` directory is a sample Terraform plan that demonstrates consuming the module to create two VDI instances.
