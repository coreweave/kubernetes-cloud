import asyncio
import json
import random
from typing import AsyncGenerator, Optional, List, Tuple

import numpy as np
from tqdm.autonotebook import tqdm
from transformers import AutoTokenizer


# Taken from vLLM
# https://github.com/vllm-project/vllm/blob/main/benchmarks/benchmark_serving.py#L34
def sample_requests(
        dataset_path: str,
        num_requests: int,
        tokenizer_path: str,
) -> List[Tuple[str, int, int]]:
    """Process the dataset and create a list of requests that can be used."""

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

    # Load the dataset.
    with open(dataset_path) as f:
        dataset = json.load(f)
    # Filter out the conversations with less than 2 turns.
    dataset = [
        data for data in dataset
        if len(data["conversations"]) >= 2
    ]
    # Only keep the first two turns of each conversation.
    dataset = [
        (data["conversations"][0]["value"], data["conversations"][1]["value"])
        for data in dataset
    ]

    print("Tokenizing the dataset...")
    # Tokenize the prompts and completions.
    prompts = [prompt for prompt, _ in dataset]
    prompt_token_ids = tokenizer(prompts).input_ids
    completions = [completion for _, completion in dataset]
    completion_token_ids = tokenizer(completions).input_ids
    tokenized_dataset = []
    for i in range(len(dataset)):
        output_len = len(completion_token_ids[i])
        tokenized_dataset.append((prompts[i], prompt_token_ids[i], output_len))

    # Filter out too long sequences.
    print("Filtering the dataset...")
    filtered_dataset: List[Tuple[str, int, int]] = []
    for prompt, prompt_token_ids, output_len in tokenized_dataset:
        prompt_len = len(prompt_token_ids)
        if prompt_len < 4 or output_len < 4:
            # Prune too short sequences.
            # This is because TGI causes errors when the input or output length
            # is too short.
            continue
        if prompt_len > 1024 or prompt_len + output_len > 2048:
            # Prune too long sequences.
            continue
        filtered_dataset.append((prompt, prompt_len, output_len))

    # Sample the requests.
    if num_requests > 0:
        return random.sample(filtered_dataset, num_requests)

    return filtered_dataset


async def get_request(
        input_requests: List[Tuple[str, int, int]],
        request_rate: float,
        rate_multiplier: float,
        rate_variation_period: int,
        pbar: Optional[tqdm] = None,
) -> AsyncGenerator[Tuple[str, int, int], None]:
    """Yield a new request to run while managing the request rate."""

    input_requests = iter(input_requests)
    for i, request in enumerate(input_requests):
        yield request

        if request_rate == float("inf"):
            # If the request rate is infinity, then we don't need to wait.
            continue

        # Calculate the sinusoidal variation between 1 and 'multiplier'
        rate_increase_factor = (
                1.0 + (rate_multiplier - 1.0) *
                (1 + np.sin(
                    2 * np.pi * i / rate_variation_period - np.pi / 2)) / 2.0
        )

        varied_rate = request_rate * rate_increase_factor

        # # This does not render nicely when you aren't using tqdm.notebook
        # if pbar:
        #     if "req/s" not in pbar.desc:
        #         pbar.set_description(f"{pbar.desc} | {varied_rate:.2f} req/s")
        #     else:
        #         pattern = r"\d+\.\d+\sreq/s"
        #         new_desc = re.sub(pattern, f"{varied_rate:.2f} req/s",
        #                           pbar.desc)
        #         pbar.set_description(new_desc)

        # Sample the request interval from the exponential distribution.
        interval = np.random.exponential(1.0 / varied_rate)

        # The next request will be sent after the interval.
        await asyncio.sleep(interval)
