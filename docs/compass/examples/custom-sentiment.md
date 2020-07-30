# PyTorch - FastAI Sentiment

## Introduction

A custom predictor allows you to deploy your own prediction implementation, useful when the existing serving implementations don't fit your needs. If migrating from Cortex, the custom predictor work exactly the same way as `PythonPredictor` does in Cortex. Most `PythonPredictors` can be converted to custom predictor by copy pasting the code and renaming some variables.

The custom predictor is packaged as a Docker container. It is recommended, but not required, to keep large model files outside of the container image itself and to load them from a storage volume. This example follows that pattern. You will need somewhere to publish your Docker image once built. This example leverages [Docker Hub](https://hub.docker.com), where storing public images are free and private images are cheap. [Google Container Registry](https://blog.container-solutions.com/using-google-container-registry-with-kubernetes) and other registries can also be used.

We're deploying a sentiment analyzer built with [FastAI](https://docs.fast.ai/text.html). It uses PyTorch under the hood, but working with the FastAI API is easier, which is why we wrap it instead of using a PyTorch predictor. The same principles can be applied to any framework.

Make sure you use a GPU enabled Docker image as a base, and that you enable GPU support when loading the model.

To follow along, please clone the manifests from [GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/custom-sentiment).

## Getting Started

After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the Inference Service. Clone this repository and folder, and execute all commands in there. We'll be using all the files.

Sign up for a [Docker Hub](https://hub.docker.com) account, or use a different container registry if you already have one. The free plan works perfectly fine, but your container images will be accessible by anyone. This guide assumes a private registry, requiring authentication. Once signed up, create a new repository. For the rest of the guide, we'll assume that the name of the new repository is `fastai-sentiment`.

### Build the Docker image

1. Enter the `custom-predictor` directory. Build and push the Docker image. No modifications are needed to any of the files to follow along. The default Docker tag is `latest`. We strongly discourage you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack. Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image.  

   ```bash
    export DOCKER_USER=coreweave
    docker build -t $DOCKER_USER/fastai-sentiment:1
    docker push $DOCKER_USER/fastai-sentiment:1
   ```

### Set up repository access

1. Create a `Secret` with the Docker Hub credentials. The secret will be named `docker-hub`. This will be used by nodes to pull your private image. Refer to the [Kubernetes Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line) for more details.

   ```bash
   kubectl create secret docker-registry docker-hub --docker-server=https://index.docker.io/v1/ --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
   ```

2. Tell Kubernetes to use the newly created `Secret` by patching the `ServiceAccount` for your namespace to reference this `Secret`.

   ```bash
   kubectl patch serviceaccounts default --patch "$(cat image-secrets-serviceaccount.patch.yaml)"
   ```

### Download the model

As we don't want to bundle the model in the Docker image for performance reasons, a storage volume needs to be set up and the pre-trained model downloaded to it. Storage volumes are allocated using a Kubernetes `PersistentVolumeClaim`. We'll also deploy a simple container that we can use to copy files to our newly created volume.

1. Apply the `PersistentVolumeClaim` and the manifest for the `sleep` container.

   ```bash
   $ kubectl apply -f model-storage-pvc.yaml
   persistentvolumeclaim/model-storage created
   $ kubectl apply -f sleep-deployment.yaml
   deployment.apps/sleep created
   ```

2. The volume is mounted to `/models` inside the `sleep` container. Download the pre-trained model locally, create a directory for it in the shared volume and upload it there. The name of the sleep Pod is assigned to a variable using `kubectl`. You can also get the name with `kubectl get pods`.

   ```bash
   curl -O https://bstore.coreweave.com/blobstore/models/fastai-sentiment/export.pkl

   export SLEEP_POD=$(kubectl get pod -l "app.kubernetes.io/name=sleep" -o jsonpath='{.items[0].metadata.name}')
   kubectl exec -it $SLEEP_POD -- sh -c 'mkdir /models/sentiment'
   kubectl cp ./export.pkl $SLEEP_POD:/models/sentiment/
   ```

3. **\(Optional\)** Instead of copying the model from the local filesystem, the model can be downloaded from Amazon S3. The Amazon CLI utilities already exist in the sleep container.

   ```bash
   $ export SLEEP_POD=$(kubectl get pod -l "app.kubernetes.io/name=sleep" -o jsonpath='{.items[0].metadata.name}')
   $ kubectl exec -it $SLEEP_POD -- sh
   $# aws configure
   $# mkdir /models/sentiment
   $# aws s3 sync --recursive s3://mybucket /models/sentiment/
   ```

### Deploy the model

1. Modify `sentiment-inferenceservice.yaml` to reference your docker image.
2. Apply the resources. This can be used to both create and update existing manifests.

   ```bash
    $ kubectl apply -f sentiment-inferenceservice.yaml
    inferenceservice.serving.kubeflow.org/sentiment configured
   ```

3. List pods to see that the Predictor has launched successfully. This can take a minute, wait for Ready to indicate 2/2.

   ```bash
   $ kubectl get pods
   NAME                                                           READY   STATUS    RESTARTS   AGE
   sentiment-predictor-default-px8xk-deployment-85bb6787d7-h42xk  2/2     Running   0          34s
   ```

   If the predictor fails to init, look in the logs for clues `kubectl logs sentiment-predictor-default-px8xk-deployment-85bb6787d7-h42xk kfserving-container`.

4. Once all the Pods are running, we can get the API endpoint for our model. The API endpoints follow the [Tensorflow V1 HTTP API](https://www.tensorflow.org/tfx/serving/api_rest#predict_api).

   ```bash
   $ kubectl get inferenceservices
   NAME        URL                                                                          READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
   sentiment   http://sentiment.tenant-test.knative.chi.coreweave.com/v1/models/sentiment   True    100                                23h
   ```

   The URL in the output is the public API URL for your newly deployed model. A HTTPs endpoint is also available, however this one bypasses any canary deployments. Retrieve this one with `kubectl get ksvc`.

5. Run a test prediction on the URL from above. Remember to add the `:predict` postfix.

   ```bash
    $ curl -d @sample.json http://sentiment.tenant-test.knative.chi.coreweave.com/v1/models/sentiment:predict
   {"predictions": ["positive"]}
   ```

6. Remove the `InferenceService`. This will delete all the associated resources, except for your model storage and sleep Deployment.

   ```bash
   $ kubectl delete inferenceservices sentiment
   inferenceservice.serving.kubeflow.org "sentiment" deleted
   ```

