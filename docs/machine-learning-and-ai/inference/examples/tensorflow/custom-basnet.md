# Object Detection and Background Removal with BASNET

In this tutorial, we'll deploy an auto-scaling Inference service from a pre-existing Docker image.

This can be useful when deploying off-the-shelf models that aren't available as ie. Tensorflow SavedModels. One example of this is the [IBM COCO Based Object Detector](https://github.com/IBM/MAX-Object-Detector). An [example InferenceService](https://github.com/coreweave/kubernetes-cloud/tree/ed7ecb3d5786e960506bc20bb1e2d044ad914555/online-inference/custom-basnet/object-detector-inferenceservice.yaml) for that also exists in this repository. The rest of this example will focus on a [public wrapped version](https://github.com/cyrildiagne/basnet-http) of the [BASNet object detection model](https://github.com/NathanUA/BASNet). This example and the test client is based on work by [Cyril Diagne](https://twitter.com/cyrildiagne/status/1256916982764646402).

To follow along, clone the manifests from [GitHub](https://github.com/coreweave/kubernetes-cloud/tree/master/online-inference/custom-basnet).

**Input**\
![input](../../../../.gitbook/assets/test.png)

**Output**\
![output](../../../../../online-inference/custom-basnet/client/expected\_output.png)

## Getting Started

After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the Inference Service. Clone all the files in this repository to follow along.

1.  Apply the resources. This can be used to both create and update existing manifests

    ```bash
     $ kubectl apply -f basnet-inferenceservice.yaml
     inferenceservice.serving.kubeflow.org/basnet configured
    ```
2.  List pods to see that the Transformer and Predictor have launched successfully

    ```bash
    $ kubectl get pods
    NAME                                                           READY   STATUS    RESTARTS   AGE
    basnet-predictor-default-sj9kr-deployment-76b67d669-4gjrp      2/2     Running   0          34s
    ```

    If the predictor fails to init, look in the logs for clues `kubectl logs basnet-predictor-default-sj9kr-deployment-76b67d669-4gjrp kfserving-container`.
3.  Once all the Pods are running, we can get the API endpoint for our model. Since this model doesn't adhere to the [Tensorflow V1 HTTP API](https://www.tensorflow.org/tfx/serving/api\_rest#predict\_api), we can't use the API endpoint provided by `kubectl get inferenceservices`. We have to hit up the predictor directly.

    ```bash
    $ kubectl get ksvc
    NAME                         URL                                                                       LATESTCREATED                      LATESTREADY                        READY   REASON
    basnet-predictor-default     https://basnet-predictor-default.tenant-test.knative.chi.coreweave.com    basnet-predictor-default-sj9kr     basnet-predictor-default-sj9kr     True
    ```

    The URL in the output is the public API URL for your newly deployed model.
4.  Enter the client directory. You can either run the test client locally or in docker. The output will be in `images/output.png`.

    ```bash
     $ cd client/
     $ export SERVICE_URL=https://basnet-predictor-default.tenant-test.knative.chi.coreweave.com
     $ docker build -t test .; docker run --rm -it -v $(pwd)/images:/app/images test --basnet_service_host $SERVICE_URL
     INFO:root: > sending to BASNet...
     INFO:root:200
     INFO:root: > saving results...
     INFO:root: > opening mask...
     INFO:root: > compositing final image...
     INFO:root: > saving final image...
     $ open images/output.png
    ```
5.  Remove the inference service

    ```bash
    $ kubectl delete inferenceservices basnet
    inferenceservice.serving.kubeflow.org "basnet" deleted
    ```
