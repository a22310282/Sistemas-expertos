# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 15:22:52 2025

@author: marqu
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.array([-5,-4,-3,-2,-1,0,1,2,3,4,5])
y = np.array([-10,-8,-6,-4,-2,0,2,4,6,8,10])
w1 = np.arange(-10,11)
Errores = []

for W1  in w1:    
    y_est = W1*x
    n = len(x)
    Y = (y-y_est)**2
    Prom = np.sum(Y)
    Error = Prom/(2*n)
    Errores.append(Error)

print(Errores)

plt.plot(w1,Errores)
plt.xlabel("W1")
plt.ylabel("Error")
plt.title("W vs Error")
