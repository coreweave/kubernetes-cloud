import asyncio
import enum
import json
import logging
import os.path
import random
import statistics
import sys
import time
import urllib.parse
from argparse import ArgumentParser
from typing import NamedTuple, Optional, Sequence

try:
    import aiohttp
except ImportError:
    aiohttp = None
try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)

inputs_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "inputs.txt"
)

with open(inputs_file_path, "r", encoding="utf-8") as inputs_file:
    inputs = [line.strip() for line in inputs_file]


class InferenceRequest(NamedTuple):
    method: str
    url: str
    data: Optional[str]


async def measure_async_fetch_all(
    queries: Sequence[InferenceRequest],
) -> Sequence[float]:
    """
    performs asynchronous get requests in bulk,
    returning the duration of each successful request
    """
    async with aiohttp.ClientSession() as session:

        async def time_fetch(query: InferenceRequest) -> Optional[float]:
            method, url, data = query
            start = time.time()
            try:
                async with session.request(
                    method=method, url=url, data=data
                ) as response:
                    if response.ok:
                        await response.text()
                        duration = time.time() - start
                        logger.info(
                            f"Good status code from {url}: {response.status}"
                        )
                        return duration
                    else:
                        logger.warning(
                            f"Bad status code from {url}: {response.status}"
                        )
                        return None
            except asyncio.TimeoutError:
                logger.warning(f"Request to {url} timed out")
                return None

        results = await asyncio.gather(*map(time_fetch, queries))
        return [r for r in results if isinstance(r, float)]


def measure_sync_fetch_all(
    queries: Sequence[InferenceRequest],
) -> Sequence[float]:
    """
    performs synchronous get requests in bulk,
    returning the duration of each successful request
    """
    times = []
    with requests.Session() as s:
        for query in queries:
            method, url, data = query
            start = time.time()
            try:
                res = s.request(method=method, url=url, data=data)
                if res.ok:
                    times.append(time.time() - start)
                    logger.info(
                        f"Good status code from {url}: {res.status_code}"
                    )
                else:
                    logger.warning(
                        f"Bad status code from {url}: {res.status_code}"
                    )
            except requests.ConnectTimeout:
                logger.warning(f"Request to {url} timed out")

    return times


def random_flask_inference_request(base_url: str) -> InferenceRequest:
    """
    Generates a random inference request for a Flask server
    """
    query = urllib.parse.quote(random.choice(inputs))
    return InferenceRequest(
        method="GET",
        url=f"{base_url}/predict/{query}",
        data=None,
    )


def random_kserve_inference_request(
    base_url: str, model_name="gptj"
) -> InferenceRequest:
    """
    Generates a random inference request for a KServe server
    """
    query = json.dumps({"instances": [random.choice(inputs)]})
    return InferenceRequest(
        method="POST",
        url=f"{base_url}/v1/models/{model_name}:predict",
        data=query,
    )


class ServerType(enum.Enum):
    FLASK = 1
    KSERVE = 2


def benchmark(
    base_url: str, isvc_type: ServerType, trials: int, asynchronous: bool
):
    if isvc_type == ServerType.FLASK:
        random_request = random_flask_inference_request
    elif isvc_type == ServerType.KSERVE:
        random_request = random_kserve_inference_request
    else:
        raise ValueError("Invalid isvc_type")

    queries = [random_request(base_url) for _ in range(trials)]
    print("Started benchmark")

    start = time.time()
    if asynchronous:
        individual_times = asyncio.run(measure_async_fetch_all(queries))
    else:
        individual_times = measure_sync_fetch_all(queries)
    total_time = time.time() - start

    # Compute statistics
    successes = len(individual_times)
    failures = trials - successes
    if successes > 0:
        average_latency = statistics.mean(individual_times)
        latency_stddev = statistics.stdev(
            individual_times, xbar=average_latency
        )
    else:
        average_latency = latency_stddev = None
    throughput = trials / total_time
    goodput = successes / total_time
    print(
        f"Benchmark finished for {base_url} in {total_time:.2f} seconds."
        " Statistics:"
    )
    print(f"Average throughput: {throughput:.4f} requests/second")
    if throughput != goodput:
        print(f"Average goodput: {goodput:.4f} successes/second")
    if average_latency is not None:
        print(
            f"Average latency: {average_latency:.4f} seconds/request"
            f" (sample standard deviation: {latency_stddev:.4f})"
        )
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
    isvc_type_group = parser.add_mutually_exclusive_group(required=True)
    isvc_type_group.add_argument(
        "--flask",
        help="Generate requests for a Flask server",
        dest="isvc_type",
        action="store_const",
        const=ServerType.FLASK,
    )
    isvc_type_group.add_argument(
        "--kserve",
        help="Generate requests for a KServe server",
        dest="isvc_type",
        action="store_const",
        const=ServerType.KSERVE,
    )
    parser.set_defaults(asynchronous=True)
    synchronicity_group = parser.add_mutually_exclusive_group(required=False)
    synchronicity_group.add_argument(
        "--async",
        help=(
            "Send overlapping, asynchronous requests (default)"
            " (requires aiohttp to be installed)"
        ),
        dest="asynchronous",
        action="store_true",
    )
    synchronicity_group.add_argument(
        "--sync",
        help=(
            "Send sequential, synchronous requests"
            " (requires requests to be installed)"
        ),
        dest="asynchronous",
        action="store_false",
    )
    parser.add_argument(
        "--requests",
        help="Number of requests to send",
        type=int,
        default=100,
    )
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
    benchmark(args.url, args.isvc_type, args.requests, args.asynchronous)


if __name__ == "__main__":
    main()
