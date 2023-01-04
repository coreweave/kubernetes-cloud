import argparse
import os
from pathlib import Path

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from filelock import FileLock
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader, RandomSampler
from torch.utils.data.distributed import DistributedSampler
from torchvision import datasets, transforms

WORLD_SIZE = int(os.environ.get('WORLD_SIZE', 1))


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


def train(args: argparse.Namespace,
          model: Net,
          device: torch.device,
          train_loader: DataLoader,
          train_sampler: DistributedSampler,
          optimizer: optim.Optimizer,
          epoch: int,
          writer: SummaryWriter) -> None:
    model.train()
    if is_distributed():
        # Set epoch to sampler for shuffling.
        train_sampler.set_epoch(epoch)
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            num_processed_samples = batch_idx * len(data)
            completion_percentage = 100. * batch_idx / len(train_loader)
            print(f'Train Epoch: {epoch} [{num_processed_samples}/{len(train_sampler)} ({completion_percentage:.0f}%)]'
                  f'\tloss={loss.item():.4f}')
            niter = epoch * len(train_loader) + batch_idx
            writer.add_scalar('loss', loss.item(), niter)


def test(model: Net,
         device: torch.device,
         test_loader: DataLoader,
         test_sampler: DistributedSampler,
         epoch: int,
         writer: SummaryWriter):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_sampler)
    accuracy = float(correct) / len(test_sampler)
    print(f'\n{accuracy=}\n')
    writer.add_scalar('accuracy', accuracy, epoch)


def should_distribute() -> bool:
    return dist.is_available() and WORLD_SIZE > 1


def is_distributed() -> bool:
    return dist.is_available() and dist.is_initialized()


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
        print('Using CUDA')

    writer = SummaryWriter(args.log_dir)

    device = torch.device("cuda" if use_cuda else "cpu")

    if should_distribute():
        print('Using distributed PyTorch with {} backend'.format(args.backend))
        dist.init_process_group(backend=args.backend)
        print(f"Current rank: {dist.get_rank()}, total world size:  {dist.get_world_size()}")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    # Whoever gets here first will get the lock and download the dataset
    args.data_dir.mkdir(parents=True, exist_ok=True)
    data_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    with FileLock(args.data_dir / ".pytorch_lock"):
        train_dataset = datasets.MNIST(args.data_dir, train=True, download=True, transform=data_transform)

    test_dataset = datasets.MNIST(args.data_dir, train=False, transform=data_transform)

    if is_distributed():
        train_sampler = DistributedSampler(train_dataset, num_replicas=dist.get_world_size(), rank=dist.get_rank())
        test_sampler = DistributedSampler(test_dataset, num_replicas=dist.get_world_size(), rank=dist.get_rank())
    else:
        train_sampler = RandomSampler(train_dataset)
        test_sampler = RandomSampler(test_dataset)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, sampler=train_sampler, **kwargs)
    test_loader = DataLoader(test_dataset, batch_size=args.test_batch_size, sampler=test_sampler, **kwargs)

    model = Net().to(device)

    if is_distributed():
        model = nn.parallel.DistributedDataParallel(model)

    lr_scaler = dist.get_world_size() if is_distributed() else 1
    optimizer = optim.SGD(model.parameters(), lr=args.lr * lr_scaler, momentum=args.momentum)

    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, train_sampler, optimizer, epoch, writer)
        test(model, device, test_loader, test_sampler, epoch, writer)

    # Only have the master checkpoint the model
    if args.model_dir and dist.get_rank() == 0:
        args.model_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), args.model_dir / "mnist_cnn.pt")


if __name__ == '__main__':
    main()
