---
description: Expose Applications using Kubernetes Services
---

# Exposing Applications

Kubernetes workloads can be exposed to each other, and to the public using Services and [Ingresses](exposing-applications.md#ingress). A Service allocates a dedicated IP for the exposed application, whereas an Ingress works for HTTP based protocols and alleviates the need for a separate IP for each endpoint. For stateless web-services, using the [Serverless](../serverless.md) framework is another option where the application is deployed with a TLS enabled hostname and auto-scaling for you.

## Internal Services

Internal, cluster local services should be configured as regular `ClusterIP` services.

## Public Services

Exposing services to the Internet is done by deploying a `LoadBalancer` service type with an annotation to allocate a public IP for the service. Without the annotation, a static private IP will be allocated, this is mostly useful for services accessed from outside the cluster via a Site to Site VPN.

Depending upon where you've requested your workloads to run, public IP pools are accessible via the region location in the following manner:

| Region | Address Pool Label |
| ------ | ------------------ |
| ORD1   | public-ord1        |
| EWR1   | public-ewr1        |
| LGA1   | public-lga1        |
| LAS1   | public-las1        |

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
To ensure optimal traffic routing, ensure that your workload is only scheduled to run in the region where a public IP is requested from. Use the [region label affinity](../label-selectors.md) to limit scheduling of the workload to a single region.
{% endhint %}

### Attaching Service IP directly to Pod

The traditional Kubernetes pattern is one or many Pods with dynamic internal IPs exposed behind a Service or Ingress with a static IP. For certain use cases, where there would only be one Pod behind a service, it can make sense to attach the Service IP directly to the Pod. A Pod would then have a static public IP as it's Pod IP. All connections originating from the pod will have this IP as it's source, and the Pod will see this as it's local IP. This is a non standard approach for containers, and should be used only when the traditional Service / Pod pattern is not feasible. Directly attaching the Service IP is beneficial in the following scenarios:

* The application needs to expose a large number of ports (above 10), where listing them out in the service definition is impractical
* The application needs to see the service IP on the network interface inside the pod
* Connections originating from the Pod to the outside need to originate from the Service IP
* The application needs to receive all traffic regardless of type and port
* A Virtual Machine type workload where a static IP provides a more native experience

Please note that an application that directly attaches a Service IP can run with a maximum of **1** replica, as there would otherwise be multiple Pods with the same Pod IP. Traffic to the Pod will not be filtered, all inbound traffic to the IP will be sent to the pod. To provide security, [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) can be applied.

A stub Service needs to be created to allocate the IP. The Service should expose only port `1` as in the example below.

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

To attach the IP from the Service directly to a Pod, annotate the Pod spec.

```yaml
  annotations:
    net.coreweave.cloud/attachLoadbalancerIP: my-app
```

### Ingress

Using an Ingress for HTTP based applications are beneficial as it saves IP addresses and automatically provides a DNS name as well as TLS certificate to allow access to your application via `https`. CoreWeave already has all the infrastructure setup including the Ingress Controller, all you need to do is deploy an `Ingress` manifest. The hostname of the Ingress needs to be in the format of `<app>.<namespace>.<region>.ingress.coreweave.cloud`. The example below demonstrates an Ingress called `my-app` exposed via an Ingress in the ORD1 region for a namespace `tenant-test-default`.

If a custom domain name is desired, a custom Ingress Controller can be deployed via [CoreWeave apps](https://apps.coreweave.com).

```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    ingress.kubernetes.io/force-ssl-redirect: "true"
    ingress.kubernetes.io/ssl-redirect: "true"
    traefik.ingress.kubernetes.io/redirect-entry-point: https
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
```

### External DNS

[Kubernetes internal DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) provides service discovery inside the cluster, allowing reachability of Services and Pods without the use of IP addresses. Many applications will need to be reached not only from inside the cluster, but also from outside on the broader Internet.  CoreWeave provides External DNS out of the box for all types of applications, similar to Ingress for HTTP. The DNS name must be in the format of `<your-chice>.<namespace>.coreweave.cloud`

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
