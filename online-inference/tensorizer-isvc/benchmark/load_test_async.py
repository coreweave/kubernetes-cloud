import asyncio
import random
import time
from argparse import ArgumentParser

import aiohttp


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
                print(response.status)
                return await response.text()

        return await asyncio.gather(*map(fetch, urls))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)

    args = parser.parse_args()

    return args


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


def main():
    args = parse_args()
    urls = [f"{args.url}/predict/{random.choice(inputs)}" for _ in range(100)]
    timed(asyncio.run)(async_aiohttp_get_all(urls))


if __name__ == "__main__":
    main()
