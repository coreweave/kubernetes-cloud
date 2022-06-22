# Remote Access and Control

Virtual Servers can be managed via the [cloud.coreweave.com](https://cloud.coreweave.com) UI. For management and access via the command line, the `virtctl` tool can be used.

## Installing virtctl

`virtctl`provides an easy, imperative method to start, stop and access VM instances. `virtctl` uses your existing Kubernetes credentials set up in [Getting Started](../coreweave-kubernetes/getting-started.md).

[Download for Linux](https://github.com/kubevirt/kubevirt/releases/download/v0.39.0/virtctl-v0.39.0-linux-amd64)\
[Download for Windows](https://github.com/kubevirt/kubevirt/releases/download/v0.39.0/virtctl-v0.39.0-windows-amd64.exe)\
[Download for Mac OS X](https://github.com/kubevirt/kubevirt/releases/download/v0.39.0/virtctl-v0.39.0-darwin-amd64)

## Instance Control

**Starting an instance** `virtctl start my-vm`\
**Restarting an instance** `virtctl restart my-vm`\
**Stopping an instance** `virtctl stop my-vm`

{% hint style="info" %}
A stopped in-stance does not incur any on-demand compute costs. Persistent Block Volumes or Shared Filesystems do however still incur storage costs until deleted.
{% endhint %}

## Remote Access

For normal operations, in-instance remote access tools such as SSH, Teradici, Parsec or RDP is recommended. During setup and troubleshooting out of band access is provided via `virtctl`.

**Console**\
The best way to access Linux VMs: `virtctl console my-vm`

**VNC**\
For accessing graphical interfaces such as GRUB and Windows: `virtctl vnc my-vm`

{% hint style="info" %}
A compatible VNC client such as VNC Viewer will need to be installed on the local system.
{% endhint %}
