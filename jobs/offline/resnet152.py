import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import time
path = '/data/zbw/MIG/MIG/ATC-MIG/jobs/offline/data/CIFAR10'
# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 数据预处理
transform = transforms.Compose([
    transforms.Resize(224),  # 将 CIFAR-10 的 32x32 图像上采样到 224x224，以适配 ResNet50
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])



# 定义模型、损失函数和优化器

def resnet152_entry(epoch, initialize, item):
    # 加载数据
    trainset = torchvision.datasets.CIFAR10(root=path, train=True,
                                        download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=32,
                                          shuffle=False, num_workers=2)

    # testset = torchvision.datasets.CIFAR10(root=path, train=False,
    #                                    download=True, transform=transform)
    # testloader = torch.utils.data.DataLoader(testset, batch_size=32,
    #                                      shuffle=False, num_workers=2)
    model = torchvision.models.resnet152(pretrained=False, num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    # 训练模型
    num_epochs = epoch
    result = 0
    if initialize == num_epochs:
        return 0
    for epoch in range(initialize, num_epochs):
        item[0] = epoch
        model.train()
        start_time = time.time()
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(trainloader):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        result = time.time() - start_time
    return result
