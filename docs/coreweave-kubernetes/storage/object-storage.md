# Object Storage

## Object Storage

Object storage allows unstructured data to be stored and referenced via metadata associated with the data.

CoreWeave object storage is S3 compatible, and existing SDKs and libraries object for object storage are compatible. CoreWeave's object storage region is named `default`.

{% hint style="info" %}
**Note**

When using AWS SDKs, the variable `AWS_REGION` is defined within the V4 signature headers. The object storage region for CoreWeave is named `default`.
{% endhint %}

### Storage Classes

{% hint style="warning" %}
**Important**

Object storage is currently in beta. To configure object storage, [please contact support](https://cloud.coreweave.com/contact).
{% endhint %}

There are three designated storage classes for object storage formats, which correspond to regional object storage endpoints:

| Storage class          | Object storage endpoint   |
| ---------------------- | ------------------------- |
| `object-standard-ord1` | object.ord1.coreweave.com |
| `object-standard-las1` | object.las1.coreweave.com |
| `object-standard-lga1` | object.lga1.coreweave.com |

Each endpoint represents an independent, exclusive object store. This means that objects stored in `ORD1`buckets are not accessible from the `LAS1` region, and so on.

Once access has been granted to your account by the CoreWeave support team, you will receive configuration files such as the example file shown below. These config files are used to authenticate to object storage by using [the free `s3cmd` CLI tool](https://s3tools.org/s3cmd).

After `s3cmd` is installed, the configuration file can be placed in the home directory with the filename `.s3cfg` (e.g., `/home/.s3cfg`).

{% hint style="info" %}
**Note**

Configuration file paths may also be passed to `s3cmd` using the `-config=` option.
{% endhint %}

**Example config file**

```
[default]
access_key = 1K3R1P9903MEDQHZ71122
secret_key = fdsoie9FmSoXX2kOf6Ud0OFCQGw9323455sdfdssdae

host_base = s3.lga1.coreweave.com
host_bucket = s3.lga1.coreweave.com

# remove this if you configured SSL
check_ssl_certificate = True
check_ssl_hostname = True
```

**Example `s3cmd` usage:**

```
$ s3cmd mb s3://my-new-bucket
$ s3cmd put my-file.txt s3://my-new-bucket
$ s3cmd --config=my-cfg-file mb s3://my-new-bucket
$ s3cmd get s3://my-new-bucket/my-file.txt
```

Users can use any regional object storage endpoint and create and use buckets as they wish, but each region comes with its own quota limit. The default quota limit is 1TB of data per region.

{% hint style="info" %}
**Note**

Should you require an increase in your quota limit, [please contact support](https://cloud.coreweave.com/contact).&#x20;
{% endhint %}

## Object Storage Pricing

The current price for object storage is `$0.03` per GB per month.
