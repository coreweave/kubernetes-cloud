---
description: Configure SSO on CoreWeave with an SSO IDP
---

# Generic IDP

To configure CoreWeave SSO using a generic IDP as your identity provider, first [create a new SSO configuration](./#create-a-new-sso-configuration) on CoreWeave.

On the configuration screen, select **Generic IDP** from the **Your IDP** drop-down menu.

<figure><img src="../../.gitbook/assets/image (30) (4).png" alt="Screenshot of the IDP selector menu"><figcaption><p>Select "Generic IDP" from the "Your IDP" drop-down</p></figcaption></figure>

Using the information provided in the setup modal, complete your IDP's SSO configuration. Ensure that all fields in the CoreWeave SSO modal are also filled in using the information provided by your IDP.

## Configuration fields

### CoreWeave-provided

For your IDP's configuration, CoreWeave provides an **Assertion Consumer Service (ACS) URL** and a **Service provider (SP) entity ID**. These values will be required and most likely requested by your IDP for that side of the configuration.

### IDP-provided

The **Entity ID**, **Single Sign-On URL**, and **X.509 Certificate** fields will be provided by your IDP for the CoreWeave side of the configuration. When provided, copy and paste the given values of these fields into the corresponding fields on the CoreWeave Cloud UI.

### Custom

The **Display Name** field is for your customization, and is only used to name the CoreWeave SSO configuration.

Once the configuration is complete, ensure that the **Configuration Active** checkbox is checked, then click the **Save** button.

{% hint style="info" %}
**Additional Resources**

See instructions for configuring [Okta](okta.md) or [JumpCloud](jumpcloud.md) for examples.
{% endhint %}

