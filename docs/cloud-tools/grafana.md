---
description: Use managed Grafana, or build custom dashboards with a self-hosted instance
---

# Grafana

## Managed Grafana <a href="#grafana" id="grafana"></a>

CoreWeave provides a managed Grafana instance to view predefined dashboards with compute and storage summaries, and detailed reports of the GPUs, CPUs, memory, and network activity for each Pod.&#x20;

To access the managed Grafana instance, use the menu in the Account Details section of [CoreWeave Cloud](https://cloud.coreweave.com) or navigate directly to [https://grafana.coreweave.com](https://grafana.coreweave.com).

<div align="left">

<figure><img src="../.gitbook/assets/image (24) (2).png" alt="Screenshot of Grafana menu in CoreWeave Cloud"><figcaption><p>Grafana menu</p></figcaption></figure>

</div>

In this Grafana instance, the dashboards cannot be cannot modified, or new ones created. For complete control, deploy a own self-hosted Grafana instance on CoreWeave Cloud.

## Self-hosted Grafana

To build custom dashboards from CoreWeave's [Prometheus metrics](../../coreweave-kubernetes/prometheus/), deploy a Grafana instance with [CoreWeave Apps](https://apps.coreweave.com).

<div align="left">

<figure><img src="../.gitbook/assets/image (21) (2).png" alt="Grafana in the application catalog"><figcaption><p>Grafana</p></figcaption></figure>

</div>

### How to deploy Grafana

1. Navigate to [CoreWeave Applications](https://apps.coreweave.com), then click **Catalog**.
2. Search for Grafana, then click it to access the deployment screen.
3. Click **Deploy** in the upper-right corner.
4. Give it a meaningful name.
5. In most cases, leave **Expose to the Public via Ingress** selected.
6. Click **Deploy**.

Wait for the Pods to deploy, then click the Ingress URL to log in with the username and password in the upper-right corner.

<figure><img src="../.gitbook/assets/image (13) (6).png" alt="Screenshot of deployment screen"><figcaption><p>Deployment screen</p></figcaption></figure>

### Connect to Prometheus

Our Prometheus scraping service offers many useful [billing metrics](../../coreweave-kubernetes/prometheus/useful-metrics.md) for use in self-hosted Grafana instances. For an on-premise Grafana instance, follow these same steps to connect to CoreWeave's Prometheus service.&#x20;

1.  In the Grafana instance, go to **Configuration -> Data Sources** in the lower left menu.\


    <div align="left">

    <figure><img src="../.gitbook/assets/image (9) (4).png" alt="Data sources menu"><figcaption><p>Data sources menu</p></figcaption></figure>

    </div>


2. Click **Add New Datasource** and select **Prometheus**.
3. Set the **Name** to **CoreWeave**.
4. Set the **URL** to `https://prometheus.ord1.coreweave.com`.
5. Click **Add Header** in the **Custom HTTP Headers** section.
6.  Set the following values for **Custom HTTP Header.** \
    \
    **Header**: `Authorization` \
    **Value**: `Bearer [my-token]`\
    \
    Replace `[my-token]` with the API Access token.\


    <div align="left">

    <figure><img src="../.gitbook/assets/image (11) (1).png" alt="Connection settings"><figcaption><p>Connection settings</p></figcaption></figure>

    </div>
7.  Click **Save & Test** at the bottom of the page to verify and save the new datasource.\
    \


    <div align="left">

    <figure><img src="../.gitbook/assets/image (8) (4).png" alt="Successful connection"><figcaption><p>Successful connection</p></figcaption></figure>

    </div>

### How to find the API Access Token

If Kubernetes is already configured, the token is in the `users` section of `kubeconfig`.  If not, generate a new one on the [API Access](https://cloud.coreweave.com/api-access) page.

To view the unredacted `kubeconfig`, use `kubectl`.

```
kubectl config view --raw
```

Here's a redacted example:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://k8s.ord1.coreweave.com
  name: coreweave
contexts:
- context:
    cluster: coreweave
    namespace: tenant-EXAMPLE
    user: token-EXAMPLE-USER
  name: coreweave
current-context: coreweave
kind: Config
preferences: {}
users:
- name: token-EXAMPLE-USER
  user:
    token: REDACTED
```

The API Access token, which is `REDACTED` in this example, is located in the `users` section at the bottom.

If there is more than one context in the kubeconfig, make sure to choose the token for the desired namespace.

## Billing metrics

If building a Grafana dashboard for the first time, we suggest reading [Build your first dashboard](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/) at Grafana Labs.

The Grafana `billing` metrics are in the CoreWeave datasource. There is no need to filter the namespace when adding these metrics to a dashboard.

<div align="left">

<figure><img src="../.gitbook/assets/image (4) (5).png" alt="Billing metrics"><figcaption><p>Billing metrics</p></figcaption></figure>

</div>

{% hint style="success" %}
There's no need to filter the `namespace` label to the namespace for any metric. It will be automatically inserted on all queries received.
{% endhint %}

For more information about the Prometheus scraping service, refer to the [Metrics](../../coreweave-kubernetes/prometheus/) article.
