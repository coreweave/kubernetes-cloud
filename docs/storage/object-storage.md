---
description: >-
  Use CoreWeave's S3-compatible Object Storage for flexible and efficient data
  storage
---

# Object Storage

Coreweave Object Storage is an S3-compatible storage system that allows data to be stored and retrieved in a flexible and efficient way.

CoreWeave's Object Storage features include:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><p><span data-gb-custom-inline data-tag="emoji" data-code="1f30e">🌎</span> <strong>Multi-region support</strong></p><p></p><p>CoreWeave Object Storage also supports multiple regions, allowing you to utilize regionally optimized clusters for your needs.</p></td><td></td><td></td></tr><tr><td><p><span data-gb-custom-inline data-tag="emoji" data-code="2699">⚙</span> <strong>Easy SDK integrations</strong></p><p></p><p>Because Object Storage works over HTTP, any compatible S3 CLI tool or SDK integration may be used in tandem with Object Storage.</p></td><td></td><td></td></tr><tr><td><p><span data-gb-custom-inline data-tag="emoji" data-code="2728">✨</span> <strong>Simple setup</strong></p><p></p><p>To get started with Object Storage, simply generate a key pair, download your credentials, and start managing your data! </p></td><td></td><td></td></tr><tr><td><span data-gb-custom-inline data-tag="emoji" data-code="26a1">⚡</span> <a href="object-storage.md#accelerated-object-storage"><strong>Accelerated Object Storage</strong></a></td><td>Accelerated Object Storage offers a series of anycasted NVMe-backed storage caches that provide blazing fast download speeds. Best suited for data such as model weights and training data.</td><td></td></tr></tbody></table>

## Get started

Currently, Object Storage is configured and accessed either by:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><p><a href="object-storage.md#the-user-crd"><strong>User CRDs</strong></a></p><p></p><p>Use CoreWeave's Kubernetes <a href="object-storage.md#the-user-crd">Custom Resource Definitions (CRD) for Users </a>to create a Custom Resource with the appropriate permissions.</p></td><td></td><td></td><td></td></tr><tr><td><p><a href="object-storage.md#using-the-cloud-ui-and-s3cmd"><strong>Cloud UI</strong></a></p><p></p><p>Use the <a href="object-storage.md#using-the-cloud-ui-and-s3cmd">CoreWeave Cloud UI </a>to generate a config file, which is then manually passed to <code>s3cmd</code> to authenticate to Object Storage.</p></td><td></td><td></td><td></td></tr></tbody></table>

## Using the Cloud UI and s3cmd

Using the CoreWeave Cloud UI, an Object Storage configuration file can be generated to authenticate to Object Storage using `s3cmd`. To access Object Storage using the [CoreWeave Cloud UI](../../virtual-servers/deployment-methods/coreweave-apps.md), log in to your CoreWeave Cloud account, then navigate to the Object Storage page.

<figure><img src="../.gitbook/assets/image (9) (2) (2).png" alt="Screenshot of the Object Storage link on the side nav of the Cloud UI"><figcaption><p>The Object Storage link is located on the left-hand menu on the Cloud UI</p></figcaption></figure>

To create a new token, click the button labelled **Create a New Token**. This will bring up the **New Storage Token** modal, which prompts you to assign a name, a default [S3 region](../data-center-regions.md) (which can be changed later), and [an access level](object-storage.md#identity-and-access-management-iam-and-access-levels) to the token.

<figure><img src="../.gitbook/assets/image (52) (1).png" alt="Screenshot of the new storage token modal"><figcaption><p>The New Storage Token modal</p></figcaption></figure>

Finally, clicking the **Generate** button generates the token's configuration file:

```ini
[default]
access_key = <redacted>
secret_key = <redacted>
# The region for the host_bucket and host_base must be the same.
host_base = object.lga1.coreweave.com
host_bucket = %(bucket)s.object.lga1.coreweave.com
check_ssl_certificate = True
check_ssl_hostname = True
```

This generated config file is used to authenticate to Object Storage by using [the free `s3cmd` CLI tool](https://s3tools.org/s3cmd).

### Authentication

After the `s3cmd` tool is installed, place the configuration file generated previously in the home directory with the filename `.s3cfg` (for example: `/home/myuser/.s3cfg`). The `s3cmd` tool looks for the config file at this path by default, but other filepaths may alternatively be passed directly to `s3cmd` using the `-config=` option.

**Example `s3cmd` usage**

Make a bucket

```
s3cmd mb s3://BUCKET
```

Remove a bucket

```
s3cmd rb s3://BUCKET
```

List the object inside a bucket

```
s3cmd ls [s3://BUCKET[/PREFIX]]
```

A list of all s3cmd commands may be found in [the s3cmd official documentation](https://s3tools.org/usage#commands).

{% hint style="info" %}
**Note**

When using AWS SDKs, the variable `AWS_REGION` is defined within the V4 signature headers. The object storage region for CoreWeave is named `default`.
{% endhint %}

## Using Custom Resource Definitions (CRDs)

CoreWeave provides [Kubernetes Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) for programmatic and automated methods of generating access to Object Storage clusters.

In most cases, a single user can be used, but if you wish to have separate access credentials per system or user in your account, it is possible to generate multiple users who have read and write permissions granted, then lock down storage buckets further by using a full access user.

### The user CRD

The user CRD generates access to the Object Storage clusters. Each user is given both an **access key** and a **secret key**, which are stored inside of a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) in your namespace. Each secret is associated with the user, and is deleted when the user is deleted.

Here is an example CRD for creating a user with the permission level `full`:

```yaml
apiVersion: objectstorage.coreweave.com/v1alpha1
kind: User
metadata:
  name: user-name
  namespace: your-namespace
spec:
  owner: your-namespace
  access: full # Possible options are: full, readwrite, read, or write
```

## Storage classes

There are three designated storage classes for Object Storage formats, which correspond to regional Object Storage endpoints:

| Storage class          | Object Storage endpoint     |
| ---------------------- | --------------------------- |
| `object-standard-ord1` | `object.ord1.coreweave.com` |
| `object-standard-las1` | `object.las1.coreweave.com` |
| `object-standard-lga1` | `object.lga1.coreweave.com` |

Each endpoint represents an independent, exclusive object store. This means that objects stored in `ORD1`buckets are not accessible from the `LAS1` region, and so on.

Users may use any regional Object Storage endpoint and create and use buckets as they wish, but each region comes with its own quota limit. The default quota limit is `30TB` of data per region.

{% hint style="info" %}
**Note**

Should you require an increase in your quota limit, [please contact support](https://cloud.coreweave.com/contact).&#x20;
{% endhint %}

## Server Side Encryption

{% hint style="info" %}
**Note**

Server Side Encryption is implemented according to [AWS SSE-C standards](https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html).
{% endhint %}

CoreWeave supports Server Side Encryption via customer-provided encryption keys. The client passes an encryption key along with each request to read or write encrypted data. No modifications to your bucket need to be made to enable Server Side Encryption (SSE-C); simply specify [the required encryption headers](object-storage.md#specifying-s3-c-encryption) in your requests.

{% hint style="warning" %}
**Important**

It is the client’s responsibility to manage all keys, and to remember which key is used to encrypt each object.
{% endhint %}

### SSE with customer-provided keys (SSE-C) <a href="#specifying-s3-c-encryption" id="specifying-s3-c-encryption"></a>

The following headers are utilized to specify SSE-C customizations.

| Name                                              | Description                                                                                                                                                                                                                                                                             |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `x-amz-server-side-encryption-customer-algorithm` | Use this header to specify the encryption algorithm. The header value must be `AES256`.                                                                                                                                                                                                 |
| `x-amz-server-side​-encryption​-customer-key`     | Use this header to provide the 256-bit, base64-encoded encryption key to encrypt or decrypt your data.                                                                                                                                                                                  |
| `x-amz-server-side​-encryption​-customer-key-MD5` | Use this header to provide the base64-encoded, 128-bit MD5 digest of the encryption key according to [RFC 1321](http://tools.ietf.org/html/rfc1321). This header is used for a message integrity check to ensure that the encryption key was transmitted without error or interference. |

#### Server Side Encryption example

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

## Identity and Access Management (IAM) and access levels

When an initial key pair is created for Object Storage access, that key pair is given the permissions specified on creation in order to read, write, and modify policies of the buckets which it owns. Each key pair is considered an individual user for access, and can be used to provide granular access to applications or users.

Permission levels that may be granted are:

| Permission level | CRD key     | Description                                                                                      |
| ---------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| Read             | `read`      | Gives access to only read from buckets you own and have created                                  |
| Write            | `write`     | Gives access to only write to buckets you own and have created                                   |
| Read/Write       | `readwrite` | Grants access to both read and write to buckets you own and have created                         |
| Full             | `full`      | Grant Write/Read access, as well as admin access to create buckets and apply policies to buckets |

### Access levels via Cloud UI

Alternatively, key pair permissions may be specified via the Cloud UI on the Object Storage page.

From the Object Storage page, the **Access Level** field displays the key's current access level. The access of a new Object Storage token is set during creation by selecting an access level from the **Select an access level** drop-down menu located at the bottom of the New Storage Token module.

<figure><img src="../.gitbook/assets/image (4) (5).png" alt=""><figcaption><p>Access levels are displayed on the Object Storage page</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (3).png" alt="Screenshot: Access levels drop-down"><figcaption><p>Any access level may be chosen from this drop-down</p></figcaption></figure>

### IAM actions

Currently, CoreWeave Cloud supports the following IAM bucket policy actions:

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

Certain S3 condition keys for bucket and object requests are also supported. In the following tables, `<perm>` may be replaced with

* `read`
* `write/read-acp`
* or `write-acp/full-control`

for read, write/read, or full control access, respectively.

#### **Supported S3 Bucket Operations**

| Permission              | Condition Keys                          |
| ----------------------- | --------------------------------------- |
| `s3:createBucket`       | `s3:x-amz-acl`, `s3:x-amz-grant-<perm>` |
| `s3:ListBucket`         | `s3:<prefix>`                           |
| `s3:ListBucketVersions` | N/A                                     |
| `s3:delimiter`          | N/A                                     |
| `s3:max-keys`           | N/A                                     |
| `s3:PutBucketAcl`       | `s3:x-amz-acl s3:x-amz-grant-<perm>`    |

#### Supported S3 Object Operations

| Permission                                       | Condition Keys                                                                          |
| ------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `s3:PutObject`                                   | `s3:x-amz-acl` and `s3:x-amz-grant-<perm>`                                              |
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

```bash
$ curl -v https://happybucket.object.las1.coreweave.com/my-new-file.txt
```

Finally, the policy is deleted using `s3cmd delpolicy`:

```bash
$ s3cmd delpolicy s3://happybucket
```

{% hint style="info" %}
**Note**

Bucket policies do not yet support string interpolation.
{% endhint %}

## Accelerated Object Storage

CoreWeave also offers Accelerated Object Storage, a series of Anycasted NVMe-backed storage caches that provide blazing fast download speeds. Accelerated Object Storage is best suited for frequently accessed data that doesn't change often, such as model weights and training data.&#x20;

One of the biggest advantages of Anycasted Object Storage Caches is that data can be pulled from across data center regions, then be cached in the data center in which your workloads are located.

For example, if your models are hosted in `ORD1` (Chicago), but have a deployment scale to all regions (`ORD1`, `LAS1`, `LGA1`), your call to `https://accel-object.ord1.coreweave.com` will be routed to a cache located closest to the workload - that is to say, if you are calling from `LGA1`, it will hit the cache in `LGA1`; if you are calling from `LAS1`, it will hit the cache in `LAS1`. This drastically reduces spin up times for workloads where scaling is a concern.

{% hint style="info" %}
**Note**

You do not need to change the endpoint for every region your application is deployed in - this is the beauty of it!
{% endhint %}

**Use of CoreWeave's Accelerated Object Storage is available at no additional cost.** To use Accelerated Object Storage, simply modify your Object Storage endpoint to one of the addresses that corresponds to your Data Center region.

| Region | Endpoint                          |
| ------ | --------------------------------- |
| LAS1   | `accel-object.las1.coreweave.com` |
| LGA1   | `accel-object.lga1.coreweave.com` |
| ORD1   | `accel-object.ord1.coreweave.com` |

## s3cmd alternatives

There are a few alternative clients to s3cmd, one of which is [s5cmd](https://github.com/peak/s5cmd). s5cmd is an interface ideal for running highly parallelized operations. As benchmarks have shown, s5cmd performs very well for tasks that involve moving large numbers of files to and from buckets.&#x20;

To use s5cmd with CoreWeave Object Storage, first create a file at `~/.aws/credentials` that contains the following parameters:

```toml
[default]
aws_access_key_id=<Your object storage access key>
aws_secret_access_key=<Your object storage secret key>
```

To use s5cmd with CoreWeave Object Storage, the `--endpoint-url` option must be included during use to specify the CoreWeave Object Storage endpoint URL:

```bash
--endpoint-url=https://object.lga1.coreweave.com
```

It may be helpful to define an `alias` so as to avoid providing the endpoint URL every time.&#x20;

```bash
$ alias s5="s5cmd --endpoint-url https://object.lga1.coreweave.com"
```

Once the `~/.aws/credentials` file above is in place, run s5cmd. The full command, without an alias, looks like:

{% code overflow="wrap" %}
```bash
$ s5cmd --endpoint-url=https://object.lga1.coreweave.com cp ./my-local-directory/* s3://my-bucket/my-prefix/
```
{% endcode %}

{% hint style="info" %}
**Note**

With extremely large filesystems ( >1 million files) s5cmd may exhibit unwanted behavior.  In these cases, reducing concurrency using the `--concurrency` option, or selecting standard endpoints instead of accelerated endpoints, may help.
{% endhint %}

## Pricing

The current price for Object Storage is `$0.03` per GB per month.
