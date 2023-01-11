import argparse
import time
from pathlib import Path
from typing import Tuple, Optional

import horovod.torch as hvd
import torch.multiprocessing as mp
import torch.nn as nn
import torch.optim as optim
import torch.utils.data.distributed
import wandb
from packaging import version
from torch.cuda.amp import GradScaler
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torchvision import transforms, models
from torchvision.datasets import ImageFolder
from torchvision.transforms.functional import InterpolationMode


def train_mixed_precision(model: models.resnet50,
                          criterion: nn.CrossEntropyLoss,
                          train_sampler: DistributedSampler,
                          train_loader: DataLoader,
                          optimizer: hvd.DistributedOptimizer,
                          epoch: int,
                          log_interval: int,
                          use_cuda: bool,
                          scaler: GradScaler,
                          wandb_run: Optional[wandb.run]) -> None:
    model.train()
    # Set epoch to sampler for shuffling.
    train_sampler.set_epoch(epoch)
    for batch_idx, (data, target) in enumerate(train_loader):
        step_start = time.perf_counter()
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        with torch.cuda.amp.autocast():
            output = model(data)
            loss = criterion(output, target)

        scaler.scale(loss).backward()
        # Make sure all async allreduces are done
        optimizer.synchronize()
        # In-place unscaling of all gradients before weights update
        scaler.unscale_(optimizer)
        with optimizer.skip_synchronize():
            scaler.step(optimizer)
        # Update scaler in case of overflow/underflow
        scaler.update()

        if wandb_run:
            step_time = time.perf_counter() - step_start
            global_step = (epoch - 1) * len(train_loader) + batch_idx
            wandb_info = {"train/loss": loss.item(),
                          "train/epoch": epoch,
                          "train/step": global_step,
                          "train/samples_seen": global_step * len(data),
                          "perf/rank_samples_per_second": len(data) / step_time}
            wandb_run.log(wandb_info, step=global_step)

        if batch_idx % log_interval == 0:
            # Use train_sampler to determine the number of examples in this worker's partition.
            processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tLoss: {loss.item():.6f}\tLoss Scale: {scaler.get_scale()}')


def train_epoch(model: models.resnet50,
                criterion: nn.CrossEntropyLoss,
                train_sampler: DistributedSampler,
                train_loader: DataLoader,
                optimizer: hvd.DistributedOptimizer,
                epoch: int,
                log_interval: int,
                use_cuda: bool,
                wandb_run: Optional[wandb.run]) -> None:
    model.train()
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

        if batch_idx % log_interval == 0:
            # Use train_sampler to determine the number of examples in this worker's partition.
            processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tLoss: {loss.item():.6f}')


def test(model: models.resnet50,
         criterion: nn.CrossEntropyLoss,
         test_sampler: DistributedSampler,
         test_loader: DataLoader,
         use_cuda: bool,
         epoch: int,
         wandb_run: Optional[wandb.run]) -> None:
    model.eval()
    test_loss = 0
    acc1 = 0
    acc5 = 0

    with torch.inference_mode():
        for data, target in test_loader:
            if use_cuda:
                data, target = data.cuda(), target.cuda()
            output = model(data)
            # sum up batch loss
            test_loss += criterion(output, target).item()

            batch_acc1, batch_acc5 = accuracy(output, target)
            acc1 += batch_acc1.item()
            acc5 += batch_acc5.item()

    # Use test_sampler to determine the number of examples in this worker's partition.
    test_loss /= len(test_sampler)
    acc1 /= len(test_sampler)
    acc5 /= len(test_sampler)

    # Average metric values across workers.
    test_loss = metric_average(test_loss, 'avg_loss')
    acc1 = metric_average(acc1, 'avg_acc1')
    acc5 = metric_average(acc5, 'avg_acc5')

    if wandb_run:
        wandb_info = {"test/loss": test_loss,
                      "test/epoch": epoch,
                      "test/acc1": acc1,
                      "test/acc5": acc5}
        wandb_run.log(wandb_info)

    # Horovod: print output only on first rank.
    if hvd.rank() == 0:
        print(f'Test Epoch: {epoch}\tloss={test_loss:.4f}\tAcc@1={acc1:.3f}\tAcc@5={acc5:.3f}')


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


def metric_average(val: float, name: str) -> float:
    tensor = torch.tensor(val)
    avg_tensor = hvd.allreduce(tensor, name=name)
    return avg_tensor.item()


def load_data(train_dir: Path,
              test_dir: Path,
              args: argparse.Namespace) -> Tuple[ImageFolder, ImageFolder, DistributedSampler, DistributedSampler]:
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
    train_dataset = ImageFolder(str(train_dir), train_transforms)

    test_transforms = transforms.Compose([
        transforms.Resize(args.val_resize_size, interpolation=interpolation),
        transforms.CenterCrop(args.val_crop_size),
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
        transforms.Normalize(mean=mean, std=std),
    ])
    test_dataset = ImageFolder(str(test_dir), test_transforms)

    train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    test_sampler = DistributedSampler(test_dataset, num_replicas=hvd.size(), rank=hvd.rank())

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
                                                                         args)

    kwargs = {'num_workers': args.workers, 'pin_memory': True} if args.cuda else {}
    # When supported, use 'forkserver' to spawn dataloader workers instead of 'fork' to prevent
    # issues with Infiniband implementations that are not fork-safe
    if (kwargs.get('num_workers', 0) > 0 and hasattr(mp, '_supports_context') and mp._supports_context and
            'forkserver' in mp.get_all_start_methods()):
        kwargs['multiprocessing_context'] = 'forkserver'

    train_loader = DataLoader(train_dataset,
                              batch_size=args.batch_size,
                              sampler=train_sampler,
                              **kwargs)
    test_loader = DataLoader(test_dataset,
                             batch_size=args.batch_size,
                             sampler=test_sampler,
                             **kwargs)

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
