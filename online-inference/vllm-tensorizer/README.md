# CoreWeave-powered Kubernetes Inference Quickstart
This is an example use case of a Knative service that deploys inference pods that run on the 
[vLLM inference backend](https://github.com/vllm-project/vllm/) and loads models using CoreWeave's `tensorizer`. The
container images used are all optimized from the CoreWeave `ml-containers` repo to be both lightweight and performant.

The manifest used here first runs a serialization job on the desired model if tensors don't exist at the specified 
location (and is idempotent on further executions once tensors exist) to ensure that pods can reach the tensors
to deserialize at runtime. The Job container image is given the following CLI arguments:

- `input-directory`: Path to model files or HF model ID
- `output_prefix`: Path to directory where model artifacts will be stored. Can be a local path or S3.

And optionally:
- `--model-type`: Whether to use `transformers` or `diffusers` frameworks for serialization.
- `--validate`: Flag to deserialize and validate tensor sameness 
- `--force`: If tensors are found at `output_prefix`, flag to overwrite existing tensors. Otherwise skips serialization.
- `-q`, `--quiet`: Less verbose output
- `-v`, `--verbose`: More verbose output

and the inference container sports the 
[usual CLI engine arguments](https://docs.vllm.ai/en/latest/models/engine_args.html) from vLLM as well as additional 
ones that allow you to fine-tune `tensorizer`'s support further, such as `--plaid-mode`. To use `tensorizer` when
loading models, `tensorizer` is set for `--load-format` and `--download-dir` can expect a local path to serialized
weights or an S3 endpoint. S3 authentication can be set with `S3_ACCESS_KEY_ID` and `S3_SECRET_ACCESS_KEY` environment
variables.

