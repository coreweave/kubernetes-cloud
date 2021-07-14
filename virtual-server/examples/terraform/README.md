# Deploying Virtual Servers to Kubernetes with Terraform

This [terraform](terraform.io) module uses the [kubernetes provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) to deploy `VirtualServers` to [CoreWeave Cloud](coreweave.com).

## Setup

This module requires your `user_namespace`, `kubeconfig_path`, your desired desktop `vs_username` (and you can optionally supply `vs_password` or set `vs_password_generate` to `true`), `vs_image` (defaults to Ubuntu 20.04), `vs_gpu_enable` (and `vs_gpu_count`), and your desired `vs_name` to set your system hostname.

## Installation

Run:

```bash
terraform plan
terraform apply -auto-approve
```

This module will output the network and credential information for the system, consumable by another module via the `network` and `password` attributes.

## Examples

In the `examples/` directory is a sample Terraform plan that demonstrates consuming the module to create two Virtual Server instances.
