resource "kubernetes_manifest" "virtualserver" {
  provider = kubernetes-alpha

  manifest = {
    "apiVersion" = "virtualservers.coreweave.com/v1alpha1"
    "kind"       = "VirtualServer"
    "metadata" = {
      "name"      = var.vs_name
      "namespace" = var.user_namespace
    }
    "spec" = {
      "initializeRunning" = var.vs_running
      "network" = {
        "directAttachLoadBalancerIP" = var.vs_attach_loadbalancer
        "public"                     = var.vs_public_networking
        "tcp" = {
          "ports" = var.vs_tcp_ports
        }
        "udp" = {
          "ports" = var.vs_udp_ports
        }
      }
      "os" = {
        "type" = var.vs_os_type
      }
      "region" = upper(var.vs_region)
      "resources" = {
        "cpu" = {
          "count" = var.vs_cpu_count
        }
        "gpu" = {
          "count" = var.vs_gpu_count
          "type"  = var.vs_gpu_enable ? var.vs_gpu : "Quadro_RTX_4000"
        }
        "memory" = var.vs_memory
      }
      "storage" = {
        "root" = {
          "size" = var.vs_root_storage
          "source" = {
            "pvc" = {
              "name"      = var.vs_image
              "namespace" = "vd-images"
            }
          }
          "storageClassName" = "block-nvme-${lower(var.vs_region)}"
        }
      }
      "users" = [
        {
          "username" = var.vs_username
          "password" = var.vs_generate_password ? random_string.vs_generate_password[0].result : var.vs_password
        },
      ]
    }
  }
}

data "kubernetes_service" "vs_loadbalancer" {
  depends_on = [kubernetes_manifest.virtualserver]
  metadata {
    name      = "${var.vs_name}-tcp"
    namespace = var.user_namespace
  }
}
