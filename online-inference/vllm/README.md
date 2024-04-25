This folder contains instructions to run the vLLM inference server.

Some of the features include:

1. Serialize HuggingFace models supported here to vLLM based format: https://github.com/vllm-project/vllm?tab=readme-ov-file#about
2. Tensorizer support for fast model deserialization and loading from vLLM 

To run the example:

1. Run `kubectl apply -f 00-optional-s3-secret.yaml` and replace access_key, secret_key and host_url
2. Run `kubectl apply -f 01-optional-s3-serialize-job.yaml and replace --model EleutherAI/pythia-70m, --serialized-directory s3://my-bucket/ and optionally --suffix vllm
3. Run `kubectl apply -f 02-inference-service.yaml and replace --model EleutherAI/pythia-70m and --model-loader-extra-config '{"tensorizer_uri": "s3://model-store/vllm/EleutherAI/pythia-70m/vllm/model.tensors"}' with your serialized model path

You should have an inference service running a container with an OpenAI compatible server. 

You can use the client to interact with it. More information about the client can be found here: https://docs.vllm.ai/en/latest/getting_started/quickstart.html
