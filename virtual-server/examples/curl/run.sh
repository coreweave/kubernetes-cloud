#!/bin/bash

# Enable to trace the script
# set -x

APISERVER=k8s.ord1.staging.coreweave.com

if [ -z ${NAMESPACE} ] || [ -z ${TOKEN} ]; then
  echo "NAMESPACE and TOKEN variable must be set: TOKEN=<token> NAMESPACE=<namespace> ./$(basename $BASH_SOURCE)"
  exit 1
fi  

# -------------- HELPER FUNCTIONS-----------

# Print formatted output from list
function print_list() {
  local OUTPUT=$1
  local TMP=$(mktemp /tmp/vs.XXXXXX)
  echo "${OUTPUT}" | jq -jr '.columnDefinitions[]| .name,"\t"' | tr '[:lower:]' '[:upper:]' > ${TMP}
  echo "" >> ${TMP}
  echo "${OUTPUT}" | jq -r '.rows[].cells | @tsv' | tr -d '"' >> ${TMP}
  echo "" >> ${TMP}
  cat ${TMP} | column -t
  rm -f ${TMP}
}


# -------------- VS OPERATIONS --------------

# Function replace NAME in the manifest virtual-server.json and creates Virtual Server
function create_vs() {
  local NAME=$1
  jq -r --arg vs_name "$NAME" '.metadata.name = $vs_name' virtual-server.json |
  curl -X POST "https://${APISERVER}/apis/virtualservers.coreweave.com/v1alpha1/namespaces/${NAMESPACE}/virtualservers" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Content-type: application/json" \
    --insecure --data @-
  return $?
}

# Delete Virtual Server
function delete_vs() {
  local NAME=$1
  curl -X DELETE "https://${APISERVER}/apis/virtualservers.coreweave.com/v1alpha1/namespaces/${NAMESPACE}/virtualservers/${NAME}" \
    --header "Authorization: Bearer $TOKEN" \
    --insecure -s 
    return $?
}

# List of all Virtual Servers in namespace
# The list is formatted by helper function `print_list`, similar to kubectl command
function list_vs() {
  local OUTPUT=$(curl -X GET "https://${APISERVER}/apis/virtualservers.coreweave.com/v1alpha1/namespaces/${NAMESPACE}/virtualservers" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s)   
  print_list "${OUTPUT}"
}

# Print formatted JSON details about Virtual Server
function get_vs() {
  local NAME=$1
  curl -X GET "https://${APISERVER}/apis/virtualservers.coreweave.com/v1alpha1/namespaces/${NAMESPACE}/virtualservers/${NAME}" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s | jq '.'  
}

# Function loops until expected condition is met. 
# The condition is checked by helper functions, passed as the second argument:
# - `expect_vs_stopped`, i.e. status=VirtualServerStopped and started==False
# - `expect_vs_running`, i.e. statrus=VirtualServerReady and started==True
function wait_until_vs_status() {
  local NAME=$1
  local STATUS_FUNC=$2

  while true;do
    local VS_STATUS=($(get_vs_status ${NAME}))
    echo "Status:${VS_STATUS[0]}, Started:${VS_STATUS[1]}"
    ${STATUS_FUNC} ${VS_STATUS[0]} ${VS_STATUS[1]}
    if [ $? == 0 ];then
      return
    fi
    sleep 2
  done
}

# Helper function that returns STATUS and STARTED values for the Virtual Server
function get_vs_status() {
  local NAME=$1
  local CURRENT_STATUS_ARRAY=($(curl "https://${APISERVER}/apis/virtualservers.coreweave.com/v1alpha1/namespaces/${NAMESPACE}/virtualservers/${NAME}" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s | jq '.rows[] | .cells[1], .cells[3]' | tr -d '"'))
  echo "${CURRENT_STATUS_ARRAY[0]} ${CURRENT_STATUS_ARRAY[1]}"
}

# Helper function that returns 0 when status=VirtualServerStopped and started==False
function expect_vs_stopped() {
  local STATUS=$1
  local STARTED=$2
  if [ "${STATUS}" == "VirtualServerStopped" ] && [ "${STARTED}" == "False" ];then
    return 0
  fi
  return 1
}

# Helper function that returns 0 when  statrus=VirtualServerReady and started==True
function expect_vs_running() {
  local STATUS=$1
  local STARTED=$2
  if [ "${STATUS}" == "VirtualServerReady" ] && [ "${STARTED}" == "True" ];then
    return 0
  fi
  return 1
}

# -------------- VM OPERATIONS --------------

# Start VM
function start_vm() {
  local NAME=$1
  curl -X PUT "https://${APISERVER}/apis/subresources.kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachines/${NAME}/start" \
    --header "Authorization: Bearer $TOKEN" \
    --insecure -s
    return $?
}

# Stop VM
function stop_vm() {
  local NAME=$1
  curl -X PUT "https://${APISERVER}/apis/subresources.kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachines/${NAME}/stop" \
    --header "Authorization: Bearer $TOKEN" \
    --insecure -s
    return $?
}

# List of all Virtual Machines in namespace
# The list is formatted by helper function `print_list`, similar to kubectl command
function list_vm() {
  local OUTPUT=$(curl -X GET "https://${APISERVER}/apis/kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachines" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s)
  print_list "${OUTPUT}"
}

# Print formatted JSON details about Virtual Machine
function get_vm() {
  local NAME=$1
  curl -X GET "https://${APISERVER}/apis/kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachines/${NAME}" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s | jq '.'  
}

# -------------- VMI OPERATIONS --------------

# List of all Virtual Machine Instances in namespace
# The list is formatted by helper function `print_list`, similar to kubectl command
function list_vmi() {
  local OUTPUT=$(curl -X GET "https://${APISERVER}/apis/kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachineinstances" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s)
  print_list "${OUTPUT}"
}

# Print formatted JSON details about Virtual Machine Instance
function get_vmi() {
  local NAME=$1
  curl -X GET "https://${APISERVER}/apis/kubevirt.io/v1/namespaces/${NAMESPACE}/virtualmachineinstances/${NAME}" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Accept: application/json;as=Table;g=meta.k8s.io;v=v1" \
    --insecure -s | jq '.'  
}

# =====================================================================

# Virtual Server name
VS_NAME=vs-example

echo -e "\n------------- CREATE VS -----------------------------------"
create_vs ${VS_NAME}

echo -e "\n------------- WAIT FOR VMI UNTIL RUNNING ------------------"
wait_until_vs_status ${VS_NAME} expect_vs_running

echo -e "\n------------- LIST VS -------------------------------------"
list_vs

echo -e "\n------------- LIST VM -------------------------------------"
list_vm

echo -e "\n------------- LIST VMI ------------------------------------"
list_vmi

echo -e "\n------------- VS DETAILS ----------------------------------"
get_vs ${VS_NAME}

echo -e "\n------------- VM DETAILS ----------------------------------"
get_vm ${VS_NAME}

echo -e "\n------------- VMI DETAILS ---------------------------------"
get_vmi ${VS_NAME}

echo -e "\n------------- STOP VM -------------------------------------"
stop_vm ${VS_NAME}

echo -e "\n------------- WAIT FOR VMI UNTIL STOPPED ------------------"
wait_until_vs_status ${VS_NAME} expect_vs_stopped

echo -e "\n------------- DELETE VS -----------------------------------"
delete_vs ${VS_NAME}

exit 0
