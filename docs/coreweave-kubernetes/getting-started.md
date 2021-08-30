# Getting Started

### Obtain Access Credentials

[Sign up for CoreWeave Cloud](https://cloud.coreweave.com/request-account) and generate a kubeconfig from the [API Access ](https://cloud.coreweave.com/api-access)page. Every time an access token is generated your corresponding kubeconfig will automatically download.

![](../.gitbook/assets/cw-access-token.png)

### Install Kubernetes Command Line Tools

Once you have received your credentials, all you have to do is put them in place and download the command line tools. No other setup is necessary, you are instantly ready to deploy your workloads and containers. Cut-and-paste instructions are below. For more detail please reference the [official documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

#### Mac OS

```text
brew install kubectl
```

#### Linux

```text
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

### Set Up Access

You will have received a pre-populated `k8s-conf` file from CoreWeave as part of your onboarding package. The snippet below assumes that you have no other Kubernetes credentials stored on your system, if you do you will need to open both files and copy the `cluster`, `context` and `user` from the supplied `k8s-conf` file into your existing `~/.kube/config` file.

Replace `~/Downloads` with the path to the `kube-config` supplied by CoreWeave.

```text
mkdir -p ~/.kube/
mv ~/Downloads/k8s-tenant-test-conf ~/.kube/config
```

### Verify Access

Since your new account will not have any resources, listing the secrets is a good start to ensure proper communication with the cluster.

```text
$ kubectl get secret                                                                                                                                                                                                                            git:(master|…
NAME                           TYPE                                  DATA   AGE
default-token-frqgm            kubernetes.io/service-account-token   3      5d3h
```

Once access is verified you can deploy the examples found in this repository.

### Next Steps

Head on over to Examples to deploy some workloads!

{% page-ref page="examples/" %}

