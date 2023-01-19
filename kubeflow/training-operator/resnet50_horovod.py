import argparse
import time
from pathlib import Path

import horovod.torch as hvd
import torch.nn as nn
import torch.optim as optim
import torch.utils.data.distributed
import wandb
from packaging import version
from torch.utils.data import DataLoader
from torchvision import models

from util import train_epoch, train_mixed_precision, test, load_data


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
    parser.add_argument('--fp16-allreduce', action='store_true', default=False,
                        help='use fp16 compression during allreduce')
    parser.add_argument('--use-mixed-precision', action='store_true', default=False,
                        help='use mixed precision for training')
    parser.add_argument('--use-adasum', action='store_true', default=False,
                        help='use adasum algorithm to do reduction')
    parser.add_argument('--gradient-predivide-factor', type=float, default=1.0,
                        help='apply gradient predivide factor in optimizer (default: 1.0)')
    parser.add_argument("--wandb-project", type=str, default=None,
                        help="WandB Project ID to use for this run")
    parser.add_argument("--wandb-run", type=str, default=None,
                        help="WandB run name to use for logging")

    args = parser.parse_args()
    args.cuda = not args.no_cuda and torch.cuda.is_available()
    return args


def main() -> None:
    args = get_args()

    # Horovod: initialize library.
    hvd.init()
    torch.manual_seed(args.seed)

    if args.wandb_project:
        wandb_run = wandb.init(project=args.wandb_project,
                               name=args.wandb_run,
                               config=vars(args),
                               dir=args.log_dir / "wandb",
                               group=args.wandb_run)
    else:
        wandb_run = None

    if args.cuda:
        # Horovod: pin GPU to local rank.
        torch.cuda.set_device(hvd.local_rank())
        torch.cuda.manual_seed(args.seed)
    else:
        if args.use_mixed_precision:
            raise ValueError("Mixed precision is only supported with cuda enabled.")

    if args.use_mixed_precision and version.parse(torch.__version__) < version.parse('1.6.0'):
        raise ValueError("""Mixed precision is using torch.cuda.amp.autocast(),
                            which requires torch >= 1.6.0""")

    train_dataset, test_dataset, train_sampler, test_sampler = load_data(args.data_dir / "train",
                                                                         args.data_dir / "val",
                                                                         args,
                                                                         hvd.size(),
                                                                         hvd.rank())

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

    # By default, Adasum doesn't need scaling up learning rate.
    lr_scaler = hvd.size() if not args.use_adasum else 1

    if args.cuda:
        # Move model to GPU.
        model.cuda()
        # If using GPU Adasum allreduce, scale learning rate by local_size.
        if args.use_adasum and hvd.nccl_built():
            lr_scaler = hvd.local_size()

    # Scale learning rate by lr_scaler.
    optimizer = optim.SGD(model.parameters(), lr=args.lr * lr_scaler, momentum=args.momentum)

    # Horovod: broadcast parameters & optimizer state.
    hvd.broadcast_parameters(model.state_dict(), root_rank=0)
    hvd.broadcast_optimizer_state(optimizer, root_rank=0)

    # Horovod: (optional) compression algorithm.
    compression = hvd.Compression.fp16 if args.fp16_allreduce else hvd.Compression.none

    # Horovod: wrap optimizer with DistributedOptimizer.
    optimizer = hvd.DistributedOptimizer(optimizer,
                                         named_parameters=model.named_parameters(),
                                         compression=compression,
                                         op=hvd.Adasum if args.use_adasum else hvd.Average,
                                         gradient_predivide_factor=args.gradient_predivide_factor)

    if args.use_mixed_precision:
        # Initialize scaler in global scale
        scaler = torch.cuda.amp.GradScaler()

    criterion = nn.CrossEntropyLoss()

    start = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        if args.use_mixed_precision:
            train_mixed_precision(model,
                                  criterion,
                                  train_sampler,
                                  train_loader,
                                  optimizer,
                                  epoch,
                                  args.log_interval,
                                  args.cuda,
                                  scaler,
                                  wandb_run)
        else:
            train_epoch(model,
                        criterion,
                        train_sampler,
                        train_loader,
                        optimizer,
                        epoch,
                        args.log_interval,
                        args.cuda,
                        wandb_run)
        # Keep test in full precision since computation is relatively light.
        test(model, criterion, test_sampler, test_loader, args.cuda, epoch, wandb_run)

    print(f"Took {time.perf_counter() - start:0.3f}s")

    if args.model_dir and hvd.rank() == 0:
        args.model_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), args.model_dir / "resnet50_imagenet.pt")

    if wandb_run:
        wandb_run.finish()


if __name__ == '__main__':
    main()
