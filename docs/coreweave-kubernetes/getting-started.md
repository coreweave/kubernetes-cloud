---
description: Learn how to configure your CoreWeave Kubernetes setup to access the Cloud
---

# Get Started with CoreWeave

## Create an account

To generate access credentials for CoreWeave Cloud, first [sign up for an account](https://cloud.coreweave.com/request-account).

After providing payment information, you will receive a verification email to the account provided. After verifying your address, your information will be submitted to our team to verify your account request. You will also be redirected to a page that confirms the request was received.

{% hint style="success" %}
**Tip**

For a higher chance of admission, it is strongly recommended to fill out [the inbound sales form](https://coreweave.com/contact-us) after submitting your account request. **Please note, account approval may take up to three business days.**
{% endhint %}

## Obtain CoreWeave access credentials

{% hint style="warning" %}
**Important**

Only organization admins may generate, view, and delete Access Tokens. For each user who requires a separate Access Token, a new Token and corresponding Kubeconfig file must be generated. The organization admin must then share this file with the user in a secure manner.
{% endhint %}

On CoreWeave, [**Kubeconfig files**](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) are used to interact with our Kubernetes cluster via clients such as `kubectl`. **API Access Tokens** are used for programmatic access to CoreWeave Cloud applications, such as [Prometheus](../../coreweave-kubernetes/prometheus/).

Once the organization admin account has been approved and is activated, the admin may [log in to the CoreWeave Cloud UI](https://cloud.coreweave.com), then navigate to **API Access** on the left-hand menu. New Kubeconfig files and credentials as well as new API tokens are edited, viewed, and generated from this page.

<figure><img src="../.gitbook/assets/image (7) (5).png" alt="Screenshot of The API &#x26; Kubeconfig page on the Cloud UI"><figcaption><p>The API &#x26; Kubeconfig page on the Cloud UI, accessed via the "API Access" link on the left-hand menu</p></figcaption></figure>

### Generate the Kubeconfig file

{% hint style="danger" %}
**Warning**

**The Kubeconfig and Access Token are shown** **only once!**\
Be sure to save this file and the token in a secure location. If you lose your Access Token, it can be found inside your [Kubeconfig file](getting-started.md#configure-kubernetes).
{% endhint %}

Organization admins may generate new Access Tokens by navigating to the [API Access page](https://cloud.coreweave.com/api-access) on the Cloud UI. From here, click the **API & Kubeconfig** tab at the top right of the page, then click the **Create a New Token** button to the right.

Once prompted, give the token a recognizable name, then click the **Generate** button. Generating the new token will also create a Kubeconfig file with the name `cw-kubeconfig`, which will embed your token. This file will download automatically.

{% hint style="info" %}
**Note**

If you would like to prevent the Kubeconfig file from downloading automatically, un-check the **Automatically download Kubeconfig** checkbox.
{% endhint %}

<figure><img src="../.gitbook/assets/image (4) (4).png" alt="The &#x22;New Access Token&#x22; modal"><figcaption><p>The "New Access Token" modal</p></figcaption></figure>

## Install the Kubernetes command line tools

Once you have obtained your Access Credentials from your organization admin, download the Kubernetes command line tools to your local machine.

{% hint style="info" %}
**Additional Resources**

For more information on Kubernetes installation and configuration, please reference the [official Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
{% endhint %}

{% tabs %}
{% tab title="Linux" %}
## Installing `kubectl` on a Linux system

### **Downloading and installing the binary**

The following command is a simple way to install `kubectl` on your Linux system by downloading the binary.

{% code overflow="wrap" %}
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
{% endcode %}

Once you have the `kubectl` binary downloaded, install it by first making the binary executable:

```bash
$ chmod +x ./kubectl
```

Then, move the file into the system `bin` directory:

```bash
$ sudo mv ./kubectl /usr/local/bin/kubectl
```

{% hint style="info" %}
**Note**

If you would prefer to install Kubernetes using a Native Package Manager, please view [the Kubernetes guide on Installing using Native Package Manager](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management).
{% endhint %}

**Verifying the kubectl binary**

If you'd like to verify kubectl, you can verify it by running a checksum operation on the downloaded file prior to installing it, such as:

{% code overflow="wrap" %}
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
echo "$(<kubectl.sha256) kubectl" | sha256sum --check
```
{% endcode %}

This should return `kubectl: OK` to confirm the file is indeed valid. If this returns an error, please review the [official `kubectl` installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).
{% endtab %}

{% tab title="macOS" %}
## Installing `kubectl` on a macOS system

### **Installing using Homebrew**

Most Mac users use [Homebrew](https://brew.sh) to install packages.

If you do not already have Homebrew installed, follow the [Brew Installation](https://brew.sh) guide to do so, then install `kubectl` using Homebrew by running the following command:

```bash
$ brew install kubectl
```
{% endtab %}

{% tab title="Windows" %}
## Installing `kubectl` on a Windows system

### **Installing using PowerShell**

Using PowerShell, `kubectl` can be installed by using the following the command:

{% code overflow="wrap" %}
```powershell
& $([scriptblock]::Create((New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/coreweave/kubernetes-cloud/master/getting-started/k8ctl_setup.ps1')))
```
{% endcode %}

{% hint style="info" %}
**Note**

Add the `-Silent` flag to the end of this string for a non-interactive setup.
{% endhint %}

### **Installing using a Package Manager**

You can also install `kubectl` on Windows using a package manager such as [Chocolatey](https://chocolatey.org) or [Scoop](https://scoop.sh).

**Using** [**Chocolatey**](https://chocolatey.org)**:**

```powershell
$ choco install kubernetes-cli
```

**Using** [**Scoop**](https://scoop.sh)**:**

```powershell
$ scoop install kubectl
```

If you would prefer to download the `kubectl` executable directly, [follow the official Kubernetes instructions to download the latest version](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-kubectl-binary-with-curl-on-windows).
{% endtab %}
{% endtabs %}

## Configure Kubernetes

Finally, once you [have `kubectl` installed](getting-started.md#installing-the-kubernetes-command-line-tools), and the `cw-kubeconfig` file has been [generated and obtained from your organization admin](getting-started.md#generate-the-kubeconfig-file), the next step is to move the config file to the right location.

By default, `kubectl` looks for the Kubeconfig file in the `$HOME/.kube` directory, and anticipates that the file is named `config`.

<details>

<summary>I do not have a <code>~/.kube/config</code> file</summary>

If this is your first time using Kubernetes, or you're using a system that has never had Kubernetes configured before, you probably don't have a Kubeconfig file.

You can check to see if you do by inspecting the Kubeconfig default path:

```bash
ls ~/.kube/config
```

If you **do not** have a Kubeconfig file, all you need to do is create the `~/.kube` directory if it does not already exist, and then move the downloaded `cw-kubeconfig` to the `~/.kube/config` path:

```bash
mkdir ~/.kube && mv ~/Downloads/cw-kubeconfig ~/.kube/config
```

If for some reason you would like to use a different path for the config file for your cluster, you can export the `$KUBECONFIG` environment variable. For example:

```bash
export KUBECONFIG=~/.kube/cw-kubeconfig
```

Or, you can specify a path using the `--kubeconfig` option with `kubectl`.

</details>

<details>

<summary>I have an existing Kubeconfig file</summary>

If you **already have an existing Kubeconfig file,** you can install the CoreWeave Kubernetes credentials by merging the `cw-kubeconfig` file into `~/.kube/config`.

To do this, first create a backup copy of the original Kubeconfig file:

```shell
$ cp ~/.kube/config ~/.kube/config.bak
```

Next, merge the downloaded `cw-kubeconfig` file into the file at the default path using `kubectl`:

```bash
$ KUBECONFIG=~/.kube/config:~/Downloads/cw-kubeconfig \
kubectl config view --merge --flatten > ~/.kube/config
```

</details>

### Paths for Windows and macOS

If you are working on a system other than a Linux system, replace `~/.kube/config` path with one of the corresponding paths below. Be sure to replace the `~/Downloads` path in this example with the actual location of your downloaded Kubeconfig file, and the default path with the one that is applicable to your system.

#### Default Kubernetes configuration directories by OS

| Operating System | Default path                     |
| ---------------- | -------------------------------- |
| Linux            | `~/.kube/config`                 |
| macOS X          | `/Users/<username>/.kube/config` |
| Windows          | `%USERPROFILE%\.kube\config`     |

### Verify Kubernetes credentials

Since your new account will not yet have any resources, listing your [cluster `secrets`](https://kubernetes.io/docs/concepts/configuration/secret/) is a good way to test that proper communication with the cluster is in place. To verify your CoreWeave Kubernetes configuration using `kubectl`, invoke the following commands.

First, set [the Kubernetes context](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#context) to `coreweave`:

```bash
$ kubectl config set-context coreweave
```

Next, request [the `secret` objects](https://kubernetes.io/docs/concepts/configuration/secret/):

```bash
$ kubectl get secret
```

This should return your default `secrets`, such as:

```
NAME                           TYPE                                  DATA   AGE
default-token-frqgm            kubernetes.io/service-account-token   3      3h
```

## Congratulations! :tada:

You are now ready to use CoreWeave Cloud to deploy all types of services on CoreWeave's Kubernetes infrastructure!

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4a5">💥</span> <strong>Check out some examples of what you can do on CoreWeave Cloud!</strong></td><td></td><td></td><td><a href="../../coreweave-kubernetes/examples/">examples</a></td></tr></tbody></table>
