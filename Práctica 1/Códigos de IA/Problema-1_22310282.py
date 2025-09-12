# -*- coding: utf-8 -*-
"""
Created on Sat May 17 20:25:56 2025

@author: marqu
"""
#Red neuronal
import numpy as np
import matplotlib.pyplot as plt

# Generar datos
np.random.seed(0)
n_samples = 1000
X = np.random.rand(n_samples, 4)
y = np.sin(X[:, 0]) + np.log(X[:, 1] + 1) + X[:, 2]**2 - np.sqrt(X[:, 3])
y = y.reshape(-1, 1)

# Inicializar pesos
def init_weights(input_size, hidden_size, output_size):
    W1 = np.random.randn(input_size, hidden_size)
    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, output_size)
    b2 = np.zeros((1, output_size))
    return W1, b1, W2, b2

# Activación ReLU
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

# Red neuronal simple (1 capa oculta)
def train_nn(X, y, hidden_size=10, lr=0.01, epochs=500):
    input_size = X.shape[1]
    output_size = 1
    W1, b1, W2, b2 = init_weights(input_size, hidden_size, output_size)
    losses = []

    for epoch in range(epochs):
        # Forward
        Z1 = X @ W1 + b1
        A1 = relu(Z1)
        Z2 = A1 @ W2 + b2
        y_pred = Z2

        # Loss
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)

        # Backprop
        dZ2 = 2 * (y_pred - y) / y.shape[0]
        dW2 = A1.T @ dZ2
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = dZ2 @ W2.T
        dZ1 = dA1 * relu_derivative(Z1)
        dW1 = X.T @ dZ1
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        # Update
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2

    return losses, W1, b1, W2, b2

# Entrenar
losses, *_ = train_nn(X, y)

# Gráfica
plt.plot(losses)
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Error en la aproximación de la función")
plt.grid()
plt.show()