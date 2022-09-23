import os
import argparse
import huggingface_hub as hf

parser = argparse.ArgumentParser()
parser.add_argument('--model-id', required=True)
parser.add_argument('--revision', default="main")
args = parser.parse_args()

hf.snapshot_download(repo_id=args.model_id, revision=args.revision)
