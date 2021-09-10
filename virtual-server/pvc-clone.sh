#!/bin/bash
# Clone the disk PVC for a given VM instance to a new PVC.
set -e -o pipefail -u

if [ $# -ne 2 ]; then
    echo "Usage: $0 <source vmi> <destination pvc name>"
    exit 1
fi

SRC="$1"
DST="$2"


get_field() {
    kubectl get $1 $2 -o=jsonpath='{'"$3"'}'
}

if kubectl get vmi $SRC &>/dev/null; then
    echo "Found running VM instance: $SRC"
    read -p "Stop it? [y/N] " STOP
    
	if [ "$(get_field vmi $SRC ".metadata.annotations.vs\.coreweave\.com/vmi")" == "true" ]; then
	SRC_PVC=$(get_field vmi $SRC ".spec.volumes..dataVolume.name")
	else
	SRC_PVC=$(get_field vmi $SRC ".spec.volumes[?(@.name=='dv')].persistentVolumeClaim.claimName")
	fi

    if [[ "$STOP" =~ ^[yY]$ ]]; then
        virtctl stop $SRC

        echo -n "Waiting for $SRC to stop..."
        while kubectl get vmi $SRC &>/dev/null; do
            sleep 1
            echo -n "."
        done
        echo " stopped."
    else
        echo "ERROR: cannot clone pvc of a running VM"
        exit 1
    fi

elif kubectl get pvc $SRC &>/dev/null; then

    SRC_PVC="$SRC"

else
    echo "ERROR: Did not find PVC or VM instance named: $SRC"
    exit 1
fi

SRC_PVC_CLASS=$(get_field pvc $SRC_PVC ".spec.storageClassName")
SRC_PVC_SIZE=$(get_field pvc $SRC_PVC ".spec.resources.requests.storage")

REGION=${SRC_PVC_CLASS//*-}

if [ "$REGION" == "replica" ]; then
    REGION="ord1"
fi

DST_PVC="${DST}-$(date '+%Y%m%d')-block-${REGION}"

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${DST_PVC}
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: ${SRC_PVC_CLASS}
  volumeMode: Block
  resources:
    requests:
      storage: ${SRC_PVC_SIZE}
  dataSource:
    kind: PersistentVolumeClaim
    name: ${SRC_PVC}
EOF

echo -n "Waiting for pvc $DST_PVC to be bound..."
while [ $(get_field pvc $DST_PVC ".status.phase") != "Bound" ]; do
    sleep 1
    echo -n "."
done
echo " done."

echo "Clone of $SRC_PVC to $DST_PVC is complete."
echo "Source VM instance $SRC can be started up or destroyed."
