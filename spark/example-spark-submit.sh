#!/bin/bash

# Replace this command with your desired namespace if you don't want to use your default namespace
NAMESPACE=$(kubectl config view --minify -o jsonpath='{..namespace}')
echo "Using the namespace: $NAMESPACE"

# TODO: Change the master back from staging
$SPARK_HOME/bin/spark-submit \
    --master k8s://https://k8s.ord1.coreweave.com \
    --deploy-mode cluster \
    --name download-imgdataset-wandb-16-64 \
    --conf spark.driver.cores=16 \
    --conf spark.kubernetes.driver.limit.cores=16 \
    --conf spark.driver.memory="64G" \
    --conf spark.executor.cores=16 \
    --conf spark.kubernetes.executor.limit.cores=16 \
    --conf spark.executor.memory="64G" \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.driver.container.image=navarrepratt/spark-download-imgdataset:1.0.2 \
    --conf spark.kubernetes.executor.container.image=navarrepratt/spark-download-imgdataset:1.0.2 \
    --conf spark.kubernetes.driver.podTemplateFile=./cpu-pod-template.yaml \
    --conf spark.kubernetes.executor.podTemplateFile=./cpu-pod-template.yaml \
    --conf spark.kubernetes.namespace="$NAMESPACE" \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-sa \
    local:///app/download_imgdataset.py --output /mnt/pvc/mscoco -t 2048
