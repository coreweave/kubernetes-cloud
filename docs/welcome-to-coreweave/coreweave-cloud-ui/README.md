---
description: Manage your resources and organization with the Cloud UI
---

# CoreWeave Cloud UI

**The CoreWeave Cloud UI**, sometimes referred to simply as the **Cloud UI**, is CoreWeave's Web management platform. Here, nearly all organization resources and account settings are managed from easy-to-use dashboards.

Each of the Cloud UI dashboards make it easy to deploy and manage resources or make changes to the organization. Below are quick overviews describing each Cloud UI dashboard and the features they control.

## Main dashboard

<figure><img src="../../.gitbook/assets/image (3).png" alt="Screenshot of the main dashboard of the CoreWeave Cloud UI"><figcaption></figcaption></figure>

The main dashboard is the first page after logging in to CoreWeave Cloud. On this page, a basic overview of the organization's statistics is displayed near the bottom of the page, which includes an overview of resource usage and billing information.

The three panels at the top of the page allow for quick navigation to the most popular dashboards:

* **Download kubeconfig:** From here, [organization administrators](../cloud-account-management/organizations.md#organization-administrators) may easily navigate to [set up a Kubeconfig file or generate an API token](../getting-started.md#generate-the-kubeconfig-file).
* **Deploy Virtual Server:** Any member of the organization may navigate here to deploy a [Virtual Server](./#virtual-servers).
* **Deploy Applications:** Any member of the organization may navigate here to deploy a new application from [the CoreWeave Applications Catalog](./#applications).

All other dashboards are accessed using the navigation on the left side of the page.

## Virtual Servers

<figure><img src="../../.gitbook/assets/image (38).png" alt="Screenshot of the Virtual Servers dashboard"><figcaption></figcaption></figure>

[Virtual Servers](broken-reference) are specialized virtual machines, configurable and deployable entirely through the Cloud UI's Web interface. Virtual Servers leverage the bare metal performance of CoreWeave Cloud for applications in [machine learning](broken-reference), [VFX rendering](broken-reference), or as [Virtual Workstations](../../vfx-and-rendering/virtual-workstations.md).

Virtual Servers are configured, deployed, and managed from the Virtual Servers dashboard.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

## Applications

The **applications dashboard** displays all applications currently installed in the organization's namespace. From this dashboard, users may also check the status of applications, edit an application's deployment configuration, or delete a deployed application.

## Catalog

<figure><img src="../../.gitbook/assets/image (18).png" alt="Screenshot of the applications catalog"><figcaption></figcaption></figure>

The [CoreWeave Cloud Applications Catalog](https://apps.coreweave.com) is a built-in catalog featuring many useful applications, which can be deployed and ready to use in just a few clicks.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="applications-catalog.md">applications-catalog.md</a></td></tr></tbody></table>

## Storage Volumes

<figure><img src="../../.gitbook/assets/image (9).png" alt="Screenshot of the storage volumes dashboard"><figcaption></figcaption></figure>

High-performance, network-attached storage volumes for [containerized custom applications](../../coreweave-kubernetes/custom-containers.md) and for [Virtual Servers](../../../virtual-servers/getting-started.md) are easy to provision and manage from the Storage Volumes dashboard.

Storage Volumes are available in both [all-NVMe](./#storage-tiers) and [HDD tiers](./#storage-tiers), and can be created as [Block Volumes](./#block-storage-volumes) or [Shared File System Volumes](./#shared-file-system-volumes). Storage Volumes can be resized at any time, and because storage resources are managed separately from compute, they can be moved between instances and between hardware types.

Quota increase requests may also be submitted here, by clicking the **Increase Quota** button at the top right.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../cloud-account-management/">cloud-account-management</a></td></tr></tbody></table>

## API Access

<figure><img src="../../.gitbook/assets/image (40).png" alt="Screenshot of the API management dashboard"><figcaption></figcaption></figure>

From the **API Access** page, [organization administrators](../cloud-account-management/organizations.md#organization-admin) may generate new [API access tokens and new Kubeconfig files](../getting-started.md) to allow organization members access to the namespace and the resources deployed within it.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../getting-started.md#generate-the-kubeconfig-file">#generate-the-kubeconfig-file</a></td></tr></tbody></table>

## Object Storage

<figure><img src="../../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>

CoreWeave [Object Storage](../../storage/object-storage.md) is an S3-compatible storage system that allows data to be stored and retrieved in a flexible and efficient way. From the Object Storage dashboard, new [Object Storage tokens](../../storage/object-storage.md#authentication) are generated and managed to configure authentication and access levels to Object Storage buckets.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../../storage/object-storage.md">object-storage.md</a></td></tr></tbody></table>

## Namespaces

<figure><img src="../../.gitbook/assets/image (22).png" alt="Screenshot of the namespace management dashboard"><figcaption></figcaption></figure>

Each organization on CoreWeave Cloud may have one or multiple namespaces, which are managed from the **Namespaces** dashboard. The current state of the namespace is seen here, and includes information such as the current number of GPUs in use, the number of Pods running in the namespace, the number of Virtual Servers deployed to the namespace, and the storage capacity of the namespace. Quota increase requests may also be submitted from this dashboard by clicking the ellipses on the right-hand side of the namespace listing.

<figure><img src="../../.gitbook/assets/image (6).png" alt="Screenshot of the namespace management dashboard"><figcaption><p>Request a quota increase from the namespace management dashboard</p></figcaption></figure>

To switch namespaces, click the **Active Namespace** dropdown selector in the upper right-hand corner of the Cloud UI, and select the desired namespace.

<figure><img src="../../.gitbook/assets/image (30).png" alt="Screenshot of the namespace selector"><figcaption></figcaption></figure>

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../cloud-account-management/namespace-management.md">namespace-management.md</a></td></tr></tbody></table>

## Grafana

This link redirects to the organization's [Grafana metrics page](../../../coreweave-kubernetes/prometheus/), providing the most in-depth view of the organization's infrastructure.

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="1f449">👉</span> Learn more</td><td></td><td></td><td><a href="../../../coreweave-kubernetes/prometheus/grafana.md">grafana.md</a></td></tr></tbody></table>

## Documentation

You are here! The documentation link redirects to [docs.coreweave.com](https://docs.coreweave.com).

## Status

Redirects to the status page for CoreWeave's systems, [status.coreweave.com](https://status.coreweave.com/).

## Upgrade Quotas

The **Upgrade Quotas** link is a quick link to submit a quota increase request. This link redirects to [the Storage Volumes page](./#storage-volumes).
