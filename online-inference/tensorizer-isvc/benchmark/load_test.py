import asyncio
import logging
import random
import statistics
import sys
import time
import urllib.parse
from argparse import ArgumentParser
from typing import Optional, Sequence

try:
    import aiohttp
except ImportError:
    aiohttp = None
try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)

with open("inputs.txt", "r", encoding="utf-8") as inputs_file:
    inputs = [line.strip() for line in inputs_file]


async def measure_async_fetch_all(urls) -> Sequence[float]:
    """
    performs asynchronous get requests in bulk,
    returning the duration of each successful request
    """
    async with aiohttp.ClientSession() as session:

        async def time_fetch(url: str) -> Optional[float]:
            start = time.time()
            try:
                async with session.get(url) as response:
                    if response.ok:
                        await response.text()
                        duration = time.time() - start
                        logger.info(f"Good status code from {url}: {response.status}")
                        return duration
                    else:
                        logger.warning(f"Bad status code from {url}: {response.status}")
                        return None
            except asyncio.TimeoutError:
                logger.warning(f"Request to {url} timed out")
                return None

        results = await asyncio.gather(*map(time_fetch, urls))
        return [r for r in results if isinstance(r, float)]


def measure_sync_fetch_all(urls) -> Sequence[float]:
    """
    performs synchronous get requests in bulk,
    returning the duration of each successful request
    """
    times = []
    with requests.Session() as s:
        for url in urls:
            start = time.time()
            try:
                res = s.get(url)
                if res.ok:
                    times.append(time.time() - start)
                    logger.info(f"Good status code from {url}: {res.status_code}")
                else:
                    logger.warning(f"Bad status code from {url}: {res.status_code}")
            except requests.ConnectTimeout:
                logger.warning(f"Request to {url} timed out")

    return times


def random_inference_url(base_url: str) -> str:
    query = urllib.parse.quote(random.choice(inputs))
    return f"{base_url}/predict/{query}"


def benchmark(base_url: str, trials: int, asynchronous: bool):
    urls = [random_inference_url(base_url) for _ in range(trials)]
    print("Started benchmark")

    start = time.time()
    if asynchronous:
        individual_times = asyncio.run(measure_async_fetch_all(urls))
    else:
        individual_times = measure_sync_fetch_all(urls)
    total_time = time.time() - start

    # Compute statistics
    successes = len(individual_times)
    failures = trials - successes
    if successes > 0:
        average_latency = statistics.mean(individual_times)
        latency_stddev = statistics.stdev(individual_times, xbar=average_latency)
    else:
        average_latency = latency_stddev = None
    throughput = trials / total_time
    goodput = successes / total_time
    print(
        f"Benchmark finished for {base_url} in {total_time:.2f} seconds." " Statistics:"
    )
    print(f"Average throughput: {throughput:.4f} requests/second")
    if throughput != goodput:
        print(f"Average goodput: {goodput:.4f} successes/second")
    if average_latency is not None:
        print(
            f"Average latency: {average_latency:.4f} seconds/request"
            f" (sample standard deviation: {latency_stddev:.2f})"
        )
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
    parser.set_defaults(asynchronous=True)
    parser.add_argument(
        "--async",
        help=(
            "Send overlapping, asynchronous requests (default)"
            " (requires aiohttp to be installed)"
        ),
        dest="asynchronous",
        action="store_true",
    )
    parser.add_argument(
        "--sync",
        help=(
            "Send sequential, synchronous requests"
            " (requires requests to be installed)"
        ),
        dest="asynchronous",
        action="store_false",
    )
    parser.add_argument("--requests", help="Number of requests to send", type=int)
    parser.set_defaults(log_level=logging.WARNING)
    parser.add_argument(
        "--verbose",
        "-v",
        help="Show more logs",
        dest="log_level",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "--quiet",
        "-q",
        help="Show fewer logs",
        dest="log_level",
        action="store_const",
        const=logging.ERROR,
    )

    args = parser.parse_args()

    if args.requests < 1:
        parser.error("--requests must be positive")

    if args.asynchronous:
        if aiohttp is None:
            parser.error(
                "--async mode requires aiohttp to be installed,"
                " but it could not be found"
            )
    elif requests is None:
        parser.error(
            "--sync mode requires requests to be installed,"
            " but it could not be found"
        )

    return args


def setup_logger(level):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.propagate = False
    logger.setLevel(level)


def main():
    args = parse_args()
    setup_logger(args.log_level)
    benchmark(args.url, args.requests, args.asynchronous)


if __name__ == "__main__":
    main()
