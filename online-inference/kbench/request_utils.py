import asyncio
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional

import aiohttp
import openai
from tqdm.autonotebook import tqdm

from data import get_request


@dataclass
class RequestStats:
    prompt_tokens: int
    output_tokens: int
    start_time: float
    end_time: float
    first_token_time: float

    @property
    def total_tokens(self):
        return self.prompt_tokens + self.output_tokens

    @property
    def time_to_first_token(self):
        return self.first_token_time - self.start_time

    @property
    def latency(self):
        return self.end_time - self.start_time

    @property
    def normalized_latency(self):
        return self.latency / self.total_tokens

    @property
    def throughput(self):
        return self.total_tokens / self.latency


async def single_request(
        api_url: str,
        request,
        best_of: int = 1,
        use_beam_search: bool = False,
        verbose: bool = False,
        n: int = 1,
        pbar: Optional[tqdm] = None
) -> RequestStats:
    """Send a single request to the API."""

    prompt, prompt_len, output_len = request
    if verbose:
        print(prompt, "\n", "~~~~" * 20)

    openai_args = {
        "api_base": api_url + "/v1",
        "api_key": "EMPTY",
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "n": n,
        "temperature": 0.0 if use_beam_search else 1.0,
        "top_p": 1.0,
        "max_tokens": output_len,
        "best_of": best_of,
        "use_beam_search": use_beam_search,
    }

    request_start_time = time.perf_counter()
    first_token_time = None
    num_tokens = 0
    timeout = aiohttp.ClientTimeout(total=3 * 3600)
    session = aiohttp.ClientSession(timeout=timeout)
    openai.aiosession.set(session)
    while True:
        try:
            response = await openai.ChatCompletion.acreate(**openai_args)
            async for chunk in response:
                if num_tokens == 0:
                    first_token_time = time.perf_counter()
                num_tokens += 1
                if verbose:
                    msg = chunk["choices"][0]["delta"]
                    print(msg.get("content", ""), end="")
        except Exception as e:
            print("Request Error:", e)
        else:
            break

    await openai.aiosession.get().close()
    request_end_time = time.perf_counter()

    stats = RequestStats(prompt_tokens=prompt_len,
                         output_tokens=output_len,
                         start_time=request_start_time,
                         end_time=request_end_time,
                         first_token_time=first_token_time)

    if verbose:
        print("\n", "~~~~" * 20)
        print("Generated Tokens:", stats.output_tokens)
        print("Total Tokens:", stats.total_tokens)
        print(f"Request Latency: {stats.latency:.2f} s")
        print(f"Normalized Latency: {stats.normalized_latency:.2f} s/tok")
        print(f"Time to First Token: {stats.time_to_first_token:.2f} s")

    if pbar:
        pbar.update(1)

    return stats


async def send_requests(
        api_url: str,
        requests: List[Tuple[str, int, int]],
        n_sampling: int = 1,
        pbar: Optional[tqdm] = None
) -> List[RequestStats]:
    """Send n requests to the API while only running 1 at a time."""

    all_stats = []
    for req in requests:
        stats = await single_request(api_url,
                                     req,
                                     n=n_sampling)
        all_stats.append(stats)

        if pbar:
            pbar.update(1)

    return all_stats


async def send_scaling_requests(
        api_url: str,
        requests: List[Tuple[str, int, int]],
        rate: float,
        rate_multiplier: float,
        rate_variation_period: int,
        n_sampling: int = 1,
        pbar: Optional[tqdm] = None
) -> List[RequestStats]:
    """Send all the given requests while managing the request rate."""

    tasks: List[asyncio.Task] = []
    async for request in get_request(requests, rate, rate_multiplier,
                                     rate_variation_period, pbar):
        task = asyncio.create_task(
            single_request(api_url, request, n=n_sampling, pbar=pbar))
        tasks.append(task)

    return await asyncio.gather(*tasks)
