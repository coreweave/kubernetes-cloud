# PVC Model Serving

## Introduction

This example is virtually the same as the [S3 based one](service-s3.md), instead of repeating all steps please read that example first as this is an abbreviated version.

## Getting Started

1. Follow the guide to [export the model through Jupyter](jupyter-pvc.md) first. The model can be placed into a CoreWeave filesystem through many other methods, such as via an SSH or rsync container. Please note that this repository does not include the PVC definition, as it is [defined in the Jupyter repository](https://github.com/coreweave/kubernetes-cloud/tree/ed7ecb3d5786e960506bc20bb1e2d044ad914555/online-inference/gpt-2/jupyter-pvc/model-storage-pvc.yaml).
2. Apply the resources. This can be used to both create and update existing manifests

   ```bash
    $ kubectl apply -f gpt-pvc-inferenceservice.yaml
    inferenceservice.serving.kubeflow.org/gpt-pvc created
   ```

3. List pods to see that the Transformer and Predictor have launched successfully

   ```bash
   $ kubectl get pods
   NAME                                                           READY   STATUS    RESTARTS   AGE
   gpt-pvc-predictor-default-ljxhm-deployment-86596d6846-kwnkd     2/2     Running   0          34s
   gpt-pvc-transformer-default-f5lf9-deployment-86bc7b4fd8-g8m69   2/2     Running   0          34s
   ```

   If the predictor fails to start, it is probably due to the model being saved at the wrong path. `kubectl logs gpt-pvc-predictor-default-ljxhm-deployment-86596d6846-kwnkd kfserving-container` will contain an error if so.

4. Once all the Pods are running, we can get the API endpoint for our model

   ```bash
   $ kubectl get ksvc
   NAME                         URL                                                                       LATESTCREATED                      LATESTREADY                        READY   REASON
   gpt-pvc-predictor-default     http://gpt-pvc-predictor-default.tenant-test.knative.chi.coreweave.com     gpt-pvc-predictor-default-ljxhm     gpt-pvc-predictor-default-ljxhm     True
   gpt-pvc-transformer-default   http://gpt-pvc-transformer-default.tenant-test.knative.chi.coreweave.com   gpt-pvc-transformer-default-f5lf9   gpt-pvc-transformer-default-f5lf9   True
   ```

   We want to use the transformer endpoint to be able to make requests in cleartext. Ensure that both services are listed as Ready.

5. The model is now available to access over the Internet. Use `curl` to test it out.

   ```bash
    $ curl -d '{"instances": ["That was easy"]}' http://gpt-pvc-transformer-default.tenant-test.knative.chi.coreweave.com/v1/models/gpt-pvc:predict
    {"predictions": ["That was easy to say, what else would you do, what would you do, would you say to your daughter and say to her, 'Where is the work you're doing, where is the work you're working on, and how are you doing it?' and she was like, 'I'm not going to be here, I can't do it!' and she became, you know, frustrated. And I think there's a different type of anxiety. There's this self-pity that comes in, and that's also why they call their child a 'brilliant' child.\n\nShe was always saying that when she was a little girl, there was something really important to do. But she really doesn't go. She knows that whatever she does, when she's ready, she's going to go into any school or program and that she's going to do. And she really needs to do that, because it's just so much more exciting to her now.\n\nIt made her less able to put her mind at the 'solution' to her child's difficulties \u2013 even as she had more opportunities than I or anyone could ever do, and at a time when we were trying a lot of things to find the balance in the world. And I"]}
   ```

