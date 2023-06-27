# Windows Images

CoreWeave offers a variety of Operating System base images, enhanced to run on CoreWeave Cloud. Images are stored in the `vd-images` namespace.

## Cloud-Init

Windows images on CoreWeave cloud use [Cloudbase-Init](https://github.com/cloudbase/cloudbase-init), a Windows implementation of Canonical's [cloud-init](https://github.com/canonical/cloud-init).

By default, we enable the following plugins, which are executed sequentially:

1. [`UserDataPlugin`](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#user-data-main)
2. [`LocalScriptsPlugin`](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#local-scripts-execution-main)
3. [`SetHostNamePlugin`](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#setting-hostname-main)

## Add custom userdata

When creating a new [Virtual Server](broken-reference) on CoreWeave Cloud, instance-specific information such as user account information and SSH keys are automatically passed through as Cloud-Init Userdata. When deploying a new Virtual Server, one has the ability to add additional information via Userdata as well.

### Via `kubectl` YAML:

```yaml
  cloudInit: |
    write_files:
    -   encoding: b64
        content: JFBTVmVyc2lvblRhYmxlIHwgT3V0LUZpbGUgQzpcdGVzdC50eHQ=
        path: C:\test.ps1
        permissions: '0644'
    runcmd:
      - 'Powershell.exe -File C:\test.ps1'
```

[View the rest of the source file on GitHub](https://docs.coreweave.com/virtual-servers/coreweave-system-images).

### Via the [CoreWeave Apps Web UI](../../coreweave-kubernetes/coreweave-cloud-ui/applications-catalog.md):

Within the Virtual Server deployment form, switch to the YAML tab:

![](<../../.gitbook/assets/image (59) (1).png>)

Towards the bottom of the page, a commented out cloudInit section will be pre-populated. Uncomment to add custom user data:

![](<../../.gitbook/assets/image (61) (1) (1).png>)

{% hint style="info" %}
**Note**

For more information on what be added via native cloud-init Userdata, see[ the Cloudbase Solutions documentation](https://cloudbase-init.readthedocs.io/en/latest/userdata.html#userdata).
{% endhint %}

## CoreWeave userdata features

There are several CoreWeave init scripts included in our base Windows image, that can be enabled via cloudInit Userdata.

### Add SMB mounts

Samba shares, or any SMB/CIFS-compliant shares, can be added via cloudInit to be mounted to the first available drive letter at initial user login.

Using an example from a Samba instance hosted via CoreWeave Cloud Apps, we can derive the following information:

* The SMB client's FQDN is `fil01.tenant-orgname-namespace-cpierre.coreweave.cloud`
* The SMB mount login information is:
  * Username: `gaben`
  * Password: `hunter2`
* The shares mounted are named `vol01` and `vol02`

![](<../../.gitbook/assets/image (144).png>)

Using this information, we can populate the `cloudInit` key-value pairs as follows:

```yaml
  cloudInit: |
    SmbMounts:
    - share: vol01
      server: fil01.tenant-orgname-namespace.coreweave.cloud
      username: gaben
      password: hunter2
    - share: vol02
      server: fil01.tenant-orgname-namespace.coreweave.cloud
      username: gaben
      password: hunter2
```

{% hint style="info" %}
**Note**

By default, available drive letters are randomized, and the first available one is selected per share. Drive letters can be manually specified by adding them, such as `Drive: Z`.
{% endhint %}

### Enroll a Parsec Teams machine

CoreWeave Windows images support [Parsec Teams](https://parsec.app/teams). To enroll a Parsec Teams machine, include the following in the `cloudInit` block when deploying a Virtual Server:

```yaml
  cloudInit: |
    ParsecTeams:
      ComputerKey: key_generated_from_parsec_admin_panel
      TeamId: parsec_team_id
      # Use EITHER Group ID or EMail or User ID
      GroupId: parsec_group_id
      UserId: parsec_user_id
      EMail: parsec_user_email
```

{% hint style="info" %}
**Note**

If a Parsec machine is assigned to an email that isn't part of the Team, the machine will be made available to them after they've been invited and accepted the invitation. If none of `GroupId`, `UserId`, or `EMail` is provided, the machine will be added to the Parsec Team unassigned.
{% endhint %}

For more information on Parsec Teams and where to obtain your enrollment key, please visit [Parsec's documentation](https://support.parsec.app/hc/en-us/articles/360054176332-Team-Computers).

{% hint style="info" %}
**Note**

When enrolling a Parsec Teams machine, Boolean values `Parsec: true` and `EDID: true` will also need to be added to your manifest.
{% endhint %}

### Install Additional Software

All CoreWeave Windows images are pre-loaded with the [Chocolatey](https://community.chocolatey.org/packages) package manager. On non-Server editions of Windows, [WinGet](https://winget.run/) is included as well.

Software specified via `cloudInit` is installed automatically at initial user logon:

```yaml
  cloudInit: |
    Choco_Install:
      - googlechrome
      - firefox
    WinGet_Install:
      - Discord.Discord
      - Microsoft.VisualStudioCode
```

### Power-off with no interactive input

Windows images include scripts that can detect user activity such as moving the mouse or keyboard inputs. When enabled, it detects a specified period of no user input, then automatically shuts down. A prompt is presented, along with a five-minute grace period, when the timer threshold is reached. Adding the following will prompt the user after ten minutes of no activity, and shut off automatically after an additional five minutes if the prompt is not acknowledged.

```yaml
  cloudInit: |
    shutoff_on_idle: 10
```

{% hint style="warning" %}
**Important**

This feature should be combined with `RunStrategy: RerunOnFailure` via `vm.Spec` to prevent the instance from automatically powering back on once shutoff. Additionally, boolean flag `Autologon` should be set to `true`, as the idle tracker runs within the user context.
{% endhint %}

### Configure readiness probe

The CoreWeave Cloud UI adds a [Readiness Probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes) to Windows Virtual Servers, to better communicate when start-up procedures have completed. Windows images include a simple TCP listener on port `1337` to communicate with the Kubernetes API. The port Windows listens on is changed in the `cloudInit` block:

```yaml
# Port used to evaluate Readiness
readinessProbePort: 1234
# If disableReadinessProbe is true, readiness probes will be disabled, enabled by default
disableReadinessProbe: false
cloudInit: |
  readinessProbePort: 1234
```

{% hint style="info" %}
**Note**

The `readinessProbePort` must also be set in the YAML section of the Virtual Server deployment, outside of the cloudInit block. Setting `readinessProbePort` in the cloudInit block to `0` will disable the listener in Windows.
{% endhint %}

### Display requests override

Certain applications in Windows, like Parsec, can disrupt idle an inactivity timers. This means that despite setting a lock screen or screensaver timer, they may never engage when a Parsec session or other application is active.

This behavior can be overridden via `cloudInit`. For Parsec or [Teradici](https://teradici.com/), only the application name is required. For other applications, specify the executable name.

```yaml
  cloudInit: |
    DisplayRequestsOverride:
      - Parsec
      - Teradici
      - chrome.exe
```

### Boolean userdata features

Some Userdata features can be enabled with Boolean values `true` or `false`.

#### Teradici PCoIP graphics agent for Windows

CoreWeave Cloud supports [Teradici PCoIP](https://docs.teradici.com/documentation/graphics-agent-for-windows/release-notes) on both Linux and Windows. Adding the following will install the graphics agent on initial logon, pointed to our licensing server:

```yaml
  cloudInit: |
    Teradici: true
```

{% hint style="warning" %}
**Important**

Teradici should not be combined with either Parsec or Virtual Display options below.
{% endhint %}

#### Virtual display

Many applications running on Windows require a display connected to GPU in order to render on the display. Adding the below value will attach a virtual 4K monitor to all available outputs, and disconnect the built-in VNC display.

```yaml
  cloudInit: |
    EDID: true
```

{% hint style="warning" %}
**Important**

When the Virtual Display is enabled, Windows will only output to the attached GPU, making the built-in VNC terminal inaccessible.

Connecting via `virtctl vnc` will result in one of the blank screens shown below:

<img src="../../.gitbook/assets/vnc-1.png" alt="" data-size="original"><img src="../../../.gitbook/assets/vnc-2 (1).png" alt="" data-size="original">

For serial console access (Windows Special Admin Console), use `virtctl console` instead.
{% endhint %}

#### Parsec Remote Desktop

CoreWeave strongly recommends [Parsec](https://parsec.app/) for remote access on Windows GPU instances. Adding the following will install Parsec on initial logon:

```yaml
  cloudInit: |
    EDID: true
    Parsec: true
```

{% hint style="info" %}
**Note**

Parsec requires the use of a Virtual Display, and thus must always be installed alongside `EDID: true`.
{% endhint %}

#### Automatic logon

This flag configures the user account created for automatic logon.

```yaml
  cloudInit: |
    Autologon: true
```

## Operating System customizations

There are several modifications made to a vanilla Windows instance in order to optimize for use on CoreWeave Cloud. Depending on the use case, the following may be disabled or modified.

### CoreWeave resize disk

By default, when the root disk of a Windows image is expanded, Windows will automatically expand the root disk partition to use all of the available space. Additionally, any new block volumes mounted to a Windows instance will automatically be initialized and partitioned as GPT, and formatted as NTFS.

Via the Windows **Apps and Features** menu, the default behavior can be modified:

![](<../../.gitbook/assets/image (54) (1) (1).png>)

Selecting **Modify** will prompt for an action to perform when it is detected that the root disk can be expanded. The default action of `ReSize` will expand the root disk. `NewPartition` will create a new partition with the unallocated space, and automatically assign a drive letter. Entering no value will disable any automatic action.

![Changing the default action to NewPartition](<../../.gitbook/assets/image (78) (1).png>)

After selecting the desired re-size disk option, an additional prompt appears to set an action for newly detected RAW disks. Automatic formatting can be enabled or disabled with `true` or `false`.

![Disabling auto RAW disk format](<../../.gitbook/assets/image (72) (2) (1).png>)

### CoreWeave auto-shutdown

Whether or not an instance powers off based on interactive user input is configured via [cloudInit](windows-images.md#coreweave-userdata-features) when an instance is initially deployed. Once an instance has already been deployed, this feature is also configurable via Windows Apps and Features:

![](<../../.gitbook/assets/image (71) (2).png>)

Clicking **Modify** prompts for an integer value in minutes to configure auto-shutoff, or set to `0` to disable:

![](<../../.gitbook/assets/image (92) (2).png>)

### CoreWeave Windows update

In order to ensure system stability and predictability, the native Windows Update manager is disabled by default on CoreWeave instances. Instead, through custom scripts, updates are applied as follows:

* Windows Defender updates are applied daily at 3:00AM UTC, or as soon as possible if missed. These are silent, and do not require reboots.
* On the second Wednesday of the month, one day after [Patch Tuesday](https://en.wikipedia.org/wiki/Patch\_Tuesday), at 3:00AM UTC, or as soon as possible if missed:
  * The `PSWindowsUpdate` module is updated
  * On non-Server OSes, WinGet is updated, where applicable
  * All Windows Updates are applied silently, without forcing reboots
  * If there is a pending reboot and no user is logged in, the system is rebooted to finish applying patches
  * If there is a pending reboot and a user logged in, the user is presented with a GUI prompt notifying them of pending system patches requiring a reboot
* Each day at 3:00AM UTC, the system is again checked for pending reboots. If there is a user logged in, they are notified, and asked to reboot. If there is no user logged in, the system will automatically be rebooted.

There are no user-configurable options for CoreWeave Windows Update. To revert to the default Windows Update behavior, simply uninstall the Windows Update manager from the Windows Apps and Features menu.

![](<../../.gitbook/assets/image (60) (1) (1).png>)

### CoreWeave PowerShell Profile

When launching a new PowerShell session, users are presented with some helpful system stats.

![](<../../.gitbook/assets/image (69) (2).png>)

To disable this functionality, simply delete the profile:

{% code overflow="wrap" %}
```powershell
rm "$env:SystemRoot\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1" -Force -Verbose
```
{% endcode %}

## CoreWeave PowerShell module

Included in CoreWeave Windows Images is a PowerShell module that provides functions for useful tasks and automation; moreover, some of the Cloud-Init Userdata features rely on the CoreWeave PowerShell module.

### Using the CoreWeave PowerShell module

The CoreWeave PowerShell Module is a system-wide module - as all Windows Images on CoreWeave Cloud use at minimum PowerShell version 5.1, the module will be automatically imported when any of its functions are called.

To manually import the CoreWeave Module:

```powershell
Import-Module CoreWeave -WarningAction SilentlyContinue
```

#### `Get-nVidiaDeviceDriverParameters`

This function matches and returns properties of the currently attached NVIDIA GPU. If there is not a valid driver installed and Windows cannot identify the attached GPU, the PCI ID will attempt to be matched instead. The output from this function is formatted for use in automating NVIDIA driver downloads.

```
Get-nVidiaDeviceDriverParameters
VERBOSE: After matching, GPU is NVIDIA Quadro RTX 4000, type is Quadro, series is Quadro RTX Series, product is Quadro
RTX 4000, OS is Windows Server 2022, Current driver is 516.25

Name                           Value
----                           -----
ProductType                    Quadro
ProductSeries                  Quadro RTX Series
Product                        Quadro RTX 4000
OperatingSystem                Windows Server 2022
RunningDriverVersion           516.25
```

#### `Download-nVidiaDisplayDriver`

This function automates downloading drivers from NVIDIA. This function has many parameters, each of which include argument completers:

{% code overflow="wrap" %}
```powershell
Syntax
    Download-nVidiaDisplayDriver [-ProductType] <string> [-ProductSeries] <string> [-Product] <string> [-OperatingSystem] <string> [-Language] <string> [[-DCH] <bool>] [[-RunningDriverVersion] <string>] [-Force ] [<CommonParameters>]
```
{% endcode %}

![Argument Completers](../../.gitbook/assets/2022.gif)

The easiest way to use this function is to combine it with [`Get-nVidiaDeviceDriverParameters`](windows-images.md#get-nvidiadevicedriverparameters). The returned output will be the location of the downloaded driver file:

{% code overflow="wrap" %}
```powershell
PS C:\> $Parameters = Get-nVidiaDeviceDriverParameters
VERBOSE: After matching, GPU is NVIDIA Quadro RTX 4000, type is Quadro, series is Quadro RTX Series, product is Quadro RTX 4000, OS is Windows Server 2019

PS C:\> Download-nVidiaDisplayDriver @Parameters -Language 'English (US)'
VERBOSE: Target driver version is 516.25
C:\Users\user\AppData\Local\Temp\1\516.25-nvidia-rtx-winserv-2016-2019-2022-64bit-international-dch-whql.exe
```
{% endcode %}

#### `Install-nVidiaDisplayDriver`

This function installs a downloaded NVIDIA driver file. If no path is provided, it will attempt to match and download the correct driver.

Setup will be ran directly and silently if it is detected that there is an attached NVIDIA GPU device. If no NVIDIA GPU device is detected, drivers will be manually added to the Windows Driver Store via `pnputil`.

{% code overflow="wrap" %}
```powershell
Synopsis
 
    Install-nVidiaDisplayDriver [[-DriverPath] <string>] [-CleanInstall] [-ForceInstall] [<CommonParameters>]
```
{% endcode %}

{% hint style="info" %}
**Note**

`-ForceInstall` will force the installation of the same or older driver version. `-CleanInstall` will wipe existing driver configurations.
{% endhint %}

The easiest way to use this function is to run it directly, allowing auto-match of the attached NVIDIA GPU. If you're already running the latest driver, no action will be taken:

{% code overflow="wrap" %}
```powershell
PS C:\> Install-nVidiaDisplayDriver
Transcript started, output file is C:\Logs\InstallnVidiaDisplayDriver.LOG
VERBOSE: After matching, GPU is NVIDIA Quadro RTX 4000, type is Quadro, series is Quadro RTX Series, product is Quadro  RTX 4000, OS is Windows Server 2022, Current driver is 516.25                                                           VERBOSE: Target driver version is 516.25
VERBOSE: Target driver 516.25 is less than or equal to running driver 516.25 and Force flag was not passed, we're not
gonna download anything
Transcript stopped, output file is C:\Logs\InstallnVidiaDisplayDriver.LOG
0
```
{% endcode %}

{% hint style="info" %}
**Note**

In the event new drivers are installed, a reboot is required, but not **enforced**.
{% endhint %}

#### `Configure-AutoLogon`

This function is called when [`Autologon: true`](windows-images.md#automatic-logon). The `-Action` parameter will either enable or disable automatic logon, with `$true` or `$false` respectively.

{% code overflow="wrap" %}
```powershell
Synopsis
    
    Configure-AutoLogon [[-InputObject] <pscredential>] [-Action] <bool> [<CommonParameters>]
```
{% endcode %}

The easiest way to use this function is to combine with `Get-Credential`:

```powershell
Configure-AutoLogon -Action:$true -InputObject (Get-Credential)
```

#### `Enroll-ParsecTeamMachine`

This function is called by the [Parsec Teams Cloud-Init feature](windows-images.md#enroll-a-parsec-teams-machine). If an instance was not enrolled at the time of deployment, enrollment can be completed silently using this function.

{% code overflow="wrap" %}
```powershell
Synopsis
    
    Enroll-ParsecTeamMachine [[-APIHost] <string>] [-ComputerKey] <string> [-TeamID] <string> [[-AppRuleID] <string>] [[-GuestAccess] <bool>] [[-UserID] <int>] [[-GroupID] <int>] [[-EMail] <string>] [[-BinPath] <string>] [<CommonParameters>]
```
{% endcode %}

#### `Invoke-SilentMSI`

This function automates silently installing a provided [Windows Installer](https://docs.microsoft.com/en-us/windows/win32/msi/windows-installer-portal) file.

{% code overflow="wrap" %}
```powershell
Synopsis
    
    Invoke-SilentMSI [-Action] <string> [[-MSI] <string>] [[-InstallerArgs] <string[]>] [<CommonParameters>]
```
{% endcode %}

An example, installing [PowerShell 7](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2):

```powershell
PS C:\> Start-BitsTransfer -Source https://github.com/PowerShell/PowerShell/releases/download/v7.2.4/PowerShell-7.2.4-win-x64.msi -Destination $env:TEMP
PS C:\> Invoke-SilentMSI -Action Install -MSI "$env:TEMP\PowerShell-7.2.4-win-x64.msi" -InstallerArgs @('ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL=1','ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1','ENABLE_PSREMOTING=1','REGISTER_MANIFEST=1')
Transcript started, output file is C:\Logs\PowerShell7-x647.2.4.0.LOG
VERBOSE: Beginning installation of PowerShell 7-x64 7.2.4.0
VERBOSE: PowerShell 7-x64 7.2.4.0  has completed with exit code 0: ERROR_SUCCESS
Transcript stopped, output file is C:\Logs\PowerShell7-x647.2.4.0.LOG
0
```

A given MSI can also be uninstalled using the same function:

{% code overflow="wrap" %}
```powershell
PS C:\> Invoke-SilentMSI -Action Remove -MSI "$env:TEMP\PowerShell-7.2.4-win-x64.msi"
Transcript started, output file is C:\Logs\PowerShell7-x647.2.4.0.LOG
VERBOSE: Beginning REMOVAL of PowerShell 7-x64 7.2.4.0
VERBOSE: PowerShell 7-x64 7.2.4.0  REMOVAL has completed with exit code 0: ERROR_SUCCESS
Transcript stopped, output file is C:\Logs\PowerShell7-x647.2.4.0.LOG
0
```
{% endcode %}
