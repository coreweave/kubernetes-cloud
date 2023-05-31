import asyncio
import logging
import random
import sys
import time
from argparse import ArgumentParser

import aiohttp

logger = logging.getLogger(__name__)
inputs = [
    "Hello, how are you?",
    "What up dig dog?",
    "You are a killer!",
    "Live a good life",
    "Life is great",
    "Chilling on a roof",
    "Love you",
    "Mox is cute",
    "You are my enemy",
    "Change is required",
    "Love the life",
]


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


def benchmark(base_url):
    urls = [f"{base_url}/predict/{random.choice(inputs)}" for _ in range(100)]
    timed(asyncio.run)(async_aiohttp_get_all(urls))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
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

    return parser.parse_args()


def setup_logger(level):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.propagate = False
    logger.setLevel(level)


def main():
    args = parse_args()
    setup_logger(args.log_level)
    benchmark(args.url)


if __name__ == "__main__":
    main()
