cat <<EOF >user-data
#cloud-config
users:
  - name: user
    plain_text_passwd: packer
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
EOF

cat <<EOF >meta-data
{"instance-id":"packer-worker"}
EOF

genisoimage -output cidata.iso -input-charset utf-8 -volid cidata -joliet -r \
            user-data meta-data