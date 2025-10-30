

# ---- Step 1: Import Libraries ----
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

# ---- Step 2: Create Graph ----
G = nx.Graph()
G.add_edge('Panadura', 'Kalutara', weight=20)
G.add_edge('Panadura', 'Horana', weight=30)
G.add_edge('Horana', 'Kalutara', weight=15)
G.add_edge('Kalutara', 'Colombo', weight=50)
G.add_edge('Horana', 'Colombo', weight=40)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

# ---- Step 3: Convert to adjacency list ----
graph_dict = {node: list(G.neighbors(node)) for node in G.nodes()}

# ---- Step 4: BFS ----
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        elif node not in visited:
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(node)

# ---- Step 5: DFS ----
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        elif node not in visited:
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
            visited.add(node)

print("BFS Path:", bfs(graph_dict, 'Panadura', 'Colombo'))
print("DFS Path:", dfs(graph_dict, 'Panadura', 'Colombo'))

# ---- Step 6: A* Search ----
heuristic = {'Panadura': 70, 'Kalutara': 50, 'Horana': 40, 'Colombo': 0}

def astar(graph, start, goal, heuristic):
    queue = [(0 + heuristic[start], 0, [start])]
    visited = set()
    while queue:
        est_total, cost_so_far, path = heapq.heappop(queue)
        node = path[-1]
        if node == goal:
            return path, cost_so_far
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_cost = cost_so_far + graph[node][neighbor]['weight']
                heapq.heappush(queue, (new_cost + heuristic[neighbor], new_cost, path + [neighbor]))

path, cost = astar(G, 'Panadura', 'Colombo', heuristic)
print("A* Path:", path, "Cost:", cost)
