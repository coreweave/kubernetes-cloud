import argparse
from pathlib import Path

from img2dataset import download
from pyspark.sql import SparkSession

parser = argparse.ArgumentParser()
parser.add_argument("--url-list", type=Path, default=Path("/mnt/pvc/mscoco.parquet"), help="Path to the url list file")
parser.add_argument("--output", type=Path, default=Path("/mnt/pvc/mscoco"), help="Path to output folder")
parser.add_argument("--thread-count", "-t", type=int, default=16, help="Number of threads for img2dataset")
args = parser.parse_args()

args.output.mkdir(parents=True, exist_ok=True)

if not args.url_list.exists():
    raise ValueError(f"The URL list does not exist at: {args.url_list}")

# All options are specified in the spark submit command. Any options specified here will override the spark submit conf
spark = SparkSession.builder.getOrCreate()

download(
    thread_count=args.thread_count,  # Process count will be num executors * num cores per executor
    url_list=str(args.url_list),
    image_size=256,
    output_folder=str(args.output),
    output_format="webdataset",
    input_format="parquet",
    url_col="URL",
    caption_col="TEXT",
    subjob_size=1000,
    distributor="pyspark",
)
