---
description: Create multiple Kubernetes namespaces for your organization
---

# Namespace Management

[Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) provide logical separations of resources within a [Kubernetes cluster](https://kubernetes.io/docs/concepts/architecture/). Typically, CoreWeave clients' resources are run inside their own single namespace, but there are sometimes cases in which more than one namespace is required for the same organization.

{% hint style="success" %}
**Learn More**

Read more about namespaces and when you may need multiple namespaces in [the official Kubernetes documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#when-to-use-multiple-namespaces).
{% endhint %}

If your organization requires more than one namespace, then you may need to use multiple namespaces.

## Multi-namespace vs. single namespace tenancy

The ability to create multiple namespaces is enabled and accessible by default for all Cloud users. Multi-namespace organizations (MNOs) bear a few differences compared to standard, single-namespace tenancies:

### Resource separation

Kubernetes namespaces provide a way to isolate resources into specific groups. Resources like pods, services, and replication controllers that are deployed within one namespace do not share any resources (that is, neither compute resources nor Kubernetes resources) that are provisioned to another namespace.

Namespace separation can be necessary to segregate workloads for security purposes, or when multiple resources need to have the same name, as resources in a single namespace cannot have the same name. They can also be used to separate workloads utilizing different resource amounts or types. To that extent, resource quotas are set per namespace on CoreWeave Cloud. Some namespace use case examples can also be found in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/#understanding-the-motivation-for-using-namespaces).

### Permissions

The permissions and quotas for new namespaces are inherited from the namespace that is set in your current context in the CoreWeave Cloud dashboard. To change any of these permissions, [contact your CoreWeave Support Specialist](https://cloud.coreweave.com/contact).&#x20;

### Kubeconfig

Even when using multiple namespaces, [your `kubeconfig` file](../coreweave-kubernetes/getting-started.md#obtain-coreweave-access-credentials) will contain the default namespace that is set as the current Kubernetes context in the CoreWeave Cloud UI, which is selected in the dropdown menu located in the upper right-hand corner of the Cloud UI screen.

For example, if the namespace `tenant-namespace-1` is the active namespace context in the CoreWeave Cloud dashboard, it will be set as the default namespace in your `kubeconfig` file as well. This namespace value can be changed at any time by editing the `kubeconfig` file.

{% hint style="info" %}
**Additional Resources**

Learn more about how to configure Kubernetes namespace contexts in [the official Kubernetes documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/).
{% endhint %}

### Billing

For each namespace, your organization holds a subscription. Each subscription belongs to a **subscription group**. Subscription groups, and per-namespace subscriptions, are accessible via the [**billing portal**](billing-portal.md)**.** All namespaces belonging to the same organization will be billed together.

### Limitations

While allowing multiple namespaces for an organization provides a Kubernetes-native experience for our clients, there are a few limitations that users should be aware of:

1. All new namespaces will inherit **the original API handle prefix**
2. Organizations are limited to a max of **10 namespaces**
3. **Namespace deletion is not supported** at this time, unless you are deactivating your account
4. The namespace identifier **max length is 7 characters**
5. Namespace management is **only** supported in the CoreWeave Cloud dashboard, provisioning namespaces via the command line is currently not supported

## Setup and Management

To create and manage your account's namespaces, first [log in to your CoreWeave Cloud account](https://cloud.coreweave.com). Then, navigate to [the **Namespaces** page](https://cloud.coreweave.com/namespaces).

<figure><img src="../.gitbook/assets/image (3) (4).png" alt="Screenshot of the namespace management page"><figcaption><p>The namespace management page</p></figcaption></figure>

To create a new namespace, click the **Create New Namespace** button in the upper right-hand corner. This will open the **New Namespace** modal.

<figure><img src="../.gitbook/assets/image (4).png" alt="Screenshot of The new namespace modal"><figcaption><p>Example of the new namespace modal</p></figcaption></figure>

The **namespace identifier** will be used as the value of `<namespace-id>` shown in the preview window in the modal. As namespaces are often used to separate workloads by development phase, some common identifiers include things like `staging`, `dev`, or `prod` for the value of the namespace identifier.
