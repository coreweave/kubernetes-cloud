#!/bin/which python3
# A simple Huggingface-based text-model finetuner meant to be used in an
# automated workflow.
import json
import gc
import resource
import psutil
import pynvml
import os
import sys
import struct
import time
import math
import torch
import logging
from torch import Tensor
from torch.utils.data import Dataset, random_split, RandomSampler
import argparse
import pathlib
from typing import Callable, Tuple, Optional, List
import socket
from contextlib import closing

import validators
import deepspeed


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_PORT"] = f"{find_free_port()}"
os.environ["RANK"] = "0"
os.environ["LOCAL_RANK"] = "0"
os.environ["WORLD_SIZE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

thisPath = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(thisPath + "/transformers/src")

import transformers
from transformers import (
    AutoTokenizer,
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
    "--eot", type=str, help="EOT token to use", default="<|endoftext|>"
)
parser.add_argument(
    "--pad", type=str, help="Pad token to use", default="<|padding|>"
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
args = parser.parse_args()

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
print("LAST CHECKPOINT:", lastCheckpoint)

# Set up `wandb` reporting if we have an API key, and resume reporting
# if we are resuming a checkpoint.
report_to = None
wandb_key = os.getenv("WANDB_API_KEY", "").lstrip().rstrip()
if not wandb_key:
    print("WANDB_API_KEY: No WANDB_API_KEY found, not reporting to wandb.")
    os.environ["WANDB_DISABLED"] = "True"

import wandb

if wandb_key:
    wandbApi = wandb.Api(overrides={"project": args.project_id})
    report_to = "wandb"

    if lastCheckpoint is not None:
        for run in wandbApi.runs(path=args.project_id):
            print("PRIOR RUN:", run, run.name, run.id, run.state)
            if run.state in ["crashed", "failed"] and run.name == args.run_name:
                print(f"CHECKPOINT: Resuming {run.id}")
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
    os.environ["WANDB_DISABLED"] = "True"
    run = wandb.init(project=args.project_id, name=args.run_name)

# Set up our tokenizer.
tokenizer: PreTrainedTokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        eos_token=args.eot,
        pad_token=args.pad,
        cache_dir=args.cache,
    )
except Exception as e:
    print(e)
    sys.exit(1)


def no_init(loading_code: Callable[[], PreTrainedModel]) -> PreTrainedModel:
    def dummy(self):
        return

    modules = [torch.nn.Linear, torch.nn.Embedding, torch.nn.LayerNorm]
    original = {}
    for mod in modules:
        original[mod] = mod.reset_parameters
        mod.reset_parameters = dummy

    with no_init_weights():
        result = loading_code()
    for mod in modules:
        mod.reset_parameters = original[mod]

    return result


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
    print(get_gpu_ram())
    print(f"Setting batch size to {new_bs}")
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
            inputs["labels"][inputs["labels"] == tokenizer.pad_token_id] = -100

        if self.label_smoother is not None and "labels" in inputs:
            labels = inputs.pop("labels")
        else:
            labels = None

        outputs = model(**inputs)

        if self.args.past_index >= 0:
            self._past = outputs[self.args.past_index]

        if labels is not None:
            loss = self.label_smoother(outputs, labels)
        else:
            loss = outputs["loss"] if isinstance(outputs, dict) else outputs[0]

        # Hack -- enable `requires_grad` on `loss`
        loss.requires_grad_(True)

        # Hack -- output an (useful) GPU ram update to flush tqdm.
        if not hasattr(self, "report_idx"):
            self.report_idx = 1
        else:
            self.report_idx += 1
        if self.report_idx % 10 == 0:
            print(f"\nLOSS: {loss:.3f} {get_gpu_ram()}", file=sys.stderr)
            sys.stderr.flush()

        return (loss, outputs) if return_outputs else loss


class ModelSampler(TrainerCallback):
    """
    Test the model on one or more prompts every so often and report to the
    console, and to WanDB.
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
                state.global_step * self.train_batch_size * self.gas
            )
            print(
                f"\nSTEP {state.global_step}: Evaluating on {self.prompt_file}...",
                file=sys.stderr,
            )
            model.eval()
            sys.stderr.flush()
            with open(self.prompt_file, "r") as f:
                prompts = [
                    i.rstrip("\n").replace("\\n", "\n") for i in f.readlines()
                ]
                for prompt in prompts:
                    print("=============================")
                    print("PROMPT:", prompt)
                    start = time.time()
                    outputs = evaluate(
                        prompt,
                        self.generate_tokens,
                        self.num_samples,
                        model,
                        self.tokenizer,
                    )
                    end = time.time()
                    print(f"INFERENCE TIME: {end - start:.2f}s")
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
                        print("-----------------------------")
                        print("RESPONSE:", output_text)
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
        self.file = open(path, "rb")
        self.length = int(file_stat.st_size / 2 / context_length)
        self.formatstr = "%sH" % context_length
        self.context_length = context_length
        length_mb = os.stat(path).st_size / (1 << 20)
        num_tokens = self.length * context_length
        print(f"DATASET: {path}")
        print(
            f"DATASET SIZE: {length_mb:,.2f}MiB, {num_tokens:,} tokens, "
            f"{self.length:,} contexts"
        )

    def __len__(self) -> int:
        return self.length

    def load(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        self.seek(idx)
        input_ids = torch.tensor(
            struct.unpack(
                self.formatstr, self.file.read(self.context_length * 2)
            )
        )
        mask = torch.zeros(self.context_length)
        return input_ids, mask

    def seek(self, idx):
        self.file.seek(self.context_length * idx * 2)

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.load(idx)


# Inform the user of host, and various versions -- useful for debugging issues.
print("RUN_NAME:", args.run_name)
print("HOST:", socket.gethostname())
print("CUDA:", torch.version.cuda)
print("TORCH:", torch.__version__)
print("TRANSFORMERS:", transformers.__version__)
print(get_gpu_ram())
print("MODEL:", args.model)
print("SHUFFLE:", not args.no_shuffle)


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
print(f"TRAIN_DATASET: {len(train_dataset):,} examples")
print(f"VALUE_DATASET: {len(val_dataset):,} examples")

# Set random seed, for ML research purposes and reproducibility, it's important
# that we set this to a consistent value.
torch.manual_seed(args.seed)
print("RANDOM SEED:", args.seed)

# Determine if we train in fp32 or fp16 mode.
print("FORCE FP16:", args.fp16)
fp16_arg = {"fp16": True} if args.fp16 else {}

# Load our model that we're training. This may fetch via HTTP if not cached
# already.
model: PreTrainedModel

try:
    model = AutoModelForCausalLM.from_pretrained(
        args.model,  # Can be a HuggingFace ID or directory.
        cache_dir=args.cache,
        use_cache=False,
    )  # Gradient checkpointing needs this off.
    if lastCheckpoint is None:
        if args.fp16:
            model = no_init(lambda: model.half().to(device))
        else:
            model = no_init(lambda: model.to(device))
    else:
        model = no_init(lambda: model)
    sys.stderr.flush()
    sys.stdout.flush()
except Exception as e:
    print(e)
    print(get_gpu_ram())
    sys.exit(1)
print(get_gpu_ram())


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
    attention_mask: Tensor = torch.ones_like(input_tokens).to(device)
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
    )

    for token in generated_tokens:
        output_text = eval_tokenizer.decode(token, skip_special_tokens=False)
        output_texts.append(output_text)

    return output_texts


# log out the tokenizer and model
print(f"TOKENIZER: {tokenizer}")

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

# Rewrite our `ds_config` to match arguments passed in.
ds_args = {}
if device != "cpu":
    ds_config = json.load(open(args.ds_config))
    if "zero_optimization" in ds_config:
        ds_config["zero_optimization"]["stage"] = args.zero_stage
    ds_args["deepspeed"] = ds_config
else:
    ds_args["no_cuda"] = True
    ds_args["local_rank"] = -1
    os.environ["LOCAL_RANK"] = "-1"

# The latest deepspeed logging is pretty obnoxious, so we disable it.
deepspeed.utils.logger.setLevel(logging.ERROR)

# Change our current directory due to some packages assumptions.
os.makedirs(args.output_path, exist_ok=True)
os.chdir(args.output_path)

# Set up our prompt testing callback if we were given a prompt file.
if args.prompt_file:
    sampler_callbacks = [
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
    sampler_callbacks = None
print(f"PROMPT FILE: {args.prompt_file}")

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
    **fp16_arg,
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
    callbacks=sampler_callbacks,
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
