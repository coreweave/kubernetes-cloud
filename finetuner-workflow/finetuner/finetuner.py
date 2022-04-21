#!/bin/which python3
# A simple Huggingface-based text-model finetuner meant to be used in an
# automated workflow.
import wandb
import json
import gc
import resource
import psutil
import pynvml
import os
import sys
import struct
import socket
import math
import torch
from torch.utils.data import Dataset, random_split
import argparse

os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '9994'
os.environ['RANK'] = "0"
os.environ['LOCAL_RANK'] = "0"
os.environ['WORLD_SIZE'] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import transformers
from transformers import AutoTokenizer, TrainingArguments, Trainer, \
    AutoModelForCausalLM, IntervalStrategy

pynvml.nvmlInit()

parser = argparse.ArgumentParser(description='Simple Text Model Finetuner')
parser.add_argument('--run_name', type=str, help='the run name to use',
                    required=True)
parser.add_argument('--model', type=str, help='the model to train against' +
                                              ' (directory, or HuggingFace ID)',
                    required=True)
parser.add_argument('--dataset', type=str, help='pre-tokenized dataset to use',
                    required=True)
parser.add_argument('--lr', type=float, help='learning rate', default=5e-5)
parser.add_argument('--epochs', type=int, help='number of epochs to train for',
                    default=1)
parser.add_argument('--train_ratio', type=float,
                    help="ratio of train to value from dataset",
                    default=0.9)
parser.add_argument('--eot', type=str, help="EOT token to use",
                    default="<|endoftext|>")
parser.add_argument('--pad', type=str, help="Pad token to use",
                    default="<|endoftext|>")
parser.add_argument('--bs', type=int, help="Batch size (-1 == autosize)",
                    default=-1)
parser.add_argument("--bs_divisor", type=float, help="Batch size divisor for "
                                                     "automatically "
                                                     "determining batch size",
                    default=1.0)
parser.add_argument("--gradients", type=int, help="Gradient accumulation steps",
                    default=5)
parser.add_argument("--zero_stage", type=int, help="ZeRO optimizer stage",
                    default=3)
parser.add_argument('--seed', type=int, help="Random seed value",
                    default=42)
parser.add_argument('--output_path', type=str, help="Root path of all output",
                    default="./")
parser.add_argument('--no_resume', type=bool, default=False,
                    help="Do not resume from last checkpoint")
parser.set_defaults(no_resume=False)
parser.add_argument("--cache", type=str, help="Huggingface cache location",
                    default="/tmp")
parser.add_argument("--save_steps", type=int,
                    help="# of steps between checkpoint saves",
                    default=500)
parser.add_argument("--context_size", type=int, help="Dataset context sizes",
                    default=2048)
parser.add_argument("--project_id", type=str, help="Project ID for reporting",
                    default="huggingface")
parser.add_argument("--tokenizer", type=str, help="Tokenizer ID to use",
                    default="gpt2")
parser.add_argument("--logs", type=str, help="log directory location",
                    default="./logs")
parser.add_argument("--ds_config", type=str, help="DeepSpeed configuration",
                    default="./ds_config.json")
args = parser.parse_args()


def estimate_batch_size(divisor: float = 1.0) -> int:
    """
    Attempts to estimate the batch size to use based on the amount of RAM
    that the model takes up, and RAM free.

    :return: batch size to use
    """
    gc.collect()
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    cudadev = torch.cuda.current_device()
    nvml_device = pynvml.nvmlDeviceGetHandleByIndex(cudadev)
    gpu_info = pynvml.nvmlDeviceGetMemoryInfo(nvml_device)
    gpu_free = gpu_info.free
    used_gpu = torch.cuda.memory_allocated()
    new_bs = int(math.ceil(gpu_free / (used_gpu * divisor)))
    print(get_gpu_ram())
    print(f"Setting batch size to {new_bs}")
    return new_bs


def get_gpu_ram() -> str:
    """
    Returns memory usage statistics for the CPU, GPU, and Torch.

    :return:
    """
    cudadev = torch.cuda.current_device()
    nvml_device = pynvml.nvmlDeviceGetHandleByIndex(cudadev)
    gpu_info = pynvml.nvmlDeviceGetMemoryInfo(nvml_device)
    gpu_total = int(gpu_info.total / 1E6)
    gpu_free = int(gpu_info.free / 1E6)
    gpu_used = int(gpu_info.used / 1E6)
    reserved_gpu = int(torch.cuda.memory.memory_reserved() / 1E6)
    reserved_max = int(torch.cuda.memory.max_memory_reserved() / 1E6)
    used_gpu = int(torch.cuda.memory_allocated() / 1E6)
    max_used_gpu = int(torch.cuda.max_memory_allocated() / 1E6)
    maxrss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1E3 +
                 resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1E3)
    vmem = psutil.virtual_memory()
    cpufree = int(vmem.free / 1E6)
    return "CPU: (maxrss: {:,}mb F: {:,}mb) ".format(maxrss, cpufree) + \
           "GPU: (U: {:,}mb F: {:,}mb T: {:,}mb) ".format(
               gpu_used, gpu_free, gpu_total) + \
           "TORCH: (R: {:,}mb/{:,}mb, A: {:,}mb/{:,}mb)".format(
               reserved_gpu, reserved_max, used_gpu, max_used_gpu)


class ModifiedTrainer(Trainer):
    """
    A modification of the Trainer class to allow for better console reporting
    in the container and fix gradient handling on the loss tensor returned.
    """

    def compute_loss(self, model, inputs, return_outputs=False):
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

        ## Hack -- enable `requires_grad` on `loss`
        loss.requires_grad_(True)

        ## Hack -- output an (useful) GPU ram update to flush tqdm.
        if not hasattr(self, 'report_idx'):
            self.report_idx = 1
        else:
            self.report_idx += 1
        if self.report_idx % 10 == 0:
            print("\n" + get_gpu_ram(), file=sys.stderr)
            sys.stderr.flush()

        return (loss, outputs) if return_outputs else loss


class TokenizedDataset(Dataset):
    """
    Consumes a flat binary file containing 16-bit token serialization, aligned
    along `context_length` chunks.
    """

    def __init__(self, path: str, context_length: int = 2048):
        file_stat = os.stat(path)
        self.file = open(path, 'rb')
        self.length = int(file_stat.st_size / 2 / context_length)
        self.formatstr = '%sH' % context_length
        self.context_length = context_length
        length_mb = int(os.stat(path).st_size / 1024.0 / 1024.0)
        num_tokens = self.length * context_length
        print(f"DATASET: {path}; {num_tokens:,} tokens; {length_mb:,.2f} mb")

    def __len__(self):
        return self.length

    def load(self, idx):
        self.seek(idx)
        input_ids = torch.tensor(
            struct.unpack(self.formatstr,
                          self.file.read(self.context_length * 2)))
        mask = torch.zeros(self.context_length)
        return input_ids, mask

    def seek(self, idx):
        self.file.seek(self.context_length * idx * 2)

    def __getitem__(self, idx):
        return self.load(idx)



# Inform the user of host, and various versions -- useful for debugging isseus.
print("RUN_NAME:", args.run_name)
print("HOST:", socket.gethostname())
print("CUDA:", torch.version.cuda)
print("TORCH:", torch.__version__)
print("TRANSFORMERS:", transformers.__version__)
print(get_gpu_ram())

# Set up our dataset from our tokenized data files, and split into training
# dataset and values dataset -- values dataset is used to test the outcome
# and determine our loss rate.
dataset = TokenizedDataset(args.dataset, context_length=args.context_size)
train_size = int(args.train_ratio * float(len(dataset)))
train_dataset, val_dataset = random_split(dataset,
                                          [train_size,
                                           len(dataset) - train_size])
print(f"TRAIN_DATASET: {len(train_dataset):,} examples")
print(f"VALUE_DATASET: {len(val_dataset):,} examples")

# Where we write our training checkpoints and final model.
output_dir = os.path.abspath(
    os.path.join(args.output_path, "results-" + args.run_name))

# Discover if we have any checkpoints to resume from.
if not args.no_resume:
    try:
        output_dir_list = os.listdir(output_dir)
        lastCheckpoint = sorted(output_dir_list,
                                key=lambda x: int(x.split("-")[1]))[-1]
    except:
        lastCheckpoint = None
else:
    lastCheckpoint = None
print("LAST CHECKPOINT:", lastCheckpoint)



# Set random seed, for ML research purposes and reproducibility, it's important
# that we set this to a consistent value.
torch.manual_seed(args.seed)
print("RANDOM SEED:", args.seed)
# Load our tokenizer. Usually `gpt2`, and only used for sizing the model's
# token embeddings.
tokenizer = AutoTokenizer.from_pretrained(args.tokenizer,
                                          eos_token=args.eot,
                                          pad_token=args.pad,
                                          cache_dir=args.cache)

# Load our model that we're training. This may fetch via HTTP if not cached
# already.
print(f"Loading {args.model}")
try:
    model = AutoModelForCausalLM.from_pretrained(
        args.model,  # Can be a HuggingFace ID or directory.
        cache_dir=args.cache,
        use_cache=False)  # Gradient checkpointing needs this off.
    model = model.half().cuda().eval()
    model.resize_token_embeddings(len(tokenizer))
    sys.stderr.flush()
    sys.stdout.flush()
except Exception as e:
    print(e)
    print(get_gpu_ram())
    sys.exit(1)
print(get_gpu_ram())

# Automatically make a guess at what (conservative) batchsize we should
# use for this model and GPU.
if args.bs == -1:
    bs = estimate_batch_size(args.bs_divisor)
else:
    bs = args.bs

# Rewrite our `ds_config` to match arguments passed in.
ds_config = json.load(open(args.ds_config))
if "zero_optimization" in ds_config and \
        ds_config["zero_optimization"].get("stage", None) != args.zero_stage:
    ds_config["zero_optimization"]["stage"] = args.zero_stage

# Change our current directory due to some packages assumptions.
os.chdir(args.output_path)

# Set up `wandb` reporting if we have an API key, and resume reporting
# if we are resuming a checkpoint.
report_to = None
if os.environ.get("WANDB_API_KEY") not in [None, ""]:
    import wandb

    wandbApi = wandb.Api(overrides={"project": args.project_id})
    report_to = "wandb"

    if lastCheckpoint != None:
        for run in wandbApi.runs(path=args.project_id):
            if run.state == "crashed" and run.name == args.run_name:
                wandb.init(id=run.id, project=args.project_id,
                           resume="must", name=run.name)
                print(f"Resuming {run.id}")
                break

# Parametrize our training based on provided arguments.
training_args = TrainingArguments(output_dir=output_dir,
                                  num_train_epochs=args.epochs,
                                  logging_steps=10,
                                  save_strategy=IntervalStrategy.STEPS,
                                  per_device_train_batch_size=bs,
                                  per_device_eval_batch_size=bs,
                                  gradient_accumulation_steps=args.gradients,
                                  gradient_checkpointing=True,
                                  learning_rate=args.lr,
                                  warmup_steps=8,
                                  weight_decay=0.01,
                                  save_steps=args.save_steps,
                                  logging_dir=args.logs,
                                  fp16=True,
                                  deepspeed=ds_config,
                                  report_to=report_to,
                                  run_name=args.run_name,
                                  disable_tqdm=False)

collector = lambda data: {'input_ids': torch.stack([f[0] for f in data]),
                          'attention_mask': torch.stack([f[1] for f in data]),
                          'labels': torch.stack([f[0] for f in data])}

# Initialize our trainer object.
trainer = ModifiedTrainer(model=model,
                          args=training_args,
                          train_dataset=train_dataset,
                          eval_dataset=val_dataset,
                          data_collator=collector)

# Finally, do our training!
if lastCheckpoint is not None:
    trainer.train(os.path.join(output_dir, lastCheckpoint))
else:
    trainer.train()

# At the end of it all, record to a `final` output.
final_path = os.path.join(output_dir, "final")
trainer.save_model(final_path)

# Write out our tokenizer files.
tokenizer.save_pretrained(final_path)

# Record that the model is ready for work.
open(os.path.join(final_path, ".ready.txt"), 'a').close()