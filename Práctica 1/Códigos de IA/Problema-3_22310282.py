# -*- coding: utf-8 -*-
"""
Created on Sat May 17 20:47:13 2025

@author: marqu
"""
#Clasificación binaria
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

#1. Cargar el dataset
tic_tac_toe_endgame = fetch_ucirepo(id=101)
X = tic_tac_toe_endgame.data.features
y = tic_tac_toe_endgame.data.targets

#2. Preprocesamiento
# Codificación de variables categóricas
X = X.apply(LabelEncoder().fit_transform)

#Codificar salida (target)
y = y.iloc[:, 0]  #Asegurar que es una serie
y = LabelEncoder().fit_transform(y)  #'positive' → 1, 'negative' → 0

#División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

#3. Entrenamiento
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#4. Predicciones
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

#5. Evaluación
print("\n== Reporte de Clasificación ==")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

#6. Gráfica: Error absoluto
plt.figure(figsize=(8, 4))
plt.plot(np.abs(y_test - y_pred), label="Error absoluto", linestyle='--', marker='o')
plt.title("Error absoluto por muestra")
plt.xlabel("Índice de muestra")
plt.ylabel("|y - ŷ|")
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()

#7. Gráfica: Salida real vs estimada
plt.figure(figsize=(10, 4))
plt.plot(y_test[:100].values, label="Target real", marker='o', linestyle='--')
plt.plot(y_pred[:100], label="Predicción", marker='x')
plt.title("Salida real vs salida estimada (primeras 100 muestras)")
plt.xlabel("Índice")
plt.ylabel("Clase (0=negativo, 1=positivo)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#8. Matriz de confusión
plt.figure(figsize=(6, 5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues")
plt.title("Matriz de Confusión")
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.tight_layout()
plt.show()