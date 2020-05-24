# README

## Introduction

Deploying a model hosted in Amazon S3 is straightforward. The small variant of the GPT-2 model is used here, which fits perfectly into GPUs with 8GB of VRAM. You will need an Amazon S3 access key and secret to run this example. The model is already uploaded to our public S3 bucket.

### Transformer

A transformer is provided to translate input and output text to/from tensors. A transformer is not required and the predictor can be queried directly with input and output tensors. How to work directly with the predictor can be found in the [KFServe Documentation](https://github.com/kubeflow/kfserving/tree/master/docs/samples/tensorflow). The API is compatible with [TensorFlow Serving REST](https://www.tensorflow.org/tfx/serving/api_rest).

## Getting Started

After installing `kubectl` and adding your CoreWeave Cloud access credentials, the following steps will deploy the Inference Service.

1. Edit the `s3-secret.yaml` resource to contain your S3 access credentials. [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) are base64 encoded, you will have to base64 encode the credentials before putting them in the file.

   ```bash
   $ echo -n "LLAFRHSSEXAMPLE" | base64
   TExBRlJIU1NTQVpCNEk1QkpNUQ==
   $ echo -n "II3Bli9tmYQ6EXAMPLE" | base64
   SUkzQmxpOXRtWVE2YXNkYWQxMTExYQ==
   ```

   Should end up in the secret as:

   ```yaml
   data:
     awsAccessKeyID: TExBRlJIU1NTQVpCNEk1QkpNUQ==
     awsSecretAccessKey: SUkzQmxpOXRtWVE2YXNkYWQxMTExYQ==
   ```

2. Apply the resources. This can be used to both create and update existing manifests

   ```bash
    $ kubectl apply -f s3-secret-real.yaml
    secret/s3-secret created
    $ kubectl apply -f s3-serviceaccount.yaml
    serviceaccount/s3-sa created
    $ kubectl apply -f gpt-s3-inferenceservice.yaml
    inferenceservice.serving.kubeflow.org/gpt-s3 created
   ```

3. List pods to see that the Transformer and Predictor have launched successfully

   ```bash
   $ kubectl get pods
   NAME                                                           READY   STATUS    RESTARTS   AGE
   gpt-s3-predictor-default-ljxhm-deployment-86596d6846-kwnkd     2/2     Running   0          34s
   gpt-s3-transformer-default-f5lf9-deployment-86bc7b4fd8-g8m69   2/2     Running   0          34s
   ```

   If the predictor fails to init, this is most likely due to issues loading the resource from S3. `kubectl logs gpt-s3-predictor-default-ljxhm-deployment-86596d6846-kwnkd storage-initializer` will contain an error if so.

4. Once all the Pods are running, we can get the API endpoint for our model

   ```bash
   $ kubectl get ksvc
   NAME                         URL                                                                       LATESTCREATED                      LATESTREADY                        READY   REASON
   gpt-s3-predictor-default     http://gpt-s3-predictor-default.tenant-test.knative.chi.coreweave.com     gpt-s3-predictor-default-ljxhm     gpt-s3-predictor-default-ljxhm     True
   gpt-s3-transformer-default   http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com   gpt-s3-transformer-default-f5lf9   gpt-s3-transformer-default-f5lf9   True
   ```

   We want to use the transformer endpoint to be able to make requests in cleartext. Ensure that both services are listed as Ready.

5. The model is now available to access over the Internet. Use `curl` to test it out.

   ```bash
    $ curl -d '{"instances": ["That was easy"]}' http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-s3:predict
    {"predictions": ["That was easy to say, what else would you do, what would you do, would you say to your daughter and say to her, 'Where is the work you're doing, where is the work you're working on, and how are you doing it?' and she was like, 'I'm not going to be here, I can't do it!' and she became, you know, frustrated. And I think there's a different type of anxiety. There's this self-pity that comes in, and that's also why they call their child a 'brilliant' child.\n\nShe was always saying that when she was a little girl, there was something really important to do. But she really doesn't go. She knows that whatever she does, when she's ready, she's going to go into any school or program and that she's going to do. And she really needs to do that, because it's just so much more exciting to her now.\n\nIt made her less able to put her mind at the 'solution' to her child's difficulties \u2013 even as she had more opportunities than I or anyone could ever do, and at a time when we were trying a lot of things to find the balance in the world. And I"]}
   ```

6. Open a couple of terminal windows
   * Run `watch kubectl get pods` in one of them
   * In the others, loop a request to the model: `while true; do curl -d '{"instances": ["That was easy"]}' http://gpt-s3-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-s3:predict; done`
   * The example service in this directory defines a desired concurrency of 4, open at least 4 terminal windows to ensure that scaling is triggered
7. After a minute, you will see the autoscaler adding additional predictor pods to handle the load.

   ```bash
   NAME                                                           READY   STATUS            RESTARTS   AGE
   gpt-s3-predictor-default-ljxhm-deployment-86596d6846-66kgl     0/2     PodInitializing   0          27s
   gpt-s3-predictor-default-ljxhm-deployment-86596d6846-kwnkd     2/2     Running           0          14m
   gpt-s3-transformer-default-f5lf9-deployment-86bc7b4fd8-g8m69   2/2     Running           0          14m
   ```

   If you stop the requests, the additional Pod will automatically be removed.

8. Remove the inference service

   ```bash
   $ kubectl delete inferenceservices gpt-s3                                                                 git:(add-btc|✚1…
   inferenceservice.serving.kubeflow.org "gpt-s3" deleted
   ```

