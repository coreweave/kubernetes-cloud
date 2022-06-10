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