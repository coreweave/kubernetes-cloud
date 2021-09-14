# Provision an Active Directory Domain Controller

**Objective:** Spin up a Windows Server and Active Directory Domain on CoreWeave Cloud.  
**Overview:** This process consists of deploying a Windows Server 2019 Virtual Server in your namespace with a static, internal only IP. We will also highlight creating a domain with the appropriate DNS configurations, and the attributes needed to join additional Virtual Servers in your namespace, to your Active Directory domain.

## Create Primary Domain Controller Virtual Server

{% hint style="success" %}
Be sure to review [Getting Started](../../coreweave-kubernetes/getting-started.md#obtain-access-credentials) and the [kubectl Virtual Server deployment method](../deployment-methods/kubectl.md#deploying-a-virtual-server) before starting this guide.
{% endhint %}

We'll start out using [this Virtual Server manifest](https://github.com/coreweave/kubernetes-cloud/blob/master/virtual-server/examples/kubectl/virtual-server-windows-internal-ip-only.yaml) to create a Windows Server 2019 Virtual Server in our Chicago datacenter:

`k create -f virtual-server-windows-internal-ip-only.yaml`

{% tabs %}
{% tab title="YAML" %}
{% code title="virtual-server-windows-internal-ip-only.yaml" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: vs-pdc
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
          name: winserver2019std-master-20210819-ord1
  # Change user name and pasword
  users:
    - username:
      password:
  network:
    directAttachLoadBalancerIP: true
    public: false
  initializeRunning: true
```
{% endcode %}

{% hint style="info" %}
This configuration creates a CPU only instance with a static internal IP - no public facing address, as we typically do not want Domain Controllers exposed publicly.
{% endhint %}
{% endtab %}
{% endtabs %}

We can monitor the Virtual Server spinning up with `k get pods --watch`

![Output of k get pods --watch](../../.gitbook/assets/image%20%287%29.png)

Once our VS has reached "Running" status, we can get an External IP to connect to it with `k get vs`

![Output of k get vs](../../.gitbook/assets/image%20%288%29.png)

{% hint style="info" %}
Allow ~5 minutes after "Running" status for the Virtual Server to complete initial start procedures.
{% endhint %}

## Install and Configure Domain Services

Once our Virtual Server is up and running, we'll connect using SSH with the Internal IP provided by `k get vs`. One can also connect using RDP if a graphical interface is preferred.

Using the below PowerShell script, we'll install and configure the Domain Services role:

{% tabs %}
{% tab title="PowerShell" %}
{% code title="cw\_adds\_setup.ps1" %}
```text
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
{% endcode %}
{% endtab %}
{% endtabs %}

We'll add the script to our server:

![Pasting cw\_adds\_setup.ps1 in over SSH](../../.gitbook/assets/image%20%286%29.png)

Once executed, follow the prompts. You'll be asked to provide:

* **Domain Name**
  * This will be the name of your Active Directory Domain
* **CoreWeave Tenant Name**
  * This is your CoreWeave tenant - usually `tenant-<orgname>-<namespace>`
  * This will be used to integrate your DNS Suffix with Kubernetes Core DNS
* **SafeModeAdministratorPassword**
  * Used for Directory Services Restore Mode

![](../../.gitbook/assets/image%20%289%29.png)

{% hint style="info" %}
After executing the script, the server will automatically reboot as part of the ADDS deployment.
{% endhint %}

Note the relevant details from this example:

* **Domain Name:** AD
* **Search Realm:** ad.tenant-orgname-namespace.svc.tenant.chi.local
* **PDC/DNS Server IP:** 10.135.123.123
* **PDC FQDN:** vs-pdc.ad.tenant-orgname-namespace.svc.tenant.chi.local

## Join a Windows Virtual Server

After provisioning another Windows Virtual Server in our namespace, we need to set its DNS server to point to our PDC:

{% tabs %}
{% tab title="PowerShell" %}
```text
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 10.135.123.123
```
{% endtab %}
{% endtabs %}

We can then join the domain:

{% tabs %}
{% tab title="PowerShell" %}
```text
Add-Computer -DomainName ad.tenant-orgname-namespace.svc.tenant.chi.local
```

{% hint style="info" %}
You will be prompted for credentials - the user account will need to have domain join permissions on your domain.
{% endhint %}
{% endtab %}
{% endtabs %}

After rebooting, your Windows Virtual Server will now be joined to your Active Directory Domain.

Confirm connectivity by performing a policy update:

![Group Policy update](../../.gitbook/assets/image%20%2812%29.png)

## Adding a secondary Domain Controller

To create an additional domain controller, spin up a [new Virtual Server](provision-an-active-directory-domain-controller.md#create-primary-domain-controller-virtual-server) as an additional DC, and [join it](provision-an-active-directory-domain-controller.md#join-a-windows-virtual-server) to your existing domain.

{% hint style="warning" %}
Ensure you reboot after joining your Virtual Server to the domain, as well as perform a policy update.
{% endhint %}

Using the below PowerShell script, we'll install the Domain Services role and configure the DC:

{% tabs %}
{% tab title="PowerShell" %}
{% code title="cw\_addc\_setup.ps1" %}
```text
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
{% endcode %}
{% endtab %}
{% endtabs %}

Add the script to your VS:

![Pasting cw\_addc\_setup.ps1 in over SSH](../../.gitbook/assets/image%20%2811%29.png)

Once executed, follow the prompts. You'll be asked to provide:‌

* **Domain Name**
  * The name of your existing Active Directory Domain
* **CoreWeave Tenant Name**
  * This is your CoreWeave tenant - usually `tenant-<orgname>-<namespace>`
* **Domain Admin UserName and Password**
  * An account on your domain in the "Domain Administrators" group
  * Be sure to enter this account with your domain name preceding, e.g. `AD\Admin`
* **SafeModeAdministratorPassword**
  * Used for Directory Services Restore Mode

{% hint style="info" %}
After executing the script, the server will automatically reboot as part of the ADDS deployment.
{% endhint %}

After rebooting, confirm your Domain Controller status with `Get-ADDomainController:`

![Output of Get-AdDomainController](../../.gitbook/assets/image%20%2810%29.png)



