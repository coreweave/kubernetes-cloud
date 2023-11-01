import argparse
import asyncio
import random
import time

import numpy as np
from tqdm.autonotebook import tqdm

from k8s_utils import get_ksvc_template, deploy_ksvc, delete_ksvc


async def test_startup_time(ksvc_template: str) -> float:
    manifest = get_ksvc_template(
        name=f"test-startup-{random.randint(10000, 99999)}",
        ksvc_template=ksvc_template
    )

    start = time.perf_counter()
    await deploy_ksvc(manifest, wait=True, verbose=False)
    startup_time = time.perf_counter() - start

    delete_ksvc(manifest=manifest, verbose=False)

    return startup_time


async def run_startup_test(ksvc_template: str,
                           n_trials: int,
                           maximum_concurrent: int = 0) -> float:
    if maximum_concurrent == 0:
        maximum_concurrent = n_trials

    pbar = tqdm(desc="Testing startup time", total=n_trials)
    semaphore = asyncio.Semaphore(maximum_concurrent)

    async def limited_test() -> float:
        async with semaphore:
            res = await test_startup_time(ksvc_template)
            pbar.update(1)
            return res

    tasks = [limited_test() for _ in range(n_trials)]
    results = await asyncio.gather(*tasks)

    return float(np.mean(results))


def get_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument("-N",
                      type=int,
                      default=10,
                      help="Number of deployments to test. Defaults to 10.")
    args.add_argument("-M",
                      type=int,
                      default=1,
                      help="Maximum number of services to deploy at once. "
                           "Defaults to 1.")
    args.add_argument("-t", "--ksvc-template",
                      type=str,
                      default="ksvc-template.yaml",
                      help="The Knative service template to use. Expects there "
                           "to be a number of python formatting variables: "
                           "'name', 'annotations', 'container_concurrency', "
                           "and 'timeout_seconds'. "
                           "Defaults to 'ksvc-template.yaml'")

    return args.parse_args()


async def main() -> None:
    args = get_args()

    avg_time = await run_startup_test(args.ksvc_template, args.N, args.M)
    print(f"Average startup time: {avg_time:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
