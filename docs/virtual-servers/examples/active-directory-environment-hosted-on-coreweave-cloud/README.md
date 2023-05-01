---
description: A Virtual Server example running Windows Server with Active Directory
---

# Windows Server with Active Directory Domain

In this example, a Virtual Server running Windows Server 2022 is deployed to host an Active Directory Domain.

The Virtual Server is deployed with a static, internal-only IP. This example also highlights how to create a domain with appropriate DNS configurations, as well as the attributes needed to join other Virtual Servers in your namespace to your Active Directory domain.

## Prerequisites

This example presumes that the user already [has an active CoreWeave account and has configured their user credentials](../../../coreweave-kubernetes/getting-started.md#create-an-account) such that resources may be deployed to their namespace.

The Windows Servers below are deployed using `kubectl`. To follow along, ensure that `kubectl` is installed on your local system.

### Example source code

To try out this example yourself, first clone the [`virtual-server-windows-internal-ip-only.yaml`](../../../../virtual-server/examples/kubectl/virtual-server-windows-internal-ip-only.yaml) manifest from GitHub.

{% embed url="https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-windows-internal-ip-only.yaml" %}

## Create a Primary Domain Controller (PDC)

First, the prepared [`virtual-server-windows-internal-ip-only.yaml`](../../../../virtual-server/examples/kubectl/virtual-server-windows-internal-ip-only.yaml) manifest is cloned locally.

<details>

<summary>Click to expand - <code>virtual-server-windows-internal-ip-only.yaml</code></summary>

```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-pdc
  labels:
    app.kubernetes.io/component: dc
spec:
  region: ORD1
  os:
    type: windows
  resources:
    cpu:
      # Reference CPU instance label selectors here:
      # https://docs.coreweave.com/resources/resource-based-pricing#cpu-only-instance-resource-pricing
      type: amd-epyc-rome
      count: 4
    memory: 16Gi
  storage:
    root:
      size: 80Gi
      storageClassName: block-nvme-ord1
      source:
        pvc:
          namespace: vd-images
          # Reference querying source image here:
          # https://docs.coreweave.com/virtual-servers/root-disk-lifecycle-management/exporting-coreweave-images-to-a-writable-pvc#identifying-source-image
          name: winsvr2022std-master-20220319-ord1
  # Change user name and pasword
  users:
    - username:
      password:
  network:
    directAttachLoadBalancerIP: true
    public: false
  initializeRunning: true
  cloudInit: |
    autologon: false
    parsec: false
    edid: false
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/component
            operator: In
            values:
            - dc
        topologyKey: topology.kubernetes.io/zone
```

</details>

Then, `kubectl` is used to deploy it using the `create` command:

```bash
$ kubectl create -f virtual-server-windows-internal-ip-only.yaml
```

The `kubectl get pods --watch` is used to watch the Virtual Server creation progress.

<figure><img src="../../../../.gitbook/assets/image (7).png" alt="Screenshot of the output of the --watch command" width="563"><figcaption></figcaption></figure>

After allowing about five minutes after the Virtual Server has reached the `Running` status so that the machine may complete its initial start procedures, the External IP is acquired using `get vs`. Virtual Servers are Custom Resource Definitions, which may be targeted by `kubectl` using `vs`.

```bash
$ kubectl get vs
```

<figure><img src="../../../.gitbook/assets/image (8) (2).png" alt="Output of kubectl get vs"><figcaption></figcaption></figure>

## Install and configure domain services

With the Virtual Server up and running, SSH is used to connect using the Internal IP acquired using `kubectl get vs`. Connections via RDP are also possible, if a graphical interface is preferred.

The following PowerShell script installs and configures the Domain Services role.

<details>

<summary>Click to expand - <code>cw_adds_setup.ps1</code></summary>

```powershell
$DomainName = Read-Host -Prompt "Enter desired Domain Name"
$Tenant = Read-Host -Prompt "Enter CoreWeave tenant name"

winrm quickconfig -q

Add-WindowsFeature AD-Domain-Services -IncludeManagementTools

Import-Module ADDSDeployment
Install-ADDSForest `
-CreateDnsDelegation:$false `
-DatabasePath "C:\Windows\NTDS" `
-DomainMode "WinThreshold" `
-DomainName "$($DomainName).$($Tenant).svc.tenant.chi.local" `
-DomainNetbiosName $($DomainName) `
-ForestMode "WinThreshold" `
-InstallDns:$true `
-LogPath "C:\Windows\NTDS" `
-NoRebootOnCompletion:$false `
-SysvolPath "C:\Windows\SYSVOL" `
-Force:$true
```

</details>

This script is simply written to an outfile called `cw_adds_setup.ps1`.

![Pasting cw\_adds\_setup.ps1 in over SSH](<../../../../.gitbook/assets/image (6).png>)

When executed, the script prompts the user to provide the following:

| **Domain Name**                   | The name of the Active Directory Domain                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **CoreWeave Tenant Name**         | The name of the CoreWeave tenant - usually `tenant-<orgname>-<namespace>.` Used to integrate your DNS Suffix with Kubernetes Core DNS |
| **SafeModeAdministratorPassword** | Used for [Directory Services Restore Mode](https://en.wikipedia.org/wiki/Directory\_Services\_Restore\_Mode)                          |

<figure><img src="../../../../.gitbook/assets/image (9).png" alt="The PowerShell script, executed"><figcaption></figcaption></figure>

When the script is finished executing, the server will automatically reboot as part of the ADDS deployment.

In this example, the server is constructed with the following attributes:

| **Domain Name**       | AD                                                      |
| --------------------- | ------------------------------------------------------- |
| **Search Realm**      | ad.tenant-orgname-namespace.svc.tenant.chi.local        |
| **PDC/DNS Server IP** | 10.135.123.123                                          |
| **PDC FQDN**          | vs-pdc.ad.tenant-orgname-namespace.svc.tenant.chi.local |

The Windows Server is now fully provisioned!

## Join another Windows Virtual Server

First, another Windows Virtual Server is provisioned using the same procedure as the first. This second server is configured to point to our Primary Domain Controller (or PDC):

{% code overflow="wrap" %}
```powershell
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 10.135.123.123
```
{% endcode %}

The domain is then added using `Add-Computer`:

```powershell
Add-Computer -DomainName ad.tenant-orgname-namespace.svc.tenant.chi.local
```

At this point, the user is prompted for credentials. The user account must have domain join permissions on your domain.

After rebooting the second server, this Windows Virtual Server will now be joined to the Active Directory Domain. Connectivity can be confirmed by performing a Group Policy update:

```powershell
gpupdate /force
```

<figure><img src="../../../.gitbook/assets/image (12) (2).png" alt="The output of gpupdate /force"><figcaption></figcaption></figure>

## Add a secondary Domain Controller

To create an additional domain controller, the procedure for [provisioning a Primary Domain Controller](./#create-a-primary-domain-controller-pdc) is repeated.

The PowerShell script below is used to install the Domain Services role and configure the new Domain Controller.

<details>

<summary>Click to expand - <code>cw_addc_setup.ps1</code></summary>

```powershell
$DomainName = Read-Host -Prompt "Enter Domain Name"
$Tenant = Read-Host -Prompt "Enter CoreWeave tenant name"
Write-Host "Ensure to precede username with $($domainname+'\')" -ForegroundColor Red -BackgroundColor Black
$usr = Read-Host "Domain Admin UserName"
$passwd= Read-Host "Domain Admin Password" -AsSecureString
$cred = new-object System.Management.Automation.PSCredential($usr,$passwd)

winrm quickconfig -q

Add-WindowsFeature AD-Domain-Services -IncludeManagementTools

Import-Module ADDSDeployment
Install-ADDSDomainController `
-NoGlobalCatalog:$false `
-CreateDnsDelegation:$false `
-Credential $cred `
-CriticalReplicationOnly:$false `
-DatabasePath "C:\Windows\NTDS" `
-DomainName "$($DomainName).$($Tenant).svc.tenant.chi.local" `
-InstallDns:$true `
-LogPath "C:\Windows\NTDS" `
-NoRebootOnCompletion:$false `
-SiteName "Default-First-Site-Name" `
-SysvolPath "C:\Windows\SYSVOL" `
-Force:$true
```

</details>

As before, the script is printed to an output file, and then executed afterwards.

![](<../../../../.gitbook/assets/image (11).png>)

When executed, the script prompts the user to provide the following:

| **Domain Name**                   | The name of the Active Directory Domain                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **CoreWeave Tenant Name**         | The name of the CoreWeave tenant - usually `tenant-<orgname>-<namespace>.` Used to integrate your DNS Suffix with Kubernetes Core DNS |
| **SafeModeAdministratorPassword** | Used for [Directory Services Restore Mode](https://en.wikipedia.org/wiki/Directory\_Services\_Restore\_Mode)                          |

The server will automatically reboot. After rebooting, the Domain Controller status is confirmed using `Get-ADDomainController`:

<figure><img src="../../../../.gitbook/assets/image (10).png" alt="Output of Get-AdDomainController"><figcaption></figcaption></figure>
