# CoreWeave-powered Kubernetes Inference Quickstart
This is an example use case of a Knative service that deploys inference pods 
that run on the [vLLM inference backend](https://github.com/vllm-project/vllm/) and loads models using CoreWeave's 
`tensorizer`. The container images used are all optimized from the CoreWeave 
`ml-containers` repo to be both lightweight and performant. 

## Supercharging Inference with CoreWeave
CoreWeave makes use of multiple different optimizations to ensure that your
inference workloads are as fast and efficient as possible. This example 
particularly demonstrates the reductions in latency and cost that can be
achieved by using CoreWeave's `tensorizer` to load models, and using 
CoreWeave's ML container images for inference.

With `tensorizer`, models can be loaded extremely quickly from HTTP/HTTPS,
Redis, or S3 endpoints. This is significantly faster than packing a container
image with the model artifacts and loading locally, especially when making
use of CoreWeave's accelerated object storage. 


CoreWeave's `ml-containers` repo contains a variety of container images that 
are optimized for machine learning workloads. These images are optimized to be
as lightweight as possible to further reduce pod startup time.

## Getting Started

The chart used here first runs a serialization job on the desired model if 
tensors don't exist at the specified location (and is idempotent on further 
executions once tensors exist) to ensure that pods can reach the tensors
to deserialize at runtime. The Job container image CLI args can be set
within the `serialization` part of `values.yaml`. 

- `model_type`: Whether to use `transformers` or `diffusers` frameworks for 
serialization.
- `input_directory`: Path to model files or HF model ID
- `output_prefix`: Path to directory where model artifacts will be stored. 
Can be a local path or S3.
- `overwrite`: If tensors are found at `output_prefix`, flag to overwrite 
existing tensors. Otherwise skips serialization.
- `validate`: Flag to deserialize and validate tensor sameness

In addition, to serialize to an S3 bucket, credentials can be stored in
`s3_access_key` and `s3_secret_key`.

The inference container sports the 
[usual CLI engine arguments](https://docs.vllm.ai/en/latest/models/engine_args.html) from vLLM as well as additional 
ones that allow you to fine-tune `tensorizer`'s support further.

To use `tensorizer` when loading models, `tensorizer` is set 
for `--load-format` and `--tensorizer-uri` can expect a local path to serialized
weights or an S3 endpoint. S3 authentication can be set with `S3_ACCESS_KEY_ID` 
and `S3_SECRET_ACCESS_KEY` environment variables. This is done for you in
`service.yaml`, and reads from `values.yaml`:

- `name`: Name of the service
- `model`: HF model ID
- `tensorizer_uri`: Path to model tensors. If using the model serialized by the
previous job, this would be under `model.tensors` in the `output_prefix`. 





