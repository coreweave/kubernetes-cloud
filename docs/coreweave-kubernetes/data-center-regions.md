---
description: Learn about CoreWeave's data center regions
---

# Data Center Regions

CoreWeave Cloud is served from **three geographically diverse regions** in the United States. Located directly adjacent to large metropolitan population centers, CoreWeave's data centers provide low latency access to accelerated compute to **over 51 million people**.

Our data centers are broken up into three geographical buckets, each of which service the regions for which they're named:

* [**US East**](data-center-regions.md#us-east-lga1)
* [**US Central**](data-center-regions.md#us-central-ord1)
* [**US West**](data-center-regions.md#us-west-las1)

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

:round\_pushpin:**Weehawken, NJ**

Located at the mouth of the Lincoln Tunnel, `LGA1` serves the Eastern US, and provides ultra-low latency to the NYC metropolitan area, covering **over 20 million people**. This **ISO 27001, SOC2 compliant** data center is packed with **NVIDIA GPU accelerated** Cloud Instances, with near-unlimited compute and storage infrastructure to go with it.

<table><thead><tr><th width="216">Region Label</th><th width="153">Speedtests</th><th>ICMP endpoint</th></tr></thead><tbody><tr><td><code>LGA1</code></td><td><a href="http://http.speedtest.lga1.coreweave.com/1G">1GB</a>, <a href="http://http.speedtest.lga1.coreweave.com/10G">10GB</a></td><td><code>ping.speedtest.lga1.coreweave.com</code></td></tr></tbody></table>

## :baseball: US Central: `ORD1`

:round\_pushpin:**Chicago, IL**

Located just outside downtown Chicago, `ORD1` serves the **Central US**. This **ISO 27001, SOC2, HIPAA** compliant data center is built for the most demanding workloads, including distributed training using **NVIDIA A100 NVLINK** accelerators connected with **Infiniband GPUDirect RDMA.**

<table><thead><tr><th width="209">Region Label</th><th width="151">Speedtests</th><th>ICMP endpoint</th></tr></thead><tbody><tr><td><code>ORD1</code></td><td><a href="http://http.speedtest.ord1.coreweave.com/1G">1GB</a>, <a href="http://http.speedtest.ord1.coreweave.com/10G">10GB</a></td><td><code>ping.speedtest.ord1.coreweave.com</code></td></tr></tbody></table>

## :game\_die: US West: `LAS1`

:round\_pushpin:**Las Vegas, NV**

Located in fabulous Las Vegas, `LAS1` serves the **Western US**. Powered by 100% renewable energy, LAS1's **ISO 27001, SOC2 and HIPAA** compliant infrastructure brings scaled **NVIDIA GPU** accelerated compute to the US West, serving both Las Vegas and the Los Angeles basin with low latency connectivity.

<table><thead><tr><th width="184">Regional label</th><th width="166">Speedtests</th><th>ICMP endpoint</th></tr></thead><tbody><tr><td><code>LAS1</code></td><td><a href="http://http.speedtest.las1.coreweave.com/1G">1GB</a>, <a href="http://http.speedtest.las1.coreweave.com/10G">10GB</a></td><td><code>ping.speedtest.las1.coreweave.com</code></td></tr></tbody></table>

## Scheduling resources by region

It's easy to schedule your workloads, whether they be containerized micro-services or [Virtual Servers](broken-reference), in any of CoreWeave's data center regions.

To schedule a Virtual Server in a specific region, we've added an easy-to-use region selector on the [CoreWeave Cloud Virtual Server UI](https://cloud.coreweave.com/virtual-servers) when creating a new Virtual Server, which allows you to easily select the desired data center.

<figure><img src="../.gitbook/assets/image (9) (4) (1).png" alt="Data region selectors on CoreWeave Cloud UI"><figcaption><p>Data region selectors on CoreWeave Cloud UI</p></figcaption></figure>

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

The following tables describe which resources are hosted in which data center region.

{% hint style="warning" %}
**Important**

The table below does not list current availability, only which types of resources are currently hosted in which regions.
{% endhint %}

### GPU regional availability

<table><thead><tr><th width="249.92264643628386">Resource Name</th><th align="center">LGA1</th><th align="center">ORD1</th><th align="center">LAS1</th></tr></thead><tbody><tr><td>A100 PCIe 40GB</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr><tr><td>A100 PCIe 80GB</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr><tr><td>A100 HGX NVLINK 40GB</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr><tr><td>A100 HGX NVLINK 80GB</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>A40</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>H100 80GB PCIe</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>H100 80GB HGX NVLINK</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>Quadro RTX 4000</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>Quadro RTX 5000</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>RTX A4000</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr><tr><td>RTX A5000</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>RTX A6000</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>

{% hint style="info" %}
**Note**

H100 HGX and A100 HGX distributed training nodes are only available via CoreWeave Bare Metal Kubernetes. These node types are not offered as Virtual Servers to eliminiate any virtualization overhead.
{% endhint %}

### CPU regional availability

<table><thead><tr><th width="223.92264643628386">Resource Name</th><th width="150.66384016610132" align="center">LGA1</th><th width="158.34547674174956" align="center">ORD1</th><th align="center">LAS1</th></tr></thead><tbody><tr><td>amd-epyc-milan</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>amd-epyc-rome</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr><tr><td>intel-xeon-scalable</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>intel-xeon-v4</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>intel-xeon-v3</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="26d4">⛔</span></td></tr></tbody></table>

### Storage class names

The following table provides the storage class names, correspondent to each storage type, per data center.

{% hint style="info" %}
**Additional Resources**

[Learn more about Storage on CoreWeave Cloud.](../storage/storage/)
{% endhint %}

<table><thead><tr><th width="127.18821327831549">Storage Class</th><th width="212" align="center">LGA1</th><th width="206.14289554743957" align="center">ORD1</th><th align="center">LAS1</th></tr></thead><tbody><tr><td>Block NVMe</td><td align="center"><code>block-nvme-lga1</code></td><td align="center"><code>block-nvme-ord1</code></td><td align="center"><code>block-nvme-las1</code></td></tr><tr><td>Shared NVMe</td><td align="center"><code>shared-nvme-lga1</code></td><td align="center"><code>shared-nvme-ord1</code></td><td align="center"><code>shared-nvme-las1</code></td></tr><tr><td>Block HDD</td><td align="center"><code>block-hdd-lga1</code></td><td align="center"><code>block-hdd-ord1</code></td><td align="center"><code>block-hdd-las1</code></td></tr><tr><td>Shared HDD</td><td align="center"><code>shared-hdd-lga1</code></td><td align="center"><code>shared-hdd-ord1</code></td><td align="center"><code>shared-hdd-las1</code></td></tr></tbody></table>

### Public IP space

<table><thead><tr><th width="129.1882132783155">IP Space Use</th><th width="200" align="center">LGA1</th><th width="213.14289554743957" align="center">ORD1</th><th align="center">LAS1</th></tr></thead><tbody><tr><td>NAT Egress</td><td align="center"><code>216.153.56.64/26</code></td><td align="center"><code>207.53.234.0/27</code></td><td align="center"><code>216.153.55.64/26</code></td></tr><tr><td>Public Range</td><td align="center"><code>216.153.56.0/21</code></td><td align="center"><p><code>216.153.50.0/23</code></p><p><code>216.153.52.0/23</code><br><code>207.53.234.0/24</code></p></td><td align="center"><code>216.153.48.0/23</code><br><code>216.153.54.0/23</code></td></tr><tr><td>Burstable Range</td><td align="center"><code>108.165.0.0/21</code></td><td align="center"><code>108.165.16.0/21</code></td><td align="center"><code>108.165.8.0/21</code></td></tr><tr><td>PTR Records</td><td align="center"><code>56.153.216.in-addr.arpa</code></td><td align="center"><code>234.53.207.in-addr.arpa</code></td><td align="center"><code>48.153.216.in-addr.arpa</code></td></tr></tbody></table>

## Security and compliance

Each of our data center regions provides different levels of security compliance. The table below describes the compliance and certification levels for each data center region.

<table><thead><tr><th width="327">Certification or Attestation Name</th><th width="128">LGA1</th><th width="119">ORD1</th><th>LAS1</th></tr></thead><tbody><tr><td><strong>ISO 27001 Certificate (2021)</strong></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><strong>Type 2 SOC 1</strong></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><strong>Type 2 SOC 2</strong></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><strong>HIPAA</strong></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><strong>HITRUST CSF Certification</strong></td><td>No <span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td>No <span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td>Yes <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>
