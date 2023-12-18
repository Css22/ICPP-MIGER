import torch
import torch.nn as nn
import time
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Parameters
lr = 0.001
batch_size = 32
epochs = 1



# Training function
def train(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    for inputs, targets in dataloader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

# Main training loop
result = 0
def SqueezeNet_entry():
    # CIFAR-10 data loaders
    transform = transforms.Compose([
        transforms.Resize(224),  # SqueezeNet expects 224x224 input size
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  
    ])
    path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/offline/data/CIFAR10'

    train_dataset = datasets.CIFAR10(root=path, train=True, transform=transform, download=True)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

    model = models.squeezenet1_1(pretrained=False, num_classes=10).to(device)  # Using SqueezeNet 1.1 version
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        start_time = time.time()
        train_loss = train(model, train_loader, criterion, optimizer, device)
        # print(f"Epoch [{epoch + 1}/{epochs}] Loss: {train_loss:.4f}")
        result = time.time() - start_time
    return result