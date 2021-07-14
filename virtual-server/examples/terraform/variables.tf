variable "kubeconfig_path" {
  description = "Path to kubeconfig"
  default     = "~/.kube/config"
}

variable "user_namespace" {
  description = "Namespace VDI will be installed to"
}

variable "vdi_name" {
  description = "VDI hostname"
  default     = "MY-VDI"
}

variable "vdi_username" {
  description = "VDI username"
}

variable "vdi_password" {
  type        = string
  default     = "null"
  description = "User provided password (vdi_generate_password must be set to false)"
}

variable "vdi_generate_password" {
  type        = bool
  default     = true
  description = "Generate password"
}

variable "vdi_memory" {
  description = "VDI RAM"
  default     = "16Gi"
}

variable "vdi_root_storage" {
  description = "VDI root device storage (i.e 80Gi)"
  default     = "80Gi"
}

variable "vdi_os_type" {
  default = "linux"
}

variable "vdi_image" {
  description = "OS image"
  default     = "ubuntu2004-docker-master-20210601-ord1"
}

variable "vdi_gpu" {
  description = "GPU"
  default     = "Quadro_RTX_4000"
}

variable "vdi_gpu_enable" {
  default = true
}

variable "vdi_gpu_count" {
  default = 1
}

variable "vdi_region" {
  description = "Region default from vdi_regions map"
  default     = "ORD1"
}
