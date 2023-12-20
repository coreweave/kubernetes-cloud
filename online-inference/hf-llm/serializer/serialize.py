import torch
import os
import logging
from tensorizer import TensorSerializer, stream_io
from argparse import ArgumentParser
from transformers import AutoModelForCausalLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

parser = ArgumentParser()
parser.add_argument("--hf-model-id", default="distilgpt2", type=str)
parser.add_argument("--precision", choices=["float16", "float32"], default="float16", type=str)
parser.add_argument("--dest-bucket", default=None, required=True, type=str)
parser.add_argument("--s3-access-key", default=os.getenv("AWS_KEY"), required=False, type=str)
parser.add_argument("--s3-secret-access-key", default=os.getenv("AWS_SECRET"), required=False, type=str)
parser.add_argument("--s3-endpoint", default=os.getenv("AWS_HOST", "object.ord1.coreweave.com"), required=False, type=str)
args = parser.parse_args()


def save_artifact_s3(model, path):
    serializer = TensorSerializer(
        stream_io.open_stream(
            path_uri=path,
            mode="wb",
            s3_access_key_id=args.s3_access_key,
            s3_secret_access_key=args.s3_secret_access_key,
            s3_endpoint=args.s3_endpoint,
            s3_config_path=None
        )
    )
    serializer.write_module(model)
    serializer.close()
    logger.info(f"Tensorized S3 artifact written to {path}")


if __name__ == "__main__":
    model_id = args.hf_model_id
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if args.precision == "float16" else torch.float32
    )

    BASE_S3_URL = f"s3://{args.dest_bucket}/"
    DTYPE_STR = "/fp16" if args.precision == "float16" else ""

    save_artifact_s3(model, BASE_S3_URL + model_id +
                     DTYPE_STR + "/model.tensors")
