# GPT-J InferenceService with Tensorizer & HuggingFace

The following instructions will guide you through setting up an
[InferenceService](https://docs.coreweave.com/machine-learning-and-ai/inference/online-inference)
with [Tensorizer](https://github.com/coreweave/tensorizer)
or [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
serving [GPT-J-6B](https://huggingface.co/EleutherAI/gpt-j-6b):

From the root of `tensorizer-isvc`:

- Provision a [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
  - `kubectl apply -f pvc.yaml`
- Download the model to the PVC
  - `kubectl apply -f model-download/model-download-job.yaml`
- Run the HuggingFace InferenceService (currently using Flask)
  - `kubectl apply -f gptj_6b_hf/flask/hf-isvc.yaml`
- Or, run the Tensorizer InferenceService (currently using Flask)
  - `kubectl apply -f gptj_6b_tensorizer/flask/tensorizer-isvc.yaml`
- Run the benchmark
  - `python3 benchmark/load_test.py --url=<ISVC_URL> --requests=<NUMBER_OF_REQUESTS>`
  - `load_test.py` defaults to running async requests with [`aiohttp`](https://pypi.org/project/aiohttp/)
  - `--sync` may be added to the command line to instead send requests sequentially
    using [`requests`](https://pypi.org/project/requests/)

Each InferenceService manifest (`*-isvc.yaml`) runs a container defined
in a Dockerfile in its same directory, such as `gptj_6b_tensorizer/flask/Dockerfile`.
These may be changed and rebuilt to customize the behavior of the InferenceService.
