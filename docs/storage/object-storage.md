---
description: Learn about CoreWeave's S3 compatible Object Storage
---

# Object Storage

Coreweave Object Storage is an S3-compatible storage system that allows data to be stored and retrieved in a flexible and efficient way. CoreWeave Object Storage also supports multiple regions, allowing you to utilize regionally optimized clusters for your needs. Additionally, because Object Storage works over HTTP, any compatible S3 CLI tool or SDK integration may be used in tandem with Object Storage.

To get started with Object Storage, simply generate a key pair, download your credentials, and start managing your data!

{% hint style="info" %}
**Note**

When using AWS SDKs, the variable `AWS_REGION` is defined within the V4 signature headers. The object storage region for CoreWeave is named `default`.
{% endhint %}

## Storage classes

{% hint style="warning" %}
**Important**

Object storage is currently in beta. To configure object storage, [please contact support](https://cloud.coreweave.com/contact).
{% endhint %}

There are three designated storage classes for object storage formats, which correspond to regional object storage endpoints:

| Storage class          | Object storage endpoint     |
| ---------------------- | --------------------------- |
| `object-standard-ord1` | `object.ord1.coreweave.com` |
| `object-standard-las1` | `object.las1.coreweave.com` |
| `object-standard-lga1` | `object.lga1.coreweave.com` |

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

Users may use any regional Object Storage endpoint and create and use buckets as they wish, but each region comes with its own quota limit. The default quota limit is `30TB` of data per region.

{% hint style="info" %}
**Note**

Should you require an increase in your quota limit, [please contact support](https://cloud.coreweave.com/contact).&#x20;
{% endhint %}

## Server Side Encryption

**Server Side Encryption is implemented according to** [**AWS SSE-C standards**](https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)**.**

CoreWeave supports Server Side Encryption via customer-provided encryption keys. The client passes an encryption key along with each request to read or write encrypted data.

No modifications to your bucket need to be made to enable Server Side Encryption (SSE-C) - simply specify the required encryption headers in your requests.&#x20;

{% hint style="warning" %}
**Important**

It is the client’s responsibility to manage all keys, and to remember which key is used to encrypt each object.
{% endhint %}

### Using Server Side Encryption with customer-provided keys (SSE-C) <a href="#specifying-s3-c-encryption" id="specifying-s3-c-encryption"></a>

The following headers are utilized to specify SSE-C customizations.

| Name                                              | Description                                                                                                                                                                                                                                                                             |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `x-amz-server-side-encryption-customer-algorithm` | Use this header to specify the encryption algorithm. The header value must be `AES256`.                                                                                                                                                                                                 |
| `x-amz-server-side​-encryption​-customer-key`     | Use this header to provide the 256-bit, base64-encoded encryption key to encrypt or decrypt your data.                                                                                                                                                                                  |
| `x-amz-server-side​-encryption​-customer-key-MD5` | Use this header to provide the base64-encoded, 128-bit MD5 digest of the encryption key according to [RFC 1321](http://tools.ietf.org/html/rfc1321). This header is used for a message integrity check to ensure that the encryption key was transmitted without error or interference. |

#### Server Side Encryption Example

The following example demonstrates using an S3 tool to configure Server Side Encryption for Object Storage.

{% hint style="info" %}
**Note**

Because SSE with static keys is not supported by `s3cmd`at this time, [the AWS CLI tool](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) is used for this example. For a full explanation of the parameters used with the `s3` tool in this example, review [the AWS CLI `s3` documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3.html).
{% endhint %}

First, run `aws configure` to set up access and to configure your Secret Keys.

```bash
$ aws configure
```

Separately, generate a key using your preferred method. In this case, we use OpenSSL to print a new key to the file `sse.key`.

```bash
$ openssl rand 32 > sse.key
```

{% hint style="warning" %}
**Important**

The generated key must be 32 bytes in length.
{% endhint %}

Once the process of `aws configure` is complete and your new key has been configured for use, run the following `s3` commands to upload a file with Server Side Encryption.

```bash
$ aws s3 --endpoint-url=https://object.las1.coreweave.com \
    cp your-file.txt s3://your-bucket/your-file.txt \
    --sse-c-key=fileb://sse.key \
    --sse-c AES256
```

Finally, to retrieve the file, pass the path of the encryption key used (`sse-customer-key`) to `aws s3` to decrypt the file:

```bash
$ aws s3 --endpoint-url=https://object.las1.coreweave.com \
    cp s3://your-bucket/your-file.txt your-file.txt  \
    --sse-c-key=fileb://sse.key \
    --sse-c AES256
```

## Identity And Access Management (IAM)

When an initial key pair is created for object storage access, that key pair is considered a **Full User** with access to read, write, and modify policies of the buckets which it owns.

The categories of access that can be granted are:

1. **Read** - Gives access to only read from buckets you own and have created.
2. **Write** - Gives access to only write to buckets you own and have created.
3. **Write/Read** - Grants access to both read and write to buckets you own and have created.&#x20;
4. **Full control** - Grant Write/Read access, as well as admin access to create buckets and apply policies to buckets.

Each key pair is considered an individual user for access, and can be used to provide granular access to applications or users.

### IAM Actions

Currently, CoreWeave Cloud supports the following IAM bucket policy actions.&#x20;

<details>

<summary>Click to expand - Supported IAM Actions</summary>

* `s3:AbortMultipartUpload`
* `s3:CreateBucket`
* `s3:DeleteBucketPolicy`
* `s3:DeleteBucket`
* `s3:DeleteBucketWebsite`
* `s3:DeleteObject`
* `s3:DeleteObjectVersion`
* `s3:DeleteReplicationConfiguration`
* `s3:GetAccelerateConfiguration`
* `s3:GetBucketACL`
* `s3:GetBucketCORS`
* `s3:GetBucketLocation`
* `s3:GetBucketLogging`
* `s3:GetBucketNotification`
* `s3:GetBucketPolicy`
* `s3:GetBucketRequestPayment`
* `s3:GetBucketTagging`
* `s3:GetBucketVersioning`
* `s3:GetBucketWebsite`
* `s3:GetLifecycleConfiguration`
* `s3:GetObjectAcl`
* `s3:GetObject`
* `s3:GetObjectTorrent`
* `s3:GetObjectVersionAcl`
* `s3:GetObjectVersion`
* `s3:GetObjectVersionTorrent`
* `s3:GetReplicationConfiguration`
* `s3:ListAllMyBuckets`
* `s3:ListBucketMultipartUploads`
* `s3:ListBucket`
* `s3:ListBucketVersions`
* `s3:ListMultipartUploadParts`
* `s3:PutAccelerateConfiguration`
* `s3:PutBucketAcl`
* `s3:PutBucketCORS`
* `s3:PutBucketLogging`
* `s3:PutBucketNotification`
* `s3:PutBucketPolicy`
* `s3:PutBucketRequestPayment`
* `s3:PutBucketTagging`
* `s3:PutBucketVersioning`
* `s3:PutBucketWebsite`
* `s3:PutLifecycleConfiguration`
* `s3:PutObjectAcl`
* `s3:PutObject`
* `s3:PutObjectVersionAcl`
* `s3:PutReplicationConfiguration`
* `s3:RestoreObject`

</details>

{% hint style="warning" %}
**Important**

CoreWeave Cloud does not yet support setting policies on users, groups, or roles. Currently, account owners need to grant access directly to individual users. Granting an account access to a bucket grants access to all users in that account.
{% endhint %}

For all requests, the condition keys CoreWeave currently supports are:

* `aws:CurrentTime`
* `aws:EpochTime`
* `aws:PrincipalType`
* `aws:Referer`
* `aws:SecureTransport`
* `aws:SourceIpaws:UserAgent`
* `aws:username`

Certain S3 condition keys for bucket and object requests are also supported. In the following tables, `<perm>` may be replaced with either

* `read`
* `write/read-acp`
* or `write-acp/full-control`

for read, write/read, or full control access, respectively.

#### **Supported S3 Bucket Operations**

| `s3:createBucket`       | `s3:x-amz-acl`, `s3:x-amz-grant-<perm>` |
| ----------------------- | --------------------------------------- |
| `s3:ListBucket`         | `s3:<prefix>`                           |
| `s3:ListBucketVersions` | N/A                                     |
| `s3:delimiter`          | N/A                                     |
| `s3:max-keys`           | N/A                                     |
| `s3:PutBucketAcl`       | `s3:x-amz-acl s3:x-amz-grant-<perm>`    |

#### Supported S3 Object Operations

| `s3:PutObject`                                   | `s3:x-amz-acl` and `s3:x-amz-grant-<perm>`                                              |
| ------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `s3:x-amz-copy-source`                           | N/A                                                                                     |
| `s3:x-amz-server-side-encryption`                | N/A                                                                                     |
| `s3:x-amz-server-side-encryption-aws-kms-key-id` | N/A                                                                                     |
| `s3:x-amz-metadata-directive`                    | Use `PUT` and `COPY` to overwrite or preserve metadata in `COPY` requests, respectively |
| `s3:RequestObjectTag/<tag-key>`                  | N/A                                                                                     |
| `s3:PutObjectAcl`                                | `s3:x-amz-acl` and `s3-amz-grant-<perm>`                                                |
| `s3:PutObjectVersionAcl`                         | `s3:x-amz-acl` and `s3-amz-grant-<perm>`                                                |
| `s3:ExistingObjectTag/<tag-key>`                 | N/A                                                                                     |
| `s3:PutObjectTagging`                            | `s3:RequestObjectTag/<tag-key>`                                                         |
| `s3:PutObjectVersionTagging`                     | `s3:RequestObjectTag/<tag-key>`                                                         |
| `s3:ExistingObjectTag/<tag-key>`                 | N/A                                                                                     |
| `s3:GetObject`                                   | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:GetObjectVersion`                            | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:GetObjectAcl`                                | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:GetObjectVersionAcl`                         | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:GetObjectTagging`                            | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:GetObjectVersionTagging`                     | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:DeleteObjectTagging`                         | `s3:ExistingObjectTag/<tag-key>`                                                        |
| `s3:DeleteObjectVersionTagging`                  | `s3:ExistingObjectTag/<tag-key>`                                                        |

### Bucket policies

Another access control mechanism is [bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html), which are managed through standard S3 operations. A bucket policy may be set or deleted by using `s3cmd`, as shown below.\
\
In this example, a bucket policy is created to make the bucket downloads public:&#x20;

```bash
$ cat > examplepol
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::happybucket/*"
      ]
    }
  ]
}
```

The policy is then applied using `s3cmd setpolicy`:

```bash
$ s3cmd setpolicy examplepol s3://happybucket
```

Once the policy is applied, the data in your bucket may be accessed without credentials, for example, by using `curl`:

```
curl -v https://happybucket.object.las1.coreweave.com/my-new-file.txt
```

Finally, the policy is deleted using `s3cmd delpolicy`:

```bash
$ s3cmd delpolicy s3://happybucket
```

{% hint style="info" %}
**Note**

Bucket policies do not yet support string interpolation.
{% endhint %}

## Object Storage pricing

The current price for object storage is `$0.03` per GB per month.

## Custom Resources

CoreWeave provides [Kubernetes Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) for programmatic and automated methods of generating access to Object Storage clusters. In most cases, a single user can be used, but if you wish to have separate access credentials per system or user in your account, it is possible to generate multiple users who have read and write permissions granted, and then lock down storage buckets further by using a full access user.

### Permissions levels

* `full` - Grants full access to all buckets, including modification permissions for bucket policies
* `readwrite` - Grants read- and write-only access to all buckets
* `read` - Grants read-only access to all buckets
* `write` - Grants write access to all buckets

The following snippet creates a full-access user, however these permissions may be specified using the `readwrite`, `read`, and `write` options respectively.

### User CRD

The user CRD generates access to the object storage clusters. Each user is given both an access key and secret key, which are stored inside of a [secret](https://kubernetes.io/docs/concepts/configuration/secret/) in your namespace. Each secret is associated with the user, and is deleted when the user is deleted.

```yaml
apiVersion: objectstorage.coreweave.com/v1alpha1
kind: User
metadata:
  name: user-name
  namespace: your-namespace
spec:
  owner: your-namespace
  access: full # Options are full, readwrite, read, or write
```

### Accelerated Object Storage

CoreWeave also offers Accelerated Object Storage, a series of Anycasted NVMe-backed storage caches that provide blazing fast download speeds. Accelerated Object Storage is best suited for frequently accessed data that doesn't change often, such as model weights and training data.&#x20;

One of the biggest advantages of Anycasted Object Storage Caches is that data can be pulled from across data center regions, then be cached in the data center in which your workloads are located. For example, if your models are hosted in `ORD1` (Chicago), but have a deployment scale to all regions (`ORD1`, `LAS1`, `LGA1`), our accelerated caching solution will route to the nearest cache, then determine to pull the data from `ORD1` so that it is located in the same region as your workloads. This drastically reduces spin up times for workloads where scaling is a concern.

Use of CoreWeave's Accelerated Object Storage is completely free. To use Accelerated Object Storage, simply modify your Object Storage endpoint to one of the addresses that corresponds to your Data Center region.

| Region | Endpoint                          |
| ------ | --------------------------------- |
| LAS1   | `accel-object.las1.coreweave.com` |
| LGA1   | `accel-object.lga1.corewaeve.com` |
| ORD1   | `accel-object.ord1.coreweave.com` |

