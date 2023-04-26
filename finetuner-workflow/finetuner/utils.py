import resource
from contextlib import contextmanager

from typing import NamedTuple, Optional

import torch
import psutil
from transformers.modeling_utils import no_init_weights

__all__ = (
    "GlobalGPUMemoryUsage",
    "TorchGPUMemoryUsage",
    "CPUMemoryUsage",
    "MemoryUsage",
    "no_init"
)


class GlobalGPUMemoryUsage(NamedTuple):
    total: int
    free: int
    used: int

    @classmethod
    def now(cls, device=None):
        if torch.cuda.is_available():
            free, total = torch.cuda.mem_get_info(device)
            return cls(total, free, total - free)
        else:
            return None

    def __str__(self):
        return "GPU: (U: {:,}MiB F: {:,}MiB T: {:,}MiB)".format(
            self.used >> 20, self.free >> 20, self.total >> 20
        )


class TorchGPUMemoryUsage(NamedTuple):
    reserved: int
    reserved_max: int
    used: int
    used_max: int

    @classmethod
    def now(cls, device=None):
        if torch.cuda.is_available():
            stats = torch.cuda.memory.memory_stats(device)
            return cls(
                stats.get("reserved_bytes.all.current", 0),
                stats.get("reserved_bytes.all.peak", 0),
                stats.get("allocated_bytes.all.current", 0),
                stats.get("allocated_bytes.all.peak", 0)
            )
        else:
            return None

    def __str__(self):
        return "TORCH: (R: {:,}MiB/{:,}MiB, A: {:,}MiB/{:,}MiB)".format(
            self.reserved >> 20, self.reserved_max >> 20,
            self.used >> 20, self.used_max >> 20
        )


class CPUMemoryUsage(NamedTuple):
    maxrss_kibibytes: int
    free: int

    @classmethod
    def now(cls):
        maxrss = (
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        )
        vmem = psutil.virtual_memory()
        return cls(maxrss, vmem.free)

    def __str__(self):
        return "CPU: (maxrss: {:,}MiB F: {:,}MiB)".format(
            self.maxrss_kibibytes >> 10, self.free >> 20
        )


class MemoryUsage(NamedTuple):
    cpu: CPUMemoryUsage
    gpu: Optional[GlobalGPUMemoryUsage]
    torch: Optional[TorchGPUMemoryUsage]

    @classmethod
    def now(cls):
        gpu_info = torch_info = None
        try:
            gpu_info = GlobalGPUMemoryUsage.now()
            torch_info = TorchGPUMemoryUsage.now()
        except AssertionError:
            pass
        return cls(CPUMemoryUsage.now(), gpu_info, torch_info)

    def __str__(self):
        return " ".join(map(str, filter(None, self)))


@contextmanager
def no_init():
    # `no_init_weights` doesn't suppress initialization of some layers by default
    # See https://github.com/huggingface/transformers/issues/18505
    def dummy(self):
        return

    modules = [torch.nn.Linear, torch.nn.Embedding, torch.nn.LayerNorm]
    original = {}
    for mod in modules:
        original[mod] = mod.reset_parameters
        mod.reset_parameters = dummy

    try:
        with no_init_weights():
            yield
    finally:
        for mod in modules:
            mod.reset_parameters = original[mod]
