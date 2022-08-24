---
description: Learn more about provisioning user accounts on Virtual Servers.
---

# User Accounts

User accounts can be provisioned onto Virtual Servers in a few different ways. You can add as many user accounts as you like to your Virtual Servers.

{% hint style="warning" %}
**Important**

Users created on Virtual Servers are automatically given **administrative privileges (`sudo` access).**
{% endhint %}

{% tabs %}
{% tab title="Cloud UI" %}
**Deployment method:** <mark style="background-color:blue;">CoreWeave Cloud UI</mark>

\
The user account configured in the **Account** section of the deployment menu will be used as the first administrative user account on the Virtual Server. This account can be configured to use either an SSH public key or a password for authentication.



![The user account creation menu.](<../../.gitbook/assets/image (68).png>)

\
Additional user accounts may be provisioned in the YAML manifest tab under the `users` block:

![The users block in the YAML manifest in the Cloud UI.](<../../.gitbook/assets/image (109).png>)

The `users` block is a YAML array, in which usernames and passwords or SSH public keys can be listed out.\
\
Multiple users in this configuration would look something like this:

```yaml
users:
  - username: "jill"
    password: "93jrwnffdk"
  - username: "jack"
    password: "932rjwfdf"
```
{% endtab %}

{% tab title="CLI" %}
**Deployment method:** <mark style="background-color:green;">Kubernetes CLI</mark>

User accounts are created using the Kubernetes CLI by adding their information to the `users` stanza of the `spec`.



#### Example

```yaml
  users:
    - username: SET YOUR USERNAME HERE
      password: SET YOUR PASSWORD HERE  
       To use key-based authentication, replace and uncomment SSH-RSA below with your public SSH key
      # sshpublickey: |
        ssh-rsa AAAAB3NzaC1yc2EAAAA ... user@hostname
```
{% endtab %}

{% tab title="Terraform" %}
**Deployment method:** <mark style="background-color:orange;">Terraform</mark>\ <mark style="background-color:orange;"></mark>\ <mark style="background-color:orange;"></mark>The Virtual Server's user account options are configured as variables passed into the [Virtual Server Terraform module](https://github.com/coreweave/kubernetes-cloud/tree/master/virtual-server/examples/terraform).



### User account configuration options

The table below describes all available configuration options for user accounts on Virtual Servers.



| Variable name          | Variable type | Description                                                                                                                                                                                                       | Default value                                                                                   |
| ---------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `vs_username`          | String        | The name of the user to create.                                                                                                                                                                                   | `linux`                                                                                         |
| `vs_password`          | String        | <p>User-defined password for the user account.<br><span data-gb-custom-inline data-tag="emoji" data-code="26a0">⚠</span><strong><code>vs_generate_password</code> must be set to <code>false</code>.</strong></p> | `ubuntu2004-docker-master-20210601-ord1` (The Ubuntu 20.04 image stored in the Chicago region.) |
| `vs_generate_password` | Boolean       | Whether or not to randomly generate a user password for the user account.                                                                                                                                         | `true`                                                                                          |

****\
**Example**

```json
variable "vs_username" {
  description = "Virtual Server username"
}

variable "vs_password" {
  type        = string
  default     = "null"
  description = "User provided password (vs_generate_password must be set to false)"
}

variable "vs_generate_password" {
  type        = bool
  default     = true
  description = "Generate password"
```
{% endtab %}
{% endtabs %}

