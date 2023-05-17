---
description: Configure Single Sign-On on CoreWeave Cloud
---

# SSO

[Single Sign-On](https://en.wikipedia.org/wiki/Single\_sign-on), commonly referred to as SSO, is an authentication scheme that allows the users in an organization to authenticate to CoreWeave Cloud from the same identity provider (IDP) used to log in to other organization-wide apps. Single Sign-On enhances security, and makes for a smoother log-in experience for your team.

CoreWeave organization admins can configure SSO from the admin dashboard on the Cloud UI.

Currently, the following IDPs are supported:

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td>Okta</td><td></td><td></td><td><a href="okta.md">okta.md</a></td><td><a href="../../.gitbook/assets/Okta-Logo.png">Okta-Logo.png</a></td></tr><tr><td>JumpCloud</td><td></td><td></td><td><a href="jumpcloud.md">jumpcloud.md</a></td><td><a href="../../.gitbook/assets/JumpCloud-Logo (1).png">JumpCloud-Logo (1).png</a></td></tr><tr><td>Generic IDP</td><td></td><td></td><td><a href="generic-idp.md">generic-idp.md</a></td><td><a href="../../.gitbook/assets/genericsso.png">genericsso.png</a></td></tr></tbody></table>

A single organization may have multiple SSO configurations, which is convenient in situations where multiple IDPs are used for different sets of users or teams.

## Create a new SSO configuration

{% hint style="warning" %}
**Important**

Only CoreWeave organization admins may configure SSO. Additionally, organization admins will not be able to log in using SSO; this is to ensure that admins do not get locked out of CoreWeave Cloud in the event that an SSO configuration encounters an issue.
{% endhint %}

To add or edit SSO configurations, first [log in to your CoreWeave Cloud account](https://cloud.coreweave.com), then navigate to the [Organization Management page](https://cloud.coreweave.com/organization). Below the **Users** section, find the **SSO Configurations** section.

<figure><img src="../../.gitbook/assets/image (58) (1) (2).png" alt="Screenshot of the SSO Configurations area on the CoreWeave Cloud UI"><figcaption><p>The SSO Configurations area on the CoreWeave Cloud UI</p></figcaption></figure>

To add a new configuration, click the **Add Configuration** button. To edit an existing configuration, select the pencil icon under the **Actions** column to the right of the configuration name.

### The SAML SSO modal

<figure><img src="../../.gitbook/assets/image (41).png" alt="Screenshot of the SAML SSO Setup modal"><figcaption><p>The SAML SSO Setup modal</p></figcaption></figure>

Adding or editing a configuration is done through the **SAML SSO Setup** modal. All SSO configurations are similar across IDPs, so most require the same information and the same process:

1. [Select an Identity Provider (IDP)](./#select-an-identity-provider-idp)
2. [Configure the IDP](./#configure-the-idp)
3. [Configure CoreWeave SSO](./#configure-coreweave-sso)
4. [Activate the SSO configuration](./#activate-the-sso-configuration)

### Select an Identity Provider (IDP)

<figure><img src="../../.gitbook/assets/image (53) (3).png" alt="Screenshot of the SAML SSO Setup modal, with the IDP drop-down highlighted"><figcaption><p>The IDP selector menu</p></figcaption></figure>

From the **Your IDP** drop-down menu, select your IDP.

### Configure the IDP

<figure><img src="../../.gitbook/assets/image (55) (1) (2).png" alt="Screenshot of the CoreWeave-specific configuration values in the SSO module"><figcaption><p>The CoreWeave-specific configuration values in the SSO module</p></figcaption></figure>

The Assertion Consumer Service (ACS) URL and the service provider (SP) entity ID are provided in the following two fields. These values are required to complete your IDP's configuration.

### Configure CoreWeave SSO

<figure><img src="../../.gitbook/assets/image (24) (1).png" alt="Screenshot of the IDP-provided fields, and the Display Name, in the SSO module"><figcaption><p>IDP-provided fields, and the Display Name, in the SSO module</p></figcaption></figure>

The fields **Entity ID provided by the IDP, Single Sign-On URL**, and **X.509 Certificate provided by IDP** are provided by your IDP. See the guide for [JumpCloud](jumpcloud.md), [Okta](okta.md), or [the generic IDP setup instructions](generic-idp.md) for further details.

{% hint style="info" %}
**Note**

See the IDP-specific configuration documentation for more information on these fields.
{% endhint %}

Finally, provide a name for the SSO configuration in the Display Name field that will make the configuration easy to identify.

### Activate the SSO configuration

<figure><img src="../../.gitbook/assets/image (29) (1).png" alt=""><figcaption><p>Check the "Configuration Active" box to turn on the SSO configuration</p></figcaption></figure>

Finally, once the other fields are complete, ensure the **Configuration Active** checkbox is checked before clicking the **Save** button. Checking this box, then clicking **Save**, will turn the SSO configuration on.
