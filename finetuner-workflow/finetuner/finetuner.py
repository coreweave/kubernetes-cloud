#!/bin/which python3
# A simple HuggingFace-based text-model finetuner meant to be used in an
# automated workflow.
import json
import gc
import mmap

import numpy
import os
import sys
import time
import math
from decimal import Decimal
import random
import torch
import torch.distributed
from torch import Tensor
from torch.utils.data import Dataset, random_split, Subset
import pathlib
from typing import Tuple, List
import socket
import subprocess
import shutil
import logging
import deepspeed
from deepspeed.runtime.zero.stage_1_and_2 import (
    estimate_zero2_model_states_mem_needs_all_live,
)
from deepspeed.runtime.zero.stage3 import (
    estimate_zero3_model_states_mem_needs_all_live,
)
from tensorizer import TensorDeserializer, utils as tensorizer_utils, stream_io

from utils import *


os.environ["TOKENIZERS_PARALLELISM"] = "false"

this_path = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(this_path + "/transformers/src")

import transformers
from transformers import (
    AutoTokenizer,
    AutoConfig,
    TrainingArguments,
    Trainer,
    AutoModelForCausalLM,
    IntervalStrategy,
    TrainerCallback,
    PreTrainedTokenizer,
)
from transformers.modeling_utils import PreTrainedModel

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"

val = validation

parser = DashParser(description="Simple Text Model Finetuner")

parser.add_argument(
    "--run-name", type=str, help="The run name to use", required=True
)
parser.add_argument(
    "--model",
    type=str,
    help="The model to train against (directory, or HuggingFace ID)",
    required=True,
)
parser.add_argument(
   "--trust-remote-code",
   action=FuzzyBoolAction,
   help="Whether to trust remote code coming with the model",
   default=False,
)
parser.add_argument(
    "--dataset",
    type=val.extant_file,
    help="Pre-tokenized dataset to use",
    required=True,
)
parser.add_argument(
    "--tensorizer-uri",
    type=str,
    help="An S3 URI or path to use to load pretrained weights for Tensorizer",
    default="",
)
parser.add_argument(
    "--lr", type=val.non_negative(float), help="Learning rate", default=5e-5
)
parser.add_argument(
    "--epochs",
    type=val.positive(int),
    help="Number of epochs to train for",
    default=1,
)
parser.add_argument(
    "--train-ratio",
    type=val.at_most_1(val.non_negative(Decimal)),
    help="Ratio of train to value from dataset",
    default=Decimal("0.9"),
)
parser.add_argument(
    "--eot",
    type=str,
    help="EOT token to use",
    default="",  # default is model-dependent
)
parser.add_argument(
    "--pad",
    type=str,
    help="Pad token to use",
    default="",  # default is model-dependent
)
parser.add_argument(
    "--bs",
    type=val.positive(int, special_val=-1),
    help="Batch size (-1 == autosize)",
    default=-1,
)
parser.add_argument(
    "--bs-divisor",
    type=val.positive(Decimal),
    help="Batch size divisor for automatically determining batch size",
    default=Decimal(1),
)
parser.add_argument(
    "--gradients",
    type=val.positive(int),
    help="Gradient accumulation steps",
    default=5,
)
parser.add_argument(
    "--zero-stage",
    type=int,
    help="ZeRO optimizer stage",
    default=3,
    choices=range(0, 4),
)
parser.add_argument(
    "--seed",
    # Range restrictions are imposed by numpy.random.seed
    type=val.at_most_32_bit(val.non_negative(int)),
    help="Random seed value",
    default=42,
)
parser.add_argument(
    "--output-path", type=str, help="Root path of all output", default="./"
)
parser.add_argument(
    "--no-resume",
    action=FuzzyBoolAction,
    help="Do not resume from last checkpoint",
    dest="resume",
    default=True,  # resume=True
)
parser.add_argument(
    "--cache", type=str, help="HuggingFace cache location", default="/tmp"
)
parser.add_argument(
    "--save-steps",
    type=val.non_negative(int),
    help="# of steps between checkpoint saves",
    default=500,
)
parser.add_argument(
    "--context-size",
    type=val.positive(int),
    help="Dataset context sizes",
    default=2048,
)
parser.add_argument(
    "--project-id",
    type=str,
    help="Project ID for reporting",
    default="huggingface",
)
parser.add_argument(
    "--logs", type=str, help="Log directory location", default="./logs"
)
parser.add_argument(
    "--ds-config",
    type=val.optional_extant_file,
    help="DeepSpeed configuration",
    default="./ds_config.json",
)
parser.add_argument(
    "--fp16",
    action=FuzzyBoolAction,
    help="Force training in fp16",
    default=False,
)
parser.add_argument(
    "--fp16-full-eval",
    action=FuzzyBoolAction,
    help="Evaluate in fp16, not in fp32 or mixed precision",
    default=False,
)
parser.add_argument(
    "--no-shuffle",
    action=FuzzyBoolAction,
    help="Disable shuffling contexts",
    dest="shuffle",
    default=True,  # shuffle=True
)
parser.add_argument(
    "--prompt-file",
    type=val.optional_extant_file,
    help="Prompt file to use for checkpoint sampling",
)
parser.add_argument(
    "--prompt-every",
    type=val.non_negative(int, special_val=-1),
    default=0,
    help="Prompt every N steps",
)
parser.add_argument(
    "--prompt-tokens",
    type=val.non_negative(int),
    default=200,
    help="Number of tokens to sample from prompt",
)
parser.add_argument(
    "--prompt-samples",
    type=val.non_negative(int),
    help="Number of samples to generate",
    default=5,
)
parser.add_argument(
    "--top-k",
    type=val.non_negative(int),
    help="Top K to use for prompt sampling",
    default=50,
)
parser.add_argument(
    "--top-p",
    type=val.at_most_1(val.non_negative(float)),
    help="Top P to use for prompt sampling",
    default=0.95,
)
parser.add_argument(
    "--temperature",
    type=val.positive(float),
    help="Temperature to use for prompt sampling",
    default=1.0,
)
parser.add_argument(
    "--repetition-penalty",
    type=val.positive(float),
    help="Repetition penalty to use for prompt sampling",
    default=1.1,
)
parser.add_argument(
    "--local-rank",
    type=val.non_negative(int, special_val=-1),
    help="For distributed training: local_rank",
    default=-1,
)
parser.add_argument(
    "--log-level",
    type=str.upper,
    help="Log level to use",
    default="INFO",
    choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(args.log_level)
fh = logging.StreamHandler()
if args.local_rank != -1:
    fh_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s(%(process)d)"
        f" - RANK {args.local_rank} - %(message)s"
    )
else:
    fh_formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
fh.setFormatter(fh_formatter)
logger.addHandler(fh)


def read_prompts(prompt_file):
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompts = (line.rstrip("\n").replace("\\n", "\n") for line in f)
        return list(filter(None, prompts))


try:
    if args.prompt_file:
        if not read_prompts(args.prompt_file):
            parser.error(f"Provided prompt file was blank: {args.prompt_file}")
except OSError:
    parser.error(
        f"Provided prompt file could not be read: {args.prompt_file}"
    )


def is_main_process() -> bool:
    return args.local_rank in [-1, 0]


# To be used in cases where using if statements is ugly.
def main_process_print(*args, **kwargs):
    if is_main_process():
        logger.info(*args, **kwargs)


# Determine the number of processes being used for training.
# First, try to get the DeepSpeed/PyTorch configured world size
world_size = os.getenv("WORLD_SIZE", None)
if world_size is not None:
    # The environment variable is an int stored as a string
    try:
        world_size = int(world_size)
    except ValueError:
        world_size = None

# Fall back to asking PyTorch
if world_size is None:
    # If distributed training is enabled, torch.distributed
    # should be able to query the world size.
    if torch.distributed.is_initialized():
        world_size = torch.distributed.get_world_size()
        if world_size == -1:
            world_size = None

    # Otherwise, assume the world comprises all visible GPUs on this node
    if world_size is None and torch.cuda.is_available():
        world_size = torch.cuda.device_count()
    else:
        # If no other information is available,
        # just assume this is the only process.
        world_size = 1


# Where we write our training checkpoints and final model.
output_dir = os.path.abspath(
    os.path.join(args.output_path, "results-" + args.run_name)
)

# Discover if we have any checkpoints to resume from.
if args.resume:
    try:
        output_dir_list = os.listdir(output_dir)
        last_checkpoint = sorted(
            output_dir_list, key=lambda x: int(x.split("-")[1])
        )[-1]
    except Exception:
        last_checkpoint = None
else:
    last_checkpoint = None
logger.info(f"LAST CHECKPOINT: {last_checkpoint}")

# Set up `wandb` reporting if we have an API key, and resume reporting
# if we are resuming a checkpoint.
report_to = ["none"]
wandb_key = os.getenv("WANDB_API_KEY", "").strip()
if not wandb_key:
    logger.warning("WANDB_API_KEY: No WANDB_API_KEY found, not reporting to wandb.")
    os.environ["WANDB_DISABLED"] = "True"

import wandb

if wandb_key and is_main_process():
    report_to = ["wandb"]

    if last_checkpoint is not None:
        wandb_api = wandb.Api(overrides={"project": args.project_id})
        for run in wandb_api.runs(path=args.project_id):
            logger.info(f"PRIOR RUN: {run} {run.name} {run.id} {run.state}")
            if run.state in ["crashed", "failed"] and run.name == args.run_name:
                logger.info(f"CHECKPOINT: Resuming {run.id}")
                run = wandb.init(
                    id=run.id,
                    project=args.project_id,
                    resume="must",
                    name=run.name,
                )
                break
    else:
        run = wandb.init(project=args.project_id, name=args.run_name)
else:
    run = wandb.init(
        project=args.project_id, name=args.run_name, mode="disabled"
    )

# We evaluate if args.model is already tensorized under a public s3 bucket.
try:
    if not args.tensorizer_uri:
        model_id = "/".join(args.model.split("/")[-2:])
        with stream_io.CURLStreamFile(
            uri=f"https://accel-object.ord1.coreweave.com/tensorized/{model_id}/model.tensors",
            end=1,
        ) as test_stream:
            test_stream.read(1)
        uri_dtype = "fp16/" if args.fp16 else ""
        args.model = model_id
        args.tensorizer_uri = (
            f"s3://tensorized/{args.model}/{uri_dtype}model.tensors"
        )
except OSError:
    pass

# Set up our tokenizer.
tokenizer: PreTrainedTokenizer
try:
    # If a special token (args.eot or args.pad) is explicitly provided,
    # then use it; otherwise use the model's defaults if they exist;
    # otherwise use hardcoded defaults.

    # The resulting padding token ID must match the one the dataset tokenizer
    # used, or the existing padding tokens in the dataset
    # will not be properly masked during training.

    tokens_to_add = {}
    if args.eot:
        tokens_to_add["eos_token"] = args.eot
    if args.pad:
        tokens_to_add["pad_token"] = args.pad

    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        **tokens_to_add,
        cache_dir=args.cache,
    )

    tokens_to_add.clear()
    if "eos_token" not in tokenizer.special_tokens_map:
        tokens_to_add["eos_token"] = "<|endoftext|>"
    if "pad_token" not in tokenizer.special_tokens_map:
        tokens_to_add["pad_token"] = "<|endoftext|>"
    if tokens_to_add:
        tokenizer.add_special_tokens(tokens_to_add)
except Exception as e:
    logger.error(e)
    sys.exit(1)


def estimate_batch_size(divisor: Decimal = Decimal(1)) -> int:
    """
    Attempts to estimate the batch size to use based on the amount of RAM
    that the model takes up, and RAM free.

    :return: batch size to use
    """
    gc.collect()
    new_bs = 1
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
    mem = MemoryUsage.now()
    if None not in (mem.gpu, mem.torch):
        new_bs = math.ceil(mem.gpu.free / (mem.torch.used * divisor))
    logger.info(mem)
    logger.info(f"Setting batch size to {new_bs}")
    # if new_bs == 1:
    #    gc.set_threshold(10)
    return new_bs


class ModifiedTrainer(Trainer):
    """
    A modification of the Trainer class to allow for better console reporting
    in the container and fix gradient handling on the loss tensor returned.
    """

    def compute_loss(self, model, inputs, return_outputs=False):
        if "labels" in inputs:
            inputs["labels"].masked_fill_(~inputs["attention_mask"], -100)

        results = super().compute_loss(model, inputs, return_outputs)
        loss = results[0] if return_outputs else results

        # Hack -- enable `requires_grad` on `loss`
        loss.requires_grad_(True)

        # Hack -- output a (useful) GPU ram update to flush tqdm.
        self.report_idx = getattr(self, "report_idx", 0) + 1
        if self.report_idx % (2 * self.args.gradient_accumulation_steps) == 0:
            if is_main_process():
                print(f"\nLOSS: {loss:.3f} {MemoryUsage.now()}",
                      file=sys.stderr, flush=True)
                sys.stderr.flush()

        return results


class PerformanceCallback(TrainerCallback):
    def __init__(self) -> None:
        super().__init__()
        self.start_time = None
        self.opt_step = None
        self.ff_step = None

    def on_step_begin(self, args, state, control, **kwargs):
        if self.start_time is None:
            self.start_time = time.time()
            self.opt_step = 0
            self.ff_step = 0

    def on_substep_end(self, args, state, control, **kwargs):
        self.ff_step = time.time()

    def on_step_end(self, args, state, control, **kwargs):
        self.opt_step = time.time()
        if is_main_process():
            # Report to WandB
            step_time = self.opt_step - self.start_time
            rank_samples_per_second = (
                args.per_device_train_batch_size
                * args.gradient_accumulation_steps
                / step_time
            )
            world_samples_per_second = world_size * rank_samples_per_second
            wandb.log(
                {
                    "perf/opt_time": self.opt_step - self.ff_step,
                    "perf/gas_time": self.ff_step - self.start_time,
                    "perf/total_time_per_step": step_time,
                    "perf/rank_samples_per_second": rank_samples_per_second,
                    "perf/world_samples_per_second": world_samples_per_second,
                },
                step=state.global_step,
            )
        self.start_time = None
        self.opt_step = None
        self.ff_step = None


class ModelSampler(TrainerCallback):
    """
    Test the model on one or more prompts every so often and report to the
    console, and to each rank's WandB run.
    """

    def __init__(
        self,
        prompt_file: str,
        tokenizer: PreTrainedTokenizer,
        generate_tokens: int = 200,
        batch_size: int = 1,
        num_samples: int = 1,
        gas: int = 1,
        report_every: int = 100,
        context_size: int = 2048,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not prompt_file:
            raise ValueError("Must provide a prompt file")
        if not os.path.exists(prompt_file):
            raise ValueError(f"Prompt file {prompt_file} does not exist")
        self.train_batch_size = batch_size
        self.tokenizer = tokenizer
        self.gas = gas
        self.prompt_file = prompt_file
        self.wandb = wandb
        self.report_every = report_every
        self.run_name = run.name
        self.generate_tokens = generate_tokens
        self.num_samples = num_samples
        self.context_size = context_size
        self.tokens_per_step = batch_size * context_size
        self.table_data = []

    def on_step_end(
        self, args, state, control, model: PreTrainedModel = None, **kwargs
    ):
        if not model:
            return
        if state.global_step % self.report_every == 0 or state.global_step == 1:
            curr_tokens_step = (
                state.global_step * self.train_batch_size * self.gas * world_size
            )
            main_process_print(
                f"\nSTEP {state.global_step}: Evaluating on {self.prompt_file}...",
            )
            model.eval()
            sys.stderr.flush()
            for prompt in read_prompts(self.prompt_file):
                main_process_print("=============================")
                main_process_print(f"PROMPT: {prompt}")
                start = time.time()
                outputs = evaluate(
                    prompt,
                    self.generate_tokens,
                    self.num_samples,
                    model,
                    self.tokenizer,
                )
                end = time.time()
                main_process_print(f"INFERENCE TIME: {end - start:.2f}s")
                for output_text in outputs:
                    self.table_data.append(
                        [
                            self.run_name,
                            state.global_step,
                            curr_tokens_step,
                            prompt,
                            output_text,
                        ]
                    )
                    main_process_print("-----------------------------")
                    main_process_print(f"RESPONSE: {output_text}")
            # It is still useful to collect evaluations on other ranks in their
            # respective WandB runs.
            wandb.log(
                {
                    "Generations": wandb.Table(
                        data=self.table_data,
                        columns=[
                            "Run",
                            "Step",
                            "Contexts Trained",
                            "Prompt",
                            "Generated Text",
                        ],
                    )
                },
                commit=False,
            )
            model.train()


class TokenizedDataset(Dataset):
    """
    Consumes a flat binary file containing 16-bit token serialization, aligned
    along `context_length` chunks.
    """

    def __init__(self, path: str, context_length: int = 2048):
        file_stat = os.stat(path)
        file_handle = os.open(path, os.O_RDONLY)
        self._mmap = mmap.mmap(
            file_handle, file_stat.st_size, access=mmap.ACCESS_READ
        )
        self._context_length = context_length
        self._context_size = context_length * 2
        self.length = int(file_stat.st_size / 2 / context_length)
        length_mb = os.stat(path).st_size / (1 << 20)
        num_tokens = self.length * context_length
        self._padding_is_ambiguous = tokenizer.pad_token_id == tokenizer.eos_token_id
        self._pad_token_id = tokenizer.pad_token_id
        if is_main_process():
            logger.info(f"DATASET: {path}")
            logger.info(
                f"DATASET SIZE: {length_mb:,.2f}MiB, {num_tokens:,} tokens, "
                f"{self.length:,} contexts"
            )

    def __len__(self) -> int:
        return self.length

    def load(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        begin = idx * self._context_size
        end = begin + self._context_size
        mv = memoryview(self._mmap)[begin:end]
        arr = numpy.ndarray.__new__(
            numpy.memmap,
            [self._context_length],
            dtype=numpy.ushort,
            buffer=mv,
            offset=0,
        ).astype(numpy.int_)
        input_ids = torch.from_numpy(arr)
        if self._padding_is_ambiguous and idx != self.length - 1:
            # Assume only the final context has padding if the padding token
            # is indistinguishable from the end-of-sentence token
            # to not accidentally mask away any semantically relevant
            # end-of-sentence tokens.
            #
            # For gpt_bpe outputs, only the final context generated is padded,
            # so this is an accurate heuristic so long as the contexts
            # were not shuffled when they were written.
            #
            # An alternative implementation of this could instead probe
            # the last two token IDs in each retrieved context
            # to check for consecutive end-of-sentence tokens
            # as an indicator that padding is present.

            mask = torch.ones_like(input_ids, dtype=torch.bool)
        else:
            mask: torch.Tensor = input_ids != self._pad_token_id
        return input_ids, mask

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.load(idx)


# Inform the user of host, and various versions -- useful for debugging issues.
torch.cuda.set_device(args.local_rank if args.local_rank != -1 else 0)
if is_main_process():
    if logger.getEffectiveLevel() <= logging.INFO and device != "cpu":
        nvidia_smi = shutil.which("nvidia-smi")
        if nvidia_smi is not None:
            try:
                logger.info(
                    "NVIDIA-SMI CHECK: "
                    + subprocess.check_output([nvidia_smi], encoding="utf-8")
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to query nvidia-smi, error: {e}")
                sys.exit(1)
    logger.info(f"RUN NAME: {args.run_name}")
    logger.info(f"PROJECT ID {args.project_id}")
    logger.info(f"HOST: {socket.gethostname()}")
    logger.info(f"CUDA: {torch.version.cuda}")
    logger.info(f"TORCH: {torch.__version__}")
    logger.info(f"TRANSFORMERS: {transformers.__version__}")
    logger.info(MemoryUsage.now())
    logger.info(f"MODEL: {args.model}")
    logger.info(f"TRAIN RATIO: {args.train_ratio}")
    logger.info(f"CONTEXT LENGTH: {args.context_size} tokens")
    logger.info(f"SHUFFLE: {args.shuffle}")
    logger.info(f"EPOCHS {args.epochs}")
    logger.info(f"CHECKPOINT STEPS: {args.save_steps}")
    logger.info(f"TOKENIZER: {tokenizer}")
    logger.info(f"TOKENIZER SPECIAL TOKENS: {tokenizer.special_tokens_map}")
    logger.info(f"PROMPT FILE: {args.prompt_file}")
    logger.info(f"PROMPT EVERY: {args.prompt_every}")
    logger.info(f"PROMPT SAMPLES: {args.prompt_samples}")
    logger.info(f"PROMPT TOKENS: {args.prompt_tokens}")
    logger.info(f"FORCE FP16: {args.fp16}")
    logger.info(f"FP16 FULL EVAL: {args.fp16_full_eval}")
    logger.info(f"LOG LEVEL: {args.log_level}")


# Set random seed, for ML research purposes and reproducibility, it's important
# that we set this to a consistent value.
torch.manual_seed(args.seed)
random.seed(args.seed)
numpy.random.seed(args.seed)

# Set up our dataset from our tokenized data files, and split into training
# dataset and values dataset -- values dataset is used to test the outcome
# and determine our loss rate.
dataset = TokenizedDataset(args.dataset, context_length=args.context_size)
# FIXME: val_dataset isn't used anywhere, so it is disabled for now.
if args.train_ratio != 1:
    if is_main_process():
        logger.warning(
            "Validation statistics are not yet implemented,"
            " but data was requested to be set aside for the validation set"
            f" (--train_ratio was set to {args.train_ratio})."
            " Setting --train_ratio to 1.0 to not discard training data."
        )
    args.train_ratio = 1
train_size = int(args.train_ratio * len(dataset))
val_size = len(dataset) - train_size

if args.shuffle:
    train_dataset, val_dataset = random_split(dataset, (train_size, val_size))
else:
    # Pick a random contiguous subrange as the val_dataset
    val_dataset_start = random.randrange(len(dataset) - val_size)
    val_dataset_end = val_dataset_start + val_size
    # The train_dataset is everything before joined with everything after
    # the section dedicated to val_dataset, preserving the original ordering
    train_dataset = Subset(
        dataset,
        (*range(val_dataset_start), *range(val_dataset_end, len(dataset)))
    )
    val_dataset = Subset(dataset, range(val_dataset_start, val_dataset_end))

# Determine if we train in fp32 or fp16 mode.
trainer_fp16_args = {}
if args.fp16:
    trainer_fp16_args["fp16"] = True
if args.fp16_full_eval:
    trainer_fp16_args["fp16_full_eval"] = True

if is_main_process():
    logger.info(f"TRAIN_DATASET: {len(train_dataset):,} examples")
    logger.info(f"VALUE_DATASET: {len(val_dataset):,} examples")
    logger.info(f"RANDOM SEED: {args.seed}")


# Load our model that we're training. This may fetch via HTTP if not cached
# already.
model: PreTrainedModel

model_fp16_args = {"torch_dtype": torch.float16} if args.fp16 else {}
model_args = {
    "eos_token_id": tokenizer.eos_token_id,
    "pad_token_id": tokenizer.pad_token_id,
    "cache_dir": args.cache,
    "use_cache": False,
    "low_cpu_mem_usage": True,
    "trust_remote_code": args.trust_remote_code,
}

try:
    if args.tensorizer_uri:
        config = AutoConfig.from_pretrained(
            args.model,
            **model_args,
            **model_fp16_args,
        )
        model = tensorizer_utils.no_init_or_tensor(
            lambda: AutoModelForCausalLM.from_config(config)
        )

        deserializer = TensorDeserializer(args.tensorizer_uri)
        deserializer.load_into_module(model)
        deserializer.close()
        del deserializer
    else:
        with no_init():
            model = AutoModelForCausalLM.from_pretrained(
                args.model,  # Can be a HuggingFace ID or directory.
                **model_args,
                **model_fp16_args,
            )  # Gradient checkpointing needs this off.
            if last_checkpoint is None:
                model = model.to(device)
    sys.stderr.flush()
    sys.stdout.flush()
except Exception as e:
    logger.error(e)
    logger.error(MemoryUsage.now())
    sys.exit(1)
model.train()
logger.info(MemoryUsage.now())


@torch.no_grad()
def evaluate(
    prompt,
    generate_tokens: int = 200,
    num_samples: int = 1,
    eval_model: PreTrainedModel = model,
    eval_tokenizer: PreTrainedTokenizer = tokenizer,
    top_k: int = args.top_k,
    top_p: float = args.top_p,
    temperature: float = args.temperature,
    repetition_penalty: float = args.repetition_penalty,
) -> List[str]:
    """
    Evaluate the model on the given prompt, and return the output text.
    """
    output_texts: List[str] = []
    input_tokens: Tensor = (
        torch.LongTensor(eval_tokenizer.encode(prompt)).unsqueeze(0).to(device)
    )
    if eval_tokenizer.pad_token_id != eval_tokenizer.eos_token_id:
        attention_mask: Tensor = input_tokens != eval_tokenizer.pad_token_id
    else:
        # If padding is indistinguishable from end-of-sentence,
        # we can't tell which to mask, so mask nothing.
        attention_mask = torch.ones_like(input_tokens, dtype=torch.bool)
    max_length = input_tokens.shape[1] + generate_tokens
    generated_tokens = eval_model.generate(
        input_tokens,
        attention_mask=attention_mask,
        max_length=max_length,
        do_sample=True,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        repetition_penalty=repetition_penalty,
        pad_token_id=eval_tokenizer.pad_token_id,
        num_return_sequences=num_samples,
        use_cache=True,
        bad_words_ids=[[eval_tokenizer.eos_token_id]],
        synced_gpus=True,
    )

    for token in generated_tokens:
        output_text = eval_tokenizer.decode(token, skip_special_tokens=False)
        output_texts.append(output_text)

    return output_texts


model.config.gradient_checkpointing = True
model.resize_token_embeddings(len(tokenizer))
model.config.use_cache = False
if hasattr(model.config, "force_fp32_attn"):
    model.config.force_fp32_attn = True

# Automatically make a guess at what (conservative) batchsize we should
# use for this model and GPU.
if args.bs == -1:
    bs = estimate_batch_size(args.bs_divisor)
else:
    bs = args.bs

if is_main_process():
    logger.info(f"BS: {bs}")
    logger.info(f"GAS: {args.gradients}")
    devices_repr = device
    if device != "cpu":
        try:
            devices_repr = (
                f"{torch.cuda.device_count()}x{torch.cuda.get_device_name(0)}"
            )
        except Exception:
            pass
    logger.info(f"DEVICES: {devices_repr}")

# Rewrite our `ds_config` to match arguments passed in.
ds_args = {}
if device != "cpu":
    with open(args.ds_config) as ds_config_file:
        ds_config = json.load(ds_config_file)
    zero_config = ds_config.get("zero_optimization", None)
    if zero_config is not None:
        zero_config["stage"] = args.zero_stage
        if args.zero_stage < 3:
            # offload_param is only valid for ZeRO stage 3
            zero_config.pop("offload_param", None)
    ds_args["deepspeed"] = ds_config
    ds_args["local_rank"] = args.local_rank
    os.environ["LOCAL_RANK"] = str(args.local_rank)
else:
    ds_args["no_cuda"] = True
    ds_args["local_rank"] = -1
    os.environ["LOCAL_RANK"] = "-1"

# Print our deepspeed estimates
estimate_fn = None
if args.zero_stage in [1, 2] and is_main_process():
    logger.info("DeepSpeed ZeRO-1/2 Memory Estimates")
    estimate_fn = estimate_zero2_model_states_mem_needs_all_live
elif args.zero_stage == 3 and is_main_process():
    logger.info("DeepSpeed ZeRO-3 Memory Estimates")
    estimate_fn = estimate_zero3_model_states_mem_needs_all_live
if estimate_fn:
    # Try to use DeepSpeed/PyTorch's configuration for GPUs per node
    num_gpus_per_node = os.getenv("LOCAL_WORLD_SIZE", None)
    if num_gpus_per_node is not None:
        try:
            num_gpus_per_node = int(num_gpus_per_node)
            if num_gpus_per_node == -1:
                num_gpus_per_node = None
        except ValueError:
            num_gpus_per_node = None
    if num_gpus_per_node is None:
        # Fall back to manually counting visible GPUs
        num_gpus_per_node = torch.cuda.device_count()

    estimate_fn(model=model, num_nodes=1, num_gpus_per_node=num_gpus_per_node)

# The latest deepspeed logging is pretty obnoxious, so we disable it
# unless debug-level logging is requested.
if args.log_level.upper() != "DEBUG":
    deepspeed.utils.logger.setLevel(logging.WARNING)

# Change our current directory due to some packages assumptions.
os.makedirs(args.output_path, exist_ok=True)
os.chdir(args.output_path)

callbacks = [PerformanceCallback()]

# Set up our prompt testing callback if we were given a prompt file.
if args.prompt_file:
    if args.prompt_every == -1:
        args.prompt_every = args.save_steps

    callbacks.append(
        ModelSampler(
            args.prompt_file,
            tokenizer,
            generate_tokens=args.prompt_tokens,
            batch_size=bs,
            num_samples=args.prompt_samples,
            gas=args.gradients,
            report_every=args.prompt_every or args.save_steps,
            context_size=args.context_size,
        )
    )

# Parametrize our training based on provided arguments.

# The grouping of arguments is based on the TrainingArguments.set_<...>
# family of functions, but set instead during initialization
# for compatibility with DeepSpeed.
training_args = TrainingArguments(
    # Training arguments
    do_train=True,
    learning_rate=args.lr,
    per_device_train_batch_size=bs,
    weight_decay=0.01,
    num_train_epochs=args.epochs,
    gradient_accumulation_steps=args.gradients,
    gradient_checkpointing=True,

    # Learning rate scheduler arguments
    warmup_steps=8,

    # Evaluation arguments
    # (Evaluation loss tracking is not finished, so these are disabled)
    # do_eval=True,
    # evaluation_strategy=...,        # Undetermined
    # eval_steps=...,                 # Undetermined
    # per_device_eval_batch_size=bs,
    # eval_accumulation_steps=...,    # Undetermined
    # eval_delay=...,                 # Undetermined
    # prediction_loss_only=False,

    # Logging arguments
    logging_dir=args.logs,
    logging_strategy=IntervalStrategy.STEPS,
    logging_steps=10,
    report_to=report_to,

    # Save arguments
    save_strategy=IntervalStrategy.STEPS,
    save_steps=args.save_steps,

    # Miscellaneous arguments
    output_dir=output_dir,
    run_name=args.run_name,
    disable_tqdm=False,
    seed=args.seed,
    **ds_args,
    **trainer_fp16_args,
)


def collector(data):
    return {
        "input_ids": torch.stack([f[0] for f in data]),
        "attention_mask": torch.stack([f[1] for f in data]),
        "labels": torch.stack([f[0] for f in data]),
    }


# Initialize our trainer object.
trainer = ModifiedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=collector,
    callbacks=callbacks,
)

# Finally, do our training!
if last_checkpoint is not None:
    trainer.train(str(os.path.join(output_dir, last_checkpoint)))
else:
    trainer.train()

# At the end of it all, record to a `final` output.
final_path = os.path.join(output_dir, "final")
trainer.save_model(final_path)

# Write out our tokenizer files.
tokenizer.save_pretrained(final_path)

# Record that the model is ready for work.
open(os.path.join(final_path, ".ready.txt"), "a").close()
