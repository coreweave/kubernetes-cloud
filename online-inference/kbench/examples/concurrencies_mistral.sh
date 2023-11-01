#!/bin/bash

BENCHMARK_SCRIPTS_PATH=${BENCHMARK_SCRIPTS_PATH:-"../"}

python "$BENCHMARK_SCRIPTS_PATH/test_concurrency.py" \
  -o "concurrency_test.pkl" \
  --ksvc-template "ksvc-template-mistral.yaml" \
  -n "100" \
  -c 1 5 10 20 30 40 50 60 70 \
  -t "mistralai/Mistral-7B-Instruct-v0.1" \
  -d "ShareGPT_V3_unfiltered_cleaned_split.json"
