import argparse
import gc
import hashlib
import os
import random
import resource
import socket
import sys
import time
from functools import partial
from pathlib import Path
from typing import Optional, Iterable

import accelerate
import diffusers
import psutil
import pynvml
import torch
import torch.nn.functional as F
import tqdm
import transformers
import wandb
from diffusers import (
    AutoencoderKL,
    UNet2DConditionModel,
    DDPMScheduler,
    PNDMScheduler,
    StableDiffusionPipeline,
)
from diffusers.optimization import get_scheduler
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker
from transformers import CLIPFeatureExtractor, CLIPTextModel, CLIPTokenizer

from datasets import LocalBase, DreamBoothDataset, PromptDataset

try:
    pynvml.nvmlInit()
except pynvml.nvml.NVMLError_LibraryNotFound:
    pynvml = None

# Latent Scale Factor - https://github.com/huggingface/diffusers/issues/437
L_SCALE_FACTOR = 0.18215


def parse_args() -> argparse.Namespace:
    # defaults should be good for everyone
    # TODO: add custom VAE support. should be simple with diffusers
    bool_t = lambda x: (str(x).lower() in ["true", "1", "t", "y", "yes"])
    parser = argparse.ArgumentParser(description="Stable Diffusion Finetuner")
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        required=True,
        help="The name of the model to use for finetuning. Could be HuggingFace ID or a directory",
    )
    parser.add_argument(
        "--run_name",
        type=str,
        default=None,
        required=True,
        help="Name of the finetune run.",
    )
    parser.add_argument("--lr", type=float, default=5e-6, help="Learning rate")
    parser.add_argument(
        "--lr_scheduler",
        type=str,
        default="constant",
        help="Type of learning rate scheduler to use."
    )
    parser.add_argument(
        "--lr_warmup_steps",
        type=int,
        default=0,
        help="Number of warm up steps to use with the learning rate scheduler."
    )
    parser.add_argument(
        "--epochs", type=int, default=10, help="Number of epochs to train for"
    )
    parser.add_argument("--batch_size", type=int, default=1, help="Batch size")
    parser.add_argument(
        "--use_ema", type=bool_t, default="False", help="Use EMA for finetuning"
    )
    parser.add_argument(
        "--gradient_checkpointing",
        dest="gradient_checkpointing",
        type=bool_t,
        default="False",
        help="Enable gradient checkpointing",
    )
    parser.add_argument(
        "--use_8bit_adam",
        dest="use_8bit_adam",
        type=bool_t,
        default="False",
        help="Use 8-bit Adam optimizer",
    )
    parser.add_argument("--adam_beta1", type=float, default=0.9, help="Adam beta1")
    parser.add_argument(
        "--adam_beta2", type=float, default=0.999, help="Adam beta2"
    )
    parser.add_argument(
        "--adam_weight_decay", type=float, default=1e-2, help="Adam weight decay"
    )
    parser.add_argument(
        "--adam_epsilon", type=float, default=1e-08, help="Adam epsilon"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed for random number generator, this is to be used for reproduceability purposes.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./output",
        help="Root path for all outputs.",
    )
    parser.add_argument(
        "--save_steps",
        type=int,
        default=500,
        help="Number of steps to save checkpoints at.",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=512,
        help="Image resolution to train against. Lower res images will be scaled up to this resolution and higher res images will be scaled down.",
    )
    parser.add_argument(
        "--center_crop",
        dest="center_crop",
        type=bool_t,
        default="True",
        help="This flag will enable center cropping during training.",
    )
    parser.add_argument(
        "--resize_interp",
        type=str,
        default="lanczos",
        help="Image sampling method to use when resizing images",
    )
    parser.add_argument(
        "--shuffle",
        dest="shuffle",
        type=bool_t,
        default="True",
        help="Shuffle dataset",
    )
    parser.add_argument(
        "--hf_token",
        type=str,
        default=None,
        required=False,
        help="A HuggingFace token is needed to download private models for training.",
    )
    parser.add_argument(
        "--project_id",
        type=str,
        default="diffusers",
        help="Project ID for reporting to WandB",
    )
    parser.add_argument(
        "--fp16",
        dest="fp16",
        type=bool_t,
        default="False",
        help="Train in mixed precision",
    )
    parser.add_argument(
        "--image_log_steps",
        type=int,
        default=10,
        help="Number of steps to log images at.",
    )
    parser.add_argument(
        "--image_log_amount",
        type=int,
        default=4,
        help="Number of images to log every image_log_steps",
    )

    # Vanilla finetuning args
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        required=False,
        help="The path to the dataset to use for finetuning.",
    )
    parser.add_argument(
        "--ucg",
        type=float,
        default=0.1,
        help="Percentage chance of dropping out the text condition per sample. Ranges from 0.0 to 1.0 where 1.0 means "
             "100% text condition dropout."
    )

    # Dreambooth finetuning args
    parser.add_argument(
        "--instance_dataset",
        type=str,
        default=None,
        required=False,
        help="Path to the dataset containing instance images."
    )
    parser.add_argument(
        "--instance_prompt",
        type=str,
        default=None,
        required=False,
        help="Prompt to use for all instance images."
    )
    parser.add_argument(
        "--class_dataset",
        type=str,
        default=None,
        required=False,
        help="Path to the dataset containing generic class images."
    )
    parser.add_argument(
        "--class_prompt",
        type=str,
        default=None,
        required=False,
        help="Prompt to use for all the class images."
    )
    parser.add_argument(
        "--prior_loss_weight",
        type=float,
        default=1.0,
        help="The weight of prior preservation loss."
    )
    parser.add_argument(
        "--num_class_images",
        type=int,
        default=100,
        help="Number of class images to use. If there are not enough in `class_dataset` then additional images will be "
             "generated using `class_prompt` and the pretrained model."
    )

    args = parser.parse_args()

    # Make sure the all the required args were given based on what finetuning method will be used
    db_arg_names = ["instance_dataset", "instance_prompt", "class_dataset", "class_prompt"]
    db_arg_values = [getattr(args, db_arg) for db_arg in db_arg_names]
    if any(db_arg_values):
        assert all(db_arg_values), "All the following values must be set when using dreambooth finetuning: " \
                                   f"{db_arg_names}"
        args.is_dreambooth = True
        print("Using the dreambooth method.")
    else:
        assert args.dataset, "--dataset must be provided when not using dreambooth finetuning"
        args.is_dreambooth = False

    return args


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

    def get_decay(self, optimization_step: int) -> float:
        """
        Compute the decay factor for the exponential moving average.
        """
        value = (1 + optimization_step) / (10 + optimization_step)
        return 1 - min(self.decay, value)

    @torch.no_grad()
    def step(self, parameters: Iterable[torch.nn.Parameter]) -> None:
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
            p.to(device=device, dtype=dtype)
            if p.is_floating_point()
            else p.to(device=device)
            for p in self.shadow_params
        ]


class StableDiffusionTrainer:
    def __init__(
            self,
            accelerator: accelerate.Accelerator,
            vae: AutoencoderKL,
            unet: UNet2DConditionModel,
            text_encoder: CLIPTextModel,
            tokenizer: CLIPTokenizer,
            ema: Optional[EMAModel],
            train_dataloader: torch.utils.data.DataLoader,
            noise_scheduler: DDPMScheduler,
            lr_scheduler: torch.optim.lr_scheduler.LambdaLR,
            optimizer: torch.optim.Optimizer,
            weight_dtype: torch.dtype,
            args: argparse.Namespace
    ):
        self.accelerator = accelerator
        self.vae = vae
        self.unet = unet
        self.text_encoder = text_encoder
        self.tokenizer = tokenizer
        self.ema = ema
        self.train_dataloader = train_dataloader
        self.noise_scheduler = noise_scheduler
        self.lr_scheduler = lr_scheduler
        self.optimizer = optimizer
        self.weight_dtype = weight_dtype
        self.args = args
        self.report_idx = 0

        if accelerator.is_main_process:
            self.progress_bar = tqdm.tqdm(
                range(self.args.epochs * len(self.train_dataloader)),
                desc="Total Steps",
                leave=False,
            )
            self.run = wandb.init(
                project=self.args.project_id,
                name=self.args.run_name,
                config={
                    k: v for k, v in vars(self.args).items() if k not in ["hf_token"]
                },
                dir=self.args.output_path + "/wandb",
            )
            self.global_step = 0

    def save_checkpoint(self):
        unet = self.accelerator.unwrap_model(self.unet)
        if self.ema is not None:
            self.ema.copy_to(unet.parameters())
        pipeline = StableDiffusionPipeline(
            text_encoder=self.text_encoder,
            vae=self.vae,
            unet=unet,
            tokenizer=self.tokenizer,
            scheduler=PNDMScheduler.from_pretrained(
                self.args.model,
                subfolder="scheduler",
            ),
            safety_checker=StableDiffusionSafetyChecker.from_pretrained(
                "CompVis/stable-diffusion-safety-checker"
            ),
            feature_extractor=CLIPFeatureExtractor.from_pretrained(
                "openai/clip-vit-base-patch32"
            ),
        )

        pipeline.save_pretrained(self.args.output_path)

    def sample(self, prompt: str) -> None:
        # get prompt from random batch
        pipeline = StableDiffusionPipeline(
            text_encoder=self.text_encoder,
            vae=self.vae,
            unet=self.accelerator.unwrap_model(self.unet),
            tokenizer=self.tokenizer,
            scheduler=PNDMScheduler.from_pretrained(
                self.args.model,
                subfolder="scheduler",
            ),
            safety_checker=None,  # display safety checker to save memory
            feature_extractor=CLIPFeatureExtractor.from_pretrained(
                "openai/clip-vit-base-patch32"
            ),
        ).to(self.accelerator.device)
        # inference
        images = []
        with torch.no_grad():
            with torch.autocast("cuda", enabled=self.args.fp16):
                for _ in range(self.args.image_log_amount):
                    images.append(
                        wandb.Image(pipeline(prompt).images[0], caption=prompt)
                    )
        # log images under single caption
        self.run.log({"images": images})

        # cleanup so we don't run out of memory
        del pipeline
        gc.collect()

    def step(self, batch: dict) -> dict:
        with self.accelerator.accumulate(self.unet):
            # Convert images to latent space
            latents = self.vae.encode(
                batch["pixel_values"].to(self.weight_dtype)
            ).latent_dist.sample()
            latents = latents * self.vae.config.get("scaling_factor", L_SCALE_FACTOR)

            # Sample noise
            noise = torch.randn_like(latents)
            bsz = latents.shape[0]
            # Sample a random timestep for each image
            timesteps = torch.randint(
                0,
                self.noise_scheduler.num_train_timesteps,
                (bsz,),
                device=latents.device,
            )
            timesteps = timesteps.long()

            # Add noise to the latents according to the noise magnitude at each timestep
            # (this is the forward diffusion process)
            noisy_latents = self.noise_scheduler.add_noise(
                latents, noise, timesteps
            )

            # Get the text embedding for conditioning
            encoder_hidden_states = self.text_encoder(batch["input_ids"])[0]

            # Predict the noise residual and compute loss
            with torch.autocast("cuda", enabled=self.args.fp16):
                noise_pred = self.unet(
                    noisy_latents, timesteps, encoder_hidden_states
                ).sample

            if self.noise_scheduler.config.prediction_type == "epsilon":
                target = noise
            elif self.noise_scheduler.config.prediction_type == "v_prediction":
                target = self.noise_scheduler.get_velocity(
                    latents, noise, timesteps
                )
            else:
                raise ValueError(
                    f"Invalid prediction type: {self.noise_scheduler.config.prediction_type}"
                )

            if self.args.is_dreambooth:  # Use prior preservation loss
                # Chunk the noise and model_pred into two parts and compute the loss on each part separately.
                model_pred, model_pred_prior = torch.chunk(noise_pred, 2, dim=0)
                target, target_prior = torch.chunk(target, 2, dim=0)

                # Compute instance loss
                loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")

                # Compute prior loss
                prior_loss = F.mse_loss(model_pred_prior.float(), target_prior.float(), reduction="mean")

                # Add the prior loss to the instance loss.
                loss = loss + self.args.prior_loss_weight * prior_loss
            else:
                loss = F.mse_loss(
                    noise_pred.float(), target.float(), reduction="mean"
                )

            # Backprop
            self.accelerator.backward(loss)
            if self.accelerator.sync_gradients:
                self.accelerator.clip_grad_norm_(self.unet.parameters(), 1.0)
            self.optimizer.step()
            self.lr_scheduler.step()
            self.optimizer.zero_grad()

        if self.accelerator.sync_gradients:
            # Update EMA
            if self.args.use_ema:
                self.ema.step(self.unet.parameters())

        return {
            "train/loss": loss.detach().item(),
            "train/lr": self.lr_scheduler.get_last_lr()[0],
        }

    def train(self) -> None:
        self.unet.train()
        for epoch in range(self.args.epochs):
            for _, batch in enumerate(self.train_dataloader):
                step_start = time.perf_counter()

                logs = self.step(batch)
                if self.accelerator.is_main_process:
                    self.log_step(epoch, batch, logs, step_start)

        self.accelerator.wait_for_everyone()
        self.save_checkpoint()

    def log_step(self, epoch: int, batch: dict, logs: dict, step_start: float) -> None:
        rank_samples_per_second = self.args.batch_size * (
                1 / (time.perf_counter() - step_start)
        )
        world_samples_per_second = (
                rank_samples_per_second * self.accelerator.num_processes
        )
        logs.update({
            "perf/rank_samples_per_second": rank_samples_per_second,
            "perf/world_samples_per_second": world_samples_per_second,
            "train/epoch": epoch,
            "train/step": self.global_step,
            "train/samples_seen": self.global_step * self.args.batch_size,
        })

        self.global_step += 1
        self.report_idx += 1

        if self.report_idx % 10 == 0:
            print(f"\nLOSS: {logs['train/loss']} {get_gpu_ram()}", file=sys.stderr)
            sys.stderr.flush()

        self.progress_bar.update(1)
        self.progress_bar.set_postfix(**logs)

        self.run.log(logs, step=self.global_step)

        if self.global_step % self.args.save_steps == 0:
            self.save_checkpoint()

        if self.global_step % self.args.image_log_steps == 0:
            prompt = self.tokenizer.decode(
                batch["input_ids"][
                    random.randint(0, len(batch["input_ids"]) - 1)
                ].tolist()
            )
            self.sample(prompt)


def generate_images(accelerator: accelerate.Accelerator,
                    model: str,
                    prompt: str,
                    batch_size: int,
                    output: str,
                    num_images: int) -> None:
    pipeline = StableDiffusionPipeline.from_pretrained(model, safety_checker=None)
    pipeline.set_progress_bar_config(disable=True)

    print(f"Generating {num_images} class images in {output}...")

    sample_dataset = PromptDataset(prompt, num_images)
    sample_dataloader = torch.utils.data.DataLoader(sample_dataset, batch_size=batch_size)

    sample_dataloader = accelerator.prepare(sample_dataloader)
    pipeline.to(accelerator.device)

    for example in tqdm.tqdm(
            sample_dataloader, desc="Generating class images", disable=not accelerator.is_local_main_process
    ):
        images = pipeline(example["prompt"]).images
        for i, image in enumerate(images):
            hash_image = hashlib.sha1(image.tobytes()).hexdigest()
            image_filename = Path(output) / f"{example['index'][i]}-{hash_image}.jpg"
            image.save(image_filename)

    del pipeline
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def main() -> None:
    args = parse_args()

    if args.hf_token is None:
        try:
            args.hf_token = os.environ["HF_API_TOKEN"]
        except KeyError:
            print(
                "Please set HF_API_TOKEN environment variable or pass --hf_token"
            )
            exit(1)
    else:
        print(
            "WARNING: Using HF_API_TOKEN from command line. This is insecure. Use environment variables instead."
        )

    tokenizer = CLIPTokenizer.from_pretrained(
        args.model, subfolder="tokenizer", use_auth_token=args.hf_token
    )
    text_encoder = CLIPTextModel.from_pretrained(
        args.model, subfolder="text_encoder", use_auth_token=args.hf_token
    )
    vae = AutoencoderKL.from_pretrained(
        args.model, subfolder="vae", use_auth_token=args.hf_token
    )
    unet = UNet2DConditionModel.from_pretrained(
        args.model, subfolder="unet", use_auth_token=args.hf_token
    )

    # Freeze vae and text_encoder
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)

    if args.gradient_checkpointing:
        unet.enable_gradient_checkpointing()

    # Bits and bytes is only supported on certain CUDA setups, so default to regular adam if it fails.
    if args.use_8bit_adam:
        try:
            import bitsandbytes as bnb

            optimizer_cls = bnb.optim.AdamW8bit
        except Exception:
            print("bitsandbytes not supported, using regular Adam optimizer")
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

    noise_scheduler = DDPMScheduler.from_pretrained(
        args.model, subfolder="scheduler", use_auth_token=args.hf_token
    )

    accelerator = accelerate.Accelerator(
        gradient_accumulation_steps=1,
        mixed_precision="fp16" if args.fp16 else "no",
    )

    # Set seed
    accelerate.utils.set_seed(args.seed)

    if accelerator.is_main_process:
        os.makedirs(args.output_path, exist_ok=True)
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
        print("RANDOM SEED:", args.seed)

    if args.is_dreambooth:
        generator_func = partial(
            generate_images,
            accelerator,
            args.model,
            args.class_prompt,
            args.batch_size,
            args.class_dataset
        )
        train_dataset = DreamBoothDataset(
            tokenizer=tokenizer,
            instance_data_root=args.instance_dataset,
            instance_prompt=args.instance_prompt,
            class_data_root=args.class_dataset,
            class_prompt=args.class_prompt,
            size=args.resolution,
            interpolation=args.resize_interp,
            num_class_images=args.num_class_images,
            class_image_generator=generator_func
        )
    else:
        train_dataset = LocalBase(
            tokenizer=tokenizer,
            data_root=args.dataset,
            size=args.resolution,
            interpolation=args.resize_interp,
            shuffle=args.shuffle,
            ucg=args.ucg
        )

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        shuffle=args.shuffle,
        batch_size=args.batch_size,
        collate_fn=train_dataset.get_collate_fn(),
    )

    lr_scheduler = get_scheduler(name=args.lr_scheduler, optimizer=optimizer, num_warmup_steps=args.lr_warmup_steps)

    unet, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
        unet, optimizer, train_dataloader, lr_scheduler
    )

    weight_dtype = torch.float16 if args.fp16 else torch.float32

    # move models to device
    vae = vae.to(accelerator.device, dtype=weight_dtype)
    text_encoder = text_encoder.to(accelerator.device, dtype=weight_dtype)

    # create ema
    if args.use_ema:
        ema_unet = EMAModel(unet.parameters())

    print(get_gpu_ram())

    trainer = StableDiffusionTrainer(
        accelerator,
        vae,
        unet,
        text_encoder,
        tokenizer,
        ema_unet if args.use_ema else None,
        train_dataloader,
        noise_scheduler,
        lr_scheduler,
        optimizer,
        weight_dtype,
        args
    )
    trainer.train()

    if accelerator.is_main_process:
        print(get_gpu_ram())
        print("Done!")


if __name__ == "__main__":
    main()
