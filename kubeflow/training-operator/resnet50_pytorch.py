import argparse
import datetime
import os
import time
from pathlib import Path
from typing import Tuple, Optional

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import wandb
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, Sampler
from torch.utils.data.distributed import DistributedSampler
from torchvision import datasets, transforms, models
from torchvision.transforms import transforms
from torchvision.transforms.functional import InterpolationMode

WORLD_SIZE = int(os.environ.get("WORLD_SIZE", 1))
LOCAL_RANK = int(os.environ.get("LOCAL_RANK", 0))


def train(args: argparse.Namespace,
          model: models.resnet50,
          criterion: nn.CrossEntropyLoss,
          use_cuda: bool,
          train_loader: DataLoader,
          train_sampler: Sampler,
          optimizer: optim.Optimizer,
          epoch: int,
          writer: SummaryWriter,
          wandb_run: Optional[wandb.run]) -> None:
    model.train()
    if is_distributed():
        # Set epoch to sampler for shuffling.
        train_sampler.set_epoch(epoch)
    for batch_idx, (data, target) in enumerate(train_loader):
        step_start = time.perf_counter()
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if wandb_run:
            step_time = time.perf_counter() - step_start
            global_step = (epoch - 1) * len(train_loader) + batch_idx
            wandb_info = {"train/loss": loss.item(),
                          "train/epoch": epoch,
                          "train/step": global_step,
                          "train/samples_seen": global_step * len(data),
                          "perf/rank_samples_per_second": len(data) / step_time}
            wandb_run.log(wandb_info, step=global_step)

        if batch_idx % args.log_interval == 0:
            num_processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{num_processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tloss={loss.item():.4f}')
            niter = epoch * len(train_loader) + batch_idx
            writer.add_scalar('loss', loss.item(), niter)


def test(model: models.resnet50,
         criterion: nn.CrossEntropyLoss,
         use_cuda: bool,
         test_loader: DataLoader,
         test_sampler: Sampler,
         epoch: int,
         writer: SummaryWriter,
         wandb_run: Optional[wandb.run]):
    model.eval()
    test_loss = 0
    acc1 = 0
    acc5 = 0
    with torch.inference_mode():
        for data, target in test_loader:
            if use_cuda:
                data, target = data.cuda(), target.cuda()
            output = model(data)
            test_loss += criterion(output, target).item()

            batch_acc1, batch_acc5 = accuracy(output, target)
            acc1 += batch_acc1.item()
            acc5 += batch_acc5.item()

    test_loss /= len(test_sampler)
    acc1 /= len(test_sampler)
    acc5 /= len(test_sampler)
    print(f'Test Epoch: {epoch}\tloss={test_loss:.4f}\tAcc@1={acc1:.3f}\tAcc@5={acc5:.3f}')
    writer.add_scalar('acc1', acc1, epoch)
    writer.add_scalar('acc5', acc5, epoch)

    if wandb_run:
        wandb_info = {"test/loss": test_loss,
                      "test/epoch": epoch,
                      "test/acc1": acc1,
                      "test/acc5": acc5}
        wandb_run.log(wandb_info)


def accuracy(output, target, topk=(1, 5)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.inference_mode():
        maxk = max(topk)
        batch_size = target.size(0)
        if target.ndim == 2:
            target = target.max(dim=1)[1]

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target[None])

        res = []
        for k in topk:
            correct_k = correct[:k].flatten().sum(dtype=torch.float32)
            res.append(correct_k * (100.0 / batch_size))
        return res


def should_distribute() -> bool:
    return dist.is_available() and WORLD_SIZE > 1


def is_distributed() -> bool:
    return dist.is_available() and dist.is_initialized()


def load_data(train_dir: Path,
              test_dir: Path,
              args: argparse.Namespace) -> Tuple[datasets.ImageFolder, datasets.ImageFolder, Sampler, Sampler]:
    # These are known ImageNet values
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)

    interpolation = InterpolationMode(args.interpolation)
    train_transforms = transforms.Compose([
        transforms.RandomResizedCrop(args.train_crop_size, interpolation=interpolation),
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
        transforms.Normalize(mean=mean, std=std)
    ])
    train_dataset = datasets.ImageFolder(str(train_dir), train_transforms)

    test_transforms = transforms.Compose([
        transforms.Resize(args.val_resize_size, interpolation=interpolation),
        transforms.CenterCrop(args.val_crop_size),
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
        transforms.Normalize(mean=mean, std=std),
    ])
    test_dataset = datasets.ImageFolder(str(test_dir), test_transforms)

    if is_distributed():
        train_sampler = DistributedSampler(train_dataset, num_replicas=dist.get_world_size(), rank=dist.get_rank())
        test_sampler = DistributedSampler(test_dataset, num_replicas=dist.get_world_size(), rank=dist.get_rank())
    else:
        train_sampler = RandomSampler(train_dataset)
        test_sampler = SequentialSampler(test_dataset)

    return train_dataset, test_dataset, train_sampler, test_sampler


def get_args() -> argparse.Namespace:
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch resnet50 Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.9, metavar='M',
                        help='SGD momentum (default: 0.9)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--log-dir', default=Path('./logs'), metavar='L', type=Path,
                        help='Location where the logs will be saved.')
    parser.add_argument("--data-dir", default=Path("./data"), metavar="D", type=Path,
                        help="Location of the dataset (will be downloaded if needed)")
    parser.add_argument("--model-dir", default=None, metavar="M", type=Path,
                        help="Location to save the model checkpoint when training is finished.")
    parser.add_argument("--interpolation", default="bilinear", type=str,
                        help="the interpolation method (default: bilinear)")
    parser.add_argument("--val-resize-size", default=256, type=int,
                        help="the resize size used for validation (default: 256)")
    parser.add_argument("--val-crop-size", default=224, type=int,
                        help="the central crop size used for validation (default: 224)")
    parser.add_argument("--train-crop-size", default=224, type=int,
                        help="the random crop size used for training (default: 224)")
    parser.add_argument("-j", "--workers", default=16, type=int, metavar="N",
                        help="number of data loading workers (default: 16)")
    parser.add_argument("--wandb-project", type=str, default=None,
                        help="WandB Project ID to use for this run")
    parser.add_argument("--wandb-run", type=str, default=None,
                        help="WandB run name to use for logging")

    if dist.is_available():
        parser.add_argument('--backend', type=str, help='Distributed backend',
                            choices=[dist.Backend.GLOO, dist.Backend.NCCL, dist.Backend.MPI],
                            default=dist.Backend.GLOO)

    return parser.parse_args()


def main() -> None:
    args = get_args()
    torch.manual_seed(args.seed)

    use_cuda = not args.no_cuda and torch.cuda.is_available()
    if use_cuda:
        # Make sure this process only uses the GPU designated to it
        torch.cuda.set_device(LOCAL_RANK)
        torch.cuda.manual_seed(args.seed)

    if args.wandb_project:
        wandb_run = wandb.init(project=args.wandb_project,
                               name=args.wandb_run,
                               config=vars(args),
                               dir=args.log_dir / "wandb",
                               group=args.wandb_run)
    else:
        wandb_run = None

    writer = SummaryWriter(args.log_dir)

    if should_distribute():
        print('Using distributed PyTorch with {} backend'.format(args.backend))
        dist.init_process_group(backend=args.backend)
        print(f"Current rank: {dist.get_rank()}\tlocal rank: {LOCAL_RANK}\ttotal world size:  {dist.get_world_size()}")

    train_dataset, test_dataset, train_sampler, test_sampler = load_data(args.data_dir / "train",
                                                                         args.data_dir / "val",
                                                                         args)

    train_loader = DataLoader(train_dataset,
                              batch_size=args.batch_size,
                              sampler=train_sampler,
                              num_workers=args.workers,
                              pin_memory=True)
    test_loader = DataLoader(test_dataset,
                             batch_size=args.batch_size,
                             sampler=test_sampler,
                             num_workers=args.workers,
                             pin_memory=True)

    model = models.resnet50(weights=None)
    if use_cuda:
        model.cuda()

    criterion = nn.CrossEntropyLoss()

    if is_distributed():
        model = nn.parallel.DistributedDataParallel(model)

    lr_scaler = dist.get_world_size() if is_distributed() else 1
    optimizer = optim.SGD(model.parameters(), lr=args.lr * lr_scaler, momentum=args.momentum)

    start = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        train(args, model, criterion, use_cuda, train_loader, train_sampler, optimizer, epoch, writer, wandb_run)
        test(model, criterion, use_cuda, test_loader, test_sampler, epoch, writer, wandb_run)

    print(f"Training time: {time.perf_counter() - start:0.3f}s")

    # Only have the master checkpoint the model
    if args.model_dir and dist.get_rank() == 0:
        args.model_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), args.model_dir / "resnet50_imagenet.pt")

    if wandb_run:
        wandb_run.finish()


if __name__ == '__main__':
    main()
