"""
These utility funcitons interact with kubernetes by running kubectl commands.
They rely on your local kubectl being configured properly.
"""

import asyncio
import re
import subprocess
import time
from typing import Dict

URL_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
KSVC_WAIT_INTERVAL = 1  # seconds


def get_ksvc_template(name: str,
                      annotations: Dict[str, str] = None,
                      container_concurrency: int = 0,
                      timeout_seconds: int = 300,
                      ksvc_template: str = "ksvc-template.yaml") -> str:
    if annotations is None:
        annotations = {}

    annotation_split = "\n" + (" " * 8)
    annotations = annotation_split.join([f'{key}: "{value}"' for key, value
                                         in annotations.items()])

    with open(ksvc_template, "r") as file:
        ksvc_manifest = file.read()

    ksvc_manifest = ksvc_manifest.format(name=name,
                                         annotations=annotations,
                                         container_concurrency=container_concurrency,
                                         timeout_seconds=timeout_seconds)

    return ksvc_manifest


def get_status(manifest: str) -> str:
    get_command = f"kubectl get -f - <<EOF\n{manifest}\nEOF"
    status = subprocess.run(get_command, shell=True, check=True,
                            capture_output=True, text=True)
    return status.stdout


async def wait_for_ksvc(manifest: str) -> str:
    while True:
        status = get_status(manifest)
        if "True" in status:
            url = re.findall(URL_PATTERN, status)[0]
            return url
        await asyncio.sleep(KSVC_WAIT_INTERVAL)


async def deploy_ksvc(manifest: str,
                      wait: bool = True,
                      verbose: bool = True) -> str:
    deploy_command = f"kubectl apply -f - <<EOF\n{manifest}\nEOF"
    start = time.perf_counter()
    subprocess.run(deploy_command,
                   shell=True,
                   check=True,
                   capture_output=not verbose)

    url = None
    while not url:
        urls = re.findall(URL_PATTERN, get_status(manifest))
        if len(urls) == 0:
            continue
        url = urls[0]

    if not wait:
        return url

    url = await wait_for_ksvc(manifest)

    startup_time = time.perf_counter() - start
    if verbose:
        print(f"Startup time: {startup_time:.2f}s")

    return url


def delete_ksvc(name: str = None,
                manifest: str = None,
                verbose: bool = True) -> None:
    try:
        if name:
            delete_command = f"kubectl delete ksvc {name}"
        else:
            delete_command = f"kubectl delete -f - <<EOF\n{manifest}\nEOF"

        subprocess.run(delete_command,
                       shell=True,
                       check=True,
                       capture_output=not verbose)
    except Exception as e:
        print("WARNING: Failed to delete ksvc:", e)
