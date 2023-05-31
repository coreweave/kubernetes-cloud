import torch
from tensorizer import TensorSerializer
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTJForCausalLM

model_ref = "EleutherAI/gpt-j-6b"

model = AutoModelForCausalLM.from_pretrained(
    model_ref,
    revision="float16",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

serializer = TensorSerializer("/mnt/gptj.tensors")
serializer.write_module(model)
serializer.close()

model.save_pretrained("/mnt")
tokenizer.save_pretrained("/mnt")
