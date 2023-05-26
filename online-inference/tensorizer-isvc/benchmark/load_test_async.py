import time
import asyncio
import random
import requests
import aiohttp
from argparse import ArgumentParser

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
    return (get_all)(urls)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
    
    args = parser.parse_args()

    return args

inputs = ["Hello, how are you?", "What up dig dog?", "You are a killer!", "Live a good life", "Life is great", "Chilling on a roof", "Love you", "Mox is cute", "You are my enemy", "Change is required", "Love the life"]

def main():
    args = parse_args()
    urls = []
    for _ in range(100):
        urls.append(f"{args.url}/predict/{random.choice(inputs)}")
    
    timed(asyncio.run)(async_aiohttp_get_all(urls))


if __name__ == '__main__':
    main()