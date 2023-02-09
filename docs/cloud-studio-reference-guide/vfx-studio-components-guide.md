---
description: Set up and deploy a VFX studio on CoreWeave Cloud
---

# Rendering

## Prerequisites

Before following the rest of this guide, ensure that the following are completed:

* [ ] You have [a CoreWeave Cloud account](https://cloud.coreweave.com/request-account)
* [ ] Your [management environment](../coreweave-kubernetes/getting-started/) is set up

{% hint style="success" %}
**Tip**

You may also want to **** [install Helm](https://helm.sh/) on your local system in order to manage and update the applications deployed in your namespace, though this is optional.
{% endhint %}

## Rendering

CoreWeave offers a fully managed, auto-scaled Thinkbox Deadline solution for handling medium to large studios' rendering needs.

{% hint style="info" %}
**Additional Resources**

For more information about setting up Deadline within your namespace, refer to our [Managed ThinkBox Deadline guide](../vfx-and-rendering/vfx/deadline.md).
{% endhint %}

One modification we may choose to make in our Worker values is to ensure that our shared storage is mounted into our Deadline workers. This is as simple as adding the following [volume mount definitions](https://kubernetes.io/docs/concepts/storage/volumes/) to our Worker manifest:

```yaml
volumeMounts:
  - name: render-output
    mountPath: /mnt/output
volumes:
  - name: general
    persistentVolumeClaim:
      claimName: render-output
```

{% hint style="info" %}
**Additional Resources**

This follows the standard Kubernetes syntax for describing `volumeMounts` and `volumes`. Learn more from [the official Kubernetes documentation](https://kubernetes.io/docs/concepts/storage/volumes/).
{% endhint %}

A complete Worker manifest will look something like the following:

```yaml
version: 10.1.18.5
rcs:
  pass: password123
 licenseForwarder:
  enabled: true
  auth:
    secrets:
      name: ubl-certificates
workers:
- name: maya-epyc
    enabled: true
    groups:
      - maya-epyc
      - maya
    pools:
      - vfx
    volumeMounts:
    - name: render-output
    mountPath: /mnt/output
    volumes:
    - name: general
    persistentVolumeClaim:
      claimName: render-output
    scale:
      pollingNames:
      - name: maya-epyc
        type: Group
      minReplicas: 0
      maxReplicas: 100
      scalingFactor: 1
    image: registry.gitlab.com/coreweave/render-images/maya2022:1
    imagePullSecrets: &imagePullSecrets
      - name: render-images
    env:
      - name: ARNOLD_LICENSE_ORDER
        value: network
      - name: ADSKFLEX_LICENSE_FILE
        value: 127.0.0.1
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: node.coreweave.cloud/cpu
                  operator: In
                  values:
                    - amd-epyc-rome
                    - intel-xeon-v4
                - key: node.coreweave.cloud/class
                  operator: In
                  values:
                    - cpu
        preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: topology.kubernetes.io/region
                    operator: In
                    values:
                      - ORD1
    resources:
      limits:
        cpu: 35
        memory: 130Gi
      requests:
        cpu: 35
        memory: 129Gi
```

{% hint style="info" %}
**Additional Resources**

If you'd like to learn more about what the pieces of this manifest mean, refer to our [Virtual Server documentation](broken-reference).
{% endhint %}
