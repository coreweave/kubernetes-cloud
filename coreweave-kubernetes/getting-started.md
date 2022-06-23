# Getting Started

### Obtain Access Credentials

[Sign up for CoreWeave Cloud](https://cloud.coreweave.com/request-account) and generate a `kubeconfig` from the [API Access ](https://cloud.coreweave.com/api-access)page. Every time an Access Token is generated, by default the corresponding `kubeconfig` will automatically download. This `kubeconfig` file allows you to interact with our Kubernetes cluster using kubectl and other Kubernetes applications.

![](../docs/.gitbook/assets/cw-access-token.png)

On CoreWeave's Access Token page click "Generate your first token" (or "Generate another token" if you have already generated a kubeconfig) and optionally give the token a recognizable name. Once you create it, a new kubeconfig will be generated that embeds the access token. By \_\_ default your corresponding kubeconfig will automatically download. The browser might ask where to save the file `cw-kubeconfig`.

* The generated **kubeconfig** file is used to interact with our Kubernetes cluster using clients like kubectl, etc.
* **Access Tokens** are used for programmatic access to CoreWeave Cloud applications like [Prometheus](prometheus/)

{% hint style="danger" %}
The kubeconfig and Access Token is shown & given one time! Be sure to save in a secure location. You can find your access token embedded inside your kubeconfig file if misplaced.
{% endhint %}

### Install Kubernetes Command Line Tools

Once you have obtained your credentials, all you have to do is put them in place and download the command line tools. No other setup is necessary, you are instantly ready to deploy your workloads and containers. Cut-and-paste instructions are below. For more detail please reference the [official documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

{% tabs %}
{% tab title="Linux" %}
The following command will install `kubectl` on your Linux system.

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Once you have kubectl downloaded, you can install it by moving the file into the system bin folder.

```
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

If you prefer to installing using the native package manager, please view Kubernetes guide on [Installing using Native Package Manager](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management).

**Verify kubectl Binary**

If you'd like to verify kubectl, you can verify it by running:

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
echo "$(<kubectl.sha256) kubectl" | sha256sum --check
```

This should return `kubectl: OK` to confirm it is indeed valid. If this returns an error, please review the [kubectl installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) from Kubernetes.
{% endtab %}

{% tab title="Mac OSX" %}
Most Mac users use [brew](https://brew.sh) to install packages, to install `kubectl` run the command below:

```
brew install kubectl
```

If you don't have brew installed, follow the [Brew Installation](https://brew.sh) guide.
{% endtab %}

{% tab title="Windows" %}
#### Install Using PowerShell

If you use PowerShell, install `kubectl` using the following the command:

```
& $([scriptblock]::Create((New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/coreweave/kubernetes-cloud/master/getting-started/k8ctl_setup.ps1')))
```

{% hint style="info" %}
Add `-Silent` to the end of this string for a non-interactive setup.
{% endhint %}

#### Install using Package Manager

You can also install `kubectl` on Windows using either [Chocolatey](https://chocolatey.org) or [Scoop](https://scoop.sh) using the following commands:

Using [Chocolatey](https://chocolatey.org):

```
choco install kubernetes-cli
```

Using [Scoop](https://scoop.sh):

```
scoop install kubectl
```

If you prefer to download the `kubectl` exe file directly, [download the latest version](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-kubectl-binary-with-curl-on-windows).
{% endtab %}
{% endtabs %}

### Setup Kubernetes Config

Once you have `kubectl` installed and the `kubeconfig` file generated and downloaded you can begin to use CoreWeave's Kubernetes infrastructure! To copy/merge with kubectl you can run the following commands:

```shell
# create a backup of current kubeconfig
cp ~/.kube/config ~/.kube/config.bak

# install CoreWeave Kubernetes credentials
KUBECONFIG=~/.kube/config:~/Downloads/cw-kubeconfig \
  kubectl config view --merge --flatten > ~/.kube/config
```

{% hint style="info" %}
Be sure to replace \~/Downloads directory with the location of your generated kubeconfig.
{% endhint %}

The command above will create a backup of your kubeconfig at `~/.kube/config.bak`

#### Default kubectl Directory

* Linux path: `~/.kube/config`
* MacOSX path: `/Users/<username>/.kube/config`
* Windows Path: `%USERPROFILE%\.kube\config`

#### Verify Kubernetes Credentials

Since your new account will not have any resources, listing the secrets is a good start to ensure proper communication with the cluster. To verify your CoreWeave Kubernetes configs using kubectl you can run the following commands:

```
kubectl config set-context coreweave
kubectl get secret
```

The command above should return your default secrets like so,

```
NAME                           TYPE                                  DATA   AGE
default-token-frqgm            kubernetes.io/service-account-token   3      3h
```

### Congratulations! :tada: You're ready to use CoreWeave Cloud!

Your system is ready to deploy all types of services on CoreWeave's Kubernetes infrastructure. Checkout some of the examples by heading over to Examples.Your file is as secret as your password! **Keep it safe, and do not share.**
