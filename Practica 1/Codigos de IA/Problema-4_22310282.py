# -*- coding: utf-8 -*-
"""
Created on Sat May 17 20:51:40 2025

@author: marqu
"""
#Regresión lineal
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

#1. Cargar el dataset
energy_efficiency = fetch_ucirepo(id=242)
X = energy_efficiency.data.features
y = energy_efficiency.data.targets

#Usamos solo "Heating Load" (Y1) como objetivo
y = y.iloc[:, 0]  #Heating Load

#2. División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#3. Modelo de regresión
model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)

#4. Predicciones
y_pred = model.predict(X_test)

#5. Evaluación
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")

#6. Gráfica del error absoluto
plt.figure(figsize=(8, 4))
plt.plot(np.abs(y_test.values - y_pred), marker='o', linestyle='--', label='|y - ŷ|')
plt.title("Error absoluto por muestra")
plt.xlabel("Índice de muestra")
plt.ylabel("Error absoluto")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#7. Target vs Predicción (100 muestras)
plt.figure(figsize=(10, 4))
plt.plot(y_test.values[:100], label="Target real", marker='o')
plt.plot(y_pred[:100], label="Predicción", marker='x')
plt.title("Salida real vs estimada (primeras 100 muestras)")
plt.xlabel("Índice")
plt.ylabel("Heating Load")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#8. Dispersión real vs estimada
plt.figure(figsize=(6, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Heating Load Real")
plt.ylabel("Heating Load Estimada")
plt.title("Dispersión: Target vs Predicción")
plt.grid(True)
plt.tight_layout()
plt.show()