# Windows Images

**Objective:** Learn the various features and enhancements in Windows images provided by CoreWeave Cloud.\
**Overview:** CoreWeave offers a variety of operating system base images, enhanced to run on CoreWeave Cloud, via our **vd-images** namespace. This guide details the Windows specific ones.

## Cloud-Init

Windows images on CoreWeave cloud use [Cloudbase-Init](https://github.com/cloudbase/cloudbase-init), a Windows implementation of Canonical's [cloud-init](https://github.com/canonical/cloud-init).

By default, we enable the following plugins (executed sequentially):

1. [UserDataPlugin](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#user-data-main)
2. [LocalScriptsPlugin](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#local-scripts-execution-main)
3. [SetHostNamePlugin](https://cloudbase-init.readthedocs.io/en/latest/plugins.html#setting-hostname-main)

### Adding Custom Userdata

When creating a new Virtual Server on CoreWeave cloud, instance specific information such as user account information and SSH keys are automatically passed through as Cloud-Init Userdata. When deploying a new Virtual Server, one has the ability to add additional information via Userdata as well.&#x20;

#### Via `kubectl` [YAML](https://github.com/coreweave/kubernetes-cloud/blob/17c3bbe10f8ded84835f07118521dcc42af297af/virtual-server/examples/kubectl/virtual-server-cloudinit.yaml#L45):&#x20;

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

#### Via the [CoreWeave Apps Web UI](../deployment-methods/coreweave-apps.md):&#x20;

Within the Virtual Server deployment form, switch to the YAML tab:

![](<../../.gitbook/assets/image (64) (1).png>)

Towards the bottom of the page, a commented out cloudInit section will be pre-populated. Uncomment to add custom user data:

![](<../../.gitbook/assets/image (66).png>)

{% hint style="info" %}
For more information on what be added via native cloudInit Userdata, view the Cloudbase Solutions documentation [here](https://cloudbase-init.readthedocs.io/en/latest/userdata.html#userdata).
{% endhint %}

### CoreWeave Userdata Features

There are several CoreWeave init scripts included in our base Windows image, that can be enabled via cloudInit Userdata.&#x20;

#### Add Samba Mounts

Samba shares (Or any SMB/CIFS compliant share) can be added via cloudInit, to be mounted to the first available drive letter, at initial user login.

Using an example from a Samba instance hosted via CoreWeave Cloud Apps, we can derive the following information:

![](<../../.gitbook/assets/image (92).png>)

Using our share information, we can populate the cloudInit `key: value` pairs:

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
By default, available drive letters are randomized and the first available one is selected per share. \
\
Drive letters can be manually specified by adding, E.G: `Drive: Z`
{% endhint %}

#### Enroll a Parsec Teams Machine

CoreWeave Windows images support [Parsec Teams](https://parsec.app/teams). To enroll a Parsec Teams machine, add the following when deploying a VS:&#x20;

```yaml
  cloudInit: |
    ParsecTeams:
      ComputerKey: key_generated_from_parsec_admin_panel
      TeamId: parsec_team_id
      # Use EITHER Group ID or EMail
      GroupId: parsec_group_id
      EMail: parsec_user_email
```

For more information on Parsec Teams and where to obtain your enrollment key, please visit [Parsec's documentation](https://support.parsec.app/hc/en-us/articles/360054176332-Team-Computers).

{% hint style="info" %}
When enrolling a Parsec Teams machine, Boolean values `Parsec: true` and `EDID: true` will also need to be added to your manifest.
{% endhint %}

#### Install Additional Software

All CoreWeave Windows images are pre-loaded with [Chocolatey](https://community.chocolatey.org/packages) package manager. On non Server editions of Windows, [WinGet](https://winget.run) is included as well.&#x20;

Software specified via cloudInit will be installed automatically at initial user logon:

```yaml
  cloudInit: |
    Choco_Install:
      - googlechrome
      - firefox
    WinGet_Install:
      - Discord.Discord
      - Microsoft.VisualStudioCode
```

#### Power-off with no interactive input

Windows images include scripts that can detect user activity (E.G, moving the mouse, keyboard inputs). When enabled, it can detect a specified period of no user input, and automatically shutdown. A prompt along with a 5 minute grace period when the timer threshold is reached. Adding the following will prompt the user after 10 minutes of no activity, and shutoff automatically after an additional 5 minutes if the prompt is not acknowledged:

```yaml
  cloudInit: |
    shutoff_on_idle: 10
```

{% hint style="warning" %}
This feature should be combined with `RunStrategy: RerunOnFailure` via `vm.Spec` to prevent the instance from automatically powering back on once shutoff.

Additionally, boolean flag `Autologon` should be set to `true`, as the idle tracker runs within the user context.
{% endhint %}

### Boolean Userdata Features

Some Userdata features can be enabled with Boolean values `true` or `false`.&#x20;

#### Teradici PCoIP Graphics Agent for Windows

CoreWeave Cloud supports [Teradici PCoIP](https://docs.teradici.com/documentation/graphics-agent-for-windows/release-notes) on both Linux and Windows. Adding the following will install the graphics agent on initial logon, pointed to our licensing server:

```yaml
  cloudInit: |
    Teradici: true
```

{% hint style="warning" %}
Teradici should not be combined with either Parsec or Virtual Display options below.
{% endhint %}

#### Virtual Display

Many applications on Windows require a display connected to GPU in order to render on it. Adding the below value will attach a virtual 4k monitor to all available outputs, and disconnect the built-in VNC display:

```yaml
  cloudInit: |
    EDID: true
```

{% hint style="info" %}
Unless set to `false`, this flag defaults to `true`.
{% endhint %}

#### Parsec Remote Desktop

CoreWeave strongly recommends [Parsec](https://parsec.app) for remote access on Windows GPU instances. Adding the following will install Parsec on initial logon:

```yaml
  cloudInit: |
    EDID: true
    Parsec: true
```

{% hint style="info" %}
Parsec requires the use of a Virtual Display, and thus must always be installed alongside `EDID: true`.

Unless set to `false`, this flag defaults to `true`.
{% endhint %}

#### Automatic Logon

This flag configures the user account created for automatic logon.

```yaml
  cloudInit: |
    Autologon: true
```

{% hint style="info" %}
Unless set to `false`, this flag defaults to `true`.
{% endhint %}

## Operating System Customizations

There are several modifications made to a vanilla Windows instance in order to optimize for use on CoreWeave Cloud. Depending on one's use case, these can be disabled or modified.

#### CoreWeave Resize Disk

By default, when the root disk of a Windows image is expanded, Windows will automatically expand the root disk partition to use all of the available space. Additionally, any new block volumes mounted to a Windows instance will automatically be initialized and partitioned as GPT, and formatted as NTFS.&#x20;

Via Windows Apps and Features, the default behavior can be modified:

![](<../../.gitbook/assets/image (62).png>)

Selecting "Modify" will prompt for an action to perform when it is detected that the root disk can be expanded. The default action of `ReSize` will expand the root disk. `NewPartition` will create a new partition with the unallocated space, and automatically assign a drive letter. Entering no value will disable any automatic action.

![Changing the default action to "NewPartition"](<../../.gitbook/assets/image (87) (1).png>)

After selecting the desired re-size disk option, an additional prompt appears to set an action for newly detected RAW disks. Automatic formatting can be enabled or disabled with `true` or `false`.

![Disabling auto RAW disk format](<../../.gitbook/assets/image (83).png>)

#### CoreWeave Auto Shutdown

Instance power-off based on interactive user input can be configured via [cloudInit](windows-images.md#coreweave-userdata-features) when an instance is initially deployed. Once an instance has already been deployed, this feature is also configurable via Windows Apps and Features:&#x20;

![](<../../.gitbook/assets/image (81).png>)

Modifying will prompt for an integer value in minutes to configure auto-shutoff, or set to 0 to disable:

![](<../../.gitbook/assets/image (96).png>)

#### CoreWeave Windows Update

In order to ensure system stability and predictability, native Windows Update is disabled by default on CoreWeave instances. Instead, through custom scripts, updates are applied as follows:

* Windows Defender updates are applied daily at 3AM UTC, or as soon as possible if missed
  * These are silent and do not require reboots
* On the second Wednesday of the month (one day after [Patch Tuesday](https://en.wikipedia.org/wiki/Patch\_Tuesday)), at 3AM UTC, or as soon as possible if missed:
  * PSWindowsUpdate module is updated
  * On non-Server OS, WinGet is updated (if applicable)&#x20;
  * All Windows Updates are applied silently, without forcing reboot
  * If there is a pending reboot and no user is logged in, the system is rebooted to finish applying patches
  * If there is a pending reboot and a user logged in, the user is presented with a GUI prompt notifying them of pending system patches requiring a reboot
* Each day at 3AM UTC, the system is again checked for pending reboots. If there is a user logged in, they are notified and asked to reboot. If there is no user logged in, the system will be automatically rebooted.&#x20;

There are no user configurable options for CoreWeave Windows Update. To revert to the default Windows Update behavior, simply uninstall from Windows Apps and Features:

![](<../../.gitbook/assets/image (65).png>)

#### CoreWeave PowerShell Profile

When launching a new PowerShell session, users are presented with some helpful system stats:

![](<../../.gitbook/assets/image (78) (1).png>)

To disable this functionality, simply delete the profile:

```powershell
rm "$env:SystemRoot\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1" -Force -Verbose
```
