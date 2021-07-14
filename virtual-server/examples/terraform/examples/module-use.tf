variable "kubeconfig_path" {}
variable "vdi_name" {}
variable "vdi_username" {}
variable "vdi_generate_password" {
  default = true
}
variable "user_namespace" {}

module "virtualdesktop_1" {

  source = "../"

  kubeconfig_path       = var.kubeconfig_path
  vdi_name              = "hostOne"
  vdi_username          = "onePerson"
  vdi_generate_password = var.vdi_generate_password
  user_namespace        = var.user_namespace
}

module "virtualdesktop_2" {

  source = "../"

  kubeconfig_path       = var.kubeconfig_path
  vdi_name              = "hostTwo"
  vdi_username          = "secondPerson"
  vdi_generate_password = var.vdi_generate_password
  user_namespace        = var.user_namespace
}

output "vdi_one_info" {
  value = module.virtualdesktop_1.vdi_network
}

output "vdi_two_info" {
  value = module.virtualdesktop_1.vdi_network
}
