#!/bin/bash

BENCHMARK_SCRIPTS_PATH=${BENCHMARK_SCRIPTS_PATH:-"../"}

python "$BENCHMARK_SCRIPTS_PATH/test_scaling_concurrency.py" \
  -o "scaling_test.pkl" \
  --ksvc-template "ksvc-template-mistral.yaml" \
  -n 10000 \
  -c 30 40 50 60 70 \
  --target-concurrency 30 \
  -r 1 \
  -m 10 \
  -p 10000 \
  -t "mistralai/Mistral-7B-Instruct-v0.1" \
  -d "ShareGPT_V3_unfiltered_claned_split.json"
