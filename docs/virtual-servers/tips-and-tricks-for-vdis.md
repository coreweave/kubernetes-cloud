---
description: How to get the best user experience with your VDI
---

# Tips and Tricks for VDIs

If you are experiencing performance issues with your [Virtual Desktop Infrastructure (VDI)](../../virtual-servers/getting-started.md#create-virtual-desktops-and-developer-workstations-accessible-from-anywhere), CoreWeave recommends taking the following actions to greatly improve your user experience.

## Using Parsec

When using Parsec to connect to your Windows-based VDI, there are a few configuration options you can change to enhance your user experience. To adjust global settings, navigate to the **Settings** page by clicking the gear icon in the left-hand vertical menu.

Once you have selected a machine to connect to, further configuration options for that instance are shown by clicking the Parsec logo button on the left-hand side of the screen.

<figure><img src="../.gitbook/assets/image (4) (2).png" alt="Screenshot: The gear icon leading to the Parsec Settings page"><figcaption><p>The gear icon leading to the Parsec Settings page</p></figcaption></figure>

### Enable H.265 (HEVC) encoding

[H.265 (HVEC) video coding](https://en.wikipedia.org/wiki/High\_Efficiency\_Video\_Coding) is considered the contemporary standard video codec for streaming video. It is recommended to enable use of this codec.

{% hint style="info" %}
**Additional Resources**

Read more about video coding on [the Parsec website](https://parsec.app/blog/an-introduction-to-video-compression-c5061a5d075e).
{% endhint %}

<figure><img src="../.gitbook/assets/image (10).png" alt="Screenshot: It is recommended to turn the H.265 (HEVC) setting to On"><figcaption><p>It is recommended to turn the H.265 (HEVC) setting to On</p></figcaption></figure>

### Always run Parsec in full screen

For most cases, matching your VDI resolution to your local display resolution will yeild the best performance and visuals in Parsec. You can do this by using the Parsec menu, or by using NVIDIA Control Panel on your VDI.

<figure><img src="../.gitbook/assets/image (3).png" alt="Screenshot: It is recommended to run Parsec in Fullscreen mode"><figcaption><p>It is recommended to run Parsec in Fullscreen mode</p></figcaption></figure>

### Set "Immersive Mode" to `Keyboard`

Parsec's "[Immersive Mode](https://support.parsec.app/hc/en-us/articles/360003146271-Send-Special-Keys-To-The-Host-By-Default-Immersive-Mode-)" passes Windows-native hotkeys to the host machine.

<figure><img src="../.gitbook/assets/image (23).png" alt="Screenshot: It is recommended to set &#x22;Immersive Mode&#x22; to &#x22;Keyboard&#x22;"><figcaption><p>It is recommended to set "Immersive Mode" to "Keyboard"</p></figcaption></figure>

### Set bandwidth limit to 50Mbps

Once connected to an instance, navigate to the **Bandwidth Limit** option and select **50 Mbps** from the Parsec menu on the left-hand side of the screen.

<figure><img src="../.gitbook/assets/image (6).png" alt="Screenshot: it is recommended to set Parsec&#x27;s bandwidth limit to 50 Mbps"><figcaption><p>It is recommended to set Parsec's bandwidth limit to 50 Mbps</p></figcaption></figure>

### Set the VDI resolution to your local display's resolution

For most cases, matching your VDI resolution to your local display resolution will yield the best performance and visuals in Parsec. The resolution may be set either by using the Parsec menu (as shown below) or by using the NVIDIA Control Panel on your VDI.

If you are trying to set your VDI to a non-standard resolution (e.g. MacBook Pro's native resolution of `2880x1800`), use the NVIDIA Control Panel, as the Parsec menu only includes standard resolution options.

<figure><img src="../.gitbook/assets/image (8) (3).png" alt="Screenshot: It is recommended to set Parsec&#x27;s resoluton to your host machine&#x27;s native resolution"><figcaption><p>It is recommended to set Parsec's resoluton to your host machine's native resolution</p></figcaption></figure>

#### Setting resolution using the NVIDIA control panel

If you'd prefer to set your resolution using the NVIDIA control panel, you can do so once logged in to your VDI, you can do so:

1. Navigate to the **Control Panel.** This can be done either by right-clicking the VDI desktop and navigating to "NVIDIA Control Panel" or by searching for it in the **Start** menu. (Windows 11 users will have to click "Show more options" to locate the option for the NVIDIA Control Panel.)
2. Once in the Control Panel, navigate to the task list and click **Change Resolution**.
3. On the list of enabled displays select the display you want to change resolution of, then below that, select the resolution you would like set.
4. Click the **Apply** button.

<figure><img src="../.gitbook/assets/image (5).png" alt="Screenshot: The NVIDIA control panel&#x27;s resolution menu"><figcaption><p>The NVIDIA control panel's resolution menu</p></figcaption></figure>

### Prefer 4:4:4 color

The default Parsec stream is in 4:2:0, which is the standard for video encoding. 4:2:0 color reduces the amount of chroma (color) information while keeping luma (brightness) intact, in order to reduce the amount of data used. 4:4:4 color, on the other hand, retains chroma information.

Unless you have an [NVIDIA Turing](https://www.nvidia.com/en-us/geforce/turing/) or other newer NVIDIA GPU in your client, it is recommended to leave or enable the "Prefer 4:4:4 color" setting.

{% hint style="info" %}
**Additional Resources**

You can learn more about how Parsec uses color encoding on [the Parsec website](https://support.parsec.app/hc/en-us/articles/4425688194189#444).
{% endhint %}

<figure><img src="../.gitbook/assets/image (11) (4).png" alt=""><figcaption></figcaption></figure>

## Network

### Hardwire your network connection

It is strongly recommended to use a hardwired network connection rather than a wireless network connection (WiFi). Wireless connections often add latency and jitter, with bursts of packet loss when there is interference. A hardwired network connection will prevent these issues, and most likely result in a smoother experience.
