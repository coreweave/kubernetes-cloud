import os
import argparse
from diffusers import StableDiffusionPipeline
from tensorizer import serialize_model

token = os.environ.get("HUGGING_FACE_HUB_TOKEN")

parser = argparse.ArgumentParser()
parser.add_argument('--model-id', default="CompVis/stable-diffusion-v1-4")
parser.add_argument('--save-path', default="CompVis/stable-diffusion-v1-4")
args = parser.parse_args()

pipeline = StableDiffusionPipeline.from_pretrained(
    args.model_id,
    use_auth_token=token,
)

os.makedirs(args.save_path, exist_ok=True)

# The first model is the CLIP Text Encoder.
serialize_model(
    model=pipeline.text_encoder,
    config=pipeline.text_encoder.config,
    model_directory=args.save_path,
    model_prefix="encoder",
)

# The second model is the VAE.
serialize_model(
    model=pipeline.vae,
    config=None,
    model_directory=args.save_path,
    model_prefix="vae",
)

# The third model is the UNet.
serialize_model(
    model=pipeline.unet,
    config=None,
    model_directory=args.save_path,
    model_prefix="unet",
)

# Save CLIP Tokenizer to the model directory.
pipeline.tokenizer.save_pretrained(args.save_path)

# We can also save the scheduler.
pipeline.scheduler.save_config(args.save_path)

