import torch
import os
import logging
from tensorizer import TensorSerializer, stream_io
from diffusers import StableDiffusionPipeline
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

parser = ArgumentParser()
parser.add_argument("--hf-model-id", default="runwayml/stable-diffusion-v1-5", type=str)
parser.add_argument("--precision", choices=["float16", "float32"], default="float16", type=str)
parser.add_argument("--dest-bucket", default=None, required=True, type=str)
parser.add_argument("--s3-access-key", default=os.getenv("AWS_KEY"), required=False, type=str)
parser.add_argument("--s3-secret-access-key", default=os.getenv("AWS_SECRET"), required=False, type=str)
parser.add_argument("--s3-endpoint", default=os.getenv("AWS_HOST", "object.ord1.coreweave.com"), required=False, type=str)
args = parser.parse_args()

def save_artifact(model, path, sub_path):
    serializer = TensorSerializer(path + sub_path)
    serializer.write_module(model)
    serializer.close()

def save_artifact_s3(model, path, sub_path):
    serializer = TensorSerializer(
        stream_io.open_stream(
            path_uri = path + sub_path,
            mode = 'wb',
            s3_access_key_id = args.s3_access_key,
            s3_secret_access_key = args.s3_secret_access_key,
            s3_endpoint = args.s3_endpoint,
            s3_config_path=None
        )
    )
    serializer.write_module(model)
    serializer.close()
    logger.info(f"Tensorized S3 artifact written to {path + sub_path}")

if __name__ == '__main__':
    model_id = args.hf_model_id
    model = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if args.precision == "float16" else torch.float32
    )

    BASE_S3_URL = f"s3://{args.dest_bucket}/"

    dtype_str = "/fp16" if args.precision == "float16" else ""

    save_artifact_s3(model.vae, BASE_S3_URL + model_id + dtype_str, '/vae.tensors')
    save_artifact_s3(model.unet, BASE_S3_URL + model_id + dtype_str, '/unet.tensors')
    save_artifact_s3(model.text_encoder, BASE_S3_URL + model_id + dtype_str, '/text_encoder.tensors')

    logger.info(f"Wrote tensorized S3 artifact to: {BASE_S3_URL + model_id}")
