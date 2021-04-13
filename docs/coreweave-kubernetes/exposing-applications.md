---
description: Expose Applications using Kubernetes Services
---

# Exposing Applications

## Internal Services

Internal, cluster local services should be configured as regular `ClusterIP` services.

## Public Services

Exposing services to the Internet is done by deploying a `LoadBalancer` service type with an annotation to allocate a public IP for the service.

Depending upon where you've requested your workloads to run, public IP pools are accessible via the region location in the following manner:

| Region | Address Pool Label |
| :--- | :--- |
| ORD1 | public-ord1 |
| EWR1 | public-ewr1 |
| LAS1 | public-las1 |

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

{% hint style="info" %}
For most public services, ensure that `externalTrafficPolicy: Local` is set on the service. This load balances ingress traffic from the Internet directly to the  nodes running the  application.
{% endhint %}



