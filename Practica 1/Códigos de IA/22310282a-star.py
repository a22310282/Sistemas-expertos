# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 21:22:04 2025

@author: marqu
"""

import heapq
import matplotlib.pyplot as plt
import numpy as np

# Función heurística: Distancia de Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Función para graficar el camino encontrado
def plot_path(grid, path, start, goal, title):
    grid = np.array(grid)
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap='Greys')

    path_x, path_y = zip(*path)
    plt.plot(path_y, path_x, color='blue', linewidth=2, label='Path')

    plt.scatter(start[1], start[0], color='green', s=200, label='Start')
    plt.scatter(goal[1], goal[0], color='red', s=200, label='Goal')

    plt.legend(loc='upper right')
    plt.title(title)
    plt.grid(True)
    plt.show()

# Implementación del algoritmo A*
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current
    return None

# Definición de mapas con sus respectivos puntos de inicio y destino
maps = [
    {"grid": [ [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
               [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
               [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
     "start": (0, 0), "goal": (9, 9)},
    
    {"grid": [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
               [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
     "start": (2, 7), "goal": (8, 2)},
    
    {"grid": [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
               [0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
     "start": (2, 7), "goal": (8, 2)}
]

# Ejecución del algoritmo en cada mapa
for i, mapa in enumerate(maps):
    print(f"Mapa {i+1}")
    path = a_star(mapa["grid"], mapa["start"], mapa["goal"])
    if path:
        print("Camino encontrado:")
        plot_path(mapa["grid"], path, mapa["start"], mapa["goal"], f"Mapa {i+1}")
    else:
        print("No hay camino")
    
    