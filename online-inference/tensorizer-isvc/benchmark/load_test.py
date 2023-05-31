import asyncio
import logging
import random
import sys
import time
from argparse import ArgumentParser

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


def timed(func):
    """
    records approximate durations of function calls
    """

    def wrapper(*args, **kwargs):
        name = func.__name__
        start = time.time()
        print(f"{name:<30} started")
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{name:<30} finished in {elapsed:.2f} seconds")
        return result

    return wrapper


async def async_aiohttp_get_all(urls):
    """
    performs asynchronous get requests in bulk
    """
    async with aiohttp.ClientSession() as session:

        async def fetch(url):
            async with session.get(url) as response:
                log_level = logging.INFO if response.ok else logging.WARNING
                logger.log(
                    log_level, f"Status {response.status} response from {url}"
                )
                return await response.text()

        return await asyncio.gather(*map(fetch, urls))


def benchmark_async(base_url: str, trials: int):
    urls = [f"{base_url}/predict/{random.choice(inputs)}" for _ in range(trials)]
    timed(asyncio.run)(async_aiohttp_get_all(urls))


def benchmark_sync(base_url: str, trials: int):
    times = []
    count_s = count_f = 0
    with requests.Session() as s:
        for _ in range(trials):
            start = time.time()
            res = s.get(f"{base_url}/predict/{random.choice(inputs)}")
            if res.status_code == 200:
                times.append(time.time() - start)
                logger.info(
                    f"Good status code from {base_url}: {res.status_code}"
                )
                count_s += 1
            else:
                logger.warning(
                    f"Bad status code from {base_url}: {res.status_code}"
                )
                count_f += 1

    print(f"Average Latency for {base_url}: {sum(times) / len(times)}")
    print(f"Successes for {base_url}: {count_s}")
    print(f"Failures for {base_url}: {count_f}")


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
    parser.add_argument(
        "--requests", help="Number of requests to send", type=int
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
                "--async mode requires aiohttp to be installed, but it could"
                " not be found"
            )
    elif requests is None:
        parser.error(
            "--sync mode requires requests to be installed, but it could not be"
            " found"
        )

    return args


def setup_logger(level):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.propagate = False
    logger.setLevel(level)


def main():
    args = parse_args()
    setup_logger(args.log_level)
    if args.asynchronous:
        benchmark_async(args.url, args.requests)
    else:
        benchmark_sync(args.url, args.requests)


if __name__ == "__main__":
    main()
