import os
import time

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

mem_map = {0: '71GIB', 1: '71GIB', 2: '71GIB', 3: '71GIB', 4: '71GIB', 5: '71GIB', 6: '71GIB', 7: '71GIB'}

options = {
    'MODEL_PATH': os.getenv('MODEL_PATH', "/mnt/pvc/bloom"),
    'MODEL_TYPE': os.getenv('MODEL_TYPE', 'text-generation'),
}

model = AutoModelForCausalLM.from_pretrained(options["MODEL_PATH"], device_map="auto", max_memory=mem_map, torch_dtype=torch.bfloat16, local_files_only=True)
model.bfloat16().eval()
tokenizer = AutoTokenizer.from_pretrained(options["MODEL_PATH"], local_files_only=True)
generator = pipeline(
    options['MODEL_TYPE'],
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
)

def predict(max_length: int, num_iter: int):
    start = time.time()

    for _ in range(num_iter):
        _ = generator(
            "<s>",
            max_length=max_length
        )

    elapsed_time = time.time() - start
    tokens_per_second = max_length / elapsed_time

    return tokens_per_second, elapsed_time

max_length = int(os.getenv('MAX_LENGTH', '128'))
num_iter = int(os.getenv('NUM_ITER', '5'))

print('Running benchmark.')
tps, et = predict(max_length, num_iter)
print(f"{options['MODEL_PATH']}: inferenced at {tps} tokens per second, {et} seconds taken to run.")
