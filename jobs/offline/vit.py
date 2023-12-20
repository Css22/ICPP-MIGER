import time
import timm
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
# from torchvision.models import vit_large_patch16_224 as vit_large

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/offline/data/CIFAR10'



# Training loop
def vit_entry(epoch):
    # Data loading and preprocessing
    transform = transforms.Compose(
        [transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainset = torchvision.datasets.CIFAR10(root=path, train=True,
                                        download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=32,
                                          shuffle=True, num_workers=2)


# Model
    model = timm.create_model('vit_large_patch16_224', pretrained=False, num_classes=10)
    model = model.cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    item = 0
    result = 0

    num_epochs = epoch
    for epoch in range(epoch):
        running_loss = 0.0
        start_time = time.time()
        for i, data in enumerate(trainloader, 0):
    
            inputs, labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 100 == 0:
                item = item + 1
                result = time.time() - start_time
                start_time = time.time()
                running_loss = 0.0
                if item == 2:
                    break
    return result
