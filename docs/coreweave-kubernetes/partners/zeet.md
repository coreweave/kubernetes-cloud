---
description: Deploy code simply on CoreWeave Cloud with Zeet
---

# Zeet

<figure><img src="../../.gitbook/assets/image (11) (3).png" alt="The Zeet logo - a black octopus-like shape inside a green square"><figcaption></figcaption></figure>

[Zeet](https://zeet.co) is a DevOps automation platform that helps teams deploy and scale ML infrastructure across cloud providers. By empowering Developers to self-serve production-ready infrastructure and enabling DevOps and infrastructure teams  to templatize and right-size infrastructure components, Zeet fosters higher levels of iteration and collaboration within your team.

The Zeet platform runs on top of your Cloud account(s), making it simple for developers to deploy code on production-grade infrastructure. Its multi-cloud capabilities allow you to easily select the best destination for any unique workload and to seamlessly manage multi-region infrastructure for low-latency applications. If you’re a company leveraging ML/AI infrastructure you can quickly enable hardware acceleration on your services by selecting from a catalog of GPUS across every cloud provider to get the best model performance, save time, and reduce the cost of running your advanced infrastructure.

Zeet works alongside your existing  tools like CI/CD workflows, monitoring platforms and  more helping you minimize switching costs with out-of-the-box compatibility. If these pieces of your stack are still on the roadmap, you can leverage Zeet’s built-in CI/CD and Git Integration, to get to a level of production readiness within minutes. Whether you’re running Serverless, kubernetes or otherwise. Zeet can help you accelerate your engineering organization and remove DevOps bottlenecks.

## How we partner

Zeet helps companies set up and deploy their Kubernetes configuration on CoreWeave. This seamless integration significantly reduces the time it takes to access GPUs and run your application on the Cloud.

With CoreWeave's Kubernetes-native infrastructure and Zeet's team of Kubernetes engineers, we're helping our clients scale and realize value faster without having to build an entire infrastructure engineering team of their own.

Our partnership allows companies to tap into the industry’s broadest selection of on-demand GPU compute resources and DevOps expertise.

### Key benefits

* Faster cloud migrations&#x20;
* Reduce costs
* Scale quickly
* Reduce infrastructure burdens

### Learn more

<table data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Blog:</strong> Zeet and CoreWeave Make It Simpler for AI Companies to Manage Kubernetes Infrastructure</td><td></td><td></td><td><a href="https://www.coreweave.com/blog/zeet-and-coreweave-make-it-simpler-for-ai-companies-to-manage-kubernetes-infrastructure">https://www.coreweave.com/blog/zeet-and-coreweave-make-it-simpler-for-ai-companies-to-manage-kubernetes-infrastructure</a></td><td><a href="../../.gitbook/assets/cwxzeet.png">cwxzeet.png</a></td></tr><tr><td><strong>Blog:</strong> Tarteel Migrates Cloud Infrastructure to CoreWeave with Help from Zeet</td><td></td><td></td><td><a href="https://www.coreweave.com/blog/tarteel-migrates-cloud-infrastructure-to-coreweave-with-help-from-zeet">https://www.coreweave.com/blog/tarteel-migrates-cloud-infrastructure-to-coreweave-with-help-from-zeet</a></td><td><a href="../../.gitbook/assets/tarteel.png">tarteel.png</a></td></tr><tr><td><strong>Webinar:</strong> How to Get Started with Platform Engineering, Featuring Zeet</td><td></td><td></td><td><a href="https://coreweave.com/blog/get-started-with-platform-engineering-zeet-webinar">https://coreweave.com/blog/get-started-with-platform-engineering-zeet-webinar</a></td><td><a href="../../.gitbook/assets/zeetwebinar.png">zeetwebinar.png</a></td></tr></tbody></table>

## Integration

Integrating with Zeet is as simple as generating new CoreWeave Cloud access credentials, then providing those credentials to Zeet.

### Prerequisites

The following presumes that you already have [an active CoreWeave Cloud account](../getting-started.md).

### Generate API token

If you already have an API token to give to Zeet, skip this step.

API tokens can be found embedded in the generated `kubeconfig` files. For more information, see [Get Started with CoreWeave](../getting-started.md#obtain-coreweave-access-credentials).

After signing in to your CoreWeave Cloud account, ask [your organization administrator](../../cloud-account-management/organizations.md#organization-admin) to generate a new API token by navigating to the **API Access page**, or navigate directly to [`https://cloud.coreweave.com/api-access`](https://cloud.coreweave.com/api-access) in your browser.

<figure><img src="../../.gitbook/assets/image (2) (1) (2) (2).png" alt=""><figcaption></figcaption></figure>

From this page, the organization administrator clicks the **Create a new token** button in the upper right-hand corner to generate a new API access token, as well as a new `cw-kubeconfig` file that embeds the same token.

{% hint style="info" %}
**Additional Resources**

See [Obtain CoreWeave Access Credentials](../getting-started.md#obtain-coreweave-access-credentials) for more information.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (5) (3).png" alt=""><figcaption></figcaption></figure>

Log in to your Zeet account, then navigate to the Zeet dashboard at [`https://zeet.co/account/cloud`](https://zeet.co/account/cloud).

Click the **Clouds** tab on the left-hand side of the screen, then click **Connect cloud**.

<figure><img src="../../.gitbook/assets/image (8) (2).png" alt=""><figcaption></figcaption></figure>

From the list of providers, select CoreWeave. From the **Connect Provider** tab, click the **Upload cw-kubeconfig** button to upload the generated `cw-kubeconfig` file.

<figure><img src="../../.gitbook/assets/image (7) (2) (3).png" alt=""><figcaption></figcaption></figure>

Once the file is uploaded, the credentials run through a verification check. Once the check succeeds, a green checkmark will appear under the **Connected** column beside the **CoreWeave Tenant** name.

<figure><img src="../../.gitbook/assets/image (13) (2) (2).png" alt=""><figcaption></figcaption></figure>

Once the Cloud has been connected, navigate to [`https://zeet.co/account/cloud`](https://zeet.co/account/cloud). From here, information about your CoreWeave cluster and all current integrations will be displayed.

<figure><img src="../../.gitbook/assets/image (1) (2).png" alt=""><figcaption></figcaption></figure>

For more information on configuring CoreWeave or to deploy applications onto CoreWeave using Zeet, visit [Zeet's CoreWeave official integration docs](https://docs.zeet.co/0.1.0/cloud/coreweave/#3-configure-coreweave-cluster).
