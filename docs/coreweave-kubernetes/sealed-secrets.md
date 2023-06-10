---
description: Use Sealed Secrets on CoreWeave Cloud
---

# Sealed Secrets

[Bitnami's Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets#usage) solution can be used to encrypt secrets such that they can safely be managed and shared using git.

`kubeseal` creates a `SealedSecret` resource, which can then only be decrypted by the controller running in the cluster. Not even the original creator of the Secret is then able to extract the original Secret from the `SealedSecret` resource.

Sealed Secrets are composed of two parts:

* A cluster-side controller/operator
* A client-side utility: `kubeseal`

A cluster-side controller for Sealed Secrets is already installed in CoreWeave Cloud, so clients may use Sealed Secrets simply by installing the client-side utility, `kubeseal`.

{% hint style="info" %}
**Additional Resources**

More information on Sealed Secrets are available in [Bitnami's Sealed Secrets repository](https://github.com/bitnami-labs/sealed-secrets).
{% endhint %}

## How it works

Sealed Secrets are encoded in a `SealedSecret` resource, which looks like this:

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: mynamespace
spec:
  encryptedData:
    foo: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq.....
```

Once "unsealed," this the secret will be revealed as a normal [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/), similar to this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
  namespace: mynamespace
data:
  foo: YmFy  # <- base64 encoded "bar"
```

This normal Kubernetes secret will appear in the cluster after a few seconds you can use it as you would use any secret that you would have created directly (e.g. reference it from a `Pod`).

## Install kubeseal

To install kubeseal, you may use any of the following methods:

### Homebrew

The `kubeseal` client is also available on [homebrew](https://formulae.brew.sh/formula/kubeseal):

```bash
brew install kubeseal
```

### MacPorts

The `kubeseal` client is also available on [MacPorts](https://ports.macports.org/port/kubeseal/summary):

```bash
port install kubeseal
```

### Linux

The `kubeseal` client can be installed on Linux, using the below commands:

```bash
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/<release-tag>/kubeseal-<version>-linux-amd64.tar.gz
tar -xvzf kubeseal-<version>-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

where `release-tag` is the [version tag](https://github.com/bitnami-labs/sealed-secrets/tags) of the kubeseal release you want to use. For example: `v0.18.0`.

### From source

The latest client tool can be installed into `$GOPATH/bin` using:

```bash
go install github.com/bitnami-labs/sealed-secrets/cmd/kubeseal@main
```

It is possible to specify a release tag or a commit SHA hash instead of `main`. The `go install` command will place the `kubeseal` binary at `$GOPATH/bin`:

```bash
$(go env GOPATH)/bin/kubeseal
```

## Create a Sealed Secret

First, create a Secret inside either a JSON or YAML file. In this example, a file containing a JSON secret (the default format for Sealed Secrets) is created via the command line. This example also uses `--dry-run` for preview purposes:

{% code overflow="wrap" %}
```bash
$ echo -n bar | kubectl create secret generic mysecret --dry-run=client --from-file=foo=/dev/stdin -o json >mysecret.json
```
{% endcode %}

Next, `kubeseal` is used to encrypt the JSON-encoded secret. First, `kubeseal` reads the namespace from the input secret, accepts an explicit `--namespace` argument, and then uses the `kubectl` default namespace, in that order. Any labels or annotations on the original `Secret` are preserved, but not automatically reflected in the `SealedSecret`.

```bash
kubeseal <mysecret.json >mysealedsecret.json
```

At this point, the secret contents of `mysealedsecret.json` are encrypted, so the file is safe to share via git or any other method. The secret can then be added as a Kubernetes secret using `kubectl create`:

```bash
kubectl create -f mysealedsecret.json
```

Once deployed, the secret can be viewed using `kubectl get`:

{% code overflow="wrap" %}
```bash
kubectl get secret mysecret
```
{% endcode %}

{% hint style="warning" %}
**Important**

`SealedSecret` and `Secret` must have the same namespace and name.
{% endhint %}

Please also note:

> By design, this scheme _does not authenticate the user_. In other words, _anyone_ can create a `SealedSecret` containing any `Secret` they like (provided the namespace/name matches). It is up to your existing config management workflow, cluster RBAC rules, etc to ensure that only the intended `SealedSecret` is uploaded to the cluster. The only change from existing Kubernetes is that the _contents_ of the `Secret` are now hidden while outside the cluster.
>
> – [Bitnami's source repo](https://github.com/bitnami-labs/sealed-secrets#usage)

## Example

The following example files demonstrate what it looks like to actually position Sealed Secrets inside a Helm context. The sample[ Helm template file](https://helm.sh/docs/chart\_best\_practices/templates/) provided here, called `sealedsecrets.yaml`, consumes the Sealed Secret values in the example values file, called `values-prod.yaml`.

**The template file:**

{% code title="sealedsecrets.yaml" %}
```yaml
{{- $prodEnv := has .Values.pythonEnv (list "staging" "production") -}}
{{- range $key, $value := .Values.sealedSecrets }}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: {{ $key }}
  namespace: {{ $.Release.Namespace }}
spec:
  encryptedData:
{{ $value | toYaml | indent 4 }}
  template:
    metadata:
      {{- if not $prodEnv }}
      annotations:
        helm.sh/hook: pre-install
      {{- end }}
      creationTimestamp: null
      name: {{ $key }}
      namespace: {{ $.Release.Namespace }}
    type: Opaque
---

{{- end }}
```
{% endcode %}

**The corresponding values file:**

{% code title="values-prod.yaml" overflow="wrap" %}
```yaml
[...]
sealedSecrets:
  slack:
    botToken: IkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0LCBjb25zZWN0ZXR1ciBhZGlwaXNjaW5nIGVsaXQsIHNlZCBkbyBlaXVzbW9kIHRlbXBvciBpbmNpZGlkdW50IHV0IGxhYm9yZSBldCBkb2xvcmUgbWFnbmEgYWxpcXVhLiA==
  freshdesk:
    password:
VXQgZW5pbSBhZCBtaW5pbSB2ZW5pYW0sIHF1aXMgbm9zdHJ1ZCBleGVyY2l0YXRpb24gdWxsYW1jbyBsYWJvcmlzIG5pc2kgdXQgYWxpcXVpcCBleCBlYSBjb21tb2RvIGNvbnNlcXVhdC4g
    apiKey:
RHVpcyBhdXRlIGlydXJlIGRvbG9yIGluIHJlcHJlaGVuZGVyaXQgaW4gdm9sdXB0YXRlIHZlbGl0IGVzc2UgY2lsbHVtIGRvbG9yZSBldSBmdWdpYXQgbnVsbGEgcGFyaWF0dXIuIEV4Y2VwdGV1ciBzaW50IG9jY2FlY2F0IGN1cGlkYXRhdCBub24gcHJvaWRlbnQsIHN1bnQgaW4gY3VscGEgcXVpIG9mZmljaWEgZGVzZXJ1bnQgbW9sbGl0IGFuaW0gaWQgZXN0IGxhYm9ydW0uIg==
  hubspot:
    privateAppToken:
IlNlZCB1dCBwZXJzcGljaWF0aXMgdW5kZSBvbW5pcyBpc3RlIG5hdHVzIGVycm9yIHNpdCB2b2x1cHRhdGVtIGFjY3VzYW50aXVtIGRvbG9yZW1xdWUgbGF1ZGFudGl1bSwgdG90YW0gcmVtIGFwZXJpYW0sIGVhcXVlIGlwc2EgcXVhZSBhYiBpbGxvIGludmVudG9yZSB2ZXJpdGF0aXMg
```
{% endcode %}
