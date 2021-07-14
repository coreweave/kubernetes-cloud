resource "kubernetes_manifest" "virtualdesktop" {
  provider = kubernetes-alpha

  manifest = {
    "apiVersion" = "virtualservers.coreweave.com/v1alpha1"
    "kind"       = "VirtualServer"
    "metadata" = {
      "name"      = var.vdi_name
      "namespace" = var.user_namespace
    }
    "spec" = {
      "initializeRunning" = true
      "network" = {
        "public" = true
        "tcp" = {
          "ports" = [
            22,
            443,
            60443,
            4172,
            3389,
          ]
        }
        "udp" = {
          "ports" = [
            4172,
            3389,
          ]
        }
      }
      "os" = {
        "type" = var.vdi_os_type
      }
      "region" = var.vdi_region
      "resources" = {
        "cpu" = {
          "count" = 3
        }
        "gpu" = {
          "count" = var.vdi_gpu_count
          "type"  = var.vdi_gpu_enable ? var.vdi_gpu : "Quadro_RTX_4000"
        }
        "memory" = var.vdi_memory
      }
      "storage" = {
        "root" = {
          "size" = var.vdi_root_storage
          "source" = {
            "pvc" = {
              "name"      = var.vdi_image
              "namespace" = "vd-images"
            }
          }
          "storageClassName" = "block-nvme-ord1"
        }
      }
      "users" = [
        {
          "username" = var.vdi_username
          "password" = var.vdi_generate_password ? random_password.vdi_generate_password[0].result : var.vdi_password
        },
      ]

    }
  }
}
