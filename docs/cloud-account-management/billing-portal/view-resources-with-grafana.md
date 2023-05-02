# View Resources with Grafana

Our Prometheus scraping service offers many useful [billing metrics](../../../coreweave-kubernetes/prometheus/useful-metrics.md) you can use in Grafana. These instructions describe how to deploy your own [Grafana dashboards](../../../coreweave-kubernetes/prometheus/grafana.md) in CoreWeave Cloud, but you can also connect an on-premise Grafana instance to our Prometheus datasource.

&#x20;Here's how:

1. Deploy the [Grafana app](https://apps.coreweave.com/) on CoreWeave Cloud.
2.  Log in to Grafana by following the Ingress Access URL on the deployment page. The account and password can be found in the upper right corner of the page.\


    <figure><img src="../../.gitbook/assets/image (12).png" alt="Access URL"><figcaption><p>Access URL</p></figcaption></figure>
3.  Go to **Configuration -> Data Sources** in the lower left menu.\


    <figure><img src="../../.gitbook/assets/image (9).png" alt="Data sources menu"><figcaption><p>Data sources menu</p></figcaption></figure>


4. Click **Add New Datasource** and select **Prometheus**.
5. Set the **Name** to **CoreWeave**.
6. Set the **URL** to `https://prometheus.ord1.coreweave.com`.
7. Click **Add Header** in the **Custom HTTP Headers** section.
8.  Set the following values for **Custom HTTP Header.** \
    \
    **Header**: `Authorization` \
    **Value**: `Bearer [my-token]`\
    \
    Replace `[my-token]` with your API Access token.\


    <figure><img src="../../.gitbook/assets/image (11).png" alt="Connection settings"><figcaption><p>Connection settings</p></figcaption></figure>
9.  Click **Save & Test** at the bottom of the page to verify and save the new datasource.\
    \


    <figure><img src="../../.gitbook/assets/image (8).png" alt="Successful connection"><figcaption><p>Successful connection</p></figcaption></figure>

### How to find your API Access Token

If you don't have a token, you can generate a new one on the [API Access](https://cloud.coreweave.com/api-access) page. If you've already configured Kubernetes, your token is in the `users` section of `kubeconfig`. &#x20;

You can view your unredacted `kubeconfig` with `kubectl`.

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

The API Access token, `REDACTED` in this example, is in the `users` section at the bottom.

If you have more than one context in your kubeconfig, make sure to choose the token for your desired namespace.

## Billing metrics

If you are building a Grafana dashboard for the first time, we suggest reading [Build your first dashboard](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/) at Grafana Labs.

If you have some experience with Grafana and need to know where to find the metrics, look for the  `billing` metrics in the CoreWeave datasource. You do not need to filter the namespace when adding these metrics to a dashboard.

<figure><img src="../../.gitbook/assets/image (4).png" alt="Billing metrics"><figcaption><p>Billing metrics</p></figcaption></figure>

