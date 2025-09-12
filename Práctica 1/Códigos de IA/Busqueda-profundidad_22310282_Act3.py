# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:26:20 2025

@author: Usuario
"""

G= {"a":["b","c","g"],"b":["a","d"],"g":["a","b","e"],"c":["e","a","d"],"d":["f","b","c"],"f":["h","d","e"],"e":["c","f","g"],"h":["f"]}

# Nodo raíz del árbol de expansión
V1 = "a"

# Inicialización
Vp = [V1]  # Lista de nodos visitados (V' en el pseudocódigo)
Ep = []  # Lista de aristas del árbol de expansión (E')
W = [V1]  #Profundidad

while W:
    w = W[-1]  # Último nodo agregado a la pila
    put = False  # Para indicar si encontramos un nodo nuevo
    
    for Vk in sorted(G[w]):
        if Vk not in Vp:  # Si el nodo no ha sido visitado
            Ep.append((w, Vk))  # Agregar arista al árbol
            Vp.append(Vk)  # Marcar como nodo visitado
            W.append(Vk)  # Avanzar al nodo
            put = True
            break  # Salimos del bucle para continuar con la profundidad
    
    if not put:  # Si no se encontró nodo nuevo, retrocedemos
        W.pop()

# Resultado final
print("Aristas del árbol de expansión:")
print(Ep)


        