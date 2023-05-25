import time
import asyncio
import random
import requests
import aiohttp
from argparse import ArgumentParser

from asgiref import sync

def timed(func):
    """
    records approximate durations of function calls
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        print('{name:<30} started'.format(name=func.__name__))
        result = func(*args, **kwargs)
        duration = "{name:<30} finished in {elapsed:.2f} seconds".format(
            name=func.__name__, elapsed=time.time() - start
        )
        print(duration)
        timed.durations.append(duration)
        return result
    return wrapper

timed.durations = []

@timed
def async_requests_get_all(urls):
    """
    asynchronous wrapper around synchronous requests
    """
    session = requests.Session()
    # wrap requests.get into an async function
    def get(url):
        return session.get(url).status_code
    async_get = sync.sync_to_async(get)

    async def get_all(urls):
        return await asyncio.gather(*[
            async_get(url) for url in urls
        ])
    # call get_all as a sync function to be used in a sync context
    return sync.async_to_sync(get_all)(urls)

@timed
def async_aiohttp_get_all(urls):
    """
    performs asynchronous get requests
    """
    async def get_all(urls):
        async with aiohttp.ClientSession() as session:
            async def fetch(url):
                async with session.get(url) as response:
                    print(response.status)
                    return await response.text()
            return await asyncio.gather(*[
                fetch(url) for url in urls
            ])
    # call get_all as a sync function to be used in a sync context
    return sync.async_to_sync(get_all)(urls)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
    
    args = parser.parse_args()

    return args

inputs = ["Hello, how are you?", "What up dig dog?", "You are a killer!", "JCPenny is a bad store", "Life is great", "Chilling on a roof", "Love you", "Mox is cute", "You are my enemy", "Change is required", "Love the life"]

def main():
    args = parse_args()
    urls = []
    for _ in range(100):
        urls.append(f"{args.url}/predict/{random.choice(inputs)}")
    
    async_aiohttp_get_all(urls)
    # async_requests_get_all(urls)
    print('----------------------')
    [print(duration) for duration in timed.durations]


if __name__ == '__main__':
    main()