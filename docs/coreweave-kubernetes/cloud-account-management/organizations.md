---
description: Manage organization admins and members in the Cloud UI
---

# Organizations

Organization management is handled from the [organization management dashboard](./#organization). To open the dashboard, click on the profile icon in the upper right-hand corner of the Cloud UI, then navigate to **Organization**.

## Organizations and organization administrators

On CoreWeave Cloud, an **organization** is a group of associated users sharing [one or more namespaces](namespace-management.md). The **organization administrator** is a user in an organization that holds `read` and/or `write` access to manage the organization's users, including those users' access controls. The organization admin is also the only user level in an organization that can list, add, or remove [API Access Tokens](../getting-started.md#obtain-coreweave-access-credentials).

This allows the organization admin user to govern features such as [inviting new users](organizations.md#invite-users) to the organization, or to manage [per-namespace user access](organizations.md#per-namespace-user-access) across organization namespaces.

Unless **CoreWeave admins** make changes to your organization, only the first user (the user who created the organization) will be granted this level of access control.

{% hint style="info" %}
**Note**

To add an additional organization admin user, or to change the current organization admin user, please [contact support](https://cloud.coreweave.com/contact).
{% endhint %}

## User management

Users within an organization may be managed from [the organization management page](https://cloud.coreweave.com/organization) on the [CoreWeave Cloud UI](../../../virtual-servers/deployment-methods/coreweave-apps.md).

### Invite users

<figure><img src="../../.gitbook/assets/image (15) (2).png" alt=""><figcaption></figcaption></figure>

Only the organization administrator may invite new users. To invite new users, ask your organization administrator to navigate to the organization management page in CoreWeave Cloud, then click the **Invite a User** button. A form will appear, prompting for the email of the person to invite. Enter this address, then click **Send Invite.**

{% hint style="warning" %}
**Important**

By default, new users inherit the same access controls to the namespace as the user who invited them.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>

The organization management page also allows admins to perform the following actions:

* **Copy** the invite link that was emailed to the invited user
* **Resend** the invitation email to the invited user
* **Revoke** the invitation from the invited user

<figure><img src="../../.gitbook/assets/image (6) (3).png" alt=""><figcaption><p>Copy, resend, or revoke the invitation under the <strong>Actions</strong> column</p></figcaption></figure>

Once an invitation is accepted and the new user has completed registration, their account may be managed from the organization management page.

Under the **Actions** column, users may be deactivated and reactivated. Deactivating users will prevent them from accessing their account, but user accounts may be reactivated at any time. To manage the activation status of a user's account, click the button located on the left side of the user row.

<figure><img src="../../.gitbook/assets/image (19) (2).png" alt=""><figcaption><p>Click the <strong>Deactivate</strong> button beside a user to deactivate their account</p></figcaption></figure>

{% hint style="danger" %}
**Warning**

Changes to per-user-namespace access **do not apply to access tokens**. [API Access Tokens](../getting-started.md#obtain-coreweave-access-credentials) are owned by organizations, and are controlled by a different set of access control policies. Only organization admins have access to add, list, and remove Access Tokens.

When removing a user, API Tokens must be removed manually from [the API Access page by an organization admin.](https://cloud.coreweave.com/api-access)

To remove a user from your organization completely, immediately deactivate the user's account and any Access Tokens associated to that user, then [contact CoreWeave support](https://cloud.coreweave.com/contact).&#x20;
{% endhint %}

### User access control by namespace

On CoreWeave, [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) policies are used to map user access controls to namespaces, which allows organization admins the ability to specify which users do or do not have control access within a given namespace.

As the organization admin, expand a user's details on the organization management page to see to which namespaces they have access. Check or uncheck the box beside a given namespace to grant or revoke permissions to the namespace, or click the **Add All** or **Remove All** buttons to remove or grant access across all namespaces. Click the **Save Changes** button to save the access configuration.

At this time, organization admins can grant users all permissions in a given namespace with the exception of `w:pods` (write to Pods) and `w:full` (full `write` access). If users other than the organization admin require these permissions, please [contact support](https://cloud.coreweave.com/contact).

<figure><img src="../../.gitbook/assets/image (18) (1) (1).png" alt=""><figcaption></figcaption></figure>
