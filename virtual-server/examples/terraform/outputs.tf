output "vdi_network" {
  sensitive = true
  value     = kubernetes_manifest.virtualdesktop
}

output "vdi_password" {
  sensitive = true
  value     = var.vdi_generate_password ? random_password.vdi_generate_password[0].result : var.vdi_password
}
