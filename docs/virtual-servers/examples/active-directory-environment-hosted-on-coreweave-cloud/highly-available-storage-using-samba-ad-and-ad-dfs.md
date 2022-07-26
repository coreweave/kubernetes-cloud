# Highly Available Storage using Samba-AD and AD DFS

**Objective:** Create a DFS namespace using multiple Samba-AD deployments for high availability.

**Overview:** This process consists of adding the [Distributed File System](https://docs.microsoft.com/en-us/windows-server/storage/dfs-namespaces/dfs-overview) Namespace role to our [previously deployed Domain Controller](provision-an-active-directory-domain-controller.md#create-primary-domain-controller-virtual-server), as well as deploying multiple Samba-AD instances presenting [Shared Filesystem](https://docs.coreweave.com/coreweave-kubernetes/storage#shared-filesystem) storage volumes. We will add each Samba-AD instance to our DFS Namespace, so our shares are highly available.

## Create Storage Volumes

Before deploying our Samba-AD instance, we must first have storage volumes to present. Logging in to the [CoreWeave Cloud Dashboard](https://docs.coreweave.com/virtual-servers/deployment-methods/coreweave-apps#accessing-the-cloud-ui), navigate to the [Storage Volumes](https://cloud.coreweave.com/storage) management page to deploy a new volume:

![](<../../../.gitbook/assets/image (148).png>)

Our Samba-AD instance uses Shared Filesystem volumes:

![](<../../../.gitbook/assets/image (130).png>)

In this example, we have three volumes we'll be using for our Samba-AD instance:

![](<../../../.gitbook/assets/image (57).png>)

## Deploy Samba-AD Instances

With our storage volumes allocated, we can now present them with Samba-AD.

Via the CoreWeave Cloud Dashboard, navigate to the catalog:

![](<../../../.gitbook/assets/image (135).png>)

Locate the Samba-AD chart:

![](<../../../.gitbook/assets/image (123).png>)

Using the information from our [Configure Domain Services](provision-an-active-directory-domain-controller.md#install-and-configure-domain-services) example, fill out the form, including instance name. The volumes we created earlier are attached to our deployment example below:

![](<../../../.gitbook/assets/image (107).png>)

Once deployed, we're taken to a status page indicating our deployment is running:

![](<../../../.gitbook/assets/image (121).png>)

We will then follow the above steps to create another instance for high availability - called `smbad02`:

![](<../../../.gitbook/assets/image (122).png>)

{% hint style="info" %}
Samba-AD includes `podAntiAffinity`, which prevents multiple instances from scheduling on the same compute node.
{% endhint %}

## Configure Distributed File System

With our instances deployed, we can set up our DFS namespace.&#x20;

With an authenticated administrative Domain Account, start a new PowerShell session on your desired DFS namespace server. Usually, this is your Primary Domain Controller.&#x20;

#### Install the DFS Namespace Role

```powershell
Install-WindowsFeature -Name FS-DFS-Namespace,FS-DFS-Replication  -IncludeManagementTools

Success Restart Needed Exit Code      Feature Result
------- -------------- ---------      --------------
True    No             Success        {DFS Namespaces, DFS Replication, DFS Mana...
```

#### Setup DFS Root Folder Structure

```powershell
New-Item -ItemType Directory $env:SystemDrive\DFSRoots\Shares -Force


    Directory: C:\DFSRoots


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         3/31/2022  12:57 AM                Shares
```

#### Create DFS Root SMB Share

```powershell
New-SmbShare -Name "Shares" -Path $env:SystemDrive\DFSRoots\Shares

Name   ScopeName Path               Description
----   --------- ----               -----------
Shares *         C:\DFSRoots\Shares
```

#### Create DFS Namespace Root

```powershell
New-DfsnRoot -TargetPath "\\vs-pdc\Shares" -Type DomainV2 -Path "\\ad\Shares"

Path        Type      Properties TimeToLiveSec State  Description
----        ----      ---------- ------------- -----  -----------
\\ad\Shares Domain V2            300           Online
```

{% hint style="info" %}
Note in this example, `vs-pdc` is the Domain Controller we are using for our DFS Namespace host. `Shares` is the directory we created and shared above.
{% endhint %}

#### Create DFS Target for each Samba-AD Instance

```powershell
New-DfsnFolderTarget -Path "\\ad\shares\vol01" -TargetPath "\\smbad01\vol01"

Path              TargetPath      State  ReferralPriorityClass ReferralPriorityRank
----              ----------      -----  --------------------- --------------------
\\ad\shares\vol01 \\smbad01\vol01 Online sitecost-normal       0

New-DfsnFolderTarget -Path "\\ad\shares\vol01" -TargetPath "\\smbad02\vol01"

Path              TargetPath      State  ReferralPriorityClass ReferralPriorityRank
----              ----------      -----  --------------------- --------------------
\\ad\shares\vol01 \\smbad02\vol01 Online sitecost-normal       0
```

{% hint style="info" %}
Repeat this step for each share your Samba-AD instance presents. In this example, we need to perform the above for `vol02` and `vol03`.
{% endhint %}

### Verify the Results

Navigating to `\\ad\Shares`, we can see each of our DFS Folder Targets:

![](<../../../.gitbook/assets/image (147).png>)

Under properties, the DFS tab shows us `smbad02` is the current active file server:

![](<../../../.gitbook/assets/image (62) (2).png>)

Copying a file to our DFS Root Folder path, we can see it's actually been copied to the shares presented by the Samba-AD instances:

![](<../../../.gitbook/assets/image (65) (2).png>)

![](<../../../.gitbook/assets/image (100).png>)

![](<../../../.gitbook/assets/image (56) (1).png>)

### Adding a secondary DFS Namespace Server

To mitigate points of failure, we will use our [secondary domain controller](provision-an-active-directory-domain-controller.md#adding-a-secondary-domain-controller) as an additional DFS Server.&#x20;

We will follow the above steps on our `vs-dc2` server:

* [Install the DFS Namespace Role](highly-available-storage-using-samba-ad-and-ad-dfs.md#install-the-dfs-namespace-role)
* [Setup DFS Root Folder Structure](highly-available-storage-using-samba-ad-and-ad-dfs.md#setup-dfs-root-folder-structure)
* [Create DFS Root SMB Share](highly-available-storage-using-samba-ad-and-ad-dfs.md#create-dfs-root-smb-share)
* [Create DFS Namespace Root](highly-available-storage-using-samba-ad-and-ad-dfs.md#create-dfs-namespace-root)
  * Here, we will substitute `vs-pdc` with `vs-dc2`

Once complete, we can see multiple Root Target Paths:

```
Get-DfsnRootTarget \\ad\shares

Path        TargetPath                                                           State  ReferralPriorityClass ReferralPriorityRank
----        ----------                                                           -----  --------------------- --------------------
\\ad\shares \\vs-pdc.ad.tenant-orgname-namespace.svc.tenant.chi.local\Shares Online sitecost-normal       0
\\ad\shares \\vs-dc2.ad.tenant-orgname-namespace.svc.tenant.chi.local\Shares Online sitecost-normal       0
```
