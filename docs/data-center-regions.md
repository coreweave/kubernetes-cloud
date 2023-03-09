---
description: Learn about CoreWeave's data center regions
---

# Data Center Regions

CoreWeave Cloud is served from **three geographically diverse regions** in the United States. Located directly adjacent to large metropolitan population centers, CoreWeave's data centers provide low latency access to accelerated compute to **over 51 million people**.

Our data centers are broken up into three geographical buckets, each of which service the regions for which they're named:

* ****[**US East**](data-center-regions.md#us-east-lga1)****
* ****[**US Central**](data-center-regions.md#us-central-ord1)****
* ****[**US West**](data-center-regions.md#us-west-las1)****

Each data center features redundant, **200Gbps+ public Internet connectivity** from Tier 1 global carriers, and are connected to each other with **400Gbps+ of dark fiber transport**, allowing for **easy,** **free data transfers** within CoreWeave Cloud.

{% hint style="info" %}
**Note**

To access and run the speedtests linked below in your terminal, either click the link to download them, or use `curl` on the link's URL.

For example:

```bash
curl http://http.speedtest.lga1.coreweave.com/1G --output /dev/null
```
{% endhint %}

CoreWeave's data center regions are:

## :cityscape: US East: `LGA1`

****:round\_pushpin:**Weehawken, NJ**

Located at the mouth of the Lincoln Tunnel, `LGA1` serves the Eastern US, and provides ultra-low latency to the NYC metropolitan area, covering **over 20 million people**. This **ISO 27001, SOC2 compliant** data center is packed with **NVIDIA GPU accelerated** Cloud Instances, with near-unlimited compute and storage infrastructure to go with it.

| Region Label | Speedtests                                                                                               | ICMP endpoint                       |
| ------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `LGA1`       | [1GB](http://http.speedtest.lga1.coreweave.com/1G), [10GB](http://http.speedtest.lga1.coreweave.com/10G) | `ping.speedtest.lga1.coreweave.com` |

## :baseball: US Central: `ORD1`

****:round\_pushpin:**Chicago, IL**

Located just outside downtown Chicago, `ORD1` serves the **Central US**. This **ISO 27001, SOC2, HIPAA** compliant data center is built for the most demanding workloads, including distributed training using **NVIDIA A100 NVLINK** accelerators connected with **Infiniband GPUDirect RDMA.**

| Region Label | Speedtests                                                                                               | ICMP endpoint                       |
| ------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `ORD1`       | [1GB](http://http.speedtest.ord1.coreweave.com/1G), [10GB](http://http.speedtest.ord1.coreweave.com/10G) | `ping.speedtest.ord1.coreweave.com` |

## :game\_die: US West: `LAS1`

****:round\_pushpin:**Las Vegas, NV**

Located in fabulous Las Vegas, `LAS1` serves the **Western US**. Powered by 100% renewable energy, LAS1's **ISO 27001, SOC2 and HIPAA** compliant infrastructure brings scaled **NVIDIA GPU** accelerated compute to the US West, serving both Las Vegas and the Los Angeles basin with low latency connectivity.

| Regional label | Speedtests                                                                                               | ICMP endpoint                       |
| -------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `LAS1`         | [1GB](http://http.speedtest.las1.coreweave.com/1G), [10GB](http://http.speedtest.las1.coreweave.com/10G) | `ping.speedtest.las1.coreweave.com` |

## Scheduling resources by region

It's easy to schedule your workloads, whether they be containerized micro-services or [Virtual Servers](broken-reference), in any of CoreWeave's data center regions.

To schedule a Virtual Server in a specific region, we've added an easy-to-use region selector on the [CoreWeave Cloud Virtual Server UI](https://cloud.coreweave.com/virtual-servers) when creating a new Virtual Server, which allows you to easily select the desired data center.

<figure><img src=".gitbook/assets/image (9) (4).png" alt="Data region selectors on CoreWeave Cloud UI"><figcaption><p>Data region selectors on CoreWeave Cloud UI</p></figcaption></figure>

To schedule resources in a specific region using the Kubernetes API, simply add an affinity such as the one shown below to your deployment or other deployable resources:

```yaml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/region
            operator: In
            values:
              - LGA1
```

## Availability and identifiers

The following tables describe which resources are available per data center region.

### GPU regional availability

| Resource Name        |         LGA1         |         ORD1         |         LAS1         |
| -------------------- | :------------------: | :------------------: | :------------------: |
| H100 80GB PCIe       | :white\_check\_mark: |      :no\_entry:     | :white\_check\_mark: |
| A100 80GB HGX NVLINK |      :no\_entry:     |      :no\_entry:     | :white\_check\_mark: |
| A100 40GB HGX NVLINK |      :no\_entry:     | :white\_check\_mark: |      :no\_entry:     |
| A100 80GB PCIe       |      :no\_entry:     | :white\_check\_mark: |      :no\_entry:     |
| A100 40GB PCIe       |      :no\_entry:     | :white\_check\_mark: |      :no\_entry:     |
| A40                  | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| RTX A6000            | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| RTX A5000            | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| RTX A4000            | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| Quadro RTX 5000      | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| Quadro RTX 4000      | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |

{% hint style="info" %}
H100 HGX and A100 HGX distributed training nodes are only available via CoreWeave Bare Metal Kubernetes. These node types are not offered as Virtual Servers to eliminiate any virtualization overhead.
{% endhint %}

### CPU regional availability

| Resource Name       |         LGA1         |         ORD1         |         LAS1         |
| ------------------- | :------------------: | :------------------: | :------------------: |
| amd-epyc-milan      | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| amd-epyc-rome       | :white\_check\_mark: | :white\_check\_mark: |      :no\_entry:     |
| intel-xeon-scalable | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| intel-xeon-v4       | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |
| intel-xeon-v3       | :white\_check\_mark: | :white\_check\_mark: | :white\_check\_mark: |

### Storage class names

The following table provides the storage class names, correspondent to each storage type, per data center.

{% hint style="info" %}
**Additional Resources**

[Learn more about Storage on CoreWeave Cloud.](storage/storage/)
{% endhint %}

| Storage Class |        LGA1        |        ORD1        |        LAS1        |
| ------------- | :----------------: | :----------------: | :----------------: |
| Block NVMe    |  `block-nvme-lga1` |  `block-nvme-ord1` |  `block-nvme-las1` |
| Shared NVMe   | `shared-nvme-lga1` | `shared-nvme-ord1` | `shared-nvme-las1` |
| Block HDD     |  `block-hdd-lga1`  |  `block-hdd-ord1`  |  `block-hdd-las1`  |
| Shared HDD    |  `shared-hdd-lga1` |  `shared-hdd-ord1` |  `shared-hdd-las1` |

### Public IP space

| IP Space Use    |            LGA1           |                                                  ORD1                                                  |                                 LAS1                                 |
| --------------- | :-----------------------: | :----------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------: |
| NAT Egress      |     `216.153.56.64/26`    |                                            `207.53.234.0/27`                                           | <p><code>216.153.48.0/27</code><br><code>216.153.55.64/26</code></p> |
| Public Range    |     `216.153.56.0/21`     | <p><code>216.153.50.0/23</code></p><p><code>216.153.52.0/23</code><br><code>207.53.234.0/24</code></p> |  <p><code>216.153.48.0/23</code><br><code>216.153.54.0/23</code></p> |
| Burstable Range |      `108.165.0.0/21`     |                                            `108.165.16.0/21`                                           |                           `108.165.8.0/21`                           |
| PTR Records     | `56.153.216.in-addr.arpa` |                                        `234.53.207.in-addr.arpa`                                       |                       `48.153.216.in-addr.arpa`                      |

## Security and compliance

Each of our data center regions provides different levels of security compliance. The table below describes the compliance and certification levels for each data center region.

| Certification or Attestation Name | LGA1                     | ORD1                     | LAS1                     |
| --------------------------------- | ------------------------ | ------------------------ | ------------------------ |
| **ISO 27001 Certificate (2021)**  | Yes :white\_check\_mark: | Yes :white\_check\_mark: | Yes :white\_check\_mark: |
| **Type 2 SOC 1**                  | Yes :white\_check\_mark: | Yes :white\_check\_mark: | Yes :white\_check\_mark: |
| **Type 2 SOC 2**                  | Yes :white\_check\_mark: | Yes :white\_check\_mark: | Yes :white\_check\_mark: |
| **HIPAA**                         | Yes :white\_check\_mark: | Yes :white\_check\_mark: | Yes :white\_check\_mark: |
| **HITRUST CSF Certification**     | No :x:                   | No :x:                   | Yes :white\_check\_mark: |
