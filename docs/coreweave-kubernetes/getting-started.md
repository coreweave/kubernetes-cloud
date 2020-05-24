# Getting Started

### Obtain Access Credentials

[Sign up for CoreWeave Kubernetes](https://www.coreweave.com/#getstarted) and receive the credentials file needed to access the Kubernetes cluster.

### Install Kubernetes Command Line Tools

Cut-and-paste instructions are below. For more detail please reference the [official documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

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

Since your new account will not have any resources, listing the secrets is a good start to make sure proper communication with the cluster.

```text
$ kubectl get secret                                                                                                                                                                                                                            git:(master|…
NAME                           TYPE                                  DATA   AGE
default-token-frqgm            kubernetes.io/service-account-token   3      5d3h
```

Once access is verified you can deploy the examples found in this repository.

### Next Steps

Head on over to Examples to deploy some workloads!

{% page-ref page="examples/" %}



