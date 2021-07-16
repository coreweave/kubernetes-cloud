variable "kubeconfig_path" {
  description = "Path to kubeconfig"
  default     = "~/.kube/config"
}

variable "user_namespace" {
  description = "Namespace Virtual Server will be installed to"
}

variable "vs_name" {
  description = "Virtual Server hostname"
  default     = "MY-VS"
}

variable "vs_username" {
  description = "Virtual Server username"
}

variable "vs_password" {
  type        = string
  default     = "null"
  description = "User provided password (vs_generate_password must be set to false)"
}

variable "vs_generate_password" {
  type        = bool
  default     = true
  description = "Generate password"
}

variable "vs_memory" {
  description = "Virtual Server RAM"
  default     = "16Gi"
}

variable "vs_root_storage" {
  description = "Virtual Server root device storage (i.e 80Gi)"
  default     = "80Gi"
}

variable "vs_os_type" {
  default = "linux"
}

variable "vs_image" {
  description = "OS image"
  default     = "ubuntu2004-docker-master-20210601-ord1"
}

variable "vs_gpu" {
  description = "GPU"
  default     = "Quadro_RTX_4000"
}

variable "vs_gpu_enable" {
  default = true
}

variable "vs_cpu_count" {
  default = 3
}

variable "vs_gpu_count" {
  default = 1
}

variable "vs_region" {
  description = "Region default from vs_regions map"
  default     = "ORD1"
}

variable "vs_running" {
  description = "Running virtual server on provisioning"
  default     = true
}

variable "vs_public_networking" {
  default = true
}

variable "vs_attach_loadbalancer" {
  description = "Attach Service LoadBalancer IP directly to VS (Ports must be empty)."
  default     = false
}

variable "vs_tcp_ports" {
  type    = list(any)
  default = [22, 443, 60443, 4172, 3389]
}

variable "vs_udp_ports" {
  type    = list(any)
  default = [4172, 3389]
}
