import numpy as np
import matplotlib.pyplot as plt

# Entradas (bias, clima, energía)
# x0 = bias
x0 = [1,1,1,1]
x1 = [ 1, 1,-1,-1]   # clima
x2 = [ 1,-1, 1,-1]   # energía

# Salida deseada
# 1 = salir a correr, -1 = quedarse en casa
y = [ 1,-1,-1,-1]

# Pesos iniciales
w = [0.5,0.5,0.5]
TazaDeAprendizaje = 0.5
errores = []

def sign(z):
    return 1 if z > 0 else -1

# Entrenamiento
while True:
    total_error = 0
    for i in range(len(y)):
        x = np.array([x0[i],x1[i],x2[i]])
        y_est = sign(np.dot(w,x))
        error = y[i] - y_est
        w += TazaDeAprendizaje * error * x
        total_error += abs(error)
        errores.append(total_error)
    
    if total_error == 0:
        print("El perceptrón aprendió correctamente:",total_error)
        break

# Visualización
for i in range(len(y)):
    if y[i] == 1:
        plt.scatter(x1[i], x2[i], color='blue', label='Salir a correr' if i == 0 else "")
    else:
        plt.scatter(x1[i], x2[i], color='red', label='Quedarse en casa' if i == 1 else "")

plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.xlabel("Clima (1=soleado, -1=lluvioso)")
plt.ylabel("Energía (1=alta, -1=baja)")
plt.legend()
plt.grid(True)
plt.show()