---
description: >-
  Useful commands to help you get comfortable using Kubernetes on CoreWeave
  Cloud
---

# Useful Commands

Kubernetes is harder to pronounce than it is to use. If you've never used it before, you'll be comfortable deploying your Docker containers on CoreWeave Cloud in no time. We've put the following command reference together to help you perform simple tasks as you get better acquainted.

{% code title="SIMPLE STATUS COMMANDS" %}
```bash
kubectl get [resource_type]
kubectl get deployments # Shows a list of all running deployments
kubectl get pods # Shows a list of all running pods
kubectl get services # Shows a list of all running services
kubectl get pvc # Show a list of all active Persistent Volume Claims
```
{% endcode %}

{% code title="DESCRIBE PODS AND GET LOGS" %}
```bash
kubectl describe [resource_type] [resource_name/id]
kubectl describe pod [pod_id] # Shows detailed information about the status of a pod
kubectl logs -f [pod_id] # Gets streaming logs of a pod
```
{% endcode %}

{% code title="DELETE RESOURCES" %}
```bash
kubectl delete [resource_type] [resource_name/id]
kubectl delete pod [pod_id] # Deletes a pod, deployment will start a new one
kubectl delete deployment [deployment_name] # Deletes a deployment, will not restart
```
{% endcode %}

{% code title="SCALE DEPLOYMENTS" %}
```bash
kubectl scale --replicas=[number] [resource_type]/[resource_name/id]

## Scale a deployment to [number] of replicas
kubectl scale --replicas=[number] deployments/[deployment_name]
```
{% endcode %}

{% code title="INTERACT WITH RUNNING PODS" %}
```bash
kubectl exec -it [pod_id] /bin/bash # Opens a bash shell in your pod
```
{% endcode %}

