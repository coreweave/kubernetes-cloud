output "vs_network" {
  value = data.kubernetes_service.vs_loadbalancer.status.0.load_balancer.0.ingress.0.ip
}

output "vs_password" {
  value = var.vs_generate_password ? random_string.vs_generate_password[0].result : var.vs_password
}
