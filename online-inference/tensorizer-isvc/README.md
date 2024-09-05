# GPT-J InferenceService with Tensorizer & HuggingFace

The following instructions will guide you through setting up an
[InferenceService](https://docs.coreweave.com/coreweave-machine-learning-and-ai/how-to-guides-and-tutorials/examples)
with [Tensorizer](https://github.com/coreweave/tensorizer)
or [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
serving [GPT-J-6B](https://huggingface.co/EleutherAI/gpt-j-6b).

From the root of `tensorizer-isvc`:

- Provision a [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
  - `kubectl apply -f pvc.yaml`
- Download the model to the PVC
  - `kubectl apply -f model-download/model-download-job.yaml`
- Run the HuggingFace InferenceService (currently using KServe)
  - `kubectl apply -f tensorizer_hf_isvc/kserve/hf-isvc.yaml`
- Or, run the Tensorizer InferenceService (currently using KServe)
  - `kubectl apply -f tensorizer_hf_isvc/kserve/tensorizer-isvc.yaml`
- View the InferenceService deployment information and URL
  - `kubectl get isvc`
  - `http://` may be required in place of `https://` when connecting to the displayed URL
- Test the InferenceService
  - The KServe services use [KServe's V1 protocol](https://kserve.github.io/website/0.10/modelserving/data_plane/v1_protocol/):
    ```bash
    curl http://<URL>/v1/models/gptj:predict -X POST -H 'Content-Type: application/json' -d '{"instances": ["Hello!"]}'
    ```
  - The Flask services simply encode queries into the URL path component:
    ```bash
    curl http://<URL>/predict/Hello%21
    ```
- Run the benchmark
  - `python benchmark/load_test.py --kserve --url=<ISVC_URL> --requests=<NUMBER_OF_REQUESTS>`
  - `load_test.py` defaults to running async requests with [`aiohttp`](https://pypi.org/project/aiohttp/)
  - `--sync` may be added to the command line to instead send requests sequentially
    using [`requests`](https://pypi.org/project/requests/)
- Delete the InferenceService
  - `kubectl delete -f tensorizer_hf_isvc/<...>/<...>-isvc.yaml`
  - Use the same manifest file that was used with `kubectl apply`

Each InferenceService manifest (`*-isvc.yaml`) runs a container defined
in a Dockerfile in its same directory, such as `tensorizer_hf_isvc/kserve/Dockerfile`.
These may be changed and rebuilt to customize the behavior of the InferenceService.

> Note: The build context for each Dockerfile is its parent directory, so the build commands look like:
> ```bash
> docker build ./tensorizer_hf_isvc -f ./tensorizer_hf_isvc/kserve/Dockerfile
> docker build ./tensorizer_hf_isvc -f ./tensorizer_hf_isvc/flask/Dockerfile
> ```
