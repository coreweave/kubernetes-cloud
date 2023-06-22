---
description: Configure SSO on CoreWeave with JumpCloud
---

# JumpCloud

To configure CoreWeave SSO using [JumpCloud](https://jumpcloud.com/) as your identity provider, first [create a new SSO configuration](./#create-a-new-sso-configuration) on CoreWeave.

On the configuration screen, select **JumpCloud** from the **Your IDP** drop-down menu.

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

It's recommended to keep the CoreWeave Cloud window open so that you may reference the values provided by CoreWeave during this configuration.
{% endhint %}

## Create a JumpCloud Single Sign-On configuration

From your JumpCloud admin dashboard, navigate to the **SSO** page. From here, navigate to **User Authentication >** **SSO** to set up the configuration.

<figure><img src="../../.gitbook/assets/image (52).png" alt="Screenshot of JumpCloud&#x27;s SSO configuration screen"><figcaption></figcaption></figure>

The **IdP Entity ID** field refers to the identity provider's entity ID. Take this value and input it into the **Entity ID provided by the IDP** field in [the CoreWeave Cloud SSO configuration module](./#the-saml-sso-modal).

The **SP Entity ID** field refers to the service provider's entity ID. This can be found in the CoreWeave Cloud SSO configuration module, and can be copy-pasted from there into the JumpCloud field.

Neither the **IdP Private Key** nor the **IdP Certificate** need to be adjusted - leave these alone.

Next, in the **ACS URL** field, enter the ACS URL provided in [the CoreWeave Cloud's SAML SSO modal](./#the-saml-sso-modal). Ignore the **Replace SP Certificate** button.

The following fields - **SAMLSubject NameID**, **SAMLSubject NameID Format**, and **Signature Algorithm**, should match the following values to properly format the user attributes:

<table><thead><tr><th width="297">Field name</th><th>Field value</th></tr></thead><tbody><tr><td>SAMLSubject NameID</td><td><code>email</code></td></tr><tr><td>SAMLSubject NameID Format</td><td><code>urn:oasis:name:tc:SAML:1.1:nameid-format:unspecified</code></td></tr><tr><td>Signature Algorithm</td><td><code>RSA-SHA256</code></td></tr></tbody></table>

<figure><img src="../../.gitbook/assets/image (17) (4).png" alt=""><figcaption></figcaption></figure>

Leave the **Sign Assertion** checkbox unchecked.

The **IDP URL** field will contain some value equivalent to `https://sso.jumpcloud.com/saml2/saml2`.

<figure><img src="../../.gitbook/assets/image (15).png" alt="Screenshot of the IDP URL field on JumpCloud"><figcaption></figcaption></figure>

### User attributes

Under the **IDP URL** field in the **Attributes** section are several fields for **Attributes**. The given JumpCloud attributes should match the following formats:

<table><thead><tr><th width="357">Service Provider Attribute Name</th><th>JumpCloud Attribute Name</th></tr></thead><tbody><tr><td>first_name</td><td><code>firstname</code></td></tr><tr><td>last_name</td><td><code>lastname</code></td></tr><tr><td>email</td><td><code>email</code></td></tr><tr><td>login</td><td><code>email</code></td></tr></tbody></table>

<figure><img src="../../.gitbook/assets/image (56).png" alt="Screenshot of JumpCloud SSO attributes"><figcaption></figcaption></figure>

{% hint style="info" %}
**Note**

The `email` attribute is what uniquely identifies users.
{% endhint %}

### Entity certificate

<figure><img src="../../.gitbook/assets/image (35).png" alt="Screenshot of the certificate status on JumpCloud SSO"><figcaption><p>The certificate status is found on the left-hand side of the SSO configuration box</p></figcaption></figure>

To acquire and provide the SSO certificate from JumpCloud to CoreWeave, first locate the certificate status field on the left-hand side of the JumpCloud SSO configuration modal. Click the small triangle to the right of the certificate status, then select **Download certificate**. An XML file will download, which contains the body of the x.509 certificate.

To provide the certificate body to CoreWeave's SSO configuration, open this file, locate the certificate body within the XML file, and copy it to your clipboard. Then, paste it into the **X.509 Certificate provided by IDP** field in [the SAML SSO configuration modal](./#the-saml-sso-modal).

{% hint style="info" %}
**Additional Resources**

For more information about configuring SSO on JumpCloud, see [JumpCloud's Getting Started: Applications (SAML SSO)](https://support.jumpcloud.com/support/s/article/getting-started-applications-saml-sso2). For more information on JumpCloud certificate and key management, refer to [Managing Application IDP Certificate and Key Pairs](https://support.jumpcloud.com/support/s/article/managing-application-idp-certificate-and-key-pairs).
{% endhint %}
