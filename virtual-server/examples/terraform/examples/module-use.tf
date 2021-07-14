variable "kubeconfig_path" {}
variable "vs_name" {}
variable "vs_username" {}
variable "vs_generate_password" {
  default = true
}
variable "user_namespace" {}

module "virtualserver_1" {

  source = "../"

  kubeconfig_path      = var.kubeconfig_path
  vs_name              = "hostOne"
  vs_username          = "onePerson"
  vs_generate_password = var.vs_generate_password
  user_namespace       = var.user_namespace
}

module "virtualserver_2" {

  source = "../"

  kubeconfig_path      = var.kubeconfig_path
  vs_name              = "hostTwo"
  vs_username          = "secondPerson"
  vs_generate_password = var.vs_generate_password
  user_namespace       = var.user_namespace
}

output "vs_one_info" {
  value = module.virtualserver_1.vs_network
}

output "vs_two_info" {
  value = module.virtualserver_2.vs_network
}
