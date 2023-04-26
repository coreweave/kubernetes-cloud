# FastAI Sentiment

A **custom predictor** allows you to deploy your own prediction implementation, useful when the existing serving implementations don't fit your needs. If migrating from Cortex, the custom predictor work exactly the same way as `PythonPredictor` does in Cortex. Most `PythonPredictors` can be converted to custom predictor by copy pasting the code and renaming some variables.

The custom predictor is packaged as a Docker container. It is recommended, but not required, to keep large model files outside of the container image itself and to load them from a storage volume. This example follows that pattern. You will need somewhere to publish your Docker image once built. This example leverages [Docker Hub](https://hub.docker.com), where storing public images are free and private images are cheap. [Google Container Registry](https://blog.container-solutions.com/using-google-container-registry-with-kubernetes) and other registries can also be used.

We're deploying a sentiment analyzer built with [FastAI](https://docs.fast.ai/text.html). It uses PyTorch under the hood, but working with the FastAI API is easier, which is why we wrap it instead of using a PyTorch predictor. The same principles can be applied to any framework.

Make sure you use a GPU enabled Docker image as a base, and that you enable GPU support when loading the model.

## Tutorial source code

To follow along with this tutorial, first clone the manifests from GitHub:

{% embed url="https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/custom-sentiment" %}
Tutorial source code for FastAI Sentiment
{% endembed %}

## Get started

After installing `kubectl` and [adding your CoreWeave Cloud access credentials](../../../../coreweave-kubernetes/getting-started.md#obtain-coreweave-access-credentials), clone the repository and folder for the tutorial source code.

This guide assumes use of a private container registry requiring authentication. Recommended solutions include using the [Docker Registry application directly on CoreWeave Cloud](../../../../coreweave-kubernetes/custom-containers.md), or else creating and using [a Docker Hub account](https://hub.docker.com/). Otherwise, another private container registry may work.

Once you have configured Docker Registry or created a Docker Hub account, create a new repository. For the rest of this guide, we'll assume that the name of the new repository is `fastai-sentiment`.  No modifications are needed to any of these files to follow along.

### Build the Docker image

From the cloned source code directory, enter the `custom-predictor` directory. From here, build and push the Docker image.

```bash
 export DOCKER_USER=coreweave
 docker build -t $DOCKER_USER/fastai-sentiment:1
 docker push $DOCKER_USER/fastai-sentiment:1
```

{% hint style="warning" %}
**Important**

The default Docker tag is `latest`. It is strongly **discouraged** to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack. Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image.
{% endhint %}

### Set up repository access

Using `kubectl create secret`, create a new `Secret` using your login credentials, and name it `docker-repository`, or something that makes sense to you. This will be used by the nodes to [pull your private image.](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line)

{% code overflow="wrap" %}
```bash
kubectl create secret docker-registry docker-hub --docker-server=https://index.docker.io/v1/ --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```
{% endcode %}

Tell Kubernetes to use the newly created `Secret` by patching the `ServiceAccount` for your namespace to reference this `Secret`.

{% code overflow="wrap" %}
```bash
kubectl patch serviceaccounts default --patch "$(cat image-secrets-serviceaccount.patch.yaml)"
```
{% endcode %}

### Download the model

For performance reasons, the model is not bundled within the Docker image, so a [Storage Volume](../../../../storage/storage/using-storage-kubectl.md) is required, to which the pre-trained model will be downloaded. Storage Volumes are allocated using a Kubernetes `PersistentVolumeClaim`, or PVC. A simple container will also be deployed, which can be used to copy files to the newly created Volume.

From the `custom-sentiment` directory, use `kubectl apply` to deploy the `PersistentVolumeClaim` (`model-storage-pvc.yaml`).

```bash
$ kubectl apply -f model-storage-pvc.yaml
persistentvolumeclaim/model-storage created
```

Then, deploy the manifest for the `sleep` container (`sleep-deployment.yaml`).

```bash
$ kubectl apply -f sleep-deployment.yaml
deployment.apps/sleep created
```

The volume is mounted to `/models` inside the `sleep` container. Download the pre-trained model locally, then create a directory for it in the shared volume to upload it into. The name of the sleep Pod is assigned to a variable using `kubectl`. You can also get the name with `kubectl get pods`, as is done here:

{% code overflow="wrap" %}
```bash
curl -O https://bstore.coreweave.com/blobstore/models/fastai-sentiment/export.pkl

export SLEEP_POD=$(kubectl get pod -l "app.kubernetes.io/name=sleep" -o jsonpath='{.items[0].metadata.name}') # Export the value of the randomly-assigned variable to the $SLEEP_POD environment variable

kubectl exec -it $SLEEP_POD -- sh -c 'mkdir /models/sentiment' # Create a new directory inside the sleep pod at /models/senitment

kubectl cp ./export.pkl $SLEEP_POD:/models/sentiment/ # Copy the locally-downloaded model into that new directory
```
{% endcode %}

**Optional –**  The model may also be downloaded from CoreWeave Object Storage or from Amazon S3. The Amazon S3 CLI utilities already exist in the sleep container to allow for this.

{% code overflow="wrap" %}
```bash
$ export SLEEP_POD=$(kubectl get pod -l "app.kubernetes.io/name=sleep" -o jsonpath='{.items[0].metadata.name}')
$ kubectl exec -it $SLEEP_POD -- sh
$# aws configure
$# mkdir /models/sentiment
$# aws s3 sync --recursive s3://mybucket /models/sentiment/
```
{% endcode %}

### Deploy the model

Modify the `sentiment-inferenceservice.yaml` to reference your own Docker image under `.spec.predictor.containers.image`.

```yaml
spec:
  predictor:
    maxReplicas: 10
    minReplicas: 0
    containerConcurrency: 1
    containers:
    - name: kfserving-container
      image: coreweave/my-fastai-sentiment-container:1
      env:
```

Apply the resources using `kubectl apply`.

```bash
 $ kubectl apply -f sentiment-inferenceservice.yaml
 inferenceservice.serving.kubeflow.org/sentiment configured
```

List the Pods to ensure the Predictor has launched successfully. This may take a minute - wait for the `READY` column to indicate that all Pods are `Running`.

```bash
$ kubectl get pods

NAME                                                           READY   STATUS    RESTARTS   AGE
sentiment-predictor-default-px8xk-deployment-85bb6787d7-h42xk  2/2     Running   0          34s
```

If the predictor fails to init, check the logs for insights as to why. For example:

{% code overflow="wrap" %}
```bash
$ kubectl logs sentiment-predictor-default-px8xk-deployment-85bb6787d7-h42xk kfserving-container
```
{% endcode %}

### Test the model

Once all the Pods are running, the API endpoint for the model will be accessible as a URL provided in the `InferenceService` object. The API endpoints follow the [Tensorflow V1 HTTP API](https://www.tensorflow.org/tfx/serving/api\_rest#predict\_api).

```bash
$ kubectl get inferenceservices

NAME        URL                                                                          READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
sentiment   http://sentiment.tenant-test.knative.chi.coreweave.com/v1/models/sentiment   True    100                                23h
```

The URL given in the output of `kubectl get` is the public API URL for your newly deployed model.

{% hint style="info" %}
**Note**

A HTTPS endpoint is also available, however the HTTPS endpoint bypasses any canary deployments. Retrieve it using `kubectl get ksvc`.
{% endhint %}

Run a test prediction by querying the acquired URL. Remember to add the `:predict` postfix.

{% code overflow="wrap" %}
```bash
 $ curl -d @sample.json http://sentiment.tenant-test.knative.chi.coreweave.com/v1/models/sentiment:predict
{"predictions": ["positive"]}
```
{% endcode %}

## Clean up

Delete the `InferenceService`. This will delete all the associated resources, except for your model storage and sleep Deployment.

```bash
$ kubectl delete inferenceservices sentiment
inferenceservice.serving.kubeflow.org "sentiment" deleted
```
