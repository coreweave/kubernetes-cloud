---
description: >-
  Invite new users and manage existing organization members all from a single
  page in your CoreWeave Cloud dashboard
---

# Organizations

CoreWeave Cloud allows you to share all of your cloud resources with the rest of your team by inviting new users to join your organization via [the organization management page](https://cloud.staging.coreweave.com/organization):

<figure><img src="../.gitbook/assets/image (1) (2).png" alt="Screenshot of the organization management page"><figcaption><p>The organization management page</p></figcaption></figure>

#### Inviting a user

Inviting a user is simple and intuitive. Selecting the "Invite a User" button triggers a form to enter the email of the invite:

![Organization Invitation Modal](<../.gitbook/assets/image (142).png>)

#### Managing an Invited User

The organization management page allows team members to easily manage their in-flight invitations with the following actions per invited user:

* **Copy** the invite link that was emailed to the invited user
* **Resend** the invitation email to the invited user
* **Revoke** the invitation from the invited user

After the invitation is accepted, the user could subsequently be deactivated and reactivated. Deactivating users will prevent them from accessing their account. You can reactivate their account at any time. To manage the users active status, click on the button located on the left side of the user row in the "_Actions"_ column.

![](<../.gitbook/assets/Screen Shot 2022-05-11 at 8.02.33 PM.png>)

#### Post Invitation

After a user accepts their invitation and completes the signup process they will be added to the organization and will show up as an accepted user. They will now have full access to your namespace and have the ability to allocate storage, create a deployment and provision a Virtual Server. To remove a user from your organization please [contact support](https://cloud.coreweave.com/contact).

#### User Permissions

It is important to note that all members of your organization will have the same read/write privileges in your namespace whereas user activation/deactivation is scoped to the organizations first owner. We fully intend to provide Role-based access control (RBAC) on a per user basis but until then it is recommended that only trusted members be added to your organization.
