import argparse
import asyncio
import pickle
import random
import time
from typing import Tuple, List, Dict, Optional

import numpy as np
from matplotlib import pyplot as plt
from tqdm.autonotebook import tqdm

from k8s_utils import get_ksvc_template, deploy_ksvc, delete_ksvc
from request_utils import send_requests, RequestArgs
from data import sample_requests


async def test_req_level(
        size: int,
        requests: List[Tuple[str, int, int]],
        ksvc_template: str,
        request_args: Optional[RequestArgs] = None,
        verbose: bool = False
) -> Tuple[List[float], List[float], float]:
    """Run N requests at a time and gather relevant metrics."""

    manifest = get_ksvc_template(
        f"concur-req-{size}-{random.randint(10000, 99999)}",
        ksvc_template=ksvc_template
    )
    api_url = await deploy_ksvc(manifest, wait=True, verbose=False)

    pbar = None
    if verbose:
        pbar = tqdm(desc=f"{size} concurrent requests",
                    total=len(requests) * size)

    # Create N streams of 1 request at a time to equal N requests at at time
    start = time.perf_counter()
    try:
        tasks = []
        for i in range(size):
            shuffled_requests = random.sample(requests, len(requests))
            task = asyncio.create_task(send_requests(api_url,
                                                     shuffled_requests,
                                                     request_args=request_args,
                                                     pbar=pbar))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        duration = time.perf_counter() - start
    finally:
        delete_ksvc(manifest=manifest)
        if pbar:
            pbar.close()

    latencies = []
    ttfts = []
    total_tokens = 0

    # Combine all the results from each request stream
    for all_stats in results:
        for stats in all_stats:
            latencies.append(stats.normalized_latency)
            ttfts.append(stats.time_to_first_token)
            total_tokens += stats.total_tokens

    throughput = total_tokens / duration

    return latencies, ttfts, throughput


async def test_req_levels(
        levels: List[int],
        requests: List[Tuple[str, int, int]],
        ksvc_template: str,
        request_args: Optional[RequestArgs] = None,
        file_name: str = "concurrent_req_results_small.pkl",
) -> Dict[int, Tuple[List[float], List[float], List[float]]]:
    """Test the throughput and latencies of various of concurrent requests."""

    tests = []
    for concurrency in levels:
        test = asyncio.create_task(test_req_level(concurrency,
                                                  requests,
                                                  ksvc_template,
                                                  request_args=request_args,
                                                  verbose=True))
        tests.append(test)

    # {size: (latencies, ttfts, throughputs)}
    results = {levels[i]: result for i, result in
               enumerate(await asyncio.gather(*tests))}

    with open(file_name, "wb") as file:
        pickle.dump(results, file)

    return results


def plot_latency(
        results: Dict[int, Tuple[List[float], List[float], List[float]]],
        axs: Optional[Tuple[plt.Axes, plt.Axes]] = None,
        title=None
) -> None:
    if axs is None:
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        fig.suptitle(title)

    latencies = [result[0] for _, result in results.items()]
    labels = [str(size) for size, _ in results.items()]

    axs[0].set_title("Per Request Latencies")
    axs[0].boxplot(latencies)
    axs[0].set_xlabel("Number of Concurrent Requests")
    axs[0].set_xticklabels(labels)
    axs[0].set_ylabel("Normalized Latency (s/token)")

    # Boxplot without outliers
    axs[1].set_title("Per Request Latencies without Outliers")
    axs[1].boxplot(latencies, showfliers=False)
    axs[1].set_xlabel("Number of Concurrent Requests")
    axs[1].set_xticklabels(labels)
    axs[1].set_ylabel("Normalized Latency (s/token)")
    # ax[1].set_ylim(0, 0.5)


def plot_ttft(
        results: Dict[int, Tuple[List[float], List[float], List[float]]],
        axs: Optional[Tuple[plt.Axes, plt.Axes]] = None,
        title=None
) -> None:
    if axs is None:
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        fig.suptitle(title)

    ttfts = [result[1] for _, result in results.items()]
    labels = [str(size) for size, _ in results.items()]

    axs[0].set_title("Time to First Response Token")
    axs[0].boxplot(ttfts)
    axs[0].set_xlabel("Percentile")
    axs[0].set_xticklabels(labels)
    axs[0].set_ylabel("Time to First Token (s)")

    axs[1].set_title("Time to First Response Token without Outliers")
    # Boxplot without outliers
    axs[1].boxplot(ttfts, showfliers=False)
    axs[1].set_xlabel("Percentile")
    axs[1].set_xticklabels(labels)
    axs[1].set_ylabel("Time to First Token (s)")
    # ax[1].set_ylim(0, 0.5)


def plot_throughputs(
        results: Dict[int, Tuple[List[float], List[float], List[float]]],
        ax: Optional[plt.Axes] = None,
        title=None
) -> None:
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    ax.set_title(title)

    throughputs = [np.mean(result[2]) for _, result in results.items()]
    labels = [str(size) for size, _ in results.items()]
    ax.plot(labels, throughputs)

    ax.set_xlabel("Concurrent Requests")
    ax.set_ylabel("Throughput (tok/s)")
    # ax.legend()


def plot_latency_vs_throughput(
        results: Dict[int, Tuple[List[float], List[float], List[float]]],
        ax: Optional[plt.Axes] = None,
        title=None
) -> None:
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    ax.set_title(title)

    throughputs = [np.mean(result[2]) for _, result in results.items()]
    latency = [np.mean(result[0]) for _, result in results.items()]
    labels = [str(size) for size, _ in results.items()]

    for i, label in enumerate(labels):
        ax.scatter(latency[i], throughputs[i], label=label)

    ax.set_xlabel("Normalized Latency (s/token)")
    ax.set_ylabel("Throughput (tok/s)")
    # Legend on the bottom right
    ax.legend(loc="lower right")


def plot_concur_req_results(
        file_name: str = "",
        results: Optional[
            Dict[int, Tuple[List[float], List[float], List[float]]]] = None,
        figsize: Tuple = (15, 15),
        output: str = ""
) -> None:
    if not results:
        with open(file_name, "rb") as file:
            results = pickle.load(file)

    fig, axs = plt.subplots(3, 2, figsize=figsize)
    fig.suptitle("Performance across Different Levels of Concurrent Requests")

    plot_latency(results,
                 axs=axs[0],
                 title="Per Request Latencies with Different Concurrent Requests")
    plot_ttft(results,
              axs=axs[1],
              title="Time to First Token with Different Concurrent Requests")
    plot_throughputs(results,
                     ax=axs[2][0],
                     title="Throughput with Different Concurrent Requests")
    plot_latency_vs_throughput(results,
                               ax=axs[2][1],
                               title="Latency vs Throughput")

    if output:
        plt.savefig(output)


def get_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument("-o", "--output",
                      type=str,
                      default="concurrent_req_results.",
                      help="File to store the results, both a pkl of the raw "
                           "data and a png of the graphs. "
                           "Defaults to 'concurrent_req_results'")
    args.add_argument("--ksvc-template",
                      type=str,
                      default="ksvc-template.yaml",
                      help="The Knative service template to use. Expects there "
                           "to be a number of python formatting variables: "
                           "'name', 'annotations', 'container_concurrency', "
                           "and 'timeout_seconds'. "
                           "Defaults to 'ksvc-template.yaml'")
    args.add_argument("--n-sampling",
                      type=int,
                      default=1,
                      help="Number of chat responses to generate per input. "
                           "Can greatly impact the KV Cache usage profile of "
                           "your requests. Defaults to 1.")
    args.add_argument("-n", "--requests",
                      type=int,
                      default=100,
                      help="The number of times N requests will be running "
                           "through the service concurrently. If the "
                           "concurrency is 4 and the number of requests is 100,"
                           " then 400 total requests will be sent."
                           "Defaults to 100")
    args.add_argument("-c", "--concurrencies",
                      type=int,
                      nargs="+",
                      default=[1],
                      help="A list of concurrency levels to test. Each level "
                           "will involve deploying a separate Knative service. "
                           "Defaults to [1].")
    args.add_argument("-t", "--tokenizer",
                      type=str,
                      default="mistralai/Mistral-7B-Instruct-v0.1",
                      help="Local or HuggingFace path to the tokenizer to use. "
                           "Defaults to 'mistralai/Mistral-7B-Instruct-v0.1'.")
    args.add_argument("-d", "--dataset",
                      type=str,
                      default="ShareGPT_V3_unfiltered_cleaned_split.json",
                      help="Local path to the dataset to use. Defaults to "
                           "'ShareGPT_V3_unfiltered_cleaned_split.json'.")
    args.add_argument("-m", "--model",
                      type=str,
                      default="mistralai/Mistral-7B-Instruct-v0.1",
                      help="The model name to use when calling the OpenAI "
                           "endpoint of the Knative service. Defaults to "
                           "'mistralai/Mistral-7B-Instruct-v0.1'.")
    return args.parse_args()


async def main() -> None:
    args = get_args()
    requests = sample_requests(args.dataset, args.requests, args.tokenizer)

    request_args = RequestArgs(model=args.model,
                               n=args.n_sampling)

    print("Running tests...")
    results = await test_req_levels(args.concurrencies,
                                    requests,
                                    args.ksvc_template,
                                    request_args=request_args,
                                    file_name=f"{args.output}.pkl")

    plot_concur_req_results(results=results)


if __name__ == "__main__":
    asyncio.run(main())
