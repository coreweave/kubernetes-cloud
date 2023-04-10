---
description: Learn how to deploy a managed Thinkbox Deadline instance
---

# Managed Thinkbox Deadline

[Thinkbox Deadline](https://docs.thinkboxsoftware.com/products/deadline/10.1/1\_User%20Manual/manual/overview.html) is an industry-standard render management platform. CoreWeave provides a fully managed implementation of Deadline, including all of its necessary components, delivered as a service to clients working in VFX and rendering who require quick setup, zero management, and automatic, limitless scalability.

CoreWeave deploys Deadline through a [Kubernetes Helm Chart](https://helm.sh/), in order to leverage templating for reconfiguring multistage Kubernetes deployments, and to provide unique configurability to Deadline users.

Most of the work required by CoreWeave users who wish to deploy Deadline instances is to simply provide the information specific to their individual pipelines; everything else is managed automatically behind the scenes.

The CoreWeave implementation of Deadline is delivered as a "High Availability Service" via Kubernetes - every component of Deadline is replicated, redundant, and containerized. This makes your Deadline deployments faster, more durable, and more scalable than ever.

{% hint style="info" %}
**Note**

Containerization comes at the cost of needing to convert existing Deadline Worker images. In this document, we provide the names of a few images you can pull today.

If you are interested in seeing examples of Dockerfiles used in the process of building and configuring Deadline Worker groups, [reach out to your CoreWeave support specialist](https://cloud.coreweave.com/contact).
{% endhint %}

## Deploy the Deadline application

There are two ways to deploy Thinkbox Deadline on CoreWeave<mark style="color:green;">**:**</mark>

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Fully Managed </strong><mark style="color:green;"><strong>(Recommended)</strong></mark></td><td>We deploy the repository and all related components entirely on CoreWeave Cloud.</td><td></td></tr><tr><td><strong>Workers-Only</strong></td><td>We deploy autoscaled deadline workers on CoreWeave, which connect to an on-premise Deadline repository.</td><td></td></tr></tbody></table>

This guide provides walkthroughs for deploying based on either method.

{% hint style="info" %}
**Note**

This guide assumes that you already have some familiarity with Deadline, if not consider checking out [the official Thinkbox documentation](https://docs.thinkboxsoftware.com/).
{% endhint %}

### Installing Deadline

To get started deploying your Deadline repository and Workers on CoreWeave Cloud, first [log in to your CoreWeave Cloud dashboard](https://cloud.coreweave.com), then navigate to [the application Catalog](https://apps.coreweave.com) from the menu on the left.

From the Catalog, search for `deadline` , then select it from the list of available applications. Click the **Deploy** button in the upper right-hand corner. This will open the Helm YAML configuration screen as shown below.

{% hint style="info" %}
**Note**

Your `version` may differ from what is shown in this example.
{% endhint %}

![An example of the default YAML configuration for an instance of Thinkbox Deadline](<../../.gitbook/assets/image (156).png>)

The Helm values given are default values for deploying the Deadline chart. If you're interested in seeing what configuration options are available to you, look this chart over; however, for this example, we are going to remove the default configurations entirely by deleting all the contents of this box, so as to begin from the beginning.

First, to make things simpler, we will split our configuration into two sections:

1. **Initialization:** These values will adjust versions, connectivity, authentication, and enable/disable deadline components.
2. **Workers:** These values will allow us to define our Deadline workers and configure autoscaling.

## Initialization

To begin, we should specify the version of Deadline that we would like to deploy.

**CoreWeave's currently supported versions are:**

* `10.1.9.2`
* `10.1.10.6`
* `10.0.24.4`
* `10.1.11.5`
* `10.1.6.4`
* `10.1.12.1`
* `10.1.13.2`
* `10.1.15.2`
* `10.1.17.4`
* `10.1.18.5`

{% hint style="info" %}
**Note**

If you require a version outside of this list, feel free to [reach out to your CoreWeave support specialist](https://cloud.coreweave.com/contact).
{% endhint %}

To specify the repository version we would like to deploy, we simply specify the version number in the `version` field, e.g.:

```
version: 10.1.18.5
```

{% hint style="info" %}
**For Workers-Only**

If you plan on deploying **Workers only**, add the following on a new line to the chart:

```
repository:
    remoteRepository:
        host: <ON-PREM HOST OR CL FORWARDS>
        port: <REPOSITORY PORT>
        auth:
          certSecret:
            name: <SECRET NAME>
          password: temp123
```

Edit the values to represent the connection details to your on-premises Deadline repository. If your repository is not accessible over a public IP, consider first setting up [Cloudlink](on-premise-integration/linux.md) to proxy your connections through.

Once ready, run `kubectl get services` and look for the Cloudlink `forwards` Service. Use the external IP of that Service as the value of `host` in your YAML file.
{% endhint %}

### **TLS certificates**

For either deployment method, if your on-premises repository utilizes TLS certificates, you will need to create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing that certificate:

```bash
$ kubectl create secret generic <secret name> --from-file=<local full path to certificate file>
```

Finally, specify the password used to decode the certificate in the `password` field of the YAML chart.

If you are deploying the **full repository**, specify:

```
rcs:
  pass: <CERTIFICATE PASSWORD>
```

We will automatically generate a Deadline certificate for your repository. This value will allow you to specify the password used to decode the generated certificate.

#### License forwarding

To enable license forwarding, include the following fields in your manifest:

```
licenseForwarder:
  enabled: true
  auth:
    secrets:
      name: <SECRET NAME>
```

This will enable a license forwarder for utilizing Thinkbox UBL. To authenticate your marketplace license allocations, you will need to create a Secret containing your certificates from the thinkbox marketplace using the following command:

```bash
$ kubectl create secret generic <secret name> --from-file=<local full path to directory containing all certificates>
```

#### Example manifetss

If you have been following along up to this point, your YAML manifests should look like one of the following, depending on which deployment style you have chosen.

{% tabs %}
{% tab title="Fully Managed" %}
If you are utilizing the **Fully Managed** method, your YAML manifest should look something like the following.

```yaml
version: 10.1.18.5
rcs:
  pass: password123
 licenseForwarder:
  enabled: true
  auth:
    secrets:
      name: ubl-certificates
```
{% endtab %}

{% tab title="Workers-Only" %}
If you are utilizing the **Workers Only** method, your YAML manifest should look something like the following.

```yaml
version: 10.1.18.5
repository:
    remoteRepository:
        host: 127.0.0.1
        port: 4433
        auth:
          certSecret:
            name: on-prem-cert
          password: password123
 licenseForwarder:
  enabled: true
  auth:
    secrets:
      name: ubl-certificates
```
{% endtab %}
{% endtabs %}

## Workers

In order for Deadline workers to spin up, we will need to specify in our YAML file which Docker images we will use to render each type of job, what kind of hardware we would like to use for those workers, as well as how we would like to scale compute power for jobs in our repository.

A Worker definition might look something like the following:

<details>

<summary><strong>Click to expand - Workers example</strong></summary>

```yaml
workers:
- name: maya-epyc
    enabled: true
    groups:
      - maya-epyc
      - maya
    pools:
      - vfx
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

</details>

### Understanding the Worker definition

#### `enabled`

The `enabled` field allows for quickly enabling and disabling different Worker types during upgrades, without ever removing them from your application. In this example, it is set to `true`.

#### `groups` and `pools`

The next values define the list of `groups` and `pools` in which we would like our Workers to be assigned. During initialization, Workers will attempt to join these `pools` and `groups`; if they do not exist, they will attempt to create them.

```
groups:
  - maya-epyc
  - maya
pools:
  - vfx
```

#### Scaling

```
scale:
  pollingNames:
  - name: maya-epyc
    type: Group
  minReplicas: 0
  maxReplicas: 100
  scalingFactor: 1
```

Scaling (`scale`) specifies how we would like our Workers to scale in response to the jobs submitted to the repository.

#### `scale.pollingNames`

`scale.pollingNames` defines which tasks should be monitored to scale up and down. In the example above, we specify that we would like to scale based off of the number of tasks submitted to the Deadline group `maya-epyc`, which is the same group that our Workers will join.

{% hint style="info" %}
**Note**

If you do not specify any polling names (`pollingNames`), your Worker will automatically create a limit with the same name as your Worker `group`, then scale based off that limit.
{% endhint %}

Other default options for the `type` field are `User` and `Pool`. Custom polling types are possible, allowing you to scale based on any job association, including tags.

{% hint style="info" %}
**Note**

For more information on Custom polling types, [reach out to a support specialist](https://cloud.coreweave.com/contact).
{% endhint %}

#### **`scale.minReplicas` and `scale.maxReplicas`**

Scaling limits for this Worker type may be configured using limits inside of Deadline, but for now, `minReplicas` and `maxReplicas` may be configured as a backstop. This way, if the Deadline limits are accidentally modified incorrectly, we will never exceed the maximum or go below the minimum number of deadline Workers of this type.

Finally, `scalingFactor` allows us to add an overall multiplier to scaling. For example, a `scalingFactor` of .`5` would mean that for every `2` tasks submitted to the queue, we would spin up `1` Worker. For most use cases, this value can remain at `1`.

### Worker Dockerfile

Next, we configure the Docker images for our Worker. A Worker's Dockerfile will look something like the following:

```
image: registry.gitlab.com/coreweave/render-images/maya2022:1
imagePullSecrets: 
- name: render-images
```

In this example, we provide a base `maya2020` Worker image, which you can pull to test as well. However, in order to use this image, you will first need to create an `imagePullSecret`.

To create the necessary credentials, run the following command:

```bash
$ kubectl create secret docker-registry render-images \
 --docker-username render-images --docker-password "rJX7s8EjsD8UmD6-73yc" \
 --docker-server registry.gitlab.com/coreweave/render-images
```

{% hint style="info" %}
**Note**

The `imagePullSecret` value defined in the Worker definitions can accept multiple pull secrets if necessary or convenient.
{% endhint %}

Next, we can add environment variables to be initialized in the containers on startup. This is a convenient way to provide environment variables such as license settings.

```
env:
  - name: ARNOLD_LICENSE_ORDER
    value: network
  - name: ADSKFLEX_LICENSE_FILE
    value: 127.0.0.1
```

The following `affinity` field allows us to choose where and on [what kind of hardware](../../../coreweave-kubernetes/node-types.md) our Deadline workers run on.

{% hint style="info" %}
**Additional Resources**

[Read more about the high-performance hardware options available on CoreWeave Cloud.](../../../coreweave-kubernetes/node-types.md)
{% endhint %}

```
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
```

In this example, we are scheduling our Maya worker on either `amd-epyc-rome` or `intel-xeon-v4` CPU nodes, with a preference to be scheduled in `ORD1`, our Chicago datacenter. The resource request at the end of this spec then determine the CPU, GPU, and memory limits for the container:

```
resources:
      limits:
        cpu: 35
        memory: 130Gi
      requests:
        cpu: 35
        memory: 129Gi
```

### Put it all together

Now that we have all our values ready, it's time to put it all together.

If you followed up to this point, your YAML might look something like the following.

<details>

<summary>Click to expand - Example Deadline deployment YAML file</summary>

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
  images:
  - name: maya-epyc
      enabled: true
      groups:
        - maya-epyc
        - maya
      pools:
        - vfx
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

</details>

To follow along, copy and paste the contents of the sample file provided above into your Deadline application's YAML configuration area, then click the **Deploy** button.

{% hint style="info" %}
**Note**

It is common to have many Worker types sometimes, or even multiple different hardware variations for the same DCC (e.g. `maya-epyc`, `maya-xeon`, `maya-A4000`, etc.).
{% endhint %}

If all goes as expected, then you should see a number of Deadline-specific Pods in your namespace when running `kubectl get pods`. It is normal while the repository is installing for some components to restart - when the Pod labeled `repository-init` transitions to state `Complete`, then you should no longer see any Deadline components restarting.

### Managing **and u**pdating your Deadline repository

You can connect to your Deadline repository once it is in the `Running` state. By default, the [Deadline remote connection server](https://docs.thinkboxsoftware.com/products/deadline/10.1/1\_User%20Manual/manual/remote-connection-server.html) is the simplest way to connect, and can be reached at the domain `rcs-<name of Deadline release>-<your namespace>.coreweave.cloud`, where `<name of Deadline release>` is the name that was used when deploying the Deadline application. In the window named **Select Repository**, place this address in the **Remote Server** field. By default, the RCS connection uses port `4433`.

<figure><img src="../../.gitbook/assets/deadline-repo-settings.PNG" alt="Screenshot of the Deadline remote connection server"><figcaption><p>Screenshot of the Deadline remote connection server</p></figcaption></figure>

To retrieve your certificate to connect, run:

{% code overflow="wrap" %}
```bash
$ kubectl cp $(kgp | grep rcs | grep "<Name of Deadline Release> | grep -o '^\S*'):/tmp/clientkey.pfx <local directory to store key>/key.pfx
```
{% endcode %}

Be sure to replace `<name of Deadline release>` and `<local directory to store key>` with their respective values. Select your downloaded certificate, then enter the passphrase you specified in the YAML manifest. Finally, click the **OK** button to connect.

Once connected, navigate to **View -> Panels -> Limits**. Here, you will see the pre-populated limits that were created upon installation. Opening one should present something like the following:

![Example license limits dialogue box](<../../../.gitbook/assets/image (78) (1) (1).png>)

This menu will display the license name, the usage level, the license count, the master Worker list, the list of Workers on deny, and the Workers excluded from the limit.

{% hint style="info" %}
**Note**&#x20;

Due to limitations in the Deadline API, license limits can only be created programmatically while they function identically to `resource`.
{% endhint %}

## Security

Once your Thinkbox Deadline instance is deployed, there are a few additional security changes to make to prepare the repository for a full-scale deployment.

### Super-user password

Secure your repository by creating a super-user password. Navigate to **Tools -> Configure Repository Options -> User Security**. In this menu, ensure that **"Use the System User for the Deadline User"** is enabled. This will ensure that users cannot impersonate other user groups.

### User groups

Next, configure the user groups by navigating to **Tools -> Manage User Groups**.

![The user group permissions configuration screen for Deadline](<../../../.gitbook/assets/image (61).png>)

{% hint style="success" %}
**Tip**

Consider creating a few user groups with different permissions for the different users who might be interacting with your repository.
{% endhint %}

Once this piece of the configuration is done, you have a production-ready Thinkbox Deadline instance running on CoreWeave Cloud!
