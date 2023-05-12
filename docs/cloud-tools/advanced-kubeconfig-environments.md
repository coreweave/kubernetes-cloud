---
description: How to integrate multiple kubeconfig files and resolve conflicts
---

# Advanced Kubeconfig Environments

Kubeconfig is a YAML file that contains information about the cluster's API server, namespace, and user authentication.

This guide explains the order of precedence when using multiple kubeconfigs, how to integrate a new CoreWeave kubeconfig with an existing kubeconfig, the steps to resolve name conflicts, how to use multiple contexts and namespaces as a single environment, and best security practices.

{% hint style="info" %}
**Quickstart**

To set up a CoreWeave kubeconfig on a system without an existing kubeconfig, see [Get Started with CoreWeave](../coreweave-kubernetes/getting-started.md).
{% endhint %}

Kubernetes tools like [kubectl](kubectl.md), Helm, and Argo Workflows follow an order of precedence to locate the active kubeconfig.

## Lowest priority: Default location

This location is used unless overridden by another option.&#x20;

| Operating System | Default path                     |
| ---------------- | -------------------------------- |
| Linux            | `~/.kube/config`                 |
| macOS            | `/Users/<username>/.kube/config` |
| Windows          | `%USERPROFILE%\.kube\config`     |

## Next priority: Environment variable

The `KUBECONFIG` environment variable overrides the default location by pointing to one or more kubeconfig files. For a single file named `config-prod`, the syntax is:

{% tabs %}
{% tab title="Linux or macOS" %}
```bash
$ export KUBECONFIG=~/.kube/config-prod
```

Add this to the shell profile to make it persistent.
{% endtab %}

{% tab title="Windows cmd" %}
For the current session, use [set](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set\_1):

```
> set KUBECONFIG=%USERPROFILE%\.kube\config-prod
```

To persist it in future sessions, use [setx](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx):

```
> setx KUBECONFIG %USERPROFILE%\.kube\config-prod /m
```
{% endtab %}

{% tab title="Windows PowerShell" %}
For the current session:

```powershell
> $env:KUBECONFIG = "$env:USERPROFILE\.kube\config-prod"
```

To persist it in future sessions, run this in an administrative PowerShell:

```powershell
> [Environment]::SetEnvironmentVariable("KUBECONFIG", $env:USERPROFILE + "\.kube\config-prod", "Machine")
```
{% endtab %}
{% endtabs %}

## Highest priority: Command line

The `--kubeconfig` command line option has the highest priority; all other kubeconfigs are ignored. For example, to use a `cw-kubeconfig` file in the `Downloads` directory to request [the `secret` objects](https://kubernetes.io/docs/concepts/configuration/secret/).

{% tabs %}
{% tab title="Linux or macOS" %}
```bash
$ kubectl get secret --kubeconfig ~/Downloads/cw-kubeconfig
```
{% endtab %}

{% tab title="Windows cmd or PowerShell" %}
```powershell
> kubectl get secret --kubeconfig %USERPROFILE%\Downloads\cw-kubeconfig
```
{% endtab %}
{% endtabs %}

Although this isn't convenient for normal use, it's a good way to test a new kubeconfig without changing the existing configuration.

## Merge multiple files with the environment variable

To merge multiple files, list them in the environment variable separated with a **colon** on Linux and macOS, or a **semicolon** on Windows. The files are used in the specified order and the first file takes precedence.&#x20;

{% tabs %}
{% tab title="Linux or macOS" %}
```bash
$ export KUBECONFIG=~/.kube/config-prod:~/.kube/config-staging
```

Add this to the shell profile to make it persistent.
{% endtab %}

{% tab title="Windows cmd" %}
For the current session, use [set](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set\_1):

```
> set KUBECONFIG=%USERPROFILE%\.kube\config-prod;%USERPROFILE%\.kube\config-staging
```

To persist the environment in future sessions, use [setx](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx):

```
> setx KUBECONFIG %USERPROFILE%\.kube\config-prod;%USERPROFILE%\.kube\config-staging /m
```
{% endtab %}

{% tab title="Windows PowerShell" %}
For the current session:

```powershell
> $env:KUBECONFIG = "$env:USERPROFILE\.kube\config-prod;$env:USERPROFILE\.kube\config-staging"
```

To persist it in future sessions, run this in an administrative PowerShell:

```powershell
> [Environment]::SetEnvironmentVariable("KUBECONFIG", $env:USERPROFILE + "\.kube\config-prod;" + $env:USERPROFILE + "\.kube\config-staging", "Machine")
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
**Warning**

Resolve any name conflicts before merging the files [as explained below](advanced-kubeconfig-environments.md#resolve-context-name-conflicts).
{% endhint %}

## How to physically merge files

To physically merge multiple kubeconfigs into a single file, add them in the environment as before. Then, use the `--flatten` option, redirect the output to a new file, and use the merged file as the new kubeconfig.

Example:

{% tabs %}
{% tab title="Linux or macOS" %}
{% code lineNumbers="true" %}
```bash
$ export KUBECONFIG=~/.kube/config-prod:~/.kube/config-staging
$ kubectl config view --flatten > ~/.kube/config-merged
$ export KUBECONFIG=~/.kube/config-merged
```
{% endcode %}
{% endtab %}

{% tab title="Windows cmd" %}
{% code lineNumbers="true" %}
```
> set KUBECONFIG=%USERPROFILE%\.kube\config-prod;%USERPROFILE%\.kube\config-staging
> kubectl config view --flatten > %USERPROFILE%\.kube\config-merged
> set KUBECONFIG=%USERPROFILE%\.kube\config-merged
```
{% endcode %}
{% endtab %}

{% tab title="Windows PowerShell" %}
{% code lineNumbers="true" %}
```powershell
> $env:KUBECONFIG = "$env:USERPROFILE\.kube\config-prod;$env:USERPROFILE\.kube\config-staging"
> kubectl config view --flatten > %USERPROFILE%\.kube\config-merged
> $env:KUBECONFIG = "$env:USERPROFILE\.kube\config-merged"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## How to use multiple contexts

A merged kubeconfigs has multiple contexts, each defining a specific cluster, user, and namespace combination.&#x20;

View the available contexts with `kubectl`:

```
$ kubectl config get-contexts
CURRENT   NAME      CLUSTER           AUTHINFO       NAMESPACE
*         prod      prod-cluster      prod-user      prod-namespace
          staging   staging-cluster   staging-user   staging-namespace
```

Use `kubectl` to switch contexts:

```
$ kubectl config use-context staging
Switched to context "staging".
```

## Resolve context name conflicts

Context name conflicts must be resolved before merging kubeconfigs. To illustrate the issue, here are two files with conflicting context names.&#x20;

<details>

<summary>Click to expand - <code>config-prod</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://prod.example.com
  name: prod-cluster
contexts:
- context:
    cluster: prod-cluster
    namespace: prod-namespace
    user: prod-user
<strong>  name: my-context
</strong>current-context: my-context
users:
- name: prod-user
  user:
    token: REDACTED
</code></pre>

</details>

<details>

<summary>Click to expand - <code>config-staging</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://staging.example.com
  name: staging-cluster
contexts:
- context:
    cluster: staging-cluster
    namespace: staging-namespace
    user: staging-user
<strong>  name: my-context
</strong>current-context: my-context
users:
- name: staging-user
  user:
    token: REDACTED

</code></pre>



</details>

Both files have the same context name on line 13. These will conflict when merged.&#x20;

First, use `kubectl` to rename the context in each file:

{% tabs %}
{% tab title="Linux or macOS" %}
{% code fullWidth="false" %}
```bash
$ kubectl config rename-context my-context prod-context --kubeconfig ~/.kube/config-prod
Context "my-context" renamed to "prod-context".

$ kubectl config rename-context my-context staging-context --kubeconfig ~/.kube/config-staging
Context "my-context" renamed to "staging-context".
```
{% endcode %}
{% endtab %}

{% tab title="Windows" %}
```powershell
> kubectl config rename-context my-context prod-context --kubeconfig %USERPROFILE%\.kube\config-prod
Context "my-context" renamed to "prod-context".

> kubectl config rename-context my-context staging-context --kubeconfig %USERPROFILE%\.kube\config-staging
Context "my-context" renamed to "staging-context".
```
{% endtab %}
{% endtabs %}

Next, merge the files.

{% tabs %}
{% tab title="Linux or macOS" %}
```
$ export KUBECONFIG=~/.kube/config-prod:~/.kube/config-staging
$ kubectl config view --flatten > ~/.kube/config-merged
```
{% endtab %}

{% tab title="Windows cmd" %}
```
> set KUBECONFIG=%USERPROFILE%\.kube\config-prod;%USERPROFILE%\.kube\config-staging
> kubectl config view --flatten > %USERPROFILE%\.kube\config-merged
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```
> $env:KUBECONFIG = "$env:USERPROFILE\.kube\config-prod;$env:USERPROFILE\.kube\config-staging"
> kubectl config view --flatten > %USERPROFILE%\.kube\config-merged
```
{% endtab %}
{% endtabs %}

The result:

<details>

<summary>Click to expand - <code>config-merged</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://prod.example.com
  name: prod-cluster
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://staging.example.com
  name: staging-cluster
contexts:
- context:
    cluster: prod-cluster
    namespace: prod-namespace
    user: prod-user
<strong>  name: prod-context
</strong>- context:
    cluster: staging-cluster
    namespace: staging-namespace
    user: staging-user
<strong>  name: staging-context
</strong>current-context: prod-context
users:
- name: prod-user
  user:
    token: REDACTED
- name: staging-user
  user:
    token: REDACTED
</code></pre>

</details>

The contexts on lines 17 and 22 no longer conflict.&#x20;

Switching contexts is the same for all operating systems:

```bash
$ kubectl config use-context prod-context
Switched to context "prod-context".

$ kubectl config use-context staging-context
Switched to context "staging-context".
```

## Resolve cluster name conflicts

Cluster names can also occasionally conflict. A cluster name is arbitrary and can be anything unique and meaningful. However, unlike context names, there isn't a kubectl command available to rename clusters, so they must be edited manually.

Here are two files with conflicting cluster names for illustration.

<details>

<summary>Click to expand - <code>my-cluster-prod</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://prod.example.com
<strong>  name: my-cluster
</strong>contexts:
- context:
<strong>    cluster: my-cluster
</strong>    namespace: prod-namespace
    user: prod-user
  name: prod-context
current-context: prod-context
users:
- name: prod-user
  user:
    token: REDACTED
</code></pre>

</details>

<details>

<summary>Click to expand - <code>my-cluster-staging</code></summary>

<pre class="language-yaml" data-line-numbers><code class="lang-yaml">apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://staging.example.com
<strong>  name: my-cluster
</strong>contexts:
- context:
<strong>    cluster: my-cluster
</strong>    namespace: staging-namespace
    user: staging-user
  name: my-context
current-context: my-context
users:
- name: staging-user
  user:
    token: REDACTED
</code></pre>



</details>

The cluster name on line 7 is the same in both files. If merged, the first file's API server is used and the second file's context is broken.&#x20;

To fix this, edit the cluster name in each file to make them unique. Make sure to edit the cluster reference in the context section so it matches also; it's line 10 in this example.

## Best practices for security

The kubeconfig contains authentication information that should be treated with the same care as passwords or SSH keys.&#x20;

* Make sure only the file owner can read and write the kubeconfig file. For example, on Linux or macOS, use `chmod 600` to set the appropriate permissions.
* Avoid storing the kubeconfig in version control.
* Use separate kubeconfigs for different users and applications, instead of sharing a single kubeconfig among multiple users or apps.
* Regularly rotate kubeconfig files and revoke access for users or applications that no longer need it, to reduce the risk of credential leakage.

## Other references

For more information about kubeconfig files, see the resources at kubernetes.io:

* [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [Configure Access to Multiple Clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
* [kubeconfig reference](https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/)
