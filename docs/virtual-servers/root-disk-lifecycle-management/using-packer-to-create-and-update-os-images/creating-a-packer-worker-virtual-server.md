# Creating a Packer Worker Virtual Server

**Objective:** Create a Virtual Server on [CoreWeave Cloud](https://apps.coreweave.com) to create images with [Hashicorp Packer](https://www.packer.io).\
**Overview:** This process consists of deploying an Ubuntu Virtual Server on CoreWeave Cloud, with the [cloned PVC](../exporting-coreweave-images-to-a-writable-pvc.md) attached. The Virtual Server is then configured with a Docker image to run Packer. Note that this example assumes a cloned PVC was created as explained in the example [Copying CoreWeave Images to a Writable PVC](../exporting-coreweave-images-to-a-writable-pvc.md).

#### References:

{% file src="../../../../.gitbook/assets/packer_vs.yaml" %}

{% file src="../../../../.gitbook/assets/configure_packer_docker.sh" %}

## Deploying Virtual Server

Using **packer\_vs.yaml**, we will deploy our Virtual Server with`k create -f packer_vs.yaml`**:**

{% tabs %}
{% tab title="YAML" %}
{% code title="packer_vs.yaml" %}
```yaml
apiVersion: virtualservers.coreweave.com/v1alpha1
kind: VirtualServer
metadata:
  name: packer-worker
  namespace: tenant-<tenant>
spec:
  region: ORD1
  os:
    type: linux
  resources:
    cpu:
      type: amd-epyc-rome
      count: 8
    memory: 32Gi
  storage:
    root:
      size: 256Gi
      storageClassName: block-nvme-ord1
      source:
        pvc:
          namespace: vd-images
          name: ubuntu2004-docker-master-20210629-ord1
    additionalDisks:
    - name: winsvr2019std
      spec:
        persistentVolumeClaim:
          claimName: winserver2019std-clone-20210701-ord1
  users:
    - username: <username>
      password: <password>
  network:
    public: true
    tcp:
      ports:
        - 22
  initializeRunning: true
```
{% endcode %}

{% hint style="success" %}
Note our region matches the region used when creating the [cloned volume](../exporting-coreweave-images-to-a-writable-pvc.md#identifying-source-image)
{% endhint %}
{% endtab %}
{% endtabs %}

`k get vs` will show us our Virtual Server has been deployed, along with an IP we can use to SSH into:

![](../../../.gitbook/assets/4.png)

### Configuring Packer Environment

Using the external IP noted from `k get vs`, connect to your Virtual Server via SSH. If you followed [Copying CoreWeave Images to a Writable PVC](../exporting-coreweave-images-to-a-writable-pvc.md), you’ll notice our root disk is mounted to **/dev/vda**, and our cloned PVC is mounted to **/dev/vdb**:

![](../../../.gitbook/assets/5.png)

Since our Virtual Server was created using **ubuntu2004-docker-master-20210629-ord1**, Docker is already installed. Running **configure\_packer\_docker.sh** will build a container to provide a consistent environment for using Packer, with all the dependencies installed.

{% tabs %}
{% tab title="Bash" %}
{% code title="configure_packer_docker.sh" %}
```bash
docker build -t "packer" -f - . <<EOF
FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libc6-dev libvirt-daemon-system libvirt-dev python3-winrm \
    qemu-kvm qemu-utils sshpass unzip curl wget git jq rsync \
    genisoimage openssh-client libguestfs-tools \
    yamllint moreutils ovmf

RUN wget -O /usr/local/bin/virtctl $(curl -L https://api.github.com/repos/kubevirt/kubevirt/releases/latest | grep browser_download_url.*-linux-amd64 | cut -d : -f 2,3| tr -d \")
RUN wget -O /usr/local/bin/kubectl https://dl.k8s.io/release/$(curl -L https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
RUN curl -L -s  https://releases.hashicorp.com/packer/$(curl -L https://checkpoint-api.hashicorp.com/v1/check/packer | jq -r -M '.current_version')/packer_$(curl -L https://checkpoint-api.hashicorp.com/v1/check/packer | jq -r -M '.current_version')_linux_amd64.zip  --output /tmp/packer_linux_amd64.zip
RUN unzip -o /tmp/packer_linux_amd64.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/*ctl
RUN rm -rf /tmp/packer_linux_amd64.zip

VOLUME /work
WORKDIR /work

ENV LIBGUESTFS_DEBUG=1 LIBGUESTFS_TRACE=1 PACKER_LOG=1

ENV PACKER_CACHE_DIR=/work/cache/packer

EOF
```
{% endcode %}
{% endtab %}
{% endtabs %}

![](../../../.gitbook/assets/7.png)
