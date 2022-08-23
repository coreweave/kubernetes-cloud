# make sure you're logged in with `huggingface-cli login`
import os
import argparse
import huggingface_hub as hf

parser = argparse.ArgumentParser()
parser.add_argument('--model-id', default="CompVis/stable-diffusion-v1-4")
args = parser.parse_args()

HUGGING_FACE_HUB_TOKEN = os.getenv('HUGGING_FACE_HUB_TOKEN', default=False)

hf.snapshot_download(repo_id=args.model_id, use_auth_token=HUGGING_FACE_HUB_TOKEN)

