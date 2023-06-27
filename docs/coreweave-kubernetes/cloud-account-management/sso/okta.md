---
description: Configure SSO on CoreWeave with Okta
---

# Okta

To configure CoreWeave SSO using [Okta](https://www.okta.com/) as your identity provider, first [create a new SSO configuration](./#create-a-new-sso-configuration) on CoreWeave.

On the configuration screen, select **Okta** from the **Your IDP** drop-down menu.

<figure><img src="../../../.gitbook/assets/image (43) (3).png" alt="Screenshot of the SSO configuration modal, set up for Okta"><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

It's recommended to keep the CoreWeave Cloud window open so that you may reference the values provided by CoreWeave during this configuration.
{% endhint %}

## Configure Okta

Navigate to [the Okta Admin Console to create a SAML app integration](https://help.okta.com/en-us/Content/Topics/Apps/Apps\_App\_Integration\_Wizard\_SAML.htm) to begin configuring Okta's side of the SSO connection.

### General settings

From the SAML integration screen, enter an application name (such as `CoreWeave Cloud`). Optionally, add an app logo to display in the Okta application menu. Then, click **Next**.

{% hint style="info" %}
**Additional Resources**

For more information on Okta's SAML integration fields, refer to [Okta's Application Integration Wizard SAML field reference](https://help.okta.com/en-us/Content/Topics/Apps/aiw-saml-reference.htm).
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (10) (2) (1).png" alt=""><figcaption><p>The Okta IDP configuration page</p></figcaption></figure>

### Configure SAML

On the following menu, **Configure SAML**, enter the **Single sign-on URL** [provided in the CoreWeave SSO configuration panel](./#configure-the-idp).

{% hint style="info" %}
**Note**

What Okta calls the **Single-sign on URL** is the same as the **Assertion Consumer Service (ACS) URL** provided in the CoreWeave SSO configuration panel.
{% endhint %}

Check the box beside "Use this for the Recipient URL and the Destination URL."

The general configuration fields should be set to the following values:

<table><thead><tr><th width="336">Field</th><th>Value</th></tr></thead><tbody><tr><td>Single sign-on URL</td><td>Provided by CoreWeave. (See: <a href="./#configure-the-idp">Configure the IDP</a>)</td></tr><tr><td>Audience URI (SP Entity ID)</td><td>Provided by CoreWeave. (See: <a href="./#configure-the-idp">Configure the IDP</a>)</td></tr><tr><td>Name ID format</td><td><code>Unspecified</code></td></tr><tr><td>Application username</td><td><code>Okta username</code></td></tr><tr><td>Update applicaton username on</td><td><code>Create and update</code></td></tr></tbody></table>

<figure><img src="../../../.gitbook/assets/image (3) (1) (1).png" alt="Screenshot of a complete SAML integration for CoreWeave Cloud on the Okta side"><figcaption><p>A complete SAML integration for CoreWeave Cloud on the Okta side</p></figcaption></figure>

### Attribute statements

Next, on the same page, configure the **Attribute Statements** for the SAML integration. The attribute statements fields should be set to the following:

<table><thead><tr><th width="223">Name</th><th width="225.33333333333331">Name format</th><th>Value</th></tr></thead><tbody><tr><td>first_name</td><td>Unspecified</td><td><code>user.firstName</code></td></tr><tr><td>last_name</td><td>Unspecified</td><td><code>user.lastName</code></td></tr><tr><td>email</td><td>Unspecified</td><td><code>user.email</code></td></tr><tr><td>login</td><td>Unspecified</td><td><code>user.login</code></td></tr></tbody></table>

<figure><img src="../../../.gitbook/assets/image (40) (2).png" alt="Screenshot of the attribute statements formatted for Okta"><figcaption><p>Attribute statements formatted for Okta</p></figcaption></figure>

{% hint style="info" %}
**Note**

The `email` attribute is what uniquely identifies users.
{% endhint %}

### Identity provider URL, issuer, and X.509 certificate

To acquire the identity provider URL, the IDP Single sign-on URL, and the X.509 certificate, click the **View SAML setup instructions** button on the right-hand side of the "Configure SAML" page.

<figure><img src="../../../.gitbook/assets/image (2) (4).png" alt=""><figcaption><p>The "View SAML setup instructions" button is on the right-hand side of the SAML configuration screen</p></figcaption></figure>

This will redirect to a "How to" page, which contains all values for these fields.

<figure><img src="../../../.gitbook/assets/image (14) (1) (1).png" alt="Screenshot of Okta setup"><figcaption></figcaption></figure>

The provided values in these fields must be added to their associated fields in [the CoreWeave SSO configuration menu](./#configure-coreweave-sso).

### Feedback

The final portion of the Okta SAML integration is a feedback form for Okta, and may be filled out as you wish - this feedback is used by Okta. Once this section is complete, click **Finish**.

<figure><img src="../../../.gitbook/assets/image (7) (1) (1).png" alt=""><figcaption></figcaption></figure>

## Configure CoreWeave SSO

If not already complete, [return to the CoreWeave SSO configuration menu](./#configure-coreweave-sso) to finish setting up and enabling the SSO configuration.
