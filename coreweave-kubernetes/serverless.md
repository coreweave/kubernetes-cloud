# Serverless

Deploying applications as serverless services is a good alternative to a regular Deployment / Service model when the applications purpose is to serve HTTP or gRPC requests, either internal or from the Internet. CoreWeave uses the [KNative](https://knative.dev/docs/serving/getting-started-knative-app/) runtime to support deploying a serverless application with a single manifest. No installation necessary.

![](../docs/.gitbook/assets/screen-shot-2020-05-25-at-9.08.48-am.png)

#### Serverless Benefits

* Automatic public HTTPS endpoints
* Auto-scaling, including scale to zero
* No public IP charges
* [Canary deployments](https://knative.dev/docs/serving/samples/blue-green-deployment/) and other advanced deployment strategies

#### One Step Example

{% code title="helloworld-ksvc.yaml" %}
```yaml
apiVersion: serving.knative.dev/v1 # Current version of Knative
kind: Service
metadata:
  name: helloworld # The name of the app
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0" # Allow scale to Zero
        autoscaling.knative.dev/maxScale: "10" # Maximum number of Pods allowed to auto-scale to
    spec:
      # The container concurrency defines how many active requests are sent to a single
      # backend pod at a time. This configuration is important as it effects how well requests
      # are load balanced over Pods. For a standard, non-blocking web applocation this can usually
      # be rather high, ie 100. For GPU Inference however, this should usually be set to 1.
      # GPU Inference only processes one request at a time, and one wants to avoid a queue being
      # built up in the local pod instead of centrally in the Load Balancer.
      containerConcurrency: 10 
      containers:
        - image: gcr.io/knative-samples/helloworld-go # The URL to the image of the app
          resources:
            limits:
              cpu: 2
              memory: 4Gi
          env:
            - name: TARGET # The environment variable printed out by the sample app
              value: "Go Sample v1"
          
```
{% endcode %}

After applying the manifest, get the public URL of the service. The service will be scaled up and down based on demand, and scaled to zero consuming no resources and incurring no billable charges when idle.

```bash
$ kubectl get ksvc
NAME            URL                                                       LATESTCREATED         LATESTREADY           READY   REASON
helloworld      https://helloworld.default.knative.chi.coreweave.com      helloworld-ngzsn      helloworld-ngzsn      True
```

### Monitoring

Managed Grafana provides monitoring of requests, success rates, response times and auto-scaling metrics transparently. No metrics specific code needs to be added to the serverless application.

![](../docs/.gitbook/assets/screen-shot-2020-05-08-at-1.34.33-am.png)
