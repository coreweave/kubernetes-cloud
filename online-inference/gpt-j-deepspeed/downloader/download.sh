#!/bin/bash

# Based on https://huggingface.co/NovelAI/genji-python-6B

set -ex

if [[ $# -ne 2 ]]; then
    echo "Invalid number of arguments"
    echo "Usage: ./download_huggingface.sh <model_name> <save_path>"
    echo "  - model_name  - model name to download e.g. NovelAI/genji-python-6b"
    echo "  - save_path  - base directory where the model is saved, e.g. /mnt/pvc"
    exit 1
fi

MODEL_NAME=$1
SAVE_PATH=$2

BLOBSTORE_PREFIX="inference"
PATH=${PATH}:"${CURRENT_DIR}/scripts/bin"

echo "SAVE_PATH: ${SAVE_PATH}"
echo "MODEL_NAME: ${MODEL_NAME}"

mkdir -pv "${SAVE_PATH}/${MODEL_NAME}"

function download_file {
  local FILE_PATH=$1
  local DIR_PATH=$(dirname "${FILE_PATH}")
  mkdir -p "${DIR_PATH}"
  curl "http://blobstore.s3.ord1.coreweave.com/inference/${FILE_PATH}" --output "${FILE_PATH}"
}

function  download {
  echo "Downloading model ${MODEL_NAME} into ${SAVE_PATH}"

  pushd "${SAVE_PATH}"
  mkdir -p "${MODEL_NAME}"
  pushd "${MODEL_NAME}"
  FILE_LIST=($(curl --insecure "http://blobstore.s3.ord1.coreweave.com/inference/${MODEL_NAME}/files.txt" | awk '{print $4;}'))
  popd

  for file in "${FILE_LIST[@]}";do
    relative_path=${file#"s3://blobstore/inference/"}
    download_file "${relative_path}"
  done

  popd
}

function set_ready {
  echo "Save .ready.txt in ${SAVE_PATH}/${MODEL_NAME}"
  pushd "${SAVE_PATH}/${MODEL_NAME}"
  touch ".ready.txt"
  tree
  popd
}

date
download
set_ready
date

exit 0
