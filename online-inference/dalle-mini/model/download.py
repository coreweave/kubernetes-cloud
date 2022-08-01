import argparse
import tempfile
import logging
import shutil
from huggingface_hub import snapshot_download
import os

logging.basicConfig(level=INFO)
logger = logging.getLogger("downloader")

parser = argparse.ArgumentParser()
parser.add_argument("--model-id", type=str, default="dalle-mini/dalle-mini")
parser.add_argument("--model-cache", type=str, default="/model-cache")
args = parser.parse_args()

logger.info(f'Downloading {args.model_id}...')

tmpdir = tempfile.TemporaryDirectory(dir=args.model_cache)
model = snapshot_download(repo_id=args.model_id, cache_dir=tmpdir.name)
model_dir = os.path.join(args.model_cache, args.model_id)
os.makedirs(model_dir)

os.chdir(model)
for file in os.listdir(model):
    os.getcwd()
    src = os.readlink(os.path.join(model, file))
    dest = os.path.join(model_dir, file)
    logger.info(f'moving {src} to {dest}')
    shutil.move(src, dest)

tmpdir.cleanup()