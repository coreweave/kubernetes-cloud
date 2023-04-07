#!/bin/which python3
import argparse
from typing import Callable, List
from torch import Tensor
import resource
import pynvml
import psutil
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer
from transformers.modeling_utils import no_init_weights, PreTrainedModel

try:
    pynvml.nvmlInit()
except pynvml.nvml.NVMLError_LibraryNotFound:
    pynvml = None

device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")


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
        gpu_total = int(gpu_info.total / 1e6)
        gpu_free = int(gpu_info.free / 1e6)
        gpu_used = int(gpu_info.used / 1e6)
        gpu_str = (
            f"GPU: (U: {gpu_used:,}mb F: {gpu_free:,}mb "
            f"T: {gpu_total:,}mb) "
        )
        torch_reserved_gpu = int(torch.cuda.memory.memory_reserved() / 1e6)
        torch_reserved_max = int(torch.cuda.memory.max_memory_reserved() / 1e6)
        torch_used_gpu = int(torch.cuda.memory_allocated() / 1e6)
        torch_max_used_gpu = int(torch.cuda.max_memory_allocated() / 1e6)
        torch_str = (
            f"TORCH: (R: {torch_reserved_gpu:,}mb/"
            f"{torch_reserved_max:,}mb, "
            f"A: {torch_used_gpu:,}mb/{torch_max_used_gpu:,}mb)"
        )
    except AssertionError:
        pass
    cpu_maxrss = int(
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e3
        + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e3
    )
    cpu_vmem = psutil.virtual_memory()
    cpu_free = int(cpu_vmem.free / 1e6)
    return (
        f"CPU: (maxrss: {cpu_maxrss:,}mb F: {cpu_free:,}mb) "
        f"{gpu_str}"
        f"{torch_str}"
    )


parser = argparse.ArgumentParser(description='Simple Model Evaluator')

parser.add_argument('--model', type=str, help='the model to evaluate against' +
                                              ' (directory, or HuggingFace ID)',
                    required=True)
parser.add_argument('--tokenizer', type=str, help='the tokenizer to use')
parser.add_argument('--eot', type=str, help="EOT token to use",
                    default="<|endoftext|>")
parser.add_argument('--pad', type=str, help="Pad token to use",
                    default="<|endoftext|>")
parser.add_argument("--cache", type=str, help="Huggingface cache location",
                    default="/tmp")
parser.add_argument("--fp16", dest='fp16', default=False, action='store_true',
                    help="Force training in fp16.")
parser.add_argument("--prompt", type=str, help="Prompt to use")
parser.add_argument("--prompt_file", type=str, help="File containing prompts")
parser.add_argument("--prompt_tokens", type=int, help="Number of tokens to generate",
                    default=200)
parser.add_argument('--seed', type=int, help="Random seed value",
                    default=None)
parser.add_argument("--prompt_samples", type=int, help="Number of samples to generate",
                    default=1)
parser.add_argument("--top_k", type=int, help="Top K to use for sampling",
                    default=16)
parser.add_argument("--top_p", type=float, help="Top P to use for sampling",
                    default=0.95)
parser.add_argument("--temperature", type=float, help="Temperature to use for sampling",
                    default=1.0)
parser.add_argument("--repetition_penalty", type=float,
                    help="Repetition penalty to use for sampling",
                    default=1.1)

args = parser.parse_args()
if args.tokenizer is None:
    args.tokenizer = args.model

if args.prompt and args.prompt_file:
    print("Cannot specify both prompt and prompt-file")
    exit(1)

if not args.prompt and not args.prompt_file:
    print("Please specify either a prompt or a prompt file")
    exit(1)

if args.prompt_file:
    with open(args.prompt_file, "r") as f:
        prompts = [i.rstrip("\n").replace("\\n", "\n")
                   for i in f.readlines()]
else:
    prompts = [args.prompt.strip()]


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

print(get_gpu_ram())

start = time.time()

tokenizer = AutoTokenizer.from_pretrained(args.tokenizer,
                                          eos_token=args.eot,
                                          pad_token=args.pad,
                                          cache_dir=args.cache,
                                          padding_side='left')

model = AutoModelForCausalLM.from_pretrained(args.model,
                                             # Can be a HuggingFace ID or directory.
                                             cache_dir=args.cache,
                                             use_cache=True)

if args.fp16:
    model = no_init(lambda: model.half().to(device))
else:
    model = no_init(lambda: model.to(device))

model.eval()


duration = time.time() - start
print(f"Loaded model in {duration:.2f}s")
print(get_gpu_ram())
torch.cuda.memory.empty_cache()
print(get_gpu_ram())


def evaluate(prompt,
             generate_tokens: int = 200,
             num_samples: int = 1,
             eval_model: PreTrainedModel = model,
             eval_tokenizer: PreTrainedTokenizer = tokenizer,
             top_k: int = args.top_k,
             top_p: float = args.top_p,
             temperature: float = args.temperature,
             repetition_penalty: float = args.repetition_penalty) -> List[str]:
    """
    Evaluate the model on the given prompt, and return the output text.
    """
    output_texts: List[str] = []
    input_tokens: Tensor = torch.LongTensor(
        tokenizer.encode(prompt)).unsqueeze(0).to(device)
    max_length = input_tokens.shape[1] + generate_tokens
    attention_mask: Tensor = torch.ones_like(input_tokens).to(device)

    generated_tokens = eval_model.generate(input_tokens,
                                           attention_mask=attention_mask,
                                           max_length=max_length,
                                           do_sample=True,
                                           top_k=top_k,
                                           top_p=top_p,
                                           temperature=temperature,
                                           repetition_penalty=repetition_penalty,
                                           pad_token_id=eval_tokenizer.pad_token_id,
                                           num_return_sequences=num_samples,
                                           bad_words_ids=[[eval_tokenizer.eos_token_id]])

    for sample_idx in range(len(generated_tokens)):
        output_text = eval_tokenizer.decode(generated_tokens[sample_idx],
                                            skip_special_tokens=False)
        output_texts.append(output_text)

    return output_texts


if args.seed is not None:
    torch.cuda.manual_seed(args.seed)

for prompt in prompts:
    print("=============================")
    print("PROMPT:", prompt)
    print("UTILIZATION:", get_gpu_ram())
    for response in evaluate(prompt, args.prompt_tokens, args.prompt_samples):
        print("-----------------------------")
        print("RESPONSE:", response)
