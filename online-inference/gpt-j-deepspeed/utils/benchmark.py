#!/usr/bin/env python3

import argparse
import json
import logging
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gpt-j-6b-benchmark-client")

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
parser.add_argument(
    "--model-path", type=str, default="/v1/models/eleutherai-gpt-j-6b:predict"
)
args = parser.parse_args()

logger.info(f" Connecting to {args.url}")

test_contexts = [[8, 8], [8, 1016], [8, 2040], [512, 512], [512, 1536], [1536, 512]]

for context in test_contexts:
    results = []
    benchmark_sequence_length = context[0]
    generated_tokens = context[1]

    logger.info(f" Input Sequence Lenghth: {benchmark_sequence_length}")

    request = json.dumps(
        {
            "benchmark": True,
            "parameters": {
                "benchmark_sequence_length": benchmark_sequence_length,
                "max_length": benchmark_sequence_length + generated_tokens,
            },
        }
    ).encode("utf-8")

    logger.info(f" Request data: {request}")

    response = (
        urllib.request.urlopen(args.url + args.model_path, data=request)
        .read()
        .decode("utf-8")
    )
    results.append(response)
    logger.info(f" Results: {response}")

logger.info(f" Final results:")
for result in results:
    logger.info(f" {result}")
