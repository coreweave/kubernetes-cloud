---
description: >-
  Use CoreWeave's billing portal and reporting tools to manage expenses and
  payments
---

# Billing and Usage Information

The billing portal offers ways to oversee usage in CoreWeave Cloud, and to manage invoices, payments, and account information. The billing portal streamlines the process of managing invoices and payment information, conveniently provides access to current expenses in [CoreWeave Cloud](../../../virtual-servers/deployment-methods/coreweave-apps.md).

Resource usage can be tracked using prebuilt Grafana dashboards, or, custom Grafana dashboards may be implemented, and Kubernetes commands may be leveraged for more detailed resource tracking. The billing portal is secure, and is compliant with industry privacy standards.

{% hint style="info" %}
**Note**

For more in-depth resource oversight, see [Grafana](../../cloud-tools/grafana.md) and [Kubernetes commands](../../cloud-tools/kubectl.md).
{% endhint %}

## Security

The CoreWeave billing portal is provided by [Maxio](https://www.maxio.com/security), and is audited annually for compliance with security and privacy standards, including SOC 1, SOC 2, PCI-DSS, GDPR, and ISO 27001.

If you have any questions about billing that are not covered here, please [reach out to CoreWeave support](https://cloud.coreweave.com/contact) - we are always here to help you.

## Billing portal

To access the billing portal, [log in to CoreWeave Cloud](https://cloud.coreweave.com/), then click on your profile icon in the upper right-hand corner. Navigate to **Billing** to open the billing portal.

{% hint style="info" %}
**Note**

Only organization administrators can access the portal. If this menu item does not appear, please contact our support team at [support@coreweave.com](mailto:support@coreweave.com).
{% endhint %}

<figure><img src="../../.gitbook/assets/image.png" alt="" width="549"><figcaption></figcaption></figure>

### My account

<div align="left">

<figure><img src="../../.gitbook/assets/image (5) (2).png" alt="Screenshot of the Billing Portal"><figcaption><p>Billing Portal</p></figcaption></figure>

</div>

To adjust settings for the billing account, click **My Account**. From this page, the account's name, email, organization, and VAT number may be changed.

{% hint style="warning" %}
**Important**

If you click **Sign Out**, you must log back in using the [Usage and Billing](https://cloud.coreweave.com/) menu on the Cloud UI. The Maxio account is integrated with your CoreWeave account, so signing in via email as is prompted will not work.
{% endhint %}

### Subscriptions

The **subscriptions** tab displays billing details for CoreWeave namespaces each month. This information is organized by plan, and is updated every twenty-four hours.

<div align="left">

<figure><img src="../../.gitbook/assets/image (90) (1).png" alt="Subscriptions tab of the billing portal"><figcaption><p>Subscriptions tab</p></figcaption></figure>

</div>

* **Plan Details** displays the date the namespace plan was created, followed by the current charges, credits, and billable resources.
* **Subscription Settings** shows the namespace for this plan. This is for informational purposes only - no modifications are necessary.
* **Update Payment Method** is used to change credit card or billing address information.
* **Edit Contact Information** is used to update contact information or shipping addresses. If you have multiple plans, you can choose to update all of them with the same information at once from here.

{% hint style="info" %}
**Note**

For a list of billable resources and charges, refer to [Resource Based Pricing](../../../resources/resource-based-pricing.md).
{% endhint %}

### Invoices

Under the **invoices** tab, alit of the current and historical invoices is displayed. Invoices are due at the time they are issued.

To view or download an invoice, click on it. If the invoice has not yet been paid, click the green **Pay Invoice Online** button at the top to use the credit card on file, or make a one-time payment using a different card.

If you have multiple subscriptions, you may see icons that indicate normal and consolidated invoices.

<div align="left">

<figure><img src="../../.gitbook/assets/image (7) (1) (4).png" alt="Examples of invoice icons"><figcaption></figcaption></figure>

</div>

To learn more about these invoice types, please visit the [Maxio Help Portal](https://maxio-chargify.zendesk.com/hc/en-us/articles/5404980119949-Invoice-Consolidation), or contact our sales team at [sales@coreweave.com](mailto:sales@coreweave.com) if you have additional questions.

## Payment policies

A valid credit card is required to use CoreWeave Cloud. To update your card information, please use the **Update Payment Method** button in the billing portal. Invoices are due when issued at the end of each month and your account may be deactivated if not paid.

If your monthly bill exceeds $20,000, you must pay by bank wire transfer. Please contact your account executive or send an email to [sales@coreweave.com](mailto:sales@coreweave.com) for information on how to complete a wire transfer.

### Reserved instances and account credits

Billing adjustments for reserved instances or other account credits are managed by your Account Executive or Client Success Manager. The exact terms are specified in your reserved instance contract and applied to each monthly invoice.&#x20;

## View resources

All billable resources may be viewed in CoreWeave Cloud.&#x20;

On the main dashboard of the Cloud UI, the **Account Overview** section offers a high-level glance at the amount of billable resources in use, as well as the total expenses for the previous day, the current billing period, and the total cost per hour.

<figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>

For a more in-depth view of resources in use, [Grafana](https://grafana.coreweave.com/) may be used to find useful dashboards with compute and storage summaries, and detailed reports of the GPUs, CPUs, memory, and network activity for each Pod. These Grafana dashboards are managed, and cannot be modified, however [new dashboards can be created](../../../coreweave-kubernetes/prometheus/grafana.md).

## Billing FAQ

<details>

<summary>Where can I find historical invoices?</summary>

Historical invoices are in the billing portal, on the **Invoices** tab. See also: [Invoices](billing-portal.md#invoices).

</details>

<details>

<summary>How can I quickly find out what I am spending right now?</summary>

The **Account Overview** section of the [CoreWeave Cloud main dashboard](../coreweave-cloud-ui/#main-dashboard) provides a summary. See also: [View resources](billing-portal.md#view-resources).

</details>

<details>

<summary>How can I monitor my expenses over time?</summary>

Use either the managed [Grafana dashboards](https://grafana.coreweave.com/), or build custom reports with [your own Grafana instance](../../../coreweave-kubernetes/prometheus/grafana.md).

</details>

<details>

<summary>How can I monitor active workloads?</summary>

Active workloads can be monitored using [Kubernetes tools](../../cloud-tools/kubectl.md).

</details>

## Software licensing

### Windows

CoreWeave offers Microsoft Windows licenses for a monthly charge, or you can [bring your own license](https://www.microsoft.com/en-us/licensing/default). We also offer usage-based licenses for many products, including:

* Autodesk Arnold
* SideFX Houdini Engine
* SideFX Karma
* SideFX Mantra
* Maxon Redshift
* Maxon Cinema 4D (C4D)

CoreWeave does not offer interactive licenses. For more information or a licensing quote, please contact your account executive.

{% hint style="info" %}
**Note**

For further assistance, please don't hesitate to contact [sales@coreweave.com](mailto:sales@coreweave.com).
{% endhint %}
