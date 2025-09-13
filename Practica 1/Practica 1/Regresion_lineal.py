import numpy as np
import matplotlib.pyplot as plt

# Datos simulados (ejemplo)
# x = tazas de café
# y = horas de sueño
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([8, 7.5, 6.5, 6, 5.5, 5])

# Inicializamos parámetros
m = 0.0  # pendiente
b = 0.0  # intercepto
alpha = 0.01  # tasa de aprendizaje
epochs = 1000 # número de iteraciones

n = len(x)

# Gradiente descendente
for _ in range(epochs):
    y_pred = m*x + b
    error = y_pred - y
    
    # Actualización de parámetros
    m -= alpha * (2/n) * np.dot(error, x)
    b -= alpha * (2/n) * np.sum(error)

print(f"Modelo entrenado: y = {m:.2f}x + {b:.2f}")

# Predicción
x_test = np.linspace(0,5,50)
y_test = m*x_test + b

# Visualización
plt.scatter(x, y, color='blue', label="Datos reales")
plt.plot(x_test, y_test, color='red', label="Regresión lineal")
plt.xlabel("Tazas de café por día")
plt.ylabel("Horas de sueño")
plt.title("Relación café vs. sueño")
plt.legend()
plt.grid(True)
plt.show()