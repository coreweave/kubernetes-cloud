import argparse
import asyncio
import pickle
import random
from typing import Tuple, List, Dict, Optional

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from k8s_utils import get_ksvc_template, deploy_ksvc, delete_ksvc
from request_utils import send_requests, send_scaling_requests, RequestStats, \
    RequestArgs
from data import sample_requests


async def test_scaling(
        requests: List[Tuple[str, int, int]],
        target_percentage: int,
        container_concurrency: int,
        request_rate: float,
        rate_multiplier: float,
        rate_variation_period: int,
        ksvc_template: str,
        stable_window: int = 90,
        panic_window_percentage: float = 50.0,
        panic_threshold_percentage: float = 200.0,
        warm_up_requests: int = 0,
        request_args: Optional[RequestArgs] = None,
        desc: str = ""
) -> List[RequestStats]:
    annotations = {
        "autoscaling.knative.dev/target-burst-capacity": -1,
        "autoscaling.knative.dev/target-utilization-percentage": target_percentage,
        "autoscaling.knative.dev/window": f"{stable_window}s",
        "autoscaling.knative.dev/panic-window-percentage": panic_window_percentage,
        "autoscaling.knative.dev/panic-threshold-percentage": panic_threshold_percentage
    }
    manifest = get_ksvc_template(
        f"scaling-test-{desc.replace(' ', '-')}-{random.randint(10000, 99999)}",
        annotations=annotations,
        container_concurrency=container_concurrency,
        ksvc_template=ksvc_template
    )
    api_url = await deploy_ksvc(manifest, wait=True, verbose=False)

    pbar = tqdm(total=len(requests), desc=f"Scaling Test {desc}")
    try:
        if warm_up_requests > 0:
            await send_requests(api_url,
                                random.sample(requests, warm_up_requests),
                                request_args=request_args)
        results = await send_scaling_requests(
            api_url,
            requests,
            rate=request_rate,
            rate_multiplier=rate_multiplier,
            rate_variation_period=rate_variation_period,
            pbar=pbar
        )
    finally:
        delete_ksvc(manifest=manifest)
        if pbar:
            pbar.close()

    return results


async def run_container_concurreny_experiment(
        requests: List[Tuple[str, int, int]],
        target_concurrency: int,
        container_concurrencies: List[int],
        request_rate: float,
        rate_multiplier: float,
        rate_variation_period: int,
        ksvc_template: str,
        file_name: str = "container_concurrency_results.pkl",
        warm_up_requests: int = 0,
        request_args: Optional[RequestArgs] = None,
) -> Dict[int, List[RequestStats]]:
    """Run scaling tests with various container concurrencies."""

    tasks = []
    for container_concurrency in container_concurrencies:
        # Keep the target concurrency the same by varying the percentage
        target_percentage = int(target_concurrency / container_concurrency * 100)
        task = asyncio.create_task(
            test_scaling(requests,
                         target_percentage,
                         container_concurrency,
                         request_rate,
                         rate_multiplier,
                         rate_variation_period,
                         ksvc_template,
                         warm_up_requests=warm_up_requests,
                         request_args=request_args,
                         desc=f"{container_concurrency}cc"))
        tasks.append(task)

    all_results = {container_concurrencies[i]: result for i, result in
                   enumerate(await asyncio.gather(*tasks))}

    with open(file_name, "wb") as file:
        pickle.dump(all_results, file)

    return all_results


def plot_scaling_latencies(results: List[RequestStats],
                           percentiles=None,
                           bin_width: int = 30,
                           avg_window: int = 120,
                           ax1: Optional[plt.Axes] = None,
                           title: str = None) -> Tuple[float, float]:
    """Plot a comparison between request rate and latency."""

    if percentiles is None:
        percentiles = [50]

    sent_times = np.array([stats.start_time for stats in results])
    sent_times -= np.min(sent_times)

    latencies = np.array([stats.normalized_latency for stats in results])

    # Sort the events by time
    sorted_indices = np.argsort(sent_times)
    sent_times = sent_times[sorted_indices]
    latencies = latencies[sorted_indices]

    # Calculate the rolling percentiles of latency over the last N min
    rolling_percentiles = np.zeros((len(percentiles),len(sent_times)),
                                   dtype=float)

    for i, event_time in enumerate(sent_times):
        if event_time < avg_window:
            continue
        within_window_expr = (sent_times >= (event_time - avg_window)) & \
                             (sent_times <= event_time)
        indices_within_window = np.where(within_window_expr)[0]
        window_percentiles = np.percentile(latencies[indices_within_window],
                                           percentiles)
        rolling_percentiles[:, i] = window_percentiles

    # Create the figure and first y-axis for rolling average
    if ax1 is None:
        _, ax1 = plt.subplots()

    # Plot the rolling percentiles
    ax1.set_title(title)
    for i, percentile in enumerate(percentiles):
        ax1.plot(sent_times[avg_window:], rolling_percentiles[i, avg_window:],
                 label=f'{percentile}th Percentile')
    ax1.set_xlabel('Time Since First Request (seconds)')
    ax1.set_ylabel('Normalized Request Latency (s/tok)')
    ax1.tick_params(axis='y')

    # Create the secondary y-axis for the histogram
    ax2 = ax1.twinx()

    # Calculate the histogram data (count of events within 5-second intervals)
    bins = np.arange(0, sent_times[-1] + bin_width, bin_width)
    hist, _ = np.histogram(sent_times, bins=bins)

    # Plot the histogram of request distributions
    ax2.bar(bins[:-1],
            hist,
            width=bin_width,
            align='edge',
            alpha=0.5,
            label='Event Frequency',
            color='gray')
    ax2.set_ylabel('Event Frequency')
    ax2.tick_params(axis='y')

    # Show legend for both y-axes
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    global_min = np.min(rolling_percentiles[:, avg_window:])
    global_max = np.max(rolling_percentiles[:, avg_window:])

    return global_min, global_max


def plot_all_scaling_latencies(all_results: Dict[int, List[RequestStats]],
                               bin_width: int = 30,
                               avg_window: int = 120,
                               num_cols: int = 2,
                               figsize: Tuple = (15, 15),
                               title: str = "Impact of Container Concurrency on Scaling Performance",
                               percentiles: Optional[List[int]] = None,
                               output: str = "") -> None:
    if percentiles is None:
        percentiles = [50]

    num_rows = int(np.ceil(len(all_results) / num_cols))

    fig, axs = plt.subplots(num_rows, num_cols, figsize=figsize)
    fig.suptitle(title)

    global_min = float("inf")
    global_max = float("-inf")

    for i, (concurrency, results) in enumerate(all_results.items()):
        row = i // num_cols
        col = i % num_cols
        avg_min, avg_max = plot_scaling_latencies(
            results,
            bin_width=bin_width,
            avg_window=avg_window,
            ax1=axs[row, col],
            title=f"Container Concurrency: {concurrency}",
            percentiles=percentiles
        )
        global_min = min(global_min, avg_min)
        global_max = max(global_max, avg_max)

    for row in range(num_rows):
        for col in range(num_cols):
            axs[row, col].set_ylim(bottom=global_min, top=global_max*1.1)

    plt.tight_layout()
    plt.show()

    if output:
        fig.savefig(output)


def get_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument("-o", "--output",
                      type=str,
                      default="scaling_concurrent_results.",
                      help="File to store the results, both a pkl of the raw "
                           "data and a png of the graphs. "
                           "Defaults to 'scaling_concurrent_results'")
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
    args.add_argument("-c", "--container-concurrencies",
                      type=int,
                      nargs="+",
                      default=[1],
                      help="A list of container concurrency levels to test "
                           "that serve as a hard limit in Knative. Each level "
                           "will involve deploying a separate Knative service. "
                           "Defaults to '1'.")
    args.add_argument("--target-concurrency",
                      type=int,
                      default=1,
                      help="The concurrency level that Knative will target and "
                           "base it's autoscaling decision on. Should be less "
                           "than any of the hard concurrencies. Defaults to 1.")
    args.add_argument("-r", "--request-rate",
                      type=float,
                      default=1.0,
                      help="The baseline requests per second. Defaults to 1.")
    args.add_argument("--rate-multiplier",
                      type=float,
                      default=1.0,
                      help="The maximum multiplier used to alter the request "
                           "rate during the experiment. The rate multiplier "
                           "will vary sinusoidally between 1 and this value. "
                           "Defaults to 1.0.")
    args.add_argument("-p", "--rate-variation-period",
                      type=int,
                      default=100,
                      help="The period of the sinusoidal rate variation in "
                           "number of requests. The rate multiplier will vary "
                           "from 1 to the 'rate_multiplier', and back to 1 "
                           "over this many requests. Smaller values correspond "
                           "to faster increaess in traffic. Defaults to 100.")
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
    args = args.parse_args()

    assert args.target_concurrency <= min(args.container_concurrencies), \
        "Target concurrency must be less than the min container concurrency."

    return args


async def main() -> None:
    args = get_args()
    requests = sample_requests(args.dataset, args.requests, args.tokenizer)

    request_args = RequestArgs(model=args.model,
                               n=args.n_sampling)

    print("Running tests...")
    results = await run_container_concurreny_experiment(
        requests,
        args.target_concurrency,
        args.container_concurrencies,
        args.request_rate,
        args.rate_multiplier,
        args.rate_variation_period,
        args.ksvc_template,
        file_name=f"{args.output}.pkl",
        request_args=request_args
    )

    plot_all_scaling_latencies(
        results,
        title="Impact of Container Concurrency on Scaling Performance w/ a "
              f"Target Conccurency of {args.target_concurrency}",
        output=f"{args.output}.png"
    )


if __name__ == "__main__":
    asyncio.run(main())
