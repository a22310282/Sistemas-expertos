# -*- coding: utf-8 -*-
"""
Created on Sat May 17 20:36:50 2025

@author: marqu
"""
#Perceptron multicapa
import numpy as np
import matplotlib.pyplot as plt

# Datos XOR
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

# Activación sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Inicialización
def init_weights(input_size, hidden_size, output_size):
    W1 = np.random.randn(input_size, hidden_size)
    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, output_size)
    b2 = np.zeros((1, output_size))
    return W1, b1, W2, b2

# Entrenamiento
def train_xor(X, y, hidden_size=4, lr=0.1, epochs=10000):
    W1, b1, W2, b2 = init_weights(2, hidden_size, 1)
    losses = []

    for epoch in range(epochs):
        # Forward
        Z1 = X @ W1 + b1
        A1 = sigmoid(Z1)
        Z2 = A1 @ W2 + b2
        A2 = sigmoid(Z2)

        # Error
        loss = np.mean((A2 - y) ** 2)
        losses.append(loss)

        # Backprop
        dA2 = 2 * (A2 - y)
        dZ2 = dA2 * sigmoid_derivative(Z2)
        dW2 = A1.T @ dZ2
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = dZ2 @ W2.T
        dZ1 = dA1 * sigmoid_derivative(Z1)
        dW1 = X.T @ dZ1
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        # Actualizar pesos
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2

    return losses, W1, b1, W2, b2

# Entrenar
losses, *_ = train_xor(X, y)

# Graficar pérdida
plt.plot(losses)
plt.xlabel("Epoch")
plt.ylabel("Error cuadrático")
plt.title("Error durante entrenamiento XOR")
plt.grid()
plt.show()