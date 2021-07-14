output "vs_network" {
  sensitive = true
  value     = kubernetes_manifest.virtualdesktop
}

output "vs_password" {
  sensitive = true
  value     = var.vs_generate_password ? random_password.vs_generate_password[0].result : var.vs_password
}
