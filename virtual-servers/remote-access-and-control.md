---
description: How to manage and access Virtual Servers from the command line.
---

# Remote Access and Control

While Virtual Servers can be managed via the [CoreWeave Cloud UI](https://cloud.coreweave.com), management and access via the command line may be accomplished using the `virtctl` tool.

## Installing `virtctl`

`virtctl`provides an easy, imperative method to start, stop and access VM instances. On CoreWeave Cloud, `virtctl` uses the Kubernetes access credentials configured in [Getting Started](../docs/coreweave-kubernetes/getting-started.md).

`virtctl` may be downloaded from one of the following sources:

* [Download for Linux](https://github.com/kubevirt/kubevirt/releases/download/v0.51.0/virtctl-v0.51.0-linux-amd64)
* [Download for Windows](https://github.com/kubevirt/kubevirt/releases/download/v0.51.0/virtctl-v0.51.0-windows-amd64.exe)
* [Download for Mac OS X](https://github.com/kubevirt/kubevirt/releases/download/v0.51.0/virtctl-v0.51.0-darwin-amd64)

## Controlling the instance

Basic instance commands using `virtctl`:

| Command                   | Effect          |
| ------------------------- | --------------- |
| `virtctl start <my-vm>`   | Starts the VM   |
| `virtctl restart <my-vm>` | Restarts the VM |
| `virtctl stop <my-vm>`    | Stops the VM    |

{% hint style="info" %}
**Note**

A `stopped` instance does not incur any on-demand compute costs. Persistent Block Volumes or Shared Filesystems do however still incur storage costs until they are deleted.
{% endhint %}

## Remote access

For normal operations, instance remote access tools such as SSH, Teradici, Parsec or RDP is recommended. During setup and troubleshooting, out of band access is provided via `virtctl`.

### **Console**

The best way to access Linux VMs is to invoke `virtctl console <my-vm>`.

### **VNC**

For accessing graphical interfaces such as GRUB and Windows you can invoke a VNC instance by using `virtctl vnc <my-vm>`.

{% hint style="info" %}
**Note**

A compatible VNC client such as VNC Viewer will need to be installed on the local system prior to invoking this command.
{% endhint %}
