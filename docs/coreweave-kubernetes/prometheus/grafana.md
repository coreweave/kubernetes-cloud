# Grafana

## Hosted Grafana Instance

CoreWeave provides a managed Grafana instance so you can make your own dashboards and charts for your own metrics. If you're already a CoreWeave user, you can start creating dashboards now. Feel free to startup your own Grafana instance using [KubeApps](https://apps.coreweave.com/).

{% hint style="success" %}
You can access **Grafana** at [https://grafana.coreweave.com](https://grafana.coreweave.com/)
{% endhint %}

## Self Hosted Grafana Instance

You can host your own Grafana instance if you choose to. To use our Prometheus server in your own Grafana instance follow the guide below.

* Login as an admin on your Grafana instance and go to **Configuration** -&gt; **Data Sources**
* **Add New Datasource** and select **Prometheus** as the provider
* Set the new **Datasource Name** to `CoreWeave`
* Under _HTTP Section_ set **URL** to `https://prometheus.ord1.coreweave.com`
* Click the "**Add Header**" button under the _Custom HTTP Headers_ section
* Set the first value \(**Header**\) to: `Authorization` 
* Set the second value \(**Value**\) to `Bearer <TOKEN>` replace "&lt;TOKEN&gt;" with your Access Token.
* Click "**Save & Test**" button to verify and save the new datasource.

You can now choose the new `CoreWeave` datasource in a dashboard to visualize Prometheus metrics hosted on CoreWeave.

{% hint style="success" %}
There's no need to filter the `namespace` label to your namespace for any metric. It will be automatically inserted on all queries received. 
{% endhint %}

