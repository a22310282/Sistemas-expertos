# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 20:42:09 2025

@author: marq
"""

import itertools
from heapq import heappush, heappop

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

class Vertex:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

class Edge:
    def __init__(self, distance, vertex):
        self.distance = distance
        self.vertex = vertex

class PriorityQueue:
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.counter = itertools.count()  # unique sequence count

    def __len__(self):
        return len(self.pq)

    def add_task(self, priority, task):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.update_priority(priority, task)
            return
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def update_priority(self, priority, task):
        'Update the priority of a task in place'
        if task in self.entry_finder:
            self.remove_task(task)
        self.add_task(priority, task)

    def remove_task(self, task):
        'Mark an existing task as removed'
        if task in self.entry_finder:
            del self.entry_finder[task]

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task in self.entry_finder:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')

def dijkstra(graph, start, end):
    previous = {v: None for v in graph.adjacency_list.keys()}
    visited = {v: False for v in graph.adjacency_list.keys()}
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0
    queue = PriorityQueue()
    queue.add_task(0, start)

    while len(queue):
        removed_distance, removed = queue.pop_task()
        if visited[removed]:
            continue
        visited[removed] = True

        if removed == end:
            path = []
            while previous[removed]:
                path.append(removed)
                removed = previous[removed]
            path.append(start)
            path.reverse()
            print(f"Shortest distance to {end.value}: {distances[end]}")
            print(f"Path to {end.value}: {path}")
            return distances[end], path

        for edge in graph.adjacency_list[removed]:
            if visited[edge.vertex]:
                continue
            new_distance = removed_distance + edge.distance
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                queue.add_task(new_distance, edge.vertex)
    
    return float("inf"), []

# Create vertices
A = Vertex("A")
B = Vertex("B")
C = Vertex("C")
D = Vertex("D")
E = Vertex("E")
F = Vertex("F")
G = Vertex("G")
Z = Vertex("Z")

# Define adjacency list
adj_list = {
    A: [Edge(2, B), Edge(1, F)],
    B: [Edge(2, A), Edge(2, D), Edge(2, C), Edge(4, E)],
    C: [Edge(2, B), Edge(3, E), Edge(1, Z)],
    D: [Edge(2, B), Edge(4, E), Edge(3, F)],
    E: [Edge(4, B), Edge(3, C), Edge(4, D), Edge(7, G)],
    F: [Edge(1, A), Edge(3, D), Edge(5, G)],
    G: [Edge(7, E), Edge(5, F), Edge(6, Z)],
    Z: [Edge(1, C), Edge(6, G)],
}

# Create graph
my_graph = Graph(adj_list)

# Run Dijkstra's algorithm
dijkstra(my_graph, start=A, end=Z)
