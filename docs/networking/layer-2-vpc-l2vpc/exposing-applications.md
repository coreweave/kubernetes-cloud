---
description: Expose your applications using Kubernetes Services
---

# Exposing Applications

[Kubernetes Workloads](https://kubernetes.io/docs/concepts/workloads/) can be exposed to each other, but they can also be publicly exposed to the Internet using [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/) and [Ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/).

A Service allocates a dedicated IP address for the exposed application, whereas an Ingress works for HTTP-based protocols to alleviate the need for a separate IP at each endpoint.

{% hint style="info" %}
**Note**

For stateless Web services, the [Serverless framework](../../../coreweave-kubernetes/serverless.md) may be a good option. In this framework, the application is automatically deployed with a TLS-enabled hostname and autoscaling enabled.
{% endhint %}

## Internal Services

Internal, cluster-local Services should be configured as regular [`ClusterIP` services](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types).

## Public Services

Making Services public to the Internet is done by deploying [a `LoadBalancer` Service type](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) with an annotation that allocates a public IP for the Service.

{% hint style="info" %}
**Note**

Without a public IP annotation, a private static IP will be allocated. This is mostly useful for Services accessed from outside the cluster via a Site-to-Site VPN.
{% endhint %}

Depending on where your workloads are configured to run, public IP pools are accessible via the region location using the following corresponding tags:

| Region | Address Pool Label |
| ------ | ------------------ |
| ORD1   | `public-ord1`      |
| LGA1   | `public-lga1`      |
| LAS1   | `public-las1`      |

#### **Example manifest**

In this example, an SSHD LoadBalancer Service is deployed with the region annotation `metallb.universe.tf/address-pool: public-ord1`:

{% code title="sshd-public-service.yaml" %}
```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    metallb.universe.tf/address-pool: public-ord1
    metallb.universe.tf/allow-shared-ip: default
  name: sshd
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  ports:
    - name: sshd
      port: 22
      protocol: TCP
      targetPort: sshd
  selector:
    app.kubernetes.io/name: sshd
```
{% endcode %}

{% hint style="warning" %}
**Important**

To ensure optimal traffic routing, ensure that your Workload is only scheduled to run in the same region from which a public IP is being requested. Use the [region label affinity](../../../coreweave-kubernetes/label-selectors.md) to limit scheduling of the Workload to a single region.
{% endhint %}

### Attaching Service IPs directly to Pods

The traditional Kubernetes pattern dictates that one or many Pods with dynamic internal IP addresses be exposed behind a Service or Ingress which itself has a static IP address.

For certain use cases, such as where only be one Pod is behind a Service, it might make sense to attach the Service IP directly to the Pod. A Pod would then have a static public IP as its Pod IP.

All connections originating from the Pod will show this IP as its source address, and this address will serve as its local IP.

{% hint style="info" %}
**Note**

This is a non-standard approach for containers, and should be used only when the traditional Service/Pod pattern is not feasible.
{% endhint %}

Directly attaching the Service IP is beneficial in the following scenarios:

* The application needs to expose a large number of ports (more than 10), so listing them out in the Service definition is impractical
* The application needs to see the Service IP on the network interface inside the Pod
* Connections originating from the Pod to the outside world need to originate from the Service IP
* The application needs to receive all traffic, regardless of type and port
* The Workload is a Virtual Machine type, where a static IP provides a more native experience

{% hint style="warning" %}
**Important**

An application that directly attaches to a Service IP can run with a maximum of `1` replicas, as there would otherwise be multiple Pods with the same Pod IP. Also, traffic to the Pod will not be filtered; all traffic inbound to the IP will be sent to the Pod. [Network Policies can be used for additional security](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
{% endhint %}

A stub Service needs to be created to allocate the IP. The Service should expose only port `1`, as shown in the example below:

#### Example manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  annotations:
    metallb.universe.tf/address-pool: public-ord1
spec:
  externalTrafficPolicy: Local
  type: LoadBalancer
  ports:
    - port: 1 # Do not change this
      targetPort: attach
      protocol: TCP
      name: attach
     # Do not add any additional ports, it is not required for direct attach
  selector: 
    coreweave.cloud/ignore: ignore # Do not change this
```

Then, to attach the IP from the Service directly to a Pod, annotate the Pod spec:

```yaml
  annotations:
    net.coreweave.cloud/attachLoadbalancerIP: my-app
```

### Using Ingresses

Using an Ingress for HTTP-based applications is beneficial, as it saves IP address space and automatically provides a DNS name as well as TLS certificate to allow access to your application via `https`.

CoreWeave provides the infrastructure setup, including the Ingress Controller; all you need to do is deploy an `Ingress` manifest in the format of `<app>.<namespace>.<region>.ingress.coreweave.cloud`.

The example below demonstrates an Ingress called `my-app`, exposed via an Ingress in the ORD1 data center region for a namespace called `tenant-test-default`. If a custom domain name is desired, a custom Ingress Controller may be deployed from the [CoreWeave application Catalog](https://apps.coreweave.com).

#### Example manifest

<pre class="language-yaml"><code class="lang-yaml"><strong>---
</strong><strong>apiVersion: networking.k8s.io/v1beta1
</strong>kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    traefik.ingress.kubernetes.io/router.middlewares: tenant-test-default-redirect-secure@kubernetescrd
  labels:
    app.kubernetes.io/name: my-app
  name: my-app
spec:
  rules:
  - host: my-app.tenant-test-default.ord1.ingress.coreweave.cloud
    http: 
      paths:
      - backend:
          serviceName: my-app
          servicePort: http
        path: /
        pathType: ImplementationSpecific
  tls:
  - hosts:
    - my-app.tenant-test-default.ord1.ingress.coreweave.cloud
    secretName: my-app-tls # This secret is automatically created for you
---
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: redirect-secure
  namespace: tenant-test-default
spec:
  redirectScheme:
    permanent: true
    scheme: https</code></pre>

###

### Using External DNS

[Kubernetes internal DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) provides Service discovery inside the cluster, allowing connections between Services and Pods without the use of IP addresses. Many applications will need to be reached both from inside the cluster as well as from the Internet.

CoreWeave provides External DNS out of the box for all types of applications - the given DNS name simply must be in the format of `<your-chice>.<namespace>.coreweave.cloud`.

#### Example manifest&#x20;

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    metallb.universe.tf/address-pool: public-ord1
    external-dns.alpha.kubernetes.io/hostname: my-sshd.tenant-test-default.coreweave.cloud
  name: sshd
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  ports:
    - name: sshd
      port: 22
      protocol: TCP
      targetPort: sshd
  selector:
    app.kubernetes.io/name: sshd
```
