import torch
T=torch.load("model.pth",map_location=torch.device('cpu'))
print(T)
