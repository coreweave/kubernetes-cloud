---
description: Deploying and managing Virtual Servers with Terraform
---

# Terraform

Virtual Servers are a Kubernetes Custom Resource available on CoreWeave Cloud, and as such, the [Kubernetes Terraform provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) can be used to create and modify the resource. The Virtual Server Terraform plan used in the following example is available in the [examples](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform) section of the CoreWeave Cloud repository.

### Configuring a Virtual Server

In the environment's Terraform variables, or the root module's `terraform.tfvars` file, the following options can be set. If a variable does not have a default value, one must be provided.

| Variable                 | Type   | Description                                                                                                              | Has Default |
| ------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------ | ----------- |
| kubeconfig\_path         | string | System path to a kubeconfig file                                                                                         | true        |
| user\_namespace          | string | Namespace the virtualserver will be deployed to                                                                          | false       |
| vs\_name                 | string | Hostname for the virtual server                                                                                          | true        |
| vs\_username             | string | Username for the virtual server                                                                                          | false       |
| vs\_generate\_password   | bool   | Set to true to generate a strong password                                                                                | true        |
| vs\_password             | string | With vs\_generate\_password set to false, provide a password for vs\_username                                            | true        |
| vs\_memory               | string | Memory requested in Gi (i.e. 16Gi)                                                                                       | true        |
| vs\_root\_storage        | string | Storage requested for root volume in Gi (i.e. 80Gi)                                                                      | true        |
| vs\_os\_type             | string | Virtual Server OS variant (i.e. linux)                                                                                   | true        |
| vs\_image                | string | OS image deployed to virtual server                                                                                      | true        |
| vs\_gpu                  | string | GPU model name for virtual server                                                                                        | true        |
| vs\_gpu\_enable          | bool   | Enable a GPU for this this virtual server                                                                                | true        |
| vs\_gpu\_count           | int    | Number of GPUs requested                                                                                                 | true        |
| vs\_cpu\_count           | int    | Number of CPUs requested                                                                                                 | true        |
| vs\_region               | string | Region to deploy server to                                                                                               | true        |
| vs\_running              | bool   | Start virtual server once deployed                                                                                       | true        |
| vs\_public\_networking   | bool   | Enable public networking                                                                                                 | true        |
| vs\_attach\_loadbalancer | bool   | Attach Service Load Balancer IP directly to Virtual Server (vs\_tcp\_ports and vs\_udp\_ports must be empty, if enabled) | true        |
| vs\_tcp\_ports           | list   | List of TCP ports to allow access to                                                                                     | true        |
| vs\_udp\_ports           | list   | List of UDP ports to allow access to                                                                                     | true        |

### Deploying a Virtual Server

With the [Virtual Server module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform) cloned, a Virtual Server can either be created by running the module directly:

```bash
$ terraform init
$ terraform plan
$ terraform apply -auto-approve
```

with a `terraform.tfvars` file in that root module, or if managing a fleet of virtual servers, ideally can be consumed by new module definitions for each machine, or by other modules using the above exportable attributes along side a copy of the [root module's variables](../../virtual-server/examples/terraform/variables.tf):

```
module "virtualserver_1" {
  source               = "./coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform"
  kubeconfig_path      = var.kubeconfig_path
  vs_name              = var.vs_name
  vs_username          = var.vs_username
  vs_generate_password = var.vs_generate_password
  user_namespace       = var.user_namespace
}
```

repeating this definition for additional machines, and then managing each virtual machine as targets:

```bash
$ terraform plan -target=module.virtualserver_1
$ terraform apply -target=module.virtualserver_1 -auto-approve
$ terraform destroy -target=module.virtualserver_1
```

The status of the machine can be verified via `kubectl`:

```
$ kubectl get vs example-vs
NAME                STATUS               REASON                                           STARTED   INTERNAL IP      EXTERNAL IP
example-vs          Initializing         Waiting for VirtualMachineInstance to be ready   False                      123.123.123.123
```

which will include the Service External IP address for accessing the server as well.

### Outputs

As shown in the example above, this module has two referencable output values that can be used as attributes:

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

vs_network = "[address]"
vs_password = "[password]"
```

which will include the Service IP address and, either, the password provided, or the one generated by Terraform, as the attrbitues `vs_network` and `vs_password` that can be referenced, for example, as outputs:

```
output "vs_network" {
  value = module.virtualserver_1.vs_network
}

output "vs_password" {
  value = module.virtualserver_1.vs_password
}
```

or to manage as values for other new or existing modules to use.
