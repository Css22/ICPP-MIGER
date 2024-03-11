import torch
import torch.nn as nn
import torch.optim as optim
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = nn.Linear(10, 5).to(device)
input_data = torch.randn(32, 10).to(device)
# output = model(input_data)

