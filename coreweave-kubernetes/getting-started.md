---
description: Learn how to configure your CoreWeave Kubernetes setup to access the Cloud.
---

# Get Started with CoreWeave

## Obtaining CoreWeave access credentials

On CoreWeave, **Kubeconfig** files are used to interact with our Kubernetes cluster by using clients such as `kubectl`, and **API Access Tokens** are used for programmatic access to CoreWeave Cloud applications such as [Prometheus](prometheus/).

To generate your access credentials, first [sign up for CoreWeave Cloud](https://cloud.coreweave.com/request-account). Once you have an account, [log in to the Cloud UI](https://cloud.coreweave.com), then navigate to [the **API & Kubeconfig** page](https://cloud.coreweave.com/api-access) from the left-hand side menu.

<figure><img src="../docs/.gitbook/assets/image (1) (2) (2).png" alt="The Cloud UI API Access page"><figcaption><p>The Cloud UI API Access page</p></figcaption></figure>

{% hint style="danger" %}
**Warning**

The Kubeconfig and Access Token is shown and given **only once**! Be sure to save this file and the token in a secure location. If you lose your Access Token, it can be found inside your Kubeconfig file.
{% endhint %}

From the [Cloud UI API Access page](https://cloud.coreweave.com/api-access), click the **New Token & Kubeconfig** button at the top right. When prompted, give the token a recognizable name, then click the **Generate** button. Generating the new token will also create a Kubeconfig file in which that token will be embedded, which will download automatically.

{% hint style="info" %}
**Note**

If you would like to prevent the Kubeconfig file from downloading automatically, un-check the **Automatically download Kubeconfig** checkbox.
{% endhint %}

<figure><img src="../docs/.gitbook/assets/image (3) (2) (1).png" alt="Create a new access token dialog box"><figcaption><p><strong>Create a new access token</strong> dialog box</p></figcaption></figure>

## Installing the Kubernetes command line tools

Once you have obtained your Access Credentials, all you have to do is put them in the right place and download the Kubernetes command line tools.

No other setup is necessary; once you install the command line tools as described below, you will be ready to deploy your workloads and containers!

{% hint style="info" %}
**Additional Resources**

For more information on Kubernetes installation and configuration, please reference the [official Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
{% endhint %}

{% tabs %}
{% tab title="Linux" %}
#### Installing `kubectl` on a Linux system

**Downloading and installing the binary**

The following command is a simple way to install `kubectl` on your Linux system by downloading the binary.

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

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

\*\*\*\*\
**Verifying the kubectl binary**

If you'd like to verify kubectl, you can verify it by running a checksum operation on the downloaded file prior to installing it, such as:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
echo "$(<kubectl.sha256) kubectl" | sha256sum --check
```

This should return `kubectl: OK` to confirm the file is indeed valid. If this returns an error, please review the [official `kubectl` installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).
{% endtab %}

{% tab title="macOS" %}
#### Installing `kubectl` on a Linux system

**Installing using Homebrew**

Most Mac users use [Homebrew](https://brew.sh) to install packages.

If you do not already have Homebrew installed, follow the [Brew Installation](https://brew.sh) guide to do so, then install `kubectl` using Homebrew by running the following command:

```bash
$ brew install kubectl
```
{% endtab %}

{% tab title="Windows" %}
#### Installing `kubectl` on a Windows system

**Installing using PowerShell**

Using PowerShell, `kubectl` can be installed by using the following the command:

```powershell
& $([scriptblock]::Create((New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/coreweave/kubernetes-cloud/master/getting-started/k8ctl_setup.ps1')))
```

{% hint style="info" %}
**Note**

Add the `-Silent` flag to the end of this string for a non-interactive setup.
{% endhint %}



**Installing using a Package Manager**

You can also install `kubectl` on Windows using a package manager such as [Chocolatey](https://chocolatey.org) or [Scoop](https://scoop.sh).

Using [Chocolatey](https://chocolatey.org):

```powershell
$ choco install kubernetes-cli
```

Using [Scoop](https://scoop.sh):

```powershell
$ scoop install kubectl
```

If you would prefer to download the `kubectl` executable directly, [follow the official Kubernetes instructions to download the latest version](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-kubectl-binary-with-curl-on-windows).
{% endtab %}
{% endtabs %}

## Configuring Kubernetes

Once you have `kubectl` installed and the Kubeconfig file is generated and downloaded, you can begin to use CoreWeave's Kubernetes infrastructure! To copy and merge the Kubeconfig file, you can run the following commands using `kubectl`:

First, create a backup copy of the Kubeconfig file:

```shell
$ cp ~/.kube/config ~/.kube/config.bak
```

Next, install the CoreWeave Kubernetes credentials by merging the config file into `~/.kube/config`, which is the default Linux filepath that Kubernetes uses to source configuration settings.

```bash
$ KUBECONFIG=~/.kube/config:~/Downloads/cw-kubeconfig \
kubectl config view --merge --flatten > ~/.kube/config
```

If you are working on a different kind of system, replace `~/.kube/config` with one of the following, and be sure to replace the `~/Downloads` path in this example with the actual location of your downloaded Kubeconfig file, and the default path with the one applicable to your system.

#### Default Kubernetes configuration directories by OS

| Operating System | Default path                     |
| ---------------- | -------------------------------- |
| Linux            | `~/.kube/config`                 |
| macOS X          | `/Users/<username>/.kube/config` |
| Windows          | `%USERPROFILE%\.kube\config`     |

#### Verify Kubernetes credentials

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

You are now ready to use CoreWeave Cloud!

Your system is ready to deploy all types of services on CoreWeave's Kubernetes infrastructure.

* [Check out some examples of what you can do](examples/).
