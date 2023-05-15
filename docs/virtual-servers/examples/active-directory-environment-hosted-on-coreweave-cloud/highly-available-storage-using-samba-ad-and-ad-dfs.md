---
description: >-
  A Virtual Server example hosting a DFS namespace with multiple Samba-AD
  deployments for high availability
---

# Highly Available Storage using Samba-AD and AD DFS

In this example, a [Distributed File System (DFS) Namespace](https://docs.microsoft.com/en-us/windows-server/storage/dfs-namespaces/dfs-overview) leveraging multiple Samba-AD deployments for high availability is provisioned onto CoreWeave Cloud.

This process consists of adding the Distributed File System Namespace role to a [previously deployed Domain Controller](./), as well as deploying multiple Samba-AD instances presenting [Shared Filesystem storage volumes](../../../storage/storage/). Each Samba-AD instance is added to the DFS Namespace so that shares are highly available.

## Prerequisites

This example presumes that [a Windows Server with an Active Directory Domain](./) has already been deployed. It is also presumed that the user already [has an active CoreWeave account and has configured their user credentials](../../../coreweave-kubernetes/getting-started.md#create-an-account) such that resources may be deployed to their namespace.

## Create Storage Volumes

Before deploying the Samba-AD instance, there must be storage volumes to present. The Samba-AD instance will use three Shared HDD Filesystems. To create these, the user navigates [to the Storage section of the CoreWeave Cloud UI](../../../storage/storage/using-storage-cloud-ui.md#create-a-new-storage-volume).

![](<../../../.gitbook/assets/image (130).png>)

In this example, three volumes are used for the Samba-AD instance. They are each titled `vol01`, `vol02`, and `vol03` respectively.

<figure><img src="../../../.gitbook/assets/image (57) (1).png" alt="Screenshot of three HDD shared filesystem volumes in the Storage section of the Cloud UI"><figcaption></figcaption></figure>

## Deploy Samba-AD Instances

With the storage volumes allocated, they may now be presented with Samba-AD.

Samba-AD is installed from [the Cloud UI Applications Catalog](../../../coreweave-kubernetes/applications-catalog.md) by searching `samba-ad`. Click the **samba-ad** card, then click the **Deploy** button to configure and launch Samba-AD.

<figure><img src="../../../.gitbook/assets/image (3) (2).png" alt="Screenshot: search for samba-ad in the applications catalog to find it"><figcaption></figcaption></figure>

### Configure Samba-AD

The Samba-AD application requires some details prior to deploying. In this example, the same details provided in [the Windows Server with Active Directory Domain example](./) are used to fill out the form, including the instance name. At the bottom of the deployment form, the filesystem volumes created earlier (`vol01`, `vol02`, and `vol03`) are attached at the end of the form, before the application is deployed.

![](<../../../.gitbook/assets/image (68) (2).png>)

The [post-deployment status page](../../../../virtual-servers/deployment-methods/coreweave-apps.md#cloud-ui-tools) indicates when the deployed Samba-AD Pods are in a `Ready` state.

![](<../../../.gitbook/assets/image (121).png>)

### Create a second Samba-AD instance

Repeating the steps above, a second Samba-AD instance is created, this one given the name `smbad02`.

![](<../../../.gitbook/assets/image (122).png>)

{% hint style="info" %}
**Note**

Samba-AD includes an `podAntiAffinity` to prevent multiple instances from being scheduled on the same compute node.
{% endhint %}

## Configure the Distributed File System

With both Samba-AD instances deployed, the DFS Namespace can be configured.

A new PowerShell session on the desired DFS Namespace server - usually, the [Primary Domain Controller](./#create-a-primary-domain-controller-pdc) -  is opened with an authenticated administrative Domain Account. The following commands are issued to configure the DFS Namespace.

### Install the DFS Namespace role

First, the DFS Namespace role is created.

```powershell
Install-WindowsFeature -Name FS-DFS-Namespace,FS-DFS-Replication  -IncludeManagementTools

Success Restart Needed Exit Code      Feature Result
------- -------------- ---------      --------------
True    No             Success        {DFS Namespaces, DFS Replication, DFS Mana...
```

### Setup DFS root folder structure

Next, the DFS root folder structure is created.

```powershell
New-Item -ItemType Directory $env:SystemDrive\DFSRoots\Shares -Force


    Directory: C:\DFSRoots


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         3/31/2022  12:57 AM                Shares
```

### Create DFS root SMB share

Then, a DFS root SMB share is provisioned.

```powershell
New-SmbShare -Name "Shares" -Path $env:SystemDrive\DFSRoots\Shares

Name   ScopeName Path               Description
----   --------- ----               -----------
Shares *         C:\DFSRoots\Shares
```

### Create the DFS Namespace root

In this example, `vs-pdc` is the Domain Controller we are using for our DFS Namespace host. The directory `Shares` is the directory created and shared previously.

```powershell
New-DfsnRoot -TargetPath "\\vs-pdc\Shares" -Type DomainV2 -Path "\\ad\Shares"

Path        Type      Properties TimeToLiveSec State  Description
----        ----      ---------- ------------- -----  -----------
\\ad\Shares Domain V2            300           Online
```

### Create DFS Targets

For each Samba-AD instance created, a [DFS folder target](https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/add-folder-targets) is created. This process is repeated for each share the Samba-AD instance presents. In this example, the process must be replicated for volumes `vol02` and `vol03`.

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

### Verify the results

Navigating to `\\ad\Shares`, each DFS folder target should now exist, as shown here:

<figure><img src="../../../.gitbook/assets/image (147).png" alt="A screenshot of a filesystem directory listing"><figcaption></figcaption></figure>

Under **Properties**, in the DFS tab, `smbad02` is shown as the currently active file server.

![](<../../../.gitbook/assets/image (62) (2).png>)

Copying a file to the DFS Root Folder path demonstrates that the file gets copied to the shares presented by the Samba-AD instances:

<figure><img src="../../../.gitbook/assets/image (2) (3).png" alt="" width="375"><figcaption></figcaption></figure>

### Adding a secondary DFS Namespace Server

To mitigate any points of failure, we will use [the secondary domain controller](./#add-a-secondary-domain-controller) created earlier as an additional DFS Namespace server.

The following steps will be repeated in order to accomplish this:

1. [Install the DFS Namespace Role](highly-available-storage-using-samba-ad-and-ad-dfs.md#install-the-dfs-namespace-role)
2. [Setup DFS Root Folder Structure](highly-available-storage-using-samba-ad-and-ad-dfs.md#setup-dfs-root-folder-structure)
3. [Create DFS Root SMB Share](highly-available-storage-using-samba-ad-and-ad-dfs.md#create-dfs-root-smb-share)
4. [Create DFS Namespace Root](highly-available-storage-using-samba-ad-and-ad-dfs.md#create-dfs-namespace-root) (In this step, `vs-pdc` is substituted with `vs-dc2`)

Once complete, multiple Root Target Paths are visible by using `Get-DfsnRootTarget \\ad\shares`:

```powershell
Get-DfsnRootTarget \\ad\shares

Path        TargetPath                                                           State  ReferralPriorityClass ReferralPriorityRank
----        ----------                                                           -----  --------------------- --------------------
\\ad\shares \\vs-pdc.ad.tenant-orgname-namespace.svc.tenant.chi.local\Shares Online sitecost-normal       0
\\ad\shares \\vs-dc2.ad.tenant-orgname-namespace.svc.tenant.chi.local\Shares Online sitecost-normal       0
```
