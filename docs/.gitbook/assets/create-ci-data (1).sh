cat <<EOF >user-data
#cloud-config
ssh_pwauth: True
users:
  - name: user
    plain_text_passwd: packer
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: false
EOF

cat <<EOF >meta-data
{"instance-id":"packer-worker.tenant-local","local-hostname":"packer-worker"}
EOF

genisoimage -output cidata.iso -input-charset utf-8 -volid cidata -joliet -r \
            user-data meta-data