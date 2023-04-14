---
description: >-
  Invite new users and manage existing organization members all from a single
  page in your CoreWeave Cloud dashboard
---

# Organizations

CoreWeave Cloud allows you to share all of your Cloud resources with the rest of your team by inviting new users to join your organization via [the organization management page](https://cloud.coreweave.com/organization):

<figure><img src="../.gitbook/assets/image (1) (2) (1).png" alt="Screenshot of the organization management page"><figcaption><p>The organization management page</p></figcaption></figure>

## Invite users

Inviting a user is simple. From the Organization Management page in CoreWeave Cloud, click the **Invite a User** button. A form will appear prompting for the email of the person you'd like to invite. Enter this address, then click **Send Invite.**

<figure><img src="../.gitbook/assets/image (84) (1).png" alt="Screenshot of the user invite modal"><figcaption><p>The user invite modal</p></figcaption></figure>

After a user accepts their invitation and completes the signup process, they will be added to the organization, and will show up as an accepted user. They will now have full access to your namespace and will have the ability to allocate storage, create a deployment, and provision a Virtual Server. To remove a user from your organization completely, please [contact support](https://cloud.coreweave.com/contact).

## Manage invited users

The organization management page allows team members to easily manage their in-flight invitations with the following actions per invited user:

* **Copy** the invite link that was emailed to the invited user
* **Resend** the invitation email to the invited user
* **Revoke** the invitation from the invited user

After the invitation is accepted, the user can be managed from the Organization Management page. Under the **Actions** column, users may be deactivated and reactivated. Deactivating users will prevent them from accessing their account, but user accounts may be reactivated at any time. To manage the activation status of a user's account, click the button located on the left side of the user row.

<figure><img src="../.gitbook/assets/Screen Shot 2022-05-11 at 8.02.33 PM.png" alt="Screenshot of activation options"><figcaption></figcaption></figure>

## User permissions

It is important to note that all members of your organization will have the same read and write privileges in your namespace, however only the organizations' primary owner may edit user activation and deactivation.

{% hint style="info" %}
**Note**

Top-level RBAC management is forthcoming. Until then, it is strongly recommended to only invite trusted users into your organization.
{% endhint %}
