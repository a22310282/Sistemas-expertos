# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 15:02:42 2025

@author: marqu
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Cargar el dataset MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalizar las imágenes (0 a 1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# Aplanar imágenes: de 28x28 a 784
x_train = x_train.reshape((-1, 28*28))
x_test = x_test.reshape((-1, 28*28))

# Crear el modelo
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 clases para dígitos 0–9
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(x_train, y_train, epochs=5, batch_size=32,
                    validation_split=0.1)

# Evaluar el modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'\nPrecisión en el conjunto de prueba: {test_acc:.4f}')

# Mostrar una predicción de ejemplo
import numpy as np
predictions = model.predict(x_test)
plt.imshow(x_test[0].reshape(28,28), cmap='gray')
plt.title(f"Predicción: {np.argmax(predictions[0])}")
plt.axis('off')
plt.show()