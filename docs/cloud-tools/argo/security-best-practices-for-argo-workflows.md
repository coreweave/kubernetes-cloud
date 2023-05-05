---
description: >-
  Following best practices is essential to minimize the risk of unauthorized
  access to your Kubernetes resources.
---

# Security Best Practices for Argo Workflows

## General recommendations

Here are some recommendations to improve security:

1. **Use client auth mode**: Client auth mode relies on Kubernetes' built-in authentication and authorization mechanisms. This ensures that access to Argo Workflows is controlled by Kubernetes Role-Based Access Control (RBAC) policies, providing a more secure and robust solution.
2. **Configure RBAC policies**: Set up Roles and RoleBindings to define and enforce the necessary permissions for Argo Workflows. This allows you to control which users or ServiceAccounts have access to specific resources and actions within the cluster.
3. **Namespace Isolation**: Install Argo Workflows in a dedicated namespace and associate the ServiceAccount with that namespace. This limits the scope of the resources that Argo Workflows can access.
4. **Separate ServiceAccounts**: If you have different components within Argo Workflows that require distinct permissions, create separate ServiceAccounts for each component. This way, if one component gets compromised, the attacker won't have access to other components' permissions.
5. **Encrypt Sensitive Data**: If you need to store sensitive data like secrets, tokens, or passwords in your Argo Workflows, use Kubernetes Secrets or another secure method of storage. Avoid storing sensitive data in plain text.
6. **Regular Audits**: Periodically review the permissions and access controls for the Argo Workflows ServiceAccounts to ensure they are still appropriate for your use case. Remove any unnecessary permissions or outdated ServiceAccounts.
7. **Monitor and Log Activity**: Monitor and log activity for the Argo Workflows ServiceAccounts to identify any suspicious or unauthorized activities. Use log analysis and monitoring tools to detect anomalies and promptly respond to potential security incidents.
8. **Keep Argo Workflows Updated**: Regularly update Argo Workflows to the latest version to benefit from security patches and improvements. This will help protect your environment against known vulnerabilities.

{% hint style="danger" %}
**Important: Avoid Server authentication mode**

Using server auth mode for Argo Workflows is strongly discouraged due to the potential security risks it introduces. In server auth mode, the Argo Workflows server handles authentication and authorization directly, which may expose your workflows and resources to public access. This could lead to unauthorized access, data leaks, or other security vulnerabilities in your environment.
{% endhint %}

When server auth mode is enabled, anyone with access to the Argo server's API or UI can potentially access and interact with your workflows, regardless of their privileges within the Kubernetes cluster. This creates a significant security concern, as it bypasses the standard Kubernetes authentication and authorization mechanisms.

By following these security best practices for Argo Workflows in regards to ServiceAccounts, you can minimize potential security risks and protect your Kubernetes cluster resources from unauthorized access.

## How CoreWeave uses ServiceAccounts with Argo Workflows

When you deploy Argo Workflows from the [Applications Catalog](https://apps.coreweave.com/), Helm creates creates three ServiceAccounts that segregate permissions between different components of the Argo Workflows system. The names are based on your deployment.&#x20;

For example, if you name your deployment **my-workflow**, it creates these:

1. **my-workflow-argo**: This ServiceAccount is used by the Argo Workflows controller, which manages the execution of workflows and their respective steps. It requires specific permissions and access to Kubernetes resources, such as creating, updating, and deleting Pods, Jobs, and ConfigMaps. Assigning a dedicated ServiceAccount to the controller ensures it has the necessary permissions to function correctly while adhering to the principle of least privilege.
2. **my-workflow-argo-client**: This ServiceAccount is intended for use by Argo CLI or other external clients that need to interact with the Argo Workflows API. It has limited permissions compared to the controller's ServiceAccount, allowing clients to create, list, and manage workflows without granting them full access to the underlying Kubernetes resources. This separation of concerns helps maintain security and prevents unauthorized access to critical cluster resources.
3. **my-workflow-argo-server**: This ServiceAccount is associated with the Argo Workflows server, which is responsible for providing the web-based user interface and the REST API. It requires specific permissions to access workflow data and interact with the Kubernetes API.&#x20;

## How to use a dedicated ServiceAccount

Argo Workflows needs access to various Kubernetes resources to provide its full range of features, such as managing artifacts, handling outputs, accessing secrets, and more. To achieve this, Argo communicates with the Kubernetes API using a ServiceAccount for authentication. Permissions for the ServiceAccount can be defined by associating it with a Role using a RoleBinding. This allows Argo to have the necessary access to Kubernetes resources based on your specific requirements.

Here are the steps to create and configure a ServiceAccount for Argo Workflows:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-role
rules:
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  verbs:
  - list
  - update
```

### Step 1: Create a Role

Define a Role with the necessary permissions for Argo Workflows. The Role should include the required access to resources such as ConfigMaps, Secrets, PersistentVolumeClaims, and Custom Resources like Workflows.

This is an example Role configuration. However, instead of copying this Role, you should thoroughly understand this topic and refer to the [tailored permissions section](security-best-practices-for-argo-workflows.md#use-tailored-permissions) to obtain a full list of resources and verbs.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-role
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - secrets
  - persistentvolumeclaims
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  verbs:
  - create
  - get
  - list
  - update
  - watch
```

### Step 2: Create a ServiceAccount

Create a dedicated ServiceAccount for Argo Workflows. Avoid using the default ServiceAccount, which usually has insufficient privileges.

```
kubectl create sa argo-sa
```

### Step 3: Create a RoleBinding

Bind the Role you created in step 1 to the ServiceAccount created in step 2 using a RoleBinding.

Example RoleBinding configuration:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: argo-role-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: argo-role
subjects:
- kind: ServiceAccount
  name: argo-sa
```

### **Step 4: Specify the ServiceAccount when submitting Workflows**

When submitting Workflows with Argo, use the `--serviceaccount` flag to specify the ServiceAccount created in step 2:

```
argo submit --serviceaccount argo-sa <your-workflow.yaml>
```

If no ServiceAccount is specified, Argo will use the default ServiceAccount from the namespace it is running in, which typically has insufficient privileges.

By following these steps, you can create and configure a ServiceAccount with the appropriate permissions for Argo Workflows, ensuring that it has the necessary access to Kubernetes resources based on your specific use case. For more information on granting Argo the necessary permissions, refer to the [Argo Workflow RBAC documentation](https://argoproj.github.io/argo-workflows/workflow-rbac/).

## Use tailored permissions

To enhance the security of your Argo Workflows deployment, it is recommended to use tailored permissions. This ensures that the roles you create have the minimum required permissions, following the principle of least privilege. Tailoring permissions granularly helps to reduce the potential impact of security breaches and limits the access to specific resources and actions within the cluster.

Here's how to create tailored permissions for Argo Workflows.

### Step 1: Create a Role with minimal permissions

Start by creating a Role that grants the minimum required permissions for Argo Workflows to function correctly. In this example, we create a Role named `argo-role` with the `list` and `update` permissions on the `workflows.argoproj.io` resource:

```bash
kubectl create role argo-role --verb=list,update --resource=workflows.argoproj.io
```

### Step 2: Identify required resources

To determine the full list of resources that Argo Workflows might need to access, use the `api-resources` command:

```bash
kubectl api-resources --api-group=argoproj.io --namespaced=true -o wide
```

This command lists all the resources within the `argoproj.io` API group that are namespace-scoped. Review the output and identify the resources that your Argo Workflows deployment requires access to. These might include Workflow, WorkflowTemplate, CronWorkflow, and ClusterWorkflowTemplate resources.

### Step 3: Update the Role with required permissions

Based on the identified resources, update the Role with the necessary permissions for each resource. You may need to add new rules or modify existing ones to include the required resources and verbs (e.g., get, list, create, update, delete, watch).

Here's an example of an updated Role configuration:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-role
rules:
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  - workflowtemplates
  - cronworkflows
  - clusterworkflowtemplates
  verbs:
  - list
  - get
  - create
  - update
  - delete
  - watch
```

### Step 4: Apply the updated Role

After updating the Role, save the configuration to a file (e.g., `argo-role.yaml`) and apply it using `kubectl apply`:

```bash
kubectl apply -f argo-role.yaml
```

By following these steps, you can create tailored permissions for your Argo Workflows deployment, ensuring that the associated Roles have the minimum required permissions. This approach helps to improve the security of your environment and follows the principle of least privilege.

## More information

For more information, please see these Argo Workflows resources:

* [Examples on GitHub](https://github.com/argoproj/argo-workflows/tree/master/examples)
* [Slack](https://argoproj.github.io/community/join-slack/)
* [Training on YouTube](https://www.youtube.com/playlist?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo)
* [Argo Blog](https://blog.argoproj.io/)
