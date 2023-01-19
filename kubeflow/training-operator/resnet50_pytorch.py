import argparse
import os
import time
from pathlib import Path

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import wandb
from torch.utils.data import DataLoader
from torchvision import models

from util import train_epoch, test, load_data

WORLD_SIZE = int(os.environ.get("WORLD_SIZE", 1))
LOCAL_RANK = int(os.environ.get("LOCAL_RANK", 0))


def should_distribute() -> bool:
    return dist.is_available() and WORLD_SIZE > 1


def is_distributed() -> bool:
    return dist.is_available() and dist.is_initialized()


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

    if should_distribute():
        print('Using distributed PyTorch with {} backend'.format(args.backend))
        dist.init_process_group(backend=args.backend)
        print(f"Current rank: {dist.get_rank()}\tlocal rank: {LOCAL_RANK}\ttotal world size:  {dist.get_world_size()}")

    train_dataset, test_dataset, train_sampler, test_sampler = load_data(args.data_dir / "train",
                                                                         args.data_dir / "val",
                                                                         args,
                                                                         dist.get_world_size(),
                                                                         dist.get_rank())

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
        train_epoch(model,
                    criterion,
                    train_sampler,
                    train_loader,
                    optimizer,
                    epoch,
                    args.log_interval,
                    use_cuda,
                    wandb_run)
        test(model, criterion, test_sampler, test_loader, use_cuda, epoch, wandb_run)

    print(f"Training time: {time.perf_counter() - start:0.3f}s")

    # Only have the master checkpoint the model
    if args.model_dir and dist.get_rank() == 0:
        args.model_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), args.model_dir / "resnet50_imagenet.pt")

    if wandb_run:
        wandb_run.finish()


if __name__ == '__main__':
    main()
