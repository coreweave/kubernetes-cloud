CONFIG="$1"
exec docker run --rm --dns 1.1.1.1 --device /dev/kvm --privileged --net=host \
     -v /var/lib/libvirt:/var/lib/libvirt \
     -v /var/run/libvirt:/var/run/libvirt \
     --volume $PWD:/work -it packer:latest \
     packer build -force -on-error=abort \
       $CONFIG