---
description: Configure network connections for your VFX Cloud Studio
---

# Configure Networking

## Create Network Policies

Connectivity between Kubernetes components and the Internet is managing by [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).

For the following example implementation, a simple group of Network Policies are created, which designate user groups with different access levels to both internal and external resources.

Network Policies are specified in YAML manifests, and are deployed to the namespace using `kubectl`:

```bash
$ kubectl apply -f <path/to/manifest>
```

### For artists

The first example Network Policy is called `artist`, and defines network permissions for the `artist` user group (`user.group`).

This Network Policy uses a [Pod Selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/), which matches any Pod that has the label `user.group: artist`. The Policy specifies that it allows inbound traffic from the local namespace on ports `3389`, `4172`, `60443` and `443`.

The Policy additionally specifies that it allows `artist` machines to send outbound traffic to any destination within the same namespace using ports `139` and `445`.

{% hint style="info" %}
**Note**

Network Policies are additive - any IP range or port not explicitly included in the Policy will not be accessible.
{% endhint %}

<details>

<summary>Click to expand - Network Policy for artists</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: artist
spec:
  podSelector:
    matchLabels:
      user.group: artist
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: tenant-sta-vfx1-reference
    ports:
    - protocol: TCP
      port: 3389
    - protocol: TCP
      port: 4172
    - protocol: TCP
      port: 60443
    - protocol: TCP
      port: 443
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: tenant-sta-vfx1-reference
    ports:
    - protocol: TCP
      port: 139
    - protocol: TCP
      port: 445
```

</details>

The Policy prevents connections that originate outside the cluster from reaching the internal machines, except on port `3389`, which is an RDP port that is left open to provide admin access for troubleshooting machines.

{% hint style="info" %}
**Tip**

The [Network Policy Editor](https://editor.networkpolicy.io/) is a visual, interactive tool that assists composing these policies by working with diagrams like the example below.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (62).png" alt="NetworkPolicy visualization"><figcaption><p>Network Policy Editor diagram</p></figcaption></figure>

If the Network Policy were to be stricter, it might only allow traffic that originates from the [Active Directory Samba](../../../virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/) and from [Teradici Connection Manager](https://www.teradici.com/web-help/pcoip\_connection\_manager\_security\_gateway/19.08/). This would prevent any external or internal resource from connecting to our machines without going through the connection manager and the [Leostream connection broker](../management.md).

Such a policy would look like this:

<details>

<summary>Click to expand - Strict Network Policy for artists</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: artist
spec:
  podSelector:
    matchLabels:
      user.group: artist
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: teradici-gateway-teridici-conn-gateway
    ports:
    - protocol: TCP
      port: 3389
    - protocol: TCP
      port: 4172
    - protocol: TCP
      port: 60443
    - protocol: TCP
      port: 443
  egress:
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: samba-ad-samba-ad
    ports:
    - protocol: TCP
      port: 139
    - protocol: TCP
      port: 445
```

</details>

{% hint style="info" %}
**Additional Resources**

To learn more about remotely managing VFX Studios, refer to [Manage a Cloud Studio](../management.md).
{% endhint %}

To apply a Policy to a relevant Virtual Workstations, first deploy them using `kubectl apply`:

```bash
$ kubectl apply -f <path/to/manifest>
```

This ensures that only those machines that are labelled as `artist` machines will be affected by the Policy.

Next, navigate to [the Virtual Server management page](https://cloud.coreweave.com/virtualservers). From here, Virtual Servers (Virtual Workstations) can be stopped, edited, and then started again. Stop the running artist machines, then edit the YAML manifest by clicking the **Edit** button and opening the YAML tab.

<figure><img src="../../../.gitbook/assets/image (18) (1).png" alt=""><figcaption></figcaption></figure>

Then, open the YAML editor by clicking the **EDIT YAML** tab on the right-hand side of the screen, and add the following `label` to the manifest:

```yaml
labels:
  user.group: "artist"
```

Start the machines once again. After restarting, the machines should contain the `artist` label, and the Network Policy should be applied.

### For administrators

Now, a different Network Policy is created for administrators.

<details>

<summary>Click to expand - Network Policy for administrators</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: administration
spec:
  podSelector:
    matchLabels:
      user.group: administration
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 3389
    - protocol: TCP
      port: 4172
    - protocol: TCP
      port: 60443
    - protocol: TCP
      port: 443
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
          - 10.0.0.0/8
```

</details>

This policy prohibits administrators from accessing the Samba storage, but allows them to connect to anything else.

### For resources

It is suggested that if you add a wide open network policy, pay close attention to whether or not a public IP address is assigned to avoid un-intended connections from external actors.

The final Network Policy to create is one that allows internal infrastructure to be reachable by other resources. A wide open egress policy is also added, so that Services can connect to resources within the namespace or on the Internet.

<details>

<summary>Click to expand - Network Policy for resources</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: infra
spec:
  podSelector:
    matchLabels:
      user.group: infra
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: tenant-sta-vfx1-reference
  egress: 
  - {}
```

</details>

{% hint style="info" %}
**Note**

Should an open egress Policy be deployed, pay close attention to whether or not a public IP addresses are assigned to avoid unintended connections from external actors.
{% endhint %}

## Firewalls

To learn more about firewalls for Virtual Servers, refer to [CoreWeave Cloud Native Networking (CCNN): Network Policies (Firewalls)](../../../networking/coreweave-cloud-native-networking-ccnn.md#network-policies-firewalls).

[CoreWeave Cloud Native Networking (CCNN)](../../../networking/coreweave-cloud-native-networking-ccnn.md) is the provided networking solution for VFX Studios, and configuring Network Policies is the standard method for network security within CCNN.

At this time, CCNN does not offer a managed intrusion detection solution (IDS) or intrusion prevention system (IPS).
