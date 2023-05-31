Please follow the instructions to run an Inference Service with Tensorizer or Huggingface for GPT:

From the root of tensorizer-isvc:

- Use a PVC: k apply -f pvc.yaml
- Download the model to PVC: k apply -f model-download-job.yaml
- Run the HF Inference Service (currently using Flask): k apply -f gptj_6b_hf/flask/hf-isvc.yaml
- Run the Tensorizer Inference Service (currently using Flask): k apply -f gptj_6b_tensorizer/flask/hf-isvc.yaml
- Run the benchmark: python3 benchmark/load_test.py --url=<ISVC_URL> --requests=<NUMBER_OF_REQUESTS> (defaults to async, can change to run sequentially)

All Dockerfiles are available in their respective folders to build and use. 

