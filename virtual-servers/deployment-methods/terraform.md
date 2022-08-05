---
description: Deploying and managing Virtual Servers with Terraform
---

# Terraform

Virtual Servers are a [Kubernetes Custom Resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) on CoreWeave Cloud, which means the [Kubernetes Terraform provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) can be used to create and modify Virtual Servers as Custom Resources.

{% hint style="info" %}
**Note**

You can view **** the Virtual Server Terraform plan used in the following example, and learn more about the Terraform configurations, in [the examples section](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform) of the CoreWeave Cloud repository.
{% endhint %}

## Deploying a Virtual Server using Terraform

The following table describes all fields exposed through the Terraform module.

| Field name               | Field type | Description                                                                                                              |
| ------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `kubeconfig_path`        | string     | System path to a kubeconfig file                                                                                         |
| `user_namespace`         | string     | Namespace the virtualserver will be deployed to                                                                          |
| `vs_name`                | string     | Hostname for the virtual server                                                                                          |
| `vs_username`            | string     | Username for the virtual server                                                                                          |
| `vs_generate_password`   | boolean    | Set to true to generate a strong password                                                                                |
| `vs_password`            | string     | If `vs_generate_password` is set to false, provide a password for `vs_username`                                          |
| `vs_memory`              | string     | Memory requested in Gi (i.e. 16Gi)                                                                                       |
| `vs_root_storage`        | string     | Storage requested for root volume in Gi (i.e. 80Gi)                                                                      |
| `vs_os_type`             | string     | Virtual Server OS variant (i.e. linux)                                                                                   |
| `vs_image`               | string     | OS image deployed to virtual server                                                                                      |
| `vs_gpu`                 | string     | GPU model name for virtual server                                                                                        |
| `vs_gpu_enable`          | boolean    | Enable a GPU for this this virtual server                                                                                |
| `vs_gpu_count`           | integer    | Number of GPUs requested                                                                                                 |
| `vs_cpu_count`           | integer    | Number of CPUs requested                                                                                                 |
| `vs_region`              | string     | Data center region in which to deploy the Virtual Server                                                                 |
| `vs_running`             | boolean    | Whether or not to start the Virtual Server once deployed                                                                 |
| `vs_public_networking`   | boolean    | Whether or not to enable public networking                                                                               |
| `vs_attach_loadbalancer` | boolean    | Attach Service Load Balancer IP directly to Virtual Server (`vs_tcp_ports` and `vs_udp_ports` must be empty, if enabled) |
| `vs_tcp_ports`           | list       | List of TCP ports to allow access to                                                                                     |
| `vs_udp_ports`           | list       | List of UDP ports to allow access to                                                                                     |

With the [Virtual Server module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform) cloned and the configurations adjusted to your preferences, a Virtual Server can either be created by running the module directly:

```bash
$ terraform init
$ terraform plan
$ terraform apply -auto-approve
```

Or, if managing a fleet of Virtual Servers, then ideally their outputs can be consumed by new module definitions for each machine, or by other modules.

#### Example

```
module "virtualserver_1" {
  source               = "./coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform"
  kubeconfig_path      = "./kube/config/kubeconfig"
  vs_name              = "myserver"
  vs_username          = "myuser"
  vs_generate_password = "true"
  user_namespace       = "mynamespace"
}
```

Repeating a single definition for additional machines, then managing each Virtual Server, can be done by using the `target` option:

```bash
$ terraform plan -target=module.virtualserver_1
$ terraform apply -target=module.virtualserver_1 -auto-approve
$ terraform destroy -target=module.virtualserver_1
```

Once deployed, the status of the new machine can be verified using `kubectl`:

```
$ kubectl get vs example-vs

NAME                STATUS               REASON                                           STARTED   INTERNAL IP      EXTERNAL IP
example-vs          Initializing         Waiting for VirtualMachineInstance to be ready   False                      123.123.123.123
```

{% hint style="info" %}
**Note**

The output of this command will include the Service External IP address for accessing the server.
{% endhint %}

### Output variables

As shown in the example above, this module has two output values that can be referenced as attributes by other modules.

#### Example

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

vs_network = "[address]"
vs_password = "[password]"
```

This will include the Service IP address and either the provided password or the one generated by Terraform as `vs_network` and `vs_password`, which can be referenced, for example, as outputs:

```
output "vs_network" {
  value = module.virtualserver_1.vs_network
}

output "vs_password" {
  value = module.virtualserver_1.vs_password
}
```
