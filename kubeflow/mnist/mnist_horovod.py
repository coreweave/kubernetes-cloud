import argparse
import time
from pathlib import Path

import horovod.torch as hvd
import torch.multiprocessing as mp
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data.distributed
from filelock import FileLock
from packaging import version
from torch.cuda.amp import GradScaler
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def train_mixed_precision(model: Net,
                          train_sampler: DistributedSampler,
                          train_loader: DataLoader,
                          optimizer: hvd.DistributedOptimizer,
                          epoch: int,
                          log_interval: int,
                          use_cuda: bool,
                          scaler: GradScaler) -> None:
    model.train()
    # Set epoch to sampler for shuffling.
    train_sampler.set_epoch(epoch)
    for batch_idx, (data, target) in enumerate(train_loader):
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        with torch.cuda.amp.autocast():
            output = model(data)
            loss = F.nll_loss(output, target)

        scaler.scale(loss).backward()
        # Make sure all async allreduces are done
        optimizer.synchronize()
        # In-place unscaling of all gradients before weights update
        scaler.unscale_(optimizer)
        with optimizer.skip_synchronize():
            scaler.step(optimizer)
        # Update scaler in case of overflow/underflow
        scaler.update()

        if batch_idx % log_interval == 0:
            # Use train_sampler to determine the number of examples in this worker's partition.
            processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tLoss: {loss.item():.6f}\tLoss Scale: {scaler.get_scale()}')


def train_epoch(model: Net,
                train_sampler: DistributedSampler,
                train_loader: DataLoader,
                optimizer: hvd.DistributedOptimizer,
                epoch: int,
                log_interval: int,
                use_cuda: bool) -> None:
    model.train()
    # Set epoch to sampler for shuffling.
    train_sampler.set_epoch(epoch)
    for batch_idx, (data, target) in enumerate(train_loader):
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            # Use train_sampler to determine the number of examples in this worker's partition.
            processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tLoss: {loss.item():.6f}')


def test(model: Net,
         test_sampler: DistributedSampler,
         test_loader: DataLoader,
         use_cuda: bool) -> None:
    model.eval()
    test_loss = 0.
    test_accuracy = 0.
    for data, target in test_loader:
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        output = model(data)
        # sum up batch loss
        test_loss += F.nll_loss(output, target, size_average=False).item()
        # get the index of the max log-probability
        pred = output.data.max(1, keepdim=True)[1]
        test_accuracy += pred.eq(target.data.view_as(pred)).cpu().float().sum()

    # Use test_sampler to determine the number of examples in this worker's partition.
    test_loss /= len(test_sampler)
    test_accuracy /= len(test_sampler)

    # Average metric values across workers.
    test_loss = metric_average(test_loss, 'avg_loss')
    test_accuracy = metric_average(test_accuracy, 'avg_accuracy')

    # Horovod: print output only on first rank.
    if hvd.rank() == 0:
        print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {100. * test_accuracy:.2f}%\n')


def metric_average(val: float, name: str) -> float:
    tensor = torch.tensor(val)
    avg_tensor = hvd.allreduce(tensor, name=name)
    return avg_tensor.item()


def get_args() -> argparse.Namespace:
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=42, metavar='S',
                        help='random seed (default: 42)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--fp16-allreduce', action='store_true', default=False,
                        help='use fp16 compression during allreduce')
    parser.add_argument('--use-mixed-precision', action='store_true', default=False,
                        help='use mixed precision for training')
    parser.add_argument('--use-adasum', action='store_true', default=False,
                        help='use adasum algorithm to do reduction')
    parser.add_argument('--gradient-predivide-factor', type=float, default=1.0,
                        help='apply gradient predivide factor in optimizer (default: 1.0)')
    parser.add_argument('--data-dir', default=Path('./data'), type=Path,
                        help='location of the training dataset in the local filesystem (will be downloaded if needed)')
    parser.add_argument('--model-dir', default=None, type=Path,
                        help="Location to save the model checkpoint when training is finished.")

    args = parser.parse_args()
    args.cuda = not args.no_cuda and torch.cuda.is_available()
    return args


def main() -> None:
    args = get_args()

    # Horovod: initialize library.
    hvd.init()
    torch.manual_seed(args.seed)

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

    # Horovod: limit # of CPU threads to be used per worker.
    torch.set_num_threads(1)

    kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}
    # When supported, use 'forkserver' to spawn dataloader workers instead of 'fork' to prevent
    # issues with Infiniband implementations that are not fork-safe
    if (kwargs.get('num_workers', 0) > 0 and hasattr(mp, '_supports_context') and
            mp._supports_context and 'forkserver' in mp.get_all_start_methods()):
        kwargs['multiprocessing_context'] = 'forkserver'

    # Whoever gets here first will get the lock and download the dataset
    args.data_dir.mkdir(parents=True, exist_ok=True)
    dataset_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    with FileLock(args.data_dir / ".horovod_lock"):
        train_dataset = datasets.MNIST(args.data_dir, train=True, download=True, transform=dataset_transform)

    # Use DistributedSampler to partition the training data.
    train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, sampler=train_sampler, **kwargs)

    # Use DistributedSampler to partition the test data.
    test_dataset = datasets.MNIST(args.data_dir, train=False, transform=dataset_transform)
    test_sampler = DistributedSampler(test_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    test_loader = DataLoader(test_dataset, batch_size=args.test_batch_size, sampler=test_sampler, **kwargs)

    model = Net()

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

    start = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        if args.use_mixed_precision:
            train_mixed_precision(model,
                                  train_sampler,
                                  train_loader,
                                  optimizer,
                                  epoch,
                                  args.log_interval,
                                  args.cuda,
                                  scaler)
        else:
            train_epoch(model,
                        train_sampler,
                        train_loader,
                        optimizer,
                        epoch,
                        args.log_interval,
                        args.cuda)
        # Keep test in full precision since computation is relatively light.
        test(model, test_sampler, test_loader, args.cuda)

    print(f"Took {time.perf_counter() - start:0.3f}s")

    if args.model_dir and hvd.rank() == 0:
        args.model_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), args.model_dir / "mnist_cnn.pt")


if __name__ == '__main__':
    main()
