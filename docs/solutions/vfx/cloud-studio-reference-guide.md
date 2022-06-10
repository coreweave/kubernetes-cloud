# Cloud Studio Reference Guide

In this guide we are going to walk through creating a VFX studio in the cloud using best practiced and recommended solutions. As a result, this guide is intended as a starting point and an explanation of concepts to build upon. Where applicable, references to additional documentation have been provided in order to further explain configuration options and deployment methods.

{% embed url="https://lucid.app/documents/embeddedchart/aba70634-17de-4a94-9721-a80f4eed5298" %}

### Recommended Reading

Before viewing this guide please consider checking out the following getting started guides:

#### Getting started on CoreWeave Cloud:

{% content-ref url="../../coreweave-kubernetes/getting-started.md" %}
[getting-started.md](../../coreweave-kubernetes/getting-started.md)
{% endcontent-ref %}

#### Useful commands in Kubernetes:

{% content-ref url="../../coreweave-kubernetes/useful-commands.md" %}
[useful-commands.md](../../coreweave-kubernetes/useful-commands.md)
{% endcontent-ref %}

#### Getting started with Virtual Servers:

{% content-ref url="../../workflows/argo.md" %}
[argo.md](../../workflows/argo.md)
{% endcontent-ref %}

## Active Directory

This guide assumes that you have some authentication in mind. Where applicable throughout we have used AD deployed using our guide here:

{% content-ref url="../../virtual-servers/examples/provision-an-active-directory-domain-controller.md" %}
[provision-an-active-directory-domain-controller.md](../../virtual-servers/examples/provision-an-active-directory-domain-controller.md)
{% endcontent-ref %}

This may be a great first step when setting up your cloud studio but you can also come back later to handle this step after you have set up other components.

## Creating Storage

Begin by logging into your cloud account and navigating to apps. Clicking on the Catalog tab you should see a range of applications that you can deploy. Find the application "filesystem-volume."

![](<../../../.gitbook/assets/image (84).png>)

Selecting this, click deploy in the upper right and then select in the creation dialogue the name, region, storage type, and storage size for your PVC object. The available storage types are our NVMe and HDD tiers. (NOTE: this application will create a shared filesystem, if you require block storage volumes please see our documentation [here](cloud-studio-reference-guide.md#storage) on provisioning storage using YAML manifests and kubectl).

![](<../../../.gitbook/assets/image (85) (2).png>)

We are going to create a filesystem-volume for render outputs, that way all of our virtual desktops can access the same shared storage as our render nodes. When rendering on CoreWeave cloud, ensuring that applications don't attempt to write over the internet to on prem storage is essential. Typically large amounts of data that is accessed infrequently such as render outputs belongs on our HDD tier. We will be provisioning everything in our Chicago datacenter (ORD) but feel free to provision resources in the datacenter closest to you.

![Storage Options](<../../../.gitbook/assets/image (66) (1).png>) ![Deployment](<../../../.gitbook/assets/image (60) (1).png>) ![Success](<../../.gitbook/assets/image (19) (1).png>)

Once you hit Deploy you should see the following message and an instance of the filesystem-volume application in the "Applications" tab.

If you would like to see the resource inside of Kubernetes you can use `kubectl get pvc` to list all the available storage volumes in your namespace and then use `kubectl describe pvc <name of pvc>` to get more information about the resource you created. If you installed Helm in your local terminal you can also use `helm list` to see the full list of applications deployed in your namespace which should.

With this storage deployed, you can now mount this shared volume into any kubernetes pod or a CoreWeave virtual server which we will do later in this guide.

## Creating and Configuring Workstations

For our reference environment we are going to create an array of virtual workstations with different configurations.

For our configurations we are going to create artist machines in Windows and Centos 7 as well as lighter weight machines designed for administrators. Later we will configure special network policies which help to provide security barriers between users of different types.

For more information on deploying virtual-machines see:

{% content-ref url="../../virtual-servers/deployment-methods/" %}
[deployment-methods](../../virtual-servers/deployment-methods/)
{% endcontent-ref %}

In particular we are going to Deploy our VMs via the CoreWeave apps UI.

{% content-ref url="../../virtual-servers/deployment-methods/coreweave-apps.md" %}
[coreweave-apps.md](../../virtual-servers/deployment-methods/coreweave-apps.md)
{% endcontent-ref %}

### Connecting Storage

In order to connect our render output storage to our virtual servers we will take two approaches. For our Linux based workstations we will mount the storage directly using virtiofs. For our Windows machines we are going to export our storage using samba and mount that from the workstation after initialization. To see the process of interacting with storage and VMs see our VFX Components Guide:

{% content-ref url="vfx-studio-components-guide.md" %}
[vfx-studio-components-guide.md](vfx-studio-components-guide.md)
{% endcontent-ref %}

Following this guide, create a Samba deployment NOTE: the AD flavor of the Samba application will require a domain controller set up in your namespace with an address specified during deployment.

### Artists

For the artist machines we will provision three separate VMs using either Teradici or Parsec for remote access.

Note that at this time Parsec is not supported for hosting on Centos 7.

To get started, log into your cloud account and navigate to the applications page or simply enter [apps.coreweave.com](https://apps.coreweave.com) in your browser. Next go to Catalog and select Virtual Server. There you can specify all the different details of your virtual desktop. To start, create a Windows VDI by selecting Windows 10 Professional in the drop down.

![](<../../.gitbook/assets/image (5) (1).png>)

Once you have specified the other details for your artist workstation, GPU, CPU, etc., put in user credentials (Note if you are utilizing AD you will have to put in a temporary user before you join the storage)

The three examples in the reference namespace are as follows:

* Windows 10 + Parsec (artist-parsec)
* Windows 10 + Teradici (artist-tera-win)
* Centos 7 + Teradici (artist-teridici-centos)

The values used to create them are the same, with the source image being the only difference:

```
affinity: {}
initializeRunning: true
labels:
  user.group: artist
network:
  directAttachLoadBalancerIP: true
  floatingIPs: []
  public: true
  tcp:
    ports:
    - 22
    - 443
    - 60443
    - 4172
    - 3389
  udp:
    ports:
    - 4172
    - 3389
persistentVolumes: []
region: ORD1
resources:
  cpu:
    count: 8
    type: ""
  definition: a
  gpu:
    count: 1
    type: Quadro_RTX_4000
  memory: 32Gi
storage:
  additionalDisks: []
  filesystems: []
  root:
    accessMode: ReadWriteOnce
    size: 255Gi
    source:
      name: virtual-artist-20211102-block-ord1
      namespace: tenant-sta-vfx1-reference
      type: pvc
    storageClassName: block-nvme-ord1
    volumeMode: Block
users:
- password: password
  username: username
```

Next click Deploy and watch your VM start up in your namespace.

Once you have logged into your new VM, start Parsec and enter your credentials. Note: you may choose to create your own Parsec teams account for management capabilities. However, if you would like to license and administer Parsec through CoreWeave please reach out to support.vfx@coreweave.com.

At this point you may decide to load up a VM with all of your applications to prepare a base image. Doing this can prevent additional work when creating the final parsec and/or Teradici master images. For more information and options regarding creating and managing base images you can see our resources here:

{% content-ref url="../../virtual-servers/root-disk-lifecycle-management/" %}
[root-disk-lifecycle-management](../../virtual-servers/root-disk-lifecycle-management/)
{% endcontent-ref %}

### Windows and Teradici

To deploy Windows 10 with Teradici the process is the same as with our previous machine however we are going to modify our cloud init values in the yaml editor to automatically install Teradici. Cloud init is a simple way of running commands on initialization to get your machine set up.

Navigating to the yaml tab inside the virtual server deploy interface you should see a commented out section such as:

```
#cloudInit: |
#  # Write a simple script
#  write_files:
#  - content: |
#      #!/bin/bash
#      echo "Hello world!"
#    path: /home/myuser/script.sh
#    permissions: '0744'
#    owner: myuser:myuser
#  # Update packages
#  package_update: true
#  # Install packages
#  packages:
#    - curl
#    - git
#  # Run additional commands
#  runcmd:
#    - [df, -h]
#    - [git, version]
#    - [curl, --version ]
#    - [bash, /home/myuser/script.sh]
```

To install Teradici on startup simply uncomment the first line and add:

```
cloudInit:
  teradici: true
```

Now, when your virtual server is done initializing you will be able to connect to it using the same credentials you specify in the creation interface. If you would like to add additional applications on initialization you can utilize chocolatey. For a list of community applications that can be automatically installed using Chocolatey visit [https://community.chocolatey.org/packages](https://community.chocolatey.org/packages). The specification in the could look like:

```
cloudInit:
    choco_install: [googlechrome,firefox,vlc]
```

For the final machine we are going to follow the same steps except here we can simply select the Teradici toggle along with the NVIDIA drivers toggle.

![Note: these options will only be available when selecting a Linux distro as your OS](<../../.gitbook/assets/Screen Shot 2021-11-08 at 3.37.58 PM.png>)

For our Linux based workstation we will also want to mount in our storage via virtio-fs. To do this switch to the YAML editor and edit the filesystem value with:

```
filesystems: 
  - name: render-outputs
    source:
      type: pvc
      name: render-outputs
```

### Administrators

Administrators and support staff often times do not need the same resources as artists for their work. Besides the networking and security aspects of this statement which we will cover shortly, allocating different amounts of compute resources to administrators is easy. You may choose, for example, to utilize Windows 10 VMs without GPUs and low cpu allocations.

![](<../../.gitbook/assets/Screen Shot 2021-11-08 at 3.46.02 PM.png>)

Note that Windows machines will not be accessible via Teradici without a NVIDIA graphics card. In that scenario you may opt to use RDP or Parsec for administrator remote access.

For our reference namespace we will create two administrator Windows 10 machines with both Teradici and Parsec in the same way as our artist machines. These machines are:

1. admin-teradici
2. admin-parsec

### Management

There are many ways we may look to manage our virtual machines. Our recommended way for managing virtual machines utilizing Teradici is using Leostream + Teradici Security Gateway/Connection Manager. The Teradici Security Gateway/Connection Manager allows for centralized provisioning and connection brokering through a common gateway while Leostream will allow us to integrate our AD credentials to dynamically assign machines to users.

To begin setting up our management stack, create a new Centos based virtual server. For our machine we will provision 8vCPU cores and 32Gi of memory one Centos 7, with no GPU. Ensure you use a direct attached IP address.Once this machine is instantiated, ssh in and run the following:

1. `sudo yum update`
2. `sudo curl http://downloads.leostream.com/broker.prod.sh | sudo bash`
3. `service leostream start`

This will start the leostream connection broker and begin looking for incoming connections. When you enter the IP address of your connection broker virtual server in your browser you should be presented with the leostream login screen. Here you can set up your leostream licensing and login with the default administrator credentials `admin:leo`. For more instructions on installing and configuring the leostream broker visit [Leostream's website](https://www.leostream.com/wp-content/uploads/2018/11/installation\_guide.pdf).

Once your connection broker is installed, logon and configure the broker. Begin by navigating to Configuration > Protocol Plans. Here create a protocol plan which prioritizes Teradici PCoIP. Additionally, if you are utilizing Active Directory navigate to Setup > Authentication Servers, and enter the details for your domain controller.

After your connection broker is running, it's time to connect your Teradici VMs to your broker.

To do this on Linux use ssh or Teradici to gain access to the command line. Once authenticated run the following commands to install the Teradici Agent. Note: this will launch a GUI installer, so be prepared to connect via Teradici. You will be asked to configure the connection broker. At this step input the IP address of the connection broker virtual server you set up earlier.

1. `sudo yum update`
2. `sudo yum install LibXScrnSaver java-1.7.0-openjdk.x86_64`
3. `wget`[`https://s3.amazonaws.com/downloads.leostream.com/LeostreamAgentJava-5.2.6.0.jar`](https://s3.amazonaws.com/downloads.leostream.com/LeostreamAgentJava-5.2.6.0.jar)\`\`
4. `sudo java -jar ./LeostreamAgentJava-5.2.6.0.jar`

Finally, to finish our management interface, we should install the Teradici Security Gateway/Connection Manager you can launch the Teradici Connection Manager from the Applications catalogue. This will require that you specify the connection broker IP address in the deployment interface. Once installed, users should be able to connect directly to the connection manager and have their session properly routed.

## Networking

The best way to manage connectivity between kubernetes components and the internet is using kubernetes network policies. For our reference implementation we will create a simple group of network policies which create "user groups" with different access to internal and external resources. Network policies are specified in YAML manifests and can be applied to the namespace using `kubectl apply -f <path to yaml manifest>`

The first network policy we will call "artist." This network policy will use a pod selector to match against any pod with the label `user.group: artist`. Our policy then specifies that it will allow inbound traffic from any internal IP address, i.e. 10.0.0.0/8, as well as any traffic over the port 3389. Our policy additionally specifies that it will allow our artist VMs to send traffic to any internal IP address.

```
piVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: artist
  namespace: tenant-sta-vfx1-reference
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

This policy would prevent connections originating outside the cluster from reaching our VMs except on port 3389, which is RDP. This could provide admins access to troubleshoot machines externally using a separate account or login.

If we wanted our network policy to have stricter policies, we could allow only traffic from our AD samba and the Teradici connection manager. This would prevent any external or internal resource from connecting to our VMs without going through our connection manager and Leostream broker.

```
piVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: artist
  namespace: tenant-sta-vfx1-reference
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
        app: teradici-gateway-teridici-conn-gateway
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

Note that all network policies are additive, so any IP range or port not explicitly mentioned will not be accessible.

To apply this policy to our virtual servers we can upgrade our workstations from the applications UI. Switch to the YAML editor and add the following entry:

```
labels:
  user.group: "artist"
```

After restarting your virtual server you will notice that the launcher pod now contains this label and the network policy will be applied.

Next we can create another network policy for our administrators. This policy should likely be the opposite: enable internet access but disable access to other internal resources.

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: administration
  namespace: tenant-sta-vfx1-reference
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

This policy for example will prohibit administrators from accessing the Samba storage but will allow them to connect to anything else.

Last but not least we should create a network policy that is open to all traffic within the namespace, that way for internal infrastructure can be reached from other resources. We also add a wide open egress policy so that our services can connect to resources in the namespace or on the internet.

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: infra
  namespace: tenant-sta-vfx1-reference
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

It is suggested that if you add a wide open network policy, pay close attention to whether or not a public IP address is assigned to avoid un-intended connections from external actors.

## Deploying Deadline

To begin setting up a managed Deadline repository in your namespace first follow the instructions here:

{% content-ref url="deadline.md" %}
[deadline.md](deadline.md)
{% endcontent-ref %}

Afterwards, there are a few additional changes we will want to make to prepare our repository for a full scale deployment.

First, secure your repository by creating a super-user password at Tools > Configure Repository Options > User Security. In that same menu ensure that "Use the System User for the Deadline User" is enabled. This will ensure that users don't attempt to impersonate other user groups.

Next configure your user groups by going to Tools > Manage User Groups.

![](<../../.gitbook/assets/image (3) (1).png>)

Consider creating a few groups for the different users who might be interacting with your repository.
