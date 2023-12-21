import torch
import torchvision
import torchvision.transforms as T
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 加载 DeepLabV3 模型

def train_one_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    
    for images, targets in dataloader:
        targets = targets.squeeze(1)
        images, targets = images.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)['out']
        loss = criterion(outputs, targets.long())
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)

def validate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    
    with torch.no_grad():
        for images, targets in dataloader:
            images, targets = images.to(device), targets.to(device)
            outputs = model(images)['out']
            loss = criterion(outputs, targets.long())
            total_loss += loss.item()

    return total_loss / len(dataloader)

def deeplabv3_entry(epoch, initialize, item):
    transform = T.Compose([
        T.Resize((256, 256)),
        T.ToTensor(),
        T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]),
    ])

    target_transform = T.Compose([
        T.Resize((256, 256), interpolation=T.InterpolationMode.NEAREST),
        T.ToTensor()
    ])
    path = '/data/zbw/MIG/MIG/ATC-MIG/jobs/offline/data/'
 
    train_dataset = torchvision.datasets.VOCSegmentation(
        root=path, year='2012', image_set='train', download=True, transform=transform, target_transform=target_transform
    )

    val_dataset = torchvision.datasets.VOCSegmentation(
        root=path, year='2012', image_set='val', download=True, transform=transform, target_transform=target_transform
    )

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=False, num_workers=4)


    model = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=False, num_classes=21).to(device)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    result = 0 
    num_epochs = epoch
    if initialize == num_epochs:
        return 0
    
    for epoch in range(initialize, num_epochs):
        item[0] = epoch
        start_time = time.time()
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        result = time.time() - start_time
    return result

