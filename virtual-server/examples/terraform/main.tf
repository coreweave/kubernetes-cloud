provider "kubernetes" {
  config_path = var.kubeconfig_path
}
resource "random_string" "vs_generate_password" {
  count            = var.vs_generate_password ? 1 : 0
  length           = 16
  special          = true
  override_special = "_%@"
}
