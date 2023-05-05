---
description: >-
  Use CoreWeave's billing portal and reporting tools to manage expenses and
  payments
---

# Billing and Usage Information

This guide explains how to track your resource usage in CoreWeave Cloud and manage invoices, payments, and account information in the billing portal. We also have more advanced guides that explain how to track usage with [Grafana dashboards](../cloud-tools/grafana.md), and use [Kubernetes commands](../cloud-tools/kubectl.md) to see what resources are running in your account.&#x20;

Our billing portal, provided by [Maxio](https://www.maxio.com/security), is audited annually for compliance with security and privacy standards, including SOC 1, SOC 2, PCI-DSS, GDPR, and ISO 27001. If you have any questions about billing that are not covered in this guide, please [reach out to CoreWeave support](https://cloud.coreweave.com/contact); we are always here to help you.

## Billing portal

To access the billing portal, [log in to CoreWeave Cloud](https://cloud.coreweave.com/) and click **Usage & Billing** in the **Account Details** section.

<figure><img src="../.gitbook/assets/image (1) (6).png" alt="Screenshot of the Usage &#x26; Billing menu"><figcaption><p>Usage &#x26; Billing menu</p></figcaption></figure>

{% hint style="info" %}
**Note**

* Only organization administrators have access to the portal. If you do not see this menu item and require access, please contact our support team at [support@coreweave.com](mailto:support@coreweave.com).
{% endhint %}

In the upper right corner of the portal, you will see two links, **My Account** and **Sign Out**.

<figure><img src="../.gitbook/assets/image (5).png" alt="Screenshot of the Billing Portal"><figcaption><p>Billing Portal</p></figcaption></figure>

* Use **My Account** to edit your name, email, organization, and VAT number.
* If you click **Sign Out**, you'll be prompted to sign in with your email. Please disregard these instructions because your Maxio account is integrated with CoreWeave. You must log in using the [Usage & Billing](https://cloud.coreweave.com/) menu from CoreWeave Cloud.

Further down the page, you'll find the **Subscriptions** and **Invoices** tabs.

### Subscriptions tab

The Subscriptions tab shows the billing details for your CoreWeave namespaces each month. The information is organized by plan and updated every 24 hours.

<figure><img src="../.gitbook/assets/image (90) (1).png" alt="Subscriptions tab of the billing portal"><figcaption><p>Subscriptions tab</p></figcaption></figure>

* **Plan Details** shows the date the when namespace plan was created, followed by the current charges, credits, and the billable resources.&#x20;
* **Subscription Settings** shows the namespace for this plan. This is for informational purposes only and you shouldn't need to modify it.
* **Update Payment Method** is used to change credit card or billing address information.
* **Edit Contact Information** is where you'll update contact information or your shipping address. If you have multiple plans, you can choose to update all of them with the same information at once.

{% hint style="info" %}
**Pricing**

Please see [Resource Based Pricing](../../resources/resource-based-pricing.md) for a list of billable resources and charges.
{% endhint %}

### Invoices tab

The Invoices tab displays a list of your current and historical invoices. Invoices are due when issued.

Click an invoice in the list to view it or download as a PDF. If it's unpaid, you can click the green **Pay Invoice Online** button at the top to use the credit card on file, or make a one-time payment using a different card.&#x20;

If you have multiple subscriptions, you may see icons that indicate normal and consolidated invoices.&#x20;

<figure><img src="../.gitbook/assets/image (7).png" alt="Examples of invoice icons"><figcaption><p>invoice icons</p></figcaption></figure>

To learn more about these invoice types, please visit the [Maxio Help Portal](https://maxio-chargify.zendesk.com/hc/en-us/articles/5404980119949-Invoice-Consolidation), or contact our sales team at [sales@coreweave.com](mailto:sales@coreweave.com) if you have additional questions.

## Payment policies

A valid credit card is required to use CoreWeave Cloud. To update your card information, please use the **Update Payment Method** button in the billing portal. Invoices are due when issued at the end of each month and your account may be deactivated if not paid.

If your monthly bill exceeds $20,000, you must pay by bank wire transfer. Please contact your account executive or send an email to [sales@coreweave.com](mailto:sales@coreweave.com) for information on how to complete a wire transfer.

### Reserved instances and account credits

Billing adjustments for reserved instances or other account credits are managed by your Account Executive or Client Success Manager. The exact terms are specified in your reserved instance contract and applied to each monthly invoice.&#x20;

## How to view resources

You can view your billable resources in CoreWeave Cloud.&#x20;

The [Account Overview](https://cloud.coreweave.com/) on the home page is the best place to start if you need a quick overview of the GPUs, CPUs, storage, and IP addresses currently active in your account. It also shows the total expenses for the previous day, the current billing period, and the total cost per hour.

Use the [Grafana menu](https://grafana.coreweave.com/) to find useful dashboards with compute and storage summaries, and detailed reports of the GPUs, CPUs, memory, and network activity for each Pod. These managed Grafana dashboards cannot be modified, but you can [create your own](../cloud-tools/grafana.md).

See these articles for advanced topics:

* [View Resources with Grafana](../cloud-tools/grafana.md): Learn how to deploy a self-hosted Grafana instance and build custom dashboards with our Prometheus metrics.
* [View Resources with `kubectl`](../cloud-tools/kubectl.md): Inventory your Pods, Services, Deployments, and more with standard Kubernetes tools.

## Frequently asked questions

### Where can I find historical invoices?

Historical invoices are in the billing portal, on the **Invoices** tab.

### How can I quickly find out what I am spending right now?

The **Account Overview** section of the CoreWeave Cloud [home page](https://cloud.coreweave.com/) has a summary.

### How can I monitor my expenses over time?

You can use our [Grafana dashboards](https://grafana.coreweave.com/), or build custom reports with [your own](../cloud-tools/grafana.md) Grafana instance.&#x20;

### How can I monitor active workloads?

You can monitor active workloads with [Kubernetes tools](../cloud-tools/kubectl.md).

## Software licensing

If you use Microsoft Windows, CoreWeave offers Windows licenses for a monthly charge or you can [bring your own license](https://www.microsoft.com/en-us/licensing/default). We also offer usage-based licenses for many products such as:

* Autodesk Arnold
* SideFX Houdini Engine
* SideFX Karma
* SideFX Mantra
* Maxon Redshift
* Maxon Cinema 4D (C4D)

However, we do not offer interactive licenses. If you'd like more information or a licensing quote, please contact your account executive.&#x20;

## Summary

Our billing portal streamlines the process of managing your invoices and payment information, and you can conveniently access your current expenses in [CoreWeave Cloud](https://cloud.coreweave.com/).

Managing your invoices and payment information in our billing portal is straightforward, and you can quickly access your current expenses in CoreWeave Cloud. Additionally, you can track your resource usage with prebuilt Grafana dashboards, or you can use custom dashboards and Kubernetes commands for more detailed tracking. Our portal is secure and compliant with industry privacy standards. We hope this guide answers your billing-related questions. Please don't hesitate to contact us at [sales@coreweave.com](mailto:sales@coreweave.com) if you need further assistance.
