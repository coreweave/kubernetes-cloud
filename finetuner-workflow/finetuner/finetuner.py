#!/bin/which python3
# A simple Huggingface-based text-model finetuner meant to be used in an
# automated workflow.
import json
import gc
import resource
import mmap

import numpy
import psutil
import pynvml
import os
import sys
import struct
import time
import math
import torch
from torch import Tensor
from torch.utils.data import Dataset, random_split, RandomSampler
import argparse
import pathlib
from typing import Tuple, List
import socket
from contextlib import closing, contextmanager
import logging
import validators
import deepspeed
from deepspeed.runtime.zero.stage_1_and_2 import estimate_zero2_model_states_mem_needs_all_live;
from deepspeed.runtime.zero.stage3 import estimate_zero3_model_states_mem_needs_all_live;
from collections import OrderedDict
from tensorizer import TensorDeserializer, utils, stream_io

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


os.environ["TOKENIZERS_PARALLELISM"] = "false"

thisPath = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(thisPath + "/transformers/src")

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
from transformers.modeling_utils import no_init_weights, PreTrainedModel

try:
    pynvml.nvmlInit()
except pynvml.nvml.NVMLError_LibraryNotFound:
    pynvml = None

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"

parser = argparse.ArgumentParser(description="Simple Text Model Finetuner")
parser.add_argument(
    "--run_name", type=str, help="the run name to use", required=True
)
parser.add_argument(
    "--model",
    type=str,
    help="the model to train against" + " (directory, or HuggingFace ID)",
    required=True,
)
parser.add_argument(
    "--dataset", type=str, help="pre-tokenized dataset to use", required=True
)
parser.add_argument(
    "--tensorizer_uri",
    type=str,
    help="An S3 or path to use to extract pretrained weights for Tensorizer.",
    default=""
)
parser.add_argument("--lr", type=float, help="learning rate", default=5e-5)
parser.add_argument(
    "--epochs", type=int, help="number of epochs to train for", default=1
)
parser.add_argument(
    "--train_ratio",
    type=float,
    help="ratio of train to value from dataset",
    default=0.9,
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
    "--bs", type=int, help="Batch size (-1 == autosize)", default=-1
)
parser.add_argument(
    "--bs_divisor",
    type=float,
    help="Batch size divisor for automatically determining batch size",
    default=1.0,
)
parser.add_argument(
    "--gradients", type=int, help="Gradient accumulation steps", default=5
)
parser.add_argument(
    "--zero_stage", type=int, help="ZeRO optimizer stage", default=3
)
parser.add_argument("--seed", type=int, help="Random seed value", default=42)
parser.add_argument(
    "--output_path", type=str, help="Root path of all output", default="./"
)
parser.add_argument(
    "--no_resume",
    type=str,
    default="False",
    help="Do not resume from last checkpoint",
)
parser.set_defaults(no_resume="False")
parser.add_argument(
    "--cache", type=str, help="Huggingface cache location", default="/tmp"
)
parser.add_argument(
    "--save_steps",
    type=int,
    help="# of steps between checkpoint saves",
    default=500,
)
parser.add_argument(
    "--context_size", type=int, help="Dataset context sizes", default=2048
)
parser.add_argument(
    "--project_id",
    type=str,
    help="Project ID for reporting",
    default="huggingface",
)
parser.add_argument(
    "--logs", type=str, help="log directory location", default="./logs"
)
parser.add_argument(
    "--ds_config",
    type=str,
    help="DeepSpeed configuration",
    default="./ds_config.json",
)
parser.add_argument(
    "--fp16",
    dest="fp16",
    default=False,
    action="store_true",
    help="Force training in fp16.",
)
parser.add_argument(
    "--no_shuffle",
    dest="no_shuffle",
    default=False,
    action="store_true",
    help="Disable shuffling contexts",
)
parser.add_argument(
    "--prompt_file", type=str, help="Prompt file to use for checkpoint sampling"
)
parser.add_argument(
    "--prompt_every", type=int, default=0, help="Prompt every N steps"
)
parser.add_argument(
    "--prompt_tokens",
    type=int,
    default=200,
    help="Number of tokens to sample from prompt",
)
parser.add_argument(
    "--prompt_samples",
    type=int,
    help="Number of samples to generate",
    default=5,
)
parser.add_argument(
    "--top_k", type=int, help="Top K to use for prompt sampling", default=50
)
parser.add_argument(
    "--top_p", type=float, help="Top P to use for prompt sampling", default=0.95
)
parser.add_argument(
    "--temperature",
    type=float,
    help="Temperature to use for prompt sampling",
    default=1.0,
)
parser.add_argument(
    "--repetition_penalty",
    type=float,
    help="Repetition penalty to use for prompt sampling",
    default=1.1,
)
parser.add_argument(
    "--local_rank",
    type=int,
    help="For distributed training: local_rank",
    default=-1,
)
parser.add_argument(
    "--fp16-full-eval",
    dest="fp16_full_eval",
    default=False,
    action="store_true",
)
parser.add_argument(
    "--log-level",
    type=str,
    help="Log level to use",
    default="INFO",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(args.log_level.upper())
fh = logging.StreamHandler()
if args.local_rank != -1:
    fh_formatter = logging.Formatter(
        f"%(asctime)s %(levelname)s %(filename)s(%(process)d) - RANK {args.local_rank}"
        " - %(message)s"
    )
else:
    fh_formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
fh.setFormatter(fh_formatter)
logger.addHandler(fh)


def is_main_process() -> bool:
    return args.local_rank in [-1, 0]


# To be used in cases where using if statements are ugly.
def main_process_print(*args, **kwargs):
    if is_main_process():
        logger.info(*args, **kwargs)


# Where we write our training checkpoints and final model.
output_dir = os.path.abspath(
    os.path.join(args.output_path, "results-" + args.run_name)
)

# Properly type-cast the param (str to bool)
FALSE = [
    "false",
    "f",
    "0",
]
args.no_resume = args.no_resume.lower() not in FALSE

# Discover if we have any checkpoints to resume from.
if not args.no_resume:
    try:
        output_dir_list = os.listdir(output_dir)
        lastCheckpoint = sorted(
            output_dir_list, key=lambda x: int(x.split("-")[1])
        )[-1]
    except:
        lastCheckpoint = None
else:
    lastCheckpoint = None
logger.info(f"LAST CHECKPOINT: {lastCheckpoint}")

# Set up `wandb` reporting if we have an API key, and resume reporting
# if we are resuming a checkpoint.
report_to = "none"
wandb_key = os.getenv("WANDB_API_KEY", "").strip()
if not wandb_key:
    logger.warning("WANDB_API_KEY: No WANDB_API_KEY found, not reporting to wandb.")
    os.environ["WANDB_DISABLED"] = "True"

import wandb

if wandb_key and is_main_process():
    report_to = "wandb"

    if lastCheckpoint is not None:
        wandbApi = wandb.Api(overrides={"project": args.project_id})
        for run in wandbApi.runs(path=args.project_id):
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


def estimate_batch_size(divisor: float = 1.0) -> int:
    """
    Attempts to estimate the batch size to use based on the amount of RAM
    that the model takes up, and RAM free.

    :return: batch size to use
    """
    gc.collect()
    new_bs = 1
    if torch.cuda.is_available() and pynvml:
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        cudadev = torch.cuda.current_device()
        used_gpu = torch.cuda.memory_allocated()
        nvml_device = pynvml.nvmlDeviceGetHandleByIndex(cudadev)
        gpu_info = pynvml.nvmlDeviceGetMemoryInfo(nvml_device)
        gpu_free = gpu_info.free
        new_bs = int(math.ceil(gpu_free / (used_gpu * divisor)))
    logger.info(get_gpu_ram())
    logger.info(f"Setting batch size to {new_bs}")
    # if new_bs == 1:
    #    gc.set_threshold(10)
    return new_bs


def get_gpu_ram() -> str:
    """
    Returns memory usage statistics for the CPU, GPU, and Torch.

    :return:
    """
    gpu_str = ""
    torch_str = ""
    try:
        cudadev = torch.cuda.current_device()
        nvml_device = pynvml.nvmlDeviceGetHandleByIndex(cudadev)
        gpu_info = pynvml.nvmlDeviceGetMemoryInfo(nvml_device)
        gpu_total = gpu_info.total >> 20
        gpu_free = gpu_info.free >> 20
        gpu_used = gpu_info.used >> 20
        gpu_str = (
            f"GPU: (U: {gpu_used:,}MiB F: {gpu_free:,}MiB T: {gpu_total:,}MiB) "
        )
        torch_reserved_gpu = torch.cuda.memory.memory_reserved() >> 20
        torch_reserved_max = torch.cuda.memory.max_memory_reserved() >> 20
        torch_used_gpu = torch.cuda.memory_allocated() >> 20
        torch_max_used_gpu = torch.cuda.max_memory_allocated() >> 20
        torch_str = (
            f"TORCH: (R: {torch_reserved_gpu:,}MiB/"
            f"{torch_reserved_max:,}MiB, "
            f"A: {torch_used_gpu:,}MiB/{torch_max_used_gpu:,}MiB)"
        )
    except AssertionError:
        pass
    cpu_maxrss = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    ) >> 10
    cpu_vmem = psutil.virtual_memory()
    cpu_free = cpu_vmem.free >> 20
    return (
        f"CPU: (maxrss: {cpu_maxrss:,}MiB F: {cpu_free:,}MiB) "
        f"{gpu_str}{torch_str}"
    )


class ModifiedTrainer(Trainer):
    """
    A modification of the Trainer class to allow for better console reporting
    in the container and fix gradient handling on the loss tensor returned.
    """

    def compute_loss(self, model, inputs, return_outputs=False):
        if "labels" in inputs:
            inputs["labels"].masked_fill_(
                inputs["labels"] == tokenizer.pad_token_id, -100
            )

        results = super().compute_loss(model, inputs, return_outputs)
        loss = results[0] if return_outputs else results

        # Hack -- enable `requires_grad` on `loss`
        loss.requires_grad_(True)

        # Hack -- output a (useful) GPU ram update to flush tqdm.
        self.report_idx = getattr(self, "report_idx", 0) + 1
        if self.report_idx % (2 * self.args.gradient_accumulation_steps) == 0:
            if is_main_process():
                print(f"\nLOSS: {loss:.3f} {get_gpu_ram()}", file=sys.stderr,
                      flush=True)
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
            # report to wandb
            rank_samples_per_second = args.per_device_train_batch_size * args.gradient_accumulation_steps * (1 / (self.opt_step - self.start_time))
            world_samples_per_second = torch.distributed.get_world_size() * rank_samples_per_second
            wandb.log(
                {
                    "perf/opt_time": self.opt_step - self.ff_step,
                    "perf/gas_time": self.ff_step - self.start_time,
                    "perf/total_time_per_step": self.opt_step - self.start_time,
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
    console, and to each rank's WanDB run.
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
        try:
            self.num_gpus = torch.cuda.device_count()
        except AssertionError:
            self.num_gpus = 1

    def on_step_end(
        self, args, state, control, model: PreTrainedModel = None, **kwargs
    ):
        if not model:
            return
        if state.global_step % self.report_every == 0 or state.global_step == 1:
            curr_tokens_step = (
                state.global_step * self.train_batch_size * self.gas * self.num_gpus
            )
            main_process_print(
                f"\nSTEP {state.global_step}: Evaluating on {self.prompt_file}...",
            )
            model.eval()
            sys.stderr.flush()
            with open(self.prompt_file, "rb") as f:
                prompt_contents = f.read().decode("utf-8").split("\n")
                prompts = [
                    i.rstrip("\n").replace("\\n", "\n") for i in prompt_contents
                ]
                for prompt in prompts:
                    if not prompt:
                        continue
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
            # it is still useful to collect evaluations on other ranks in their
            # respective wandb runs.
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
        mask: torch.Tensor = input_ids != tokenizer.pad_token_id
        return input_ids, mask

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.load(idx)


# Inform the user of host, and various versions -- useful for debugging issues.
torch.cuda.set_device(args.local_rank)
if is_main_process():
    logger.info(f"RUN_NAME: {args.run_name}")
    logger.info(f"PROJECT ID {args.project_id}")
    logger.info(f"HOST: {socket.gethostname()}")
    logger.info(f"CUDA: {torch.version.cuda}")
    logger.info(f"TORCH: {torch.__version__}")
    logger.info(f"TRANSFORMERS: {transformers.__version__}")
    logger.info(get_gpu_ram())
    logger.info(f"MODEL: {args.model}")
    logger.info(f"TRAIN_RATIO: {args.train_ratio}")
    logger.info(f"CONTEXT LENGTH: {args.context_size} tokens")
    logger.info(f"SHUFFLE: {not args.no_shuffle}")
    logger.info(f"EPOCHS {args.epochs}")
    logger.info(f"CHECKPOINT STEPS: {args.checkpoint_steps}")
    logger.info(f"TOKENIZER: {tokenizer}")
    logger.info(f"TOKENIZER SPECIAL TOKENS: {tokenizer.special_tokens_map}")
    logger.info(f"TRAIN_RATIO: {args.train_ratio}")
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

# Set up our dataset from our tokenized data files, and split into training
# dataset and values dataset -- values dataset is used to test the outcome
# and determine our loss rate.
dataset = TokenizedDataset(args.dataset, context_length=args.context_size)
train_size = int(args.train_ratio * float(len(dataset)))

if args.no_shuffle:
    train_dataset = dataset
    val_dataset = RandomSampler(dataset, num_samples=len(dataset) - train_size)
else:
    train_dataset, val_dataset = random_split(
        dataset, [train_size, len(dataset) - train_size]
    )

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

model_fp16_args = {"torch_dtype": torch.float16}
model_args = {"eos_token_id": tokenizer.eos_token_id,
            "pad_token_id": tokenizer.pad_token_id,
            "cache_dir": args.cache,
            "use_cache": False,
            "low_cpu_mem_usage": True}

# we evaluate if args.model is already tensorized under a public s3 bucket.
try:
    if not args.tensorizer_uri:
        model_id = '/'.join(args.model.split('/')[-2:])
        stream_io.CURLStreamFile(
            uri=f"https://accel-object.ord1.coreweave.com/tensorized/{model_id}/model.tensors"
        ).read(1)
        uri_dtype = 'fp16/' if args.fp16 else ''
        args.model = model_id
        args.tensorizer_uri=f"s3://tensorized/{args.model}/{uri_dtype}model.tensors"
except OSError:
    pass

try:
    if args.tensorizer_uri:
        config = AutoConfig.from_pretrained(
            args.model,
            **model_args,
            **model_fp16_args,
        )
        model = utils.no_init_or_tensor(
            lambda: AutoModelForCausalLM.from_pretrained(
                None, config=config, state_dict=OrderedDict()
            )
        )

        deserializer = TensorDeserializer(args.tensorizer_uri)
        deserializer.load_into_module(model)
        deserializer.close()
        model.train()
    else:
        with no_init():
            model = AutoModelForCausalLM.from_pretrained(
                args.model,  # Can be a HuggingFace ID or directory.
                **model_args,
                **model_fp16_args,
            )  # Gradient checkpointing needs this off.
            if lastCheckpoint is None:
                model = model.to(device)
    sys.stderr.flush()
    sys.stdout.flush()
except Exception as e:
    logger.error(e)
    logger.error(get_gpu_ram())
    sys.exit(1)
logger.info(get_gpu_ram())



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
        torch.LongTensor(tokenizer.encode(prompt)).unsqueeze(0).to(device)
    )
    attention_mask: Tensor = input_tokens != tokenizer.pad_token_id
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
            devices_repr = (f"{torch.cuda.device_count()}x"
                            f"{torch.cuda.get_device_name(0)}")
        except Exception:
            pass
    logger.info(f"DEVICES: {devices_repr}")

# Rewrite our `ds_config` to match arguments passed in.
ds_args = {}
if device != "cpu":
    ds_config = json.load(open(args.ds_config))
    if "zero_optimization" in ds_config:
        ds_config["zero_optimization"]["stage"] = args.zero_stage
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
    estimate_fn(model=model,
                num_nodes=1,
                num_gpus_per_node=torch.cuda.device_count())

# The latest deepspeed logging is pretty obnoxious, so we disable it.
deepspeed.utils.logger.setLevel(logging.WARNING)

# Change our current directory due to some packages assumptions.
os.makedirs(args.output_path, exist_ok=True)
os.chdir(args.output_path)

callbacks = [
    PerformanceCallback()
]

# Set up our prompt testing callback if we were given a prompt file.
if args.prompt_file:
    if args.prompt_every == -1:
        args.prompt_every = args.save_steps

    callbacks += [
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
    ]
else:
    callbacks = None

if is_main_process():
    logger.info(f"PROMPT FILE: {args.prompt_file}")

# Parametrize our training based on provided arguments.
training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=args.epochs,
    logging_steps=10,
    save_strategy=IntervalStrategy.STEPS,
    per_device_train_batch_size=bs,
    per_device_eval_batch_size=bs,
    gradient_accumulation_steps=args.gradients,
    learning_rate=args.lr,
    warmup_steps=8,
    weight_decay=0.01,
    save_steps=args.save_steps,
    logging_dir=args.logs,
    report_to=report_to,
    run_name=args.run_name,
    gradient_checkpointing=True,
    disable_tqdm=False,
    **ds_args,
    **trainer_fp16_args,
)

collector = lambda data: {
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
if lastCheckpoint is not None:
    trainer.train(str(os.path.join(output_dir, lastCheckpoint)))
else:
    trainer.train()

# At the end of it all, record to a `final` output.
final_path = os.path.join(output_dir, "final")
trainer.save_model(final_path)

# Write out our tokenizer files.
tokenizer.save_pretrained(final_path)

# Record that the model is ready for work.
open(os.path.join(final_path, ".ready.txt"), "a").close()
