import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
class UNet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UNet, self).__init__()

        def double_conv(in_channels, out_channels):
            return nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
                nn.ReLU(inplace=True)
            )

        self.dconv_down1 = double_conv(in_channels, 64)
        self.dconv_down2 = double_conv(64, 128)
        self.dconv_down3 = double_conv(128, 256)
        self.dconv_down4 = double_conv(256, 512)

        self.maxpool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)

        self.dconv_up3 = double_conv(256 + 512, 256)
        self.dconv_up2 = double_conv(128 + 256, 128)
        self.dconv_up1 = double_conv(128 + 64, 64)

        self.conv_last = nn.Conv2d(64, out_channels, 1)

    def forward(self, x):
        conv1 = self.dconv_down1(x)
        x = self.maxpool(conv1)

        conv2 = self.dconv_down2(x)
        x = self.maxpool(conv2)

        conv3 = self.dconv_down3(x)
        x = self.maxpool(conv3)

        x = self.dconv_down4(x)

        x = self.upsample(x)
        x = torch.cat([x, conv3], dim=1)
        x = self.dconv_up3(x)

        x = self.upsample(x)
        x = torch.cat([x, conv2], dim=1)
        x = self.dconv_up2(x)

        x = self.upsample(x)
        x = torch.cat([x, conv1], dim=1)
        x = self.dconv_up1(x)

        return self.conv_last(x)



# Parameters
lr = 0.001
batch_size = 32
epochs = 1

# Dataset & DataLoader
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])
def target_transform(target):
    return torch.full((128, 128), target, dtype=torch.int64)


# Training function
def train_epoch(model, dataloader, criterion, optimizer):

    model.train()
    total_loss = 0
    for inputs, targets in dataloader:
        inputs, targets = inputs.cuda(), targets.cuda()
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

# Training loop
def unet_entry(epoch, initialize, item):
    path = '/data/zbw/MIG/MIG/ATC-MIG/jobs/offline/data/CIFAR10'

    train_dataset = datasets.CIFAR10(root=path, train=True, transform=transform, download=True, target_transform=target_transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
    model = UNet(in_channels=3, out_channels=10).cuda()  # Here, out_channels = number of classes in CIFAR10
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    result = 0

    epochs = epoch
    if initialize == epochs:
        return 0
    
    for epoch in range(initialize, epochs):
        item[0] = epoch
        start_time = time.time()
        train_loss = train_epoch(model, train_loader, criterion, optimizer)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {train_loss:.4f}")
        result = time.time() - start_time
    return result
