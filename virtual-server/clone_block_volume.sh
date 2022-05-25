clone_block_volume() {
	if [ $# -lt 2 ]; then
	  echo "Usage:  clone_block_volume --source <source pvc> --destination <destination pvc> --region <destination region (optional)> --namespace <namespace (optional)>"
	  return 1
	fi

	while [[ "$#" -gt 0 ]]
	do
	  case $1 in
		-n|--namespace)
		  local NS="${2,,}"
		  ;;
		-r|--region)
		  local DST_PVC_REGION="${2,,}"
		  ;;
		-d|--destination)
		  local DST_PVC="${2,,}"
		  ;;
		-s|--source)
		  local SRC_PVC="${2,,}"
		  ;;
	  esac
	  shift
	done

	NS=${NS:=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}')}

	SRC_PVC_CLASS=$(kubectl -n ${NS} get pvc $SRC_PVC -o=jsonpath='{.spec.storageClassName}')
	SRC_PVC_SIZE=$(kubectl -n ${NS} get pvc $SRC_PVC -o=jsonpath='{.spec.resources.requests.storage}')
	SRC_PVC_REGION=${SRC_PVC_CLASS//*-}
	
	if [ -z ${DST_PVC_REGION+x} ]; then
		DST_PVC_REGION=${SRC_PVC_REGION}
		DST_PVC_CLASS=${SRC_PVC_CLASS}
	else
		DST_PVC_CLASS="block-nvme-${DST_PVC_REGION}"
		DST_PVC="${DST_PVC}-${DST_PVC_REGION}"
	fi
	
	NAME=clone-${DST_PVC}
	if [ ${#NAME} -gt 62 ]
	then
	  JOB_NAME=$(echo ${NAME:(-62)} | sed s/^-//)
	else
	  JOB_NAME=${NAME}
	fi

	cat <<-EOF | kubectl -n ${NS} apply -f -
		{
		  "apiVersion": "v1",
		  "kind": "PersistentVolumeClaim",
		  "metadata": {
			"name": "${DST_PVC}"
		  },
		  "spec": {
			"accessModes": [
			  "ReadWriteOnce"
			],
			"storageClassName": "${DST_PVC_CLASS}",
			"volumeMode": "Block",
			"resources": {
			  "requests": {
				"storage": "${SRC_PVC_SIZE}"
			  }
			}
		  }
		}
	EOF
	
	cat <<-EOF | kubectl -n ${NS} apply -f -
		{
		  "apiVersion": "batch/v1",
		  "kind": "Job",
		  "metadata": {
			"name": "${JOB_NAME}"
		  },
		  "spec": {
			"template": {
			  "spec": {
				"affinity": {
				  "nodeAffinity": {
					"requiredDuringSchedulingIgnoredDuringExecution": {
					  "nodeSelectorTerms": [
						{
						  "matchExpressions": [
							{
							  "key": "topology.kubernetes.io/region",
							  "operator": "In",
							  "values": [
								"${SRC_PVC_REGION^^}"
							  ]
							},
							{
							  "key": "node.coreweave.cloud/class",
							  "operator": "In",
							  "values": [
								"cpu"
							  ]
							},
							{
							  "key": "ethernet.coreweave.cloud/speed",
							  "operator": "In",
							  "values": [
								"10G",
								"40G"
							  ]
							}
						  ]
						}
					  ]
					}
				  }
				},
				"containers": [
				  {
					"name": "clone",
					"resources": {
					  "requests": {
						"cpu": "1",
						"memory": "2Gi"
					  }
					},
					"image": "registry.gitlab.com/coreweave/utility-images/admin-shell:36f48c0d",
					"command": [
					  "sh",
					  "-c",
					  "dd if=/dev/xvda of=/dev/xvdb bs=1M conv=sparse status=progress"
					],
					"volumeDevices": [
					  {
						"devicePath": "/dev/xvda",
						"name": "source"
					  },
					  {
						"devicePath": "/dev/xvdb",
						"name": "dest"
					  }
					]
				  }
				],
				"restartPolicy": "OnFailure",
				"volumes": [
				  {
					"name": "source",
					"persistentVolumeClaim": {
					  "claimName": "${SRC_PVC}",
					  "readOnly": true
					}
				  },
				  {
					"name": "dest",
					"persistentVolumeClaim": {
					  "claimName": "${DST_PVC}",
					  "readOnly": false
					}
				  }
				],
				"tolerations": [
				  {
					"key": "node.coreweave.cloud/hypervisor",
					"operator": "Exists"
				  },
				  {
					"key": "is_cpu_compute",
					"operator": "Exists"
				  }
				]
			  }
			}
		  }
		}
	EOF

	until kubectl get pods -n ${NS} --selector=job-name=${JOB_NAME}
	do sleep 1
	done
	
    kubectl -n ${NS} wait --for=condition=ContainersReady --timeout=120s pod/$(kubectl get pods -n ${NS}  --sort-by=.metadata.creationTimestamp --selector=job-name=${JOB_NAME} --output=jsonpath='{.items[-1].metadata.name}')
    kubectl -n ${NS} wait --for=condition=Complete --timeout=-1s job/${JOB_NAME}
    kubectl -n ${NS} logs pod/$(kubectl get pods -n ${NS} --sort-by=.metadata.creationTimestamp --selector=job-name=${JOB_NAME} --output=jsonpath='{.items[-1].metadata.name}')
    kubectl -n ${NS} delete job/${JOB_NAME}
}
