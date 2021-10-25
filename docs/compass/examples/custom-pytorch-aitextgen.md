# PyTorch - GPT-2 AITextgen

## Introduction

A custom predictor allows you to deploy your own prediction implementation, useful when the existing serving implementations don't fit your needs. If migrating from Cortex, the custom predictor work exactly the same way as `PythonPredictor` does in Cortex. Most `PythonPredictors` can be converted to custom predictor by copy pasting the code and renaming some variables.

The custom predictor is packaged as a Docker container. It is recommended, but not required, to keep large model files outside of the container image itself and to load them from a storage volume. This example does not follow that pattern. Refer to the [Custom Sentiment](custom-sentiment.md) example for a better production setup. You will need somewhere to publish your Docker image once built. This example leverages [Docker Hub](https://hub.docker.com), where storing public images are free and private images are cheap. [Google Container Registry](https://blog.container-solutions.com/using-google-container-registry-with-kubernetes) and other registries can also be used.

We're deploying the new text generation toolchain for GPT-2, [aitextgen](https://docs.aitextgen.io). It uses PyTorch under the hood. We will serve up the large 1.5B parameter GPT-2 model (1558M) using optimized FP16 on Tesla V100s. The predictor is a direct implementation of [the authors recommendations](https://docs.aitextgen.io/tutorials/generate\_1\_5b/). In our testing, GPU memory usage is greatly reduced thanks to FP16, however single prediction latency is higher than the same model [deployed via Tensorflow serving](gpt-2/).

Make sure you use a GPU enabled Docker image as a base, and that you enable GPU support when loading the model.

To follow along, please clone the manifests from [GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/custom-pytorch-aitextgen).&#x20;

## Getting Started

After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the Inference Service. Clone this repository and folder, and execute all commands in there. We'll be using all the files.

Sign up for a [Docker Hub](https://hub.docker.com) account, or use a different container registry if you already have one. The free plan works perfectly fine, but your container images will be accessible by anyone. This guide assumes a private registry, requiring authentication. Once signed up, create a new repository. For the rest of the guide, we'll assume that the name of the new repository is `aitextgen-model`.

### Build the Docker image

1.  Enter the `custom-predictor` directory. Build and push the Docker image. No modifications are needed to any of the files to follow along. The Docker image can be quite resource intensive to build, as it rebuilds the NVIDIA Apex library with fp16 support. The default Docker tag is `latest`. We strongly discourage you to use this, as containers are cached on the nodes and in other parts of the CoreWeave stack. Once you have pushed to a tag, do not push to that tag again. Below, we use simple versioning by using tag `1` for the first iteration of the image. &#x20;

    ```bash
     export DOCKER_USER=coreweave
     docker build -t $DOCKER_USER/aitextgen-model:1
     docker push $DOCKER_USER/aitextgen-model:1
    ```

### Set up repository access

1.  Create a `Secret` with the Docker Hub credentials. The secret will be named `docker-hub`. This will be used by nodes to pull your private image. Refer to the [Kubernetes Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line) for more details.

    ```bash
    kubectl create secret docker-registry docker-hub --docker-server=https://index.docker.io/v1/ --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
    ```
2.  Tell Kubernetes to use the newly created `Secret` by patching the `ServiceAccount` for your namespace to reference this `Secret`.

    ```bash
    kubectl patch serviceaccounts default --patch "$(cat image-secrets-serviceaccount.patch.yaml)"
    ```

### Deploy the model

1. Modify `aitextgen-inferenceservice.yaml` to reference your docker image.
2.  Apply the resources. This can be used to both create and update existing manifests.

    ```bash
     $ kubectl apply -f aitextgen-inferenceservice.yaml
     inferenceservice.serving.kubeflow.org/aitextgen configured
    ```
3.  List pods to see that the Predictor has launched successfully. This can take a minute, wait for Ready to indicate 2/2.

    ```bash
    $ kubectl get pods
    NAME                                                           READY   STATUS    RESTARTS   AGE
    aitextgen-predictor-default-px8xk-deployment-85bb6787d7-h42xk  2/2     Running   0          34s
    ```

    If the predictor fails to init, look in the logs for clues `kubectl logs aitextgen-predictor-default-px8xk-deployment-85bb6787d7-h42xk kfserving-container`.
4.  Once all the Pods are running, we can get the API endpoint for our model. The API endpoints follow the [Tensorflow V1 HTTP API](https://www.tensorflow.org/tfx/serving/api\_rest#predict\_api).

    ```bash
    $ kubectl get inferenceservices
    NAME        URL                                                                          READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
    aitextgen   http://aitextgen.tenant-test.knative.chi.coreweave.com/v1/models/aitextgen   True    100                                23h
    ```

    The URL in the output is the public API URL for your newly deployed model. A HTTPs endpoint is also available, however this one bypasses any canary deployments. Retrieve this one with `kubectl get ksvc`.
5.  Run a test prediction on the URL from above. Remember to add the `:predict` postfix.

    ```bash
     $ curl -d @sample.json http://aitextgen.tenant-test.knative.chi.coreweave.com/v1/models/sentiment:predict
    {"predictions": ["positive"]}
    ```
6.  Remove the `InferenceService`. This will delete all the associated resources, except for your model storage and sleep Deployment.

    ```bash
    $ kubectl delete inferenceservices aitextgen
    inferenceservice.serving.kubeflow.org "aitextgen" deleted
    ```
