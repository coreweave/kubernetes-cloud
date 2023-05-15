import argparse
import copy
import operator
import os.path
import resource
import types
from contextlib import contextmanager
from functools import wraps, partial

from typing import NamedTuple, Optional

import torch
import psutil
from transformers.modeling_utils import no_init_weights

__all__ = (
    "GlobalGPUMemoryUsage",
    "TorchGPUMemoryUsage",
    "CPUMemoryUsage",
    "MemoryUsage",
    "no_init",
    "DashParser",
    "FuzzyBoolAction",
    "validation",
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
        return " ".join(str(item) for item in self if item)


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


# Argparse utilities

class _NoUnderscoreHelpFormatter(argparse.HelpFormatter):
    """
    Help formatter that hides argument aliases containing underscores.
    """

    def add_argument(self, action):
        # Don't modify the actual action
        action = copy.deepcopy(action)
        if action.option_strings:
            action.option_strings = [
                s for s in action.option_strings if "_" not in s
            ]
        return super().add_argument(action)


class DashParser(argparse.ArgumentParser):
    """
    Argument parser that automatically adds variants of arguments with dashes
    instead of underscores, and vice-versa, so --x_y also adds --x-y,
    and --x-y also adds --x_y.
    Only the version with dashes is displayed in the help text.
    """

    @wraps(argparse.ArgumentParser.__init__)
    def __init__(self, *args, **kwargs):
        self._dash_aliases = {}
        kwargs.setdefault("formatter_class", _NoUnderscoreHelpFormatter)
        super().__init__(*args, **kwargs)

    @wraps(argparse.ArgumentParser.add_argument)
    def add_argument(self, *args, **kwargs):
        dashed_args = []
        for arg in args:
            bare_arg = arg.lstrip(self.prefix_chars)
            if not bare_arg:
                dashed_args.append(arg)
                continue
            prefix = arg[: len(arg) - len(bare_arg)]
            if prefix:
                canonical = None
                # Flags:
                # Add a counterpart with dashes, if underscores are used
                if "_" in bare_arg:
                    dashed_arg = prefix + bare_arg.replace("_", "-")
                    dashed_args.append(dashed_arg)
                    canonical = dashed_arg
                # Add the original
                dashed_args.append(arg)
                if canonical is None:
                    canonical = arg
                else:
                    self._dash_aliases[arg] = canonical
                # Add a counterpart with underscores, if dashes are used
                if "-" in bare_arg:
                    underscored_arg = prefix + bare_arg.replace("-", "_")
                    dashed_args.append(underscored_arg)
                    self._dash_aliases[underscored_arg] = canonical
                # This ordering intentionally puts dashed arguments
                # before underscored ones to make them "canonical."
            else:
                # Positional arguments:
                if "-" in arg:
                    # Dashes are invalid in positional arguments
                    arg = arg.replace("-", "_")
                if "_" in arg and "metavar" not in kwargs:
                    # Show a dash in the usage text
                    kwargs["metavar"] = arg.replace("_", "-")
                dashed_args.append(arg)
        return super().add_argument(*dashed_args, **kwargs)

    if hasattr(argparse.ArgumentParser, "_get_option_tuples"):
        def _get_option_tuples(self, *args, **kwargs):
            # Fixing a sort-of-bug in CPython that marks aliases
            # of a single argument as being ambiguous.
            # Won't affect anything if this function isn't used internally,
            # but the implementation has been relatively untouched from 2015
            # (CPython 3.5) through at least CPython 3.11,
            # so this is fairly stable.
            tuples = getattr(super(), "_get_option_tuples")(*args, **kwargs)
            if len(tuples) <= 1:
                return tuples
            # Deduplicate tuples sharing the same
            # canonical option_string and action
            filtered_tuples = {}
            for t in tuples:
                action, option_string, *rest = t
                # Canonicalize the option_string
                option_string = self._dash_aliases.get(option_string, option_string)
                filtered_tuples[(action, option_string)] = rest
            return [
                (action, option_string, *rest)
                for (action, option_string), rest in filtered_tuples.items()
            ]


class FuzzyBoolAction(argparse.Action):
    """
    Action type that accepts boolean flags with optional explicit arguments
    E.g. both bare ``--opt`` and ``--opt=True`` or ``--opt=False``,
    to make scripting simpler.

    Performs fuzzy matching so "0", "no", "f", and "false" (case insensitive)
    mean ``False``, and everything else means ``True``.

    ``True`` means the same as the flag being present,
    and ``False`` means the same as the flag being absent.
    Thus, if default=True, then the behaviour is inverted,
    and ``--opt`` sets ``False``,
    ``--opt=True`` sets ``False``,
    and ``--opt=False`` sets ``True``.
    This lets you define an argument like
    ``parser.add_argument("--no-opt", dest="opt", default=True)``
    that will control ``args.opt`` in an inverted way,
    like ``action="store_false"`` allows.
    """

    def match(self, arg: str) -> bool:
        if arg.strip().lower() in ("0", "no", "f", "false"):
            return self.default
        else:
            return self.const

    def __init__(
        self,
        option_strings,
        dest,
        nargs=argparse.OPTIONAL,
        default=False,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar="BOOL",
    ):
        type = self.match if type is None or type is bool else type
        # nargs, default, and metavar are specified above for clarity,
        # but they are set again here too to override any explicit Nones
        # that may be passed down through argparse.
        nargs = argparse.OPTIONAL if nargs is None else nargs
        default = False if default is None else default
        const = not default
        metavar = "BOOL" if metavar is None else metavar
        if not isinstance(default, bool):
            raise ValueError("FuzzyBoolAction default must be a boolean")
        super().__init__(
            option_strings,
            dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


# Argparse validators

def _compares(
    numeric_type,
    comparator,
    threshold,
    *,
    condition: str,
    special_val=None,
):
    if special_val:
        condition = f"{condition} or {special_val}"

    def check(s: str) -> numeric_type:
        i = numeric_type(s)
        valid = (
            comparator(i, threshold)
            or (special_val is not None and i == special_val)
        )
        if not valid:
            raise argparse.ArgumentTypeError(f"must be {condition}, not {i}")
        return i

    return check


def _extant_file(s: str, *, optional=False) -> str:
    if not s:
        if optional:
            return ""
        else:
            raise argparse.ArgumentTypeError("must be specified")
    if not os.path.isfile(s):
        if os.path.lexists(s):
            error = f"invalid file: {s} exists, but isn't a file"
        else:
            error = f"file not found: {s}"
        raise argparse.ArgumentTypeError(error)
    return s


# Small in-line module to act as a namespace.
validation = types.ModuleType("_validation")
validation.__dict__.update(
    positive=partial(
        _compares, comparator=operator.gt, threshold=0, condition="positive"
    ),
    non_negative=partial(
        _compares, comparator=operator.ge, threshold=0, condition="non-negative"
    ),
    at_most_1=partial(
        _compares, comparator=operator.le, threshold=1, condition="at most 1"
    ),
    at_most_32_bit=partial(
        _compares,
        comparator=operator.le,
        threshold=(1 << 32) - 1,
        condition="at most 2 ** 32 - 1",
    ),
    extant_file=_extant_file,
    optional_extant_file=partial(_extant_file, optional=True),
)
