# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 19:22:52 2025

@author: marqu
"""

import numpy as np
import matplotlib.pyplot as plt

#Entradas
x0 = [1,1,1,1]
x1 = [-1,1,-1,1]
x2 = [1,-1,-1,1]
#Salida
y = [-1,-1,-1,1]

w = [1,1,1]
i = 0
TazaDeAprendizaje = 1/2

errores =[]

def sign(z):
    return 1 if z > 0 else -1

while True:
    total_error = 0
    for i in range(len(y)):
        x = np.array([x0[i],x1[i],x2[i]])
        y_est = sign(np.dot(w,x))
        error = y[i]-y_est
        w += TazaDeAprendizaje * error * x
        total_error += abs(error)
        errores.append(total_error)
    
    if total_error == 0:
        print("El perceptrón aprendió correctamente:",total_error)
        break

for i in range(len(y)):
    if y[i] == 1:
        plt.scatter(x1[i], x2[i], color='blue', label='Clase 1' if i == 3 else "")
    else:
        plt.scatter(x1[i], x2[i], color='red', label='Clase -1' if i == 0 else "")

plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.grid(True)
        
            