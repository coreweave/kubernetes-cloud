#!/bin/which python3
import argparse
from typing import Callable, List
from torch import Tensor
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer
from transformers.modeling_utils import no_init_weights, PreTrainedModel

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"

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
parser.add_argument("--prompt-file", type=str, help="File containing prompts")
parser.add_argument("--generate-tokens", type=int, help="Number of tokens to generate",
                    default=200)
parser.add_argument('--seed', type=int, help="Random seed value",
                    default=None)
parser.add_argument("--num-samples", type=int, help="Number of samples to generate",
                    default=1)
parser.add_argument("--top-k", type=int, help="Top K to use for sampling",
                    default=50)
parser.add_argument("--top-p", type=float, help="Top P to use for sampling",
                    default=0.95)
parser.add_argument("--temperature", type=float, help="Temperature to use for sampling",
                    default=1.0)
parser.add_argument("--repetition-penalty", type=float,
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


tokenizer = AutoTokenizer.from_pretrained(args.tokenizer,
                                          eos_token=args.eot,
                                          pad_token=args.pad,
                                          cache_dir=args.cache,
                                          padding_side='left')

model = AutoModelForCausalLM.from_pretrained(args.model,
                                             # Can be a HuggingFace ID or directory.
                                             cache_dir=args.cache,
                                             use_cache=True)  # Gradient checkpointing
# needs this off.
if args.fp16:
    model = no_init(lambda: model.half().to(device))
else:
    model = no_init(lambda: model.to(device))

model.eval()


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
    for response in evaluate(prompt, args.max_tokens, args.num_samples):
        print("-----------------------------")
        print("RESPONSE:", response)
