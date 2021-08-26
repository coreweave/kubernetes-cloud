---
description: CoreWeave manages the Prometheus cluster that will host your metrics.
---

# Metrics

To access CoreWeave's Prometheus server you'll first need a CoreWeave account and an Access Token. If you don't have an account yet, follow the steps on the [Getting Started](../getting-started.md) guide. 

You'll be able to access the Prometheus Dashboard once you're logged into CoreWeave.

{% hint style="success" %}
Access the **Prometheus Dashboard** at [**https://prometheus.ord1.coreweave.com**](https://prometheus.ord1.coreweave.com/)\*\*\*\*
{% endhint %}

## API Key Authentication

You can access the Prometheus server by sending your [Access Token](../getting-started.md#obtain-access-credentials) as the Authorization Header during your request. 

* Header: **`Authorization`** Value: **`Bearer <TOKEN>`**
* URL: **`https://prometheus.ord1.coreweave.com`**
* Methods: **`GET`** or **`POST`**

{% hint style="warning" %}
 Replace `<TOKEN>` with your CoreWeave Access Token generated from [https://cloud.coreweave.com/api-access](https://cloud.coreweave.com/api-access).
{% endhint %}

{% api-method method="post" host="https://prometheus.ord1.coreweave.com" path="/v1/api/query" %}
{% api-method-summary %}
Prometheus Query using Access Token
{% endapi-method-summary %}

{% api-method-description %}
Example usage for sending a request to the Prometheus API using your Access Token.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-headers %}
{% api-method-parameter name="Authorization" type="string" required=true %}
Set value to `Bearer <TOKEN>` as the value, replacing `<TOKEN>` with your CoreWeave Access Token.
{% endapi-method-parameter %}
{% endapi-method-headers %}

{% api-method-query-parameters %}
{% api-method-parameter name="time" type="number" required=true %}
Unix timestamp of current time
{% endapi-method-parameter %}

{% api-method-parameter name="query" type="string" required=true %}
Insert PromQL Query \(`kube_pod_container_info`\)
{% endapi-method-parameter %}
{% endapi-method-query-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Prometheus Data response on a query
{% endapi-method-response-example-description %}

```javascript
{
	"status": "success",
	"data": {
		"resultType": "vector",
		"result": [{
			"metric": {
				"__name__": "kube_pod_container_info",
				"container": "example",
				"container_id": "docker://1548c7ce5d717cfb9e3e797464d9fe4fbda0cea6f324fda8b9b64b2f5fd44e2f",
				"endpoint": "http",
				"image": "example/example_image:1.6.4",
				"image_id": "docker-pullable://docker-registry-image",
				"instance": "10.0.0.1:8080
				"job": "kube-state-metrics",
				"namespace": "tenant-example",
				"pod": "example-5d796977bc-crk9m",
				"service": "tenant-metrics-kube-state-metrics"
			},
			"value": [1629254349.447, "1"]
		}]
	}
}3
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

## Metric Scraping

CoreWeave's hosted Prometheus cluster will scrape your targets using a [ServiceMonitor](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/user-guides/getting-started.md). Annotations from the ServiceMonitor must match the Service hosting the Prometheus exporter endpoint. Usually `/metrics`

Below is an example of a Prometheus exporter that will be scraped by our Prometheus clusters.

{% tabs %}
{% tab title="servicemonitor.yaml" %}
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example
  namespace: tenant-example
  labels:
    app: example
spec:
  jobLabel: example-scraping
  selector:
    matchLabels:
      app: example
  namespaceSelector:
    matchNames:
      - tenant-example
  endpoints:
    - port: http
      scheme: http
      path: /metrics
      interval: 15s
      scrapeTimeout: 15s
```
{% endtab %}

{% tab title="deployment.yaml" %}
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example
  namespace: tenant-example
  labels:
    app: example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: example
  template:
    metadata:
      labels:
        app: example
    spec:
      containers:
        - name: example
          image: "infinityworks/docker-hub-exporter:latest"
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 9170
              protocol: TCP

```
{% endtab %}

{% tab title="service.yaml" %}
```yaml
apiVersion: v1
kind: Service
metadata:
  name: example
  namespace: tenant-example
  labels:
    app: example
spec:
  type: ClusterIP
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app: example

```
{% endtab %}
{% endtabs %}

