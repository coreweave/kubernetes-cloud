---
description: Learn about CoreWeave's S3 compatible Object Storage
---

# Object Storage

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

```ini
[default]
access_key = 1K3R1P9903MEDQHZ71122
secret_key = fdsoie9FmSoXX2kOf6Ud0OFCQGw9323455sdfdssdae

host_base = object.lga1.coreweave.com
host_bucket = object.lga1.coreweave.com

# remove this if you configured SSL
check_ssl_certificate = True
check_ssl_hostname = True
```

**Example `s3cmd` usage**

```bash
$ s3cmd mb s3://my-new-bucket
$ s3cmd put my-file.txt s3://my-new-bucket
$ s3cmd --config=my-cfg-file mb s3://my-new-bucket
$ s3cmd get s3://my-new-bucket/my-file.txt
```

Users can use any regional object storage endpoint and create and use buckets as they wish, but each region comes with its own quota limit. The default quota limit is 30TB of data per region.

{% hint style="info" %}
**Note**

Should you require an increase in your quota limit, [please contact support](https://cloud.coreweave.com/contact).&#x20;
{% endhint %}

### Server Side Encryption

**Server Side Encryption is implemented according to** [**AWS SSE-C standards**](https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)**.**

CoreWeave supports Server Side Encryption via customer-provided encryption keys. The client passes an encryption key along with each request to read or write encrypted data.

No modifications to your bucket need to be made to enable Server Side Encryption (SSE-C) - simply specify the required encryption headers in your requests.&#x20;

{% hint style="warning" %}
**Important**

It is the client’s responsibility to manage all keys, and to remember which key is used to encrypt each object.
{% endhint %}

### Specifying Server Side Encryption with customer-provided keys (SSE-C) <a href="#specifying-s3-c-encryption" id="specifying-s3-c-encryption"></a>

The following headers are utilized to specify SSE-C customizations.

| Name                                              | Description                                                                                                                                                                                                                                                                             |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `x-amz-server-side-encryption-customer-algorithm` | Use this header to specify the encryption algorithm. The header value must be `AES256`.                                                                                                                                                                                                 |
| `x-amz-server-side​-encryption​-customer-key`     | Use this header to provide the 256-bit, base64-encoded encryption key to encrypt or decrypt your data.                                                                                                                                                                                  |
| `x-amz-server-side​-encryption​-customer-key-MD5` | Use this header to provide the base64-encoded, 128-bit MD5 digest of the encryption key according to [RFC 1321](http://tools.ietf.org/html/rfc1321). This header is used for a message integrity check to ensure that the encryption key was transmitted without error or interference. |

## Object Storage Pricing

The current price for object storage is `$0.03` per GB per month.
