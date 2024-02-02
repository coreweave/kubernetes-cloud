# CoreWeave-powered Kubernetes Inference Quickstart
This is an example use case of a Knative service that deploys inference pods that run on the 
[vLLM inference backend](https://github.com/vllm-project/vllm/) and load models using CoreWeave's `tensorizer`. The
container images used are all optimized from the CoreWeave `ml-containers` repo to be both lightweight and performant.

The manifest used here first runs a serialization job on the desired model if tensors don't exist at the specified 
location (and is idempotent on further executions once tensors exist) to ensure that pods can reach the tensors
to deserialize at runtime. The Job container image can be given the following CLI arguments:

<PLACEHOLDER FOR `hf.serialization.py` CLI ARGS>

and the inference container sports the [usual CLI engine arguments]
(https://docs.vllm.ai/en/latest/models/engine_args.html) from vLLM as well as additional ones that allow you to
fine-tune `tensorizer`'s support further:

<PLACEHOLDER FOR CLI ARGS FROM `tensorizer` INTEGRATION>
