# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 15:03:42 2025

@author: marqu
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# Transformaciones: Normalización y aumento de datos
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),  # Augmentation
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465),
                         (0.2023, 0.1994, 0.2010))
])

# Cargar el dataset CIFAR-10
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=100,
                                         shuffle=False, num_workers=2)

# Definir la red neuronal
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv_block = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),  # [B, 3, 32, 32] → [B, 32, 32, 32]
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1), # → [B, 64, 32, 32]
            nn.ReLU(),
            nn.MaxPool2d(2, 2),              # → [B, 64, 16, 16]

            nn.Conv2d(64, 128, 3, padding=1), # → [B, 128, 16, 16]
            nn.ReLU(),
            nn.MaxPool2d(2, 2)               # → [B, 128, 8, 8]
        )
        self.fc_block = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 10)
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.fc_block(x)
        return x

# Inicializar red, pérdida y optimizador
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

# Entrenamiento de la red
for epoch in range(10):  # 10 épocas
    running_loss = 0.0
    net.train()
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data[0].to(device), data[1].to(device)
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch {epoch+1} - Loss: {running_loss/len(trainloader):.4f}")

# Evaluación del modelo
net.eval()
correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data[0].to(device), data[1].to(device)
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Precisión en el conjunto de prueba: {100 * correct / total:.2f}%')