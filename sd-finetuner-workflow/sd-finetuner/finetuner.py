import argparse
import socket
import torch
import torchvision
import transformers
import diffusers
import os
import io
import PIL
import glob
import random
import tqdm
import resource
import psutil
import pynvml
import sys
import wandb
import gc

try:
    pynvml.nvmlInit()
except pynvml.nvml.NVMLError_LibraryNotFound:
    pynvml = None

from typing import Iterable
from diffusers import AutoencoderKL, UNet2DConditionModel, DDPMScheduler, PNDMScheduler, StableDiffusionPipeline
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker
from diffusers.optimization import get_scheduler
from transformers import CLIPFeatureExtractor, CLIPTextModel, CLIPTokenizer
from PIL import Image, ImageOps

# defaults should be good for everyone
# TODO: add custom VAE support. should be simple with diffusers
parser = argparse.ArgumentParser(description='Stable Diffusion Finetuner')
parser.add_argument('--model', type=str, default=None, required=True, help='The name of the model to use for finetuning. Could be HuggingFace ID or a directory')
parser.add_argument('--run_name', type=str, default=None, required=True, help='Name of the finetune run.')
parser.add_argument('--dataset', type=str, default=None, required=True, help='The path to the dataset to use for finetuning.')
parser.add_argument('--lr', type=float, default=5e-6, help='Learning rate')
parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train for')
parser.add_argument('--batch_size', type=int, default=1, help='Batch size')
parser.add_argument('--use_ema', type=bool, default=False, help='Use EMA for finetuning')
parser.add_argument('--ucg', type=float, default=0.1, help='Percentage chance of dropping out the text condition per batch. Ranges from 0.0 to 1.0 where 1.0 means 100% text condition dropout.') # 10% dropout probability
parser.add_argument('--gradient_checkpointing', dest='gradient_checkpointing', type=bool, default=False, help='Enable gradient checkpointing')
parser.add_argument('--use_8bit_adam', dest='use_8bit_adam', type=bool, default=False, help='Use 8-bit Adam optimizer')
parser.add_argument('--adam_beta1', type=float, default=0.9, help='Adam beta1')
parser.add_argument('--adam_beta2', type=float, default=0.999, help='Adam beta2')
parser.add_argument('--adam_weight_decay', type=float, default=1e-2, help='Adam weight decay')
parser.add_argument('--adam_epsilon', type=float, default=1e-08, help='Adam epsilon')
parser.add_argument('--seed', type=int, default=42, help='Seed for random number generator, this is to be used for reproduceability purposes.')
parser.add_argument('--output_path', type=str, default='./output', help='Root path for all outputs.')
parser.add_argument('--save_steps', type=int, default=500, help='Number of steps to save checkpoints at.')
parser.add_argument('--resolution', type=int, default=512, help='Image resolution to train against. Lower res images will be scaled up to this resolution and higher res images will be scaled down.')
parser.add_argument('--resize', dest='resize', type=bool, default=True, help='This flag will enable image resizing during training.')
parser.add_argument('--center_crop', dest='center_crop', type=bool, default=True, help='This flag will enable center cropping during training.')
parser.add_argument('--resize_interp', type=str, default='lanczos', help='Image sampling method to use when resizing images')
parser.add_argument('--shuffle', dest='shuffle', type=bool, default=True, help='Shuffle dataset')
parser.add_argument('--hf_token', type=str, default=None, required=False, help='A HuggingFace token is needed to download private models for training.')
parser.add_argument('--project_id', type=str, default='diffusers', help='Project ID for reporting to WandB')
parser.add_argument('--fp16', dest='fp16', type=bool, default=False, help='Train in mixed precision')
parser.add_argument('--image_log_steps', type=int, default=10, help='Number of steps to log images at.')
parser.add_argument('--image_log_amount', type=int, default=4, help='Number of images to log every image_log_steps')
args = parser.parse_args()

os.makedirs(args.output_path, exist_ok=True)

# remove hf_token from args so sneaky people don't steal it from the wandb logs
sanitized_args = {k: v for k, v in vars(args).items() if k not in ['hf_token']}
run = wandb.init(project=args.project_id, name=args.run_name, config=sanitized_args, dir=args.output_path+'/wandb')

# Inform the user of host, and various versions -- useful for debugging isseus.
print("RUN_NAME:", args.run_name)
print("HOST:", socket.gethostname())
print("CUDA:", torch.version.cuda)
print("TORCH:", torch.__version__)
print("TRANSFORMERS:", transformers.__version__)
print("DIFFUSERS:", diffusers.__version__)
print("MODEL:", args.model)
print("FP16:", args.fp16)
print("RESOLUTION:", args.resolution)

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
        gpu_total = int(gpu_info.total / 1E6)
        gpu_free = int(gpu_info.free / 1E6)
        gpu_used = int(gpu_info.used / 1E6)
        gpu_str = f"GPU: (U: {gpu_used:,}mb F: {gpu_free:,}mb " \
                  f"T: {gpu_total:,}mb) "
        torch_reserved_gpu = int(torch.cuda.memory.memory_reserved() / 1E6)
        torch_reserved_max = int(torch.cuda.memory.max_memory_reserved() / 1E6)
        torch_used_gpu = int(torch.cuda.memory_allocated() / 1E6)
        torch_max_used_gpu = int(torch.cuda.max_memory_allocated() / 1E6)
        torch_str = f"TORCH: (R: {torch_reserved_gpu:,}mb/"  \
                    f"{torch_reserved_max:,}mb, " \
                    f"A: {torch_used_gpu:,}mb/{torch_max_used_gpu:,}mb)"
    except AssertionError:
        pass
    cpu_maxrss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1E3 +
                     resource.getrusage(
                         resource.RUSAGE_CHILDREN).ru_maxrss / 1E3)
    cpu_vmem = psutil.virtual_memory()
    cpu_free = int(cpu_vmem.free / 1E6)
    return f"CPU: (maxrss: {cpu_maxrss:,}mb F: {cpu_free:,}mb) " \
           f"{gpu_str}" \
           f"{torch_str}"

def resize_image(image: Image, max_size=(512,512), reasmple=Image.Resampling.LANCZOS):
    image = ImageOps.contain(image, max_size, reasmple)
    # resize to integer multiple of 64
    w, h = image.size
    w, h = map(lambda x: x - x % 64, (w, h))

    ratio = w / h
    src_ratio = image.width / image.height

    src_w = w if ratio > src_ratio else image.width * h // image.height
    src_h = h if ratio <= src_ratio else image.height * w // image.width

    resized = image.resize((src_w, src_h), reasmple)
    res = Image.new("RGB", (w, h))
    res.paste(resized, box=(w // 2 - src_w // 2, h // 2 - src_h // 2))

    return res

class LocalBase(torch.utils.data.Dataset):
    def __init__(self,
                 data_root='../example_data',
                 size=512,
                 ucg=0.1,
                 interpolation="lanczos",
                 resize=True,
                 shuffle=False,
                 tokenizer=None,
                 ):
        super().__init__()

        self.shuffle=shuffle
        self.resize=resize

        ext = ['png', 'jpg', 'jpeg', 'bmp', 'webp']
        self.image_files = []
        [self.image_files.extend(glob.glob(f'{data_root}/' + '*.' + e)) for e in ext]

        self.examples = {}
        self.hashes = []
        for i in self.image_files:
            hash = i[len(f'{data_root}/'):].split('.')[0]
            self.examples[hash] = {
                'image': i,
                'text': f'{data_root}/{hash}.txt'
            }
            self.hashes.append(hash)

        self.size = size
        self.interpolation = {"bilinear": PIL.Image.Resampling.BILINEAR,
                              "bicubic": PIL.Image.Resampling.BICUBIC,
                              "lanczos": PIL.Image.Resampling.LANCZOS,
                              }[interpolation]
        
        self.transforms = torchvision.transforms.Compose([
            torchvision.transforms.Lambda(lambda x: resize_image(x, (self.size, self.size), self.interpolation)),
            torchvision.transforms.CenterCrop(self.size) if args.center_crop else torchvision.transforms.RandomCrop(self.size),
            torchvision.transforms.RandomHorizontalFlip(p=0.5),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.5], [0.5]),
        ])

        self.ucg = ucg
        self.tokenizer = tokenizer

    def get_caption(self, i):
        example = self.examples[self.hashes[i]]
        caption = open(example['text'], 'r').read()
        caption = caption.replace('  ', ' ').replace('\n', ' ').lstrip().rstrip()
        return caption

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, i):
        image = {} # pixel values, input ids
        try:
            image_file = self.examples[self.hashes[i]]['image']
            with open(image_file, 'rb') as f:
                image_pil = Image.open(f).convert('RGB')
                image['pixel_values'] = self.transforms(image_pil)
            text_file = self.examples[self.hashes[i]]['text']
            with open(text_file, 'rb') as f:
                text = f.read().decode('utf-8')
                text = text.replace('  ', ' ').replace('\n', ' ').lstrip().rstrip()
                image['input_ids'] = self.tokenizer(text, max_length=self.tokenizer.model_max_length, padding='do_not_pad', truncation=True).input_ids
        except Exception as e:
            print(f'Error with {self.examples[self.hashes[i]]["image"]} -- {e} -- skipping {i}')
            return None

        if random.random() < self.ucg:
            image['caption'] = ''

        return image

# Adapted from torch-ema https://github.com/fadel/pytorch_ema/blob/master/torch_ema/ema.py#L14
class EMAModel:
    """
    Exponential Moving Average of models weights
    """

    def __init__(self, parameters: Iterable[torch.nn.Parameter], decay=0.9999):
        parameters = list(parameters)
        self.shadow_params = [p.clone().detach() for p in parameters]

        self.decay = decay
        self.optimization_step = 0

    def get_decay(self, optimization_step):
        """
        Compute the decay factor for the exponential moving average.
        """
        value = (1 + optimization_step) / (10 + optimization_step)
        return 1 - min(self.decay, value)

    @torch.no_grad()
    def step(self, parameters):
        parameters = list(parameters)

        self.optimization_step += 1
        self.decay = self.get_decay(self.optimization_step)

        for s_param, param in zip(self.shadow_params, parameters):
            if param.requires_grad:
                tmp = self.decay * (s_param - param)
                s_param.sub_(tmp)
            else:
                s_param.copy_(param)

        torch.cuda.empty_cache()

    def copy_to(self, parameters: Iterable[torch.nn.Parameter]) -> None:
        """
        Copy current averaged parameters into given collection of parameters.
        Args:
            parameters: Iterable of `torch.nn.Parameter`; the parameters to be
                updated with the stored moving averages. If `None`, the
                parameters with which this `ExponentialMovingAverage` was
                initialized will be used.
        """
        parameters = list(parameters)
        for s_param, param in zip(self.shadow_params, parameters):
            param.data.copy_(s_param.data)

    def to(self, device=None, dtype=None) -> None:
        r"""Move internal buffers of the ExponentialMovingAverage to `device`.
        Args:
            device: like `device` argument to `torch.Tensor.to`
        """
        # .to() on the tensors handles None correctly
        self.shadow_params = [
            p.to(device=device, dtype=dtype) if p.is_floating_point() else p.to(device=device)
            for p in self.shadow_params
        ]

def main():
    # get device. TODO: support multi-gpu
    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda'
    
    print("DEVICE:", device)

    # setup fp16 stuff
    scaler = torch.cuda.amp.GradScaler(enabled=args.fp16)

    # Set seed
    torch.manual_seed(args.seed)
    print('RANDOM SEED:', args.seed)

    tokenizer = CLIPTokenizer.from_pretrained(args.model, subfolder='tokenizer', use_auth_token=args.hf_token)
    text_encoder = CLIPTextModel.from_pretrained(args.model, subfolder='text_encoder', use_auth_token=args.hf_token)
    vae = AutoencoderKL.from_pretrained(args.model, subfolder='vae', use_auth_token=args.hf_token)
    unet = UNet2DConditionModel.from_pretrained(args.model, subfolder='unet', use_auth_token=args.hf_token)

    # Freeze vae and text_encoder
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)

    if args.gradient_checkpointing:
        unet.enable_gradient_checkpointing()
    
    if args.use_8bit_adam: # Bits and bytes is only supported on certain CUDA setups, so default to regular adam if it fails.
        try:
            import bitsandbytes as bnb
            optimizer_cls = bnb.optim.AdamW8bit
        except:
            print('bitsandbytes not supported, using regular Adam optimizer')
            optimizer_cls = torch.optim.AdamW
    else:
        optimizer_cls = torch.optim.AdamW
    
    optimizer = optimizer_cls(
        unet.parameters(),
        lr=args.lr,
        betas=(args.adam_beta1, args.adam_beta2),
        eps=args.adam_epsilon,
        weight_decay=args.adam_weight_decay,
    )

    noise_scheduler = DDPMScheduler(
        beta_start=0.00085,
        beta_end=0.012,
        beta_schedule='scaled_linear',
        num_train_timesteps=1000,
        tensor_format='pt'
    )

    # load dataset

    def collate_fn(examples):
        pixel_values = torch.stack([example['pixel_values'] for example in examples if example is not None])
        pixel_values.to(memory_format=torch.contiguous_format).float()
        input_ids = [example['input_ids'] for example in examples if example is not None]
        padded_tokens = tokenizer.pad({'input_ids': input_ids}, return_tensors='pt', padding=True)
        return {
            'pixel_values': pixel_values,
            'input_ids': padded_tokens.input_ids,
            'attention_mask': padded_tokens.attention_mask,
        }

    train_dataset = LocalBase(
        args.dataset,
        args.resolution,
        args.ucg,
        args.resize_interp,
        args.resize,
        args.shuffle,
        tokenizer
    )

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        shuffle=args.shuffle,
        batch_size=args.batch_size,
        collate_fn=collate_fn,
    )

    lr_scheduler = get_scheduler(
        'constant',
        optimizer=optimizer
    )

    weight_dtype = torch.float16 if args.fp16 else torch.float32

    # move models to device
    vae = vae.to(device, dtype=weight_dtype)
    unet = unet.to(device, dtype=torch.float32)
    text_encoder = text_encoder.to(device, dtype=weight_dtype)

    # create ema
    if args.use_ema:
        ema_unet = EMAModel(unet.parameters())
    
    print(get_gpu_ram())

    num_steps_per_epoch = len(train_dataloader)
    progress_bar = tqdm.tqdm(range(args.epochs * num_steps_per_epoch), desc="Total Steps", leave=False)
    global_step = 0

    def save_checkpoint():
        if args.use_ema:
            ema_unet.copy_to(unet.parameters())
        pipeline = StableDiffusionPipeline(
            text_encoder=text_encoder,
            vae=vae,
            unet=unet,
            tokenizer=tokenizer,
            scheduler=PNDMScheduler(
                beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", skip_prk_steps=True
            ),
            safety_checker=StableDiffusionSafetyChecker.from_pretrained("CompVis/stable-diffusion-safety-checker"),
            feature_extractor=CLIPFeatureExtractor.from_pretrained("openai/clip-vit-base-patch32"),
        )
        pipeline.save_pretrained(args.output_path)
    
    # train!
    for epoch in range(args.epochs):
        unet.train()
        train_loss = 0.0
        for step, batch in enumerate(train_dataloader):
            # Convert images to latent space
            latents = vae.encode(batch['pixel_values'].to(device, dtype=weight_dtype)).latent_dist.sample()
            latents = latents * 0.18215

            # Sample noise
            noise = torch.randn_like(latents)
            bsz = latents.shape[0]
            # Sample a random timestep for each image
            timesteps = torch.randint(0, noise_scheduler.num_train_timesteps, (bsz,), device=latents.device)
            timesteps = timesteps.long()

            # Add noise to the latents according to the noise magnitude at each timestep
            # (this is the forward diffusion process)
            noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

            # Get the text embedding for conditioning
            encoder_hidden_states = text_encoder(batch["input_ids"].to(device))[0]

            # Predict the noise residual and compute loss
            with torch.autocast('cuda', enabled=args.fp16):
                noise_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample
            
            loss = torch.nn.functional.mse_loss(noise_pred.float(), noise.float(), reduction="mean")

            # Backprop
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            lr_scheduler.step()
            optimizer.zero_grad()

            # Update EMA
            if args.use_ema:
                ema_unet.step(unet.parameters())
            
            progress_bar.update(1)
            global_step += 1
            logs = {
                "loss": loss.detach().item(),
                "lr": lr_scheduler.get_last_lr()[0],
                "epoch": epoch
            }
            progress_bar.set_postfix(logs)
            run.log(logs)

            if global_step % args.save_steps == 0:
                save_checkpoint()
            
            if global_step % args.image_log_steps == 0:
                # get prompt from random batch
                prompt = tokenizer.decode(batch['input_ids'][random.randint(0, len(batch['input_ids'])-1)].tolist())
                pipeline = StableDiffusionPipeline(
                    text_encoder=text_encoder,
                    vae=vae,
                    unet=unet,
                    tokenizer=tokenizer,
                    scheduler=PNDMScheduler(
                        beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", skip_prk_steps=True
                    ),
                    safety_checker=None, # display safety checker to save memory
                    feature_extractor=CLIPFeatureExtractor.from_pretrained("openai/clip-vit-base-patch32"),
                ).to(device)
                # inference
                images = []
                with torch.no_grad():
                    with torch.autocast('cuda', enabled=args.fp16):
                        for _ in range(args.image_log_amount):
                            images.append(wandb.Image(pipeline(prompt).images[0], caption=prompt))
                # log images under single caption
                run.log({'images': images})

                # cleanup so we don't run out of memory
                del pipeline
                gc.collect()
    
    save_checkpoint()

    print(get_gpu_ram())
    print('Done!')


if __name__ == '__main__':
    main()

"""
import numpy as np
# save a sample
img = batch['pixel_values'][0].permute(1, 2, 0).cpu().numpy()
img = ((img + 1.0) * 127.5).astype(np.uint8)
img = Image.fromarray(img)
img.save('sample.png')
break
"""