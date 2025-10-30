# maze_search.py

import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import heapq

# ---- Step 1: Create the Maze ----
# 0 = free cell, 1 = wall
maze = np.array([
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0]
])

start = (0, 0)   # Top-left corner
goal = (4,4)    # Bottom-right corner

# ---- Step 2: Visualize Maze ----
def draw_maze(maze, path=None, title="Maze Search"):
    plt.imshow(maze, cmap="gray_r")
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, color='red', linewidth=2, marker='o')
    plt.title(title)
    plt.show()

# ---- Step 3: Get Neighbors ----
def get_neighbors(pos, maze):
    neighbors = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right
    for d in directions:
        new_pos = (pos[0] + d[0], pos[1] + d[1])
        if (0 <= new_pos[0] < maze.shape[0]) and (0 <= new_pos[1] < maze.shape[1]):
            if maze[new_pos] == 0:
                neighbors.append(new_pos)
    return neighbors

# ---- Step 4: BFS (Uninformed Search) ----
def bfs(maze, start, goal):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in get_neighbors(node, maze):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

# ---- Step 5: DFS (Uninformed Search) ----
def dfs(maze, start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in get_neighbors(node, maze):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None

# ---- Step 6: A* (Informed Search) ----
def heuristic(a, b):
    # Manhattan distance
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(maze, start, goal):
    open_list = [(heuristic(start, goal), 0, [start])]
    visited = set()
    while open_list:
        est_total, cost_so_far, path = heapq.heappop(open_list)
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in get_neighbors(node, maze):
                new_cost = cost_so_far + 1
                est = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (est, new_cost, path + [neighbor]))
    return None

# ---- Step 7: Run and Visualize ----
print("BFS Path:", bfs(maze, start, goal))
print("DFS Path:", dfs(maze, start, goal))
print("A* Path:", astar(maze, start, goal))

# ---- Step 8: Visualizations ----
draw_maze(maze, bfs(maze, start, goal), "BFS Path")
draw_maze(maze, dfs(maze, start, goal), "DFS Path")
draw_maze(maze, astar(maze, start, goal), "A* Path")
