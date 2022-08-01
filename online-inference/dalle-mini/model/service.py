import kserve
import logging
import os
import random
import base64
from io import BytesIO
from typing import Dict

import jax
import numpy as np
import jax.numpy as jnp
from functools import partial
from PIL import Image
from dalle_mini import DalleBart, DalleBartProcessor
from flax.jax_utils import replicate
from flax.training.common_utils import shard_prng_key
from tqdm.notebook import trange
from transformers import CLIPProcessor, FlaxCLIPModel
from vqgan_jax.modeling_flax_vqgan import VQModel

options = {
	'MODEL_NAME': os.getenv('MODEL_NAME', default="dalle-mini/dalle-mini"),
	'MODEL_CACHE': os.getenv('MODEL_CACHE', default="/model-cache")
}

model_options = {
	'N_PREDICTIONS': int(os.getenv('N_PREDICTIONS', default=1)),
	'TOP_K': os.getenv('TOP_K', default=None),
	'TOP_P': os.getenv('TOP_P', default=None),
	'TEMPERATURE': os.getenv('TEMPERATURE', default=None),
	'COND_SCALE': float(os.getenv('COND_SCALE', default=10.0))
}

TOP_K = None
TOP_P = None
TEMPERATURE = None
CONDITION_SCALE = 10.0

VQGAN_REPO = "dalle-mini/vqgan_imagenet_f16_16384"
VQGAN_COMMIT_ID = "e93a26e7707683d349bf5d5c41c5b0ef69b677a9"

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)
logger = logging.getLogger(options['MODEL_NAME'])

devices = jax.local_devices()
logger.info(f'Compute Devices: {devices}')

seed = random.randint(0, 2**32 - 1)
key = jax.random.PRNGKey(seed)

class Model(kserve.Model):
	def __init__(self, name: str):
		super().__init__(name)
		self.name = name
		self.ready = False
		self.model = None
		self.model_params = None
		self.vqgan = None
		self.vqgan_params = None
		self.processor = None
		self.generator = None
		self.model_name = options['MODEL_NAME']

	def load(self):
		self.model, model_params = DalleBart.from_pretrained(
			options['MODEL_NAME'],
			revision=None, 
			dtype=jnp.float16, 
			_do_init=False,
			#local_files_only=True
		)
		self.model_params = replicate(model_params)
		self.vqgan, vqgan_params = VQModel.from_pretrained(
			VQGAN_REPO,
			revision=VQGAN_COMMIT_ID,
			_do_init=False
		)
		self.vqgan_params = replicate(vqgan_params)
		self.processor = DalleBartProcessor.from_pretrained(options['MODEL_NAME'], revision=None)
		self.ready=True
	
	@partial(jax.pmap, axis_name="batch", static_broadcasted_argnums=(0, 4, 5, 6, 7))
	def p_generate(
		self, tokenized_prompt, key, params, top_k, top_p, temperature, condition_scale
	):
		return self.model.generate(
				**tokenized_prompt,
				prng_key=key,
				params=params,
				top_k=top_k,
				top_p=top_p,
				temperature=temperature,
				condition_scale=condition_scale,
			)

	@partial(jax.pmap, axis_name="batch", static_broadcasted_argnums=(0))
	def p_decode(self, indices, params):
		return self.vqgan.decode_code(indices, params=params)

	def configure_request(self, request: Dict, generation_params) -> Dict:
		parameters = request['parameters']
		for k, pv in parameters.items():
			pk = k.upper()
			if pk in generation_params:
				logger.debug(f'Parameter {pk} changed from {request_params[pk]} to {pv}')
				request_params[pk] = pv

		return generation_params

	def predict(self, request: Dict) -> Dict:
		seed = random.randint(0, 2**32 - 1)
		key = jax.random.PRNGKey(seed)

		tokenized_prompt = self.processor([request['prompt']])
		tokenized_prompt = replicate(tokenized_prompt)

		#images = []
		for i in trange(max(model_options['N_PREDICTIONS'] // jax.device_count(), 1)):
			key, subkey = jax.random.split(key)
			encoded_images = self.p_generate(
				tokenized_prompt,
				shard_prng_key(subkey),
				self.model_params,
				TOP_K,
				TOP_P,
				TEMPERATURE,
				CONDITION_SCALE,
			)

			encoded_images = encoded_images.sequences[..., 1:]
			decoded_images = self.p_decode(encoded_images, self.vqgan_params)
			decoded_images = decoded_images.clip(0.0, 1.0).reshape((-1, 256, 256, 3))
	
			for decoded_img in decoded_images:
				img = Image.fromarray(np.asarray(decoded_img * 255, dtype=np.uint8))
				img_file = BytesIO()
				img.save(img_file, format="PNG")
				img_bytes = img_file.getvalue()
				payload = base64.b64encode(img_bytes)
				payload = str(payload, 'utf-8')
				#images.append(img)

		return {'image': payload}

	@staticmethod
	def is_ready():
		pass

if __name__ == '__main__':
	#Model.is_ready()
	model = Model(options['MODEL_NAME'])
	logger.info(f'Loading model {options["MODEL_NAME"]}')
	model.load()
	logger.info(f'Model {options["MODEL_NAME"]} loaded')
	logger.info(f'Starting Model Server')
	kserve.ModelServer().start([model])