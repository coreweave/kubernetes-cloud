import abc
from pathlib import Path
from typing import Optional, Dict, Callable, List, Union

import PIL
import torch
import torchvision
import transformers


class DiffusionDataset(torch.utils.data.Dataset, abc.ABC):
    """Base class for all Diffusion datasets."""

    def __init__(self,
                 tokenizer: transformers.PreTrainedTokenizer,
                 size: int = 512,
                 center_crop: bool = False,
                 interpolation: str = "lanczos"):
        self.tokenizer = tokenizer
        self.size = size
        self.center_crop = center_crop
        interpolation = {
            "bilinear": PIL.Image.Resampling.BILINEAR,
            "bicubic": PIL.Image.Resampling.BICUBIC,
            "lanczos": PIL.Image.Resampling.LANCZOS,
        }[interpolation]

        self.image_transforms = torchvision.transforms.Compose(
            [
                torchvision.transforms.Resize(size, interpolation=interpolation),
                torchvision.transforms.CenterCrop(size) if center_crop else torchvision.transforms.RandomCrop(size),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize([0.5], [0.5]),
            ]
        )

        self.ext = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

    def load_image(self, image_path: Path) -> torch.Tensor:
        image = PIL.Image.open(image_path)
        if not image.mode == "RGB":
            image = image.convert("RGB")
        return self.image_transforms(image)

    @abc.abstractmethod
    def get_collate_fn(self) -> Callable[[List[Dict]], Dict[str, torch.Tensor]]:
        raise NotImplementedError("DiffusionDataset subclasses need to implement this method")


class DreamBoothDataset(DiffusionDataset):
    """Dataset to be used with the DreamBooth finetune method.

    Data is split in two directories, instance and class.
    Instance images contains the object you are trying to teach the model about.
    Class images contains generic images of the type of object. Usually generated with a pretrained diffusion model.

    All images within each group share the same caption.
    """

    def __init__(self,
                 tokenizer: transformers.PreTrainedTokenizer,
                 instance_data_root: Union[Path, str],
                 instance_prompt: str,
                 class_prompt: str,
                 class_data_root: Union[Path, str],
                 num_class_images: int,
                 class_image_generator: Callable[[int], None],
                 **args):
        super().__init__(tokenizer, **args)

        if isinstance(instance_data_root, str):
            instance_data_root = Path(instance_data_root)
        if isinstance(class_data_root, str):
            class_data_root = Path(class_data_root)

        if not instance_data_root.exists():
            raise ValueError(f"Instance images root doesn't exist: {self.instance_data_root}")

        self.instance_images_paths = [f for f in instance_data_root.iterdir()
                                      if f.suffix in self.ext]
        self.num_instance_images = len(self.instance_images_paths)
        print(f"Found {self.num_instance_images} instance images")
        self.instance_ids = self.tokenizer(instance_prompt,
                                           truncation=True,
                                           padding="do_not_pad",
                                           max_length=self.tokenizer.model_max_length).input_ids

        class_data_root.mkdir(parents=True, exist_ok=True)
        self.class_images_path = [f for f in class_data_root.iterdir()
                                  if f.suffix in self.ext]
        self.num_class_images = len(self.class_images_path)

        if self.num_class_images < num_class_images:
            class_image_generator(num_class_images - self.num_class_images)
            self.class_images_path = [f for f in class_data_root.iterdir()
                                      if f.suffix in self.ext]
            self.num_class_images = len(self.class_images_path)
        elif self.num_class_images > num_class_images:
            self.num_class_images = self.num_class_images[:num_class_images]

        self.class_ids = self.tokenizer(class_prompt,
                                        truncation=True,
                                        padding="do_not_pad",
                                        max_length=self.tokenizer.model_max_length).input_ids

        self._length = max(self.num_class_images, self.num_instance_images)

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, index: int) -> Dict[str, torch.Tensor]:
        instance_img_path = self.instance_images_paths[index % self.num_instance_images]
        class_img_path = self.class_images_path[index % self.num_class_images]

        return {
            "instance_image": self.load_image(instance_img_path),
            "class_image": self.load_image(class_img_path),
        }

    def get_collate_fn(self) -> Callable[[List[Dict[str, torch.Tensor]]], Dict[str, torch.Tensor]]:
        def collate_fn(examples: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
            pixel_values = [example["instance_image"] for example in examples]
            pixel_values += [example["class_image"] for example in examples]
            pixel_values = (
                torch.stack(pixel_values)
                .to(memory_format=torch.contiguous_format)
                .float()
            )

            input_ids = [self.instance_ids] * len(examples) + [self.class_ids] * len(examples)
            padded_tokens = self.tokenizer.pad({"input_ids": input_ids},
                                               return_tensors="pt",
                                               padding=True)
            return {
                "pixel_values": pixel_values,
                "input_ids": padded_tokens.input_ids,
                "attention_mask": padded_tokens.attention_mask
            }

        return collate_fn


class LocalBase(DiffusionDataset):
    """Dataset for standard finetuning that gets loaded in from a single root directory.

    Image and text files are matched up based on the file name.
    Ex: dog_1.png and dog_1.txt will be used together for a single example
    """

    def __init__(
            self,
            tokenizer: transformers.PreTrainedTokenizer,
            data_root: Optional[Union[Path, str]] = None,
            ucg: float = 0.1,
            shuffle: bool = False,
            **args
    ):
        super().__init__(tokenizer, **args)

        if not data_root:
            data_root = Path("./data")
        if isinstance(data_root, str):
            data_root = Path(data_root)
        if not data_root.exists():
            raise ValueError(f"Data root doesn't exist: {data_root}")

        self.shuffle = shuffle
        self.ucg = ucg

        image_files = [f for f in data_root.iterdir()
                       if f.suffix in self.ext]
        # Group the image and prompt files based on file name without the extension
        self.examples = [(file_path, data_root / f"{file_path.stem}.txt")
                         for file_path in image_files]

    def get_input_ids(self, text_path: Path) -> torch.Tensor:
        """Read and tokenize image prompt from a .txt file."""

        with open(text_path, "rb") as f:
            text = f.read().decode("utf-8")

        text = text.replace("  ", " ").replace("\n", " ").strip()
        return self.tokenizer(text,
                              max_length=self.tokenizer.model_max_length,
                              padding="do_not_pad",
                              return_tensors="pt",
                              truncation=True).input_ids.squeeze(0)

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, i: int) -> Optional[Dict[str, torch.Tensor]]:
        image_path, text_path = self.examples[i]

        try:
            image = self.load_image(image_path)
            input_ids = self.get_input_ids(text_path)
        except Exception as e:
            print(f"Error with {image_path.stem} -- {e} -- skipping {i}")
            return

        return {"pixel_values": image,
                "input_ids": input_ids}

    def get_collate_fn(self) -> Callable[[List[Dict[str, torch.Tensor]]], Dict[str, torch.Tensor]]:
        def collate_fn(examples: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
            pixel_values = (
                torch.stack([example["pixel_values"] for example in examples
                             if example is not None])
                .to(memory_format=torch.contiguous_format)
                .float()
            )

            input_ids = [example["input_ids"].tolist() for example in examples
                         if example is not None]

            padded_tokens = self.tokenizer.pad({"input_ids": input_ids},
                                               return_tensors="pt",
                                               padding=True)

            return {
                "pixel_values": pixel_values,
                "input_ids": padded_tokens.input_ids,
                "attention_mask": padded_tokens.attention_mask,
            }

        return collate_fn


class PromptDataset(torch.utils.data.Dataset):
    """A simple dataset to prepare the prompts to generate class images."""

    def __init__(self, prompt, num_samples):
        self.prompt = prompt
        self.num_samples = num_samples

    def __len__(self):
        return self.num_samples

    def __getitem__(self, index):
        return {
            "prompt": self.prompt,
            "index": index
        }
