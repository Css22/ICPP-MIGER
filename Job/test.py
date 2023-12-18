import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

def load_image(image_path):
    """加载图像并进行预处理"""
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)

def infer(image_path):
    """加载模型并进行推理"""
    # 加载预训练的 ResNet50 模型
    model = resnet50(pretrained=True)
    model.eval()

    # GPU 加速（如果可用）
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 加载并预处理图像
    image_path = image_path.to(device)

    # 推理
    with torch.no_grad():
        output = model(image_path)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)

    # 返回最可能的类别及其概率（这里只返回了概率值）
    return probabilities

# 使用示例
image_path = torch.randn(32,3,224, 224) # 替换为您的图像路径

while True:
    probabilities = infer(image_path)
