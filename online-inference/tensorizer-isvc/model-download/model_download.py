import torch
from tensorizer import TensorSerializer
from transformers import AutoModelForCausalLM, AutoTokenizer

model_ref = "EleutherAI/gpt-j-6b"

tokenizer = AutoTokenizer.from_pretrained(model_ref)
tokenizer.save_pretrained("/mnt")
del tokenizer

model = AutoModelForCausalLM.from_pretrained(
    model_ref,
    revision="float16",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)
# If only the tensorized model is desired, instead of saving the whole
# PyTorch model, only the PretrainedConfig for the model need be saved
# with the tokenizer and .tensors file.
# model.config.save_pretrained("/mnt")
model.save_pretrained("/mnt")

serializer = TensorSerializer("/mnt/gptj.tensors")
serializer.write_module(model, remove_tensors=True)
serializer.close()
