

import heapq
import matplotlib.pyplot as plt
import networkx as nx

# ---- Step 1: Create Graph ----
# Each edge has a "distance" weight
graph = {
    'Panadura': {'Moratuwa': 12, 'Horana': 20},
    'Moratuwa': {'Colombo': 18, 'Panadura': 12},
    'Horana': {'Ratnapura': 45, 'Panadura': 20, 'Kaduwela': 30},
    'Colombo': {'Kaduwela': 15, 'Moratuwa': 18},
    'Kaduwela': {'Colombo': 15, 'Horana': 30, 'Ratnapura': 55},
    'Ratnapura': {'Horana': 45, 'Kaduwela': 55}
}

# ---- Step 2: Heuristic values (straight-line estimates to goal: Ratnapura) ----
heuristic = {
    'Panadura': 60,
    'Moratuwa': 55,
    'Colombo': 50,
    'Kaduwela': 35,
    'Horana': 25,
    'Ratnapura': 0
}

# ---- Step 3: Uniform Cost Search (UCS) ----
def uniform_cost_search(graph, start, goal):
    pq = [(0, [start])]  # (cost, path)
    visited = set()
    
    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                new_cost = cost + weight
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_cost, new_path))
    return None, float('inf')

# ---- Step 4: A* Search ----
def astar_search(graph, start, goal, heuristic):
    pq = [(heuristic[start], 0, [start])]  # (estimated total, cost so far, path)
    visited = set()

    while pq:
        est_total, cost_so_far, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path, cost_so_far
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                new_cost = cost_so_far + weight
                est = new_cost + heuristic[neighbor]
                heapq.heappush(pq, (est, new_cost, path + [neighbor]))
    return None, float('inf')

# ---- Step 5: Visualization ----
def draw_graph(graph, path=None, title="Route Map"):
    G = nx.Graph()
    for city, neighbors in graph.items():
        for neighbor, dist in neighbors.items():
            G.add_edge(city, neighbor, weight=dist)
    
    pos = nx.spring_layout(G, seed=5)
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='lightblue', font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    if path:
        edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, width=4, edge_color='red')
    
    plt.title(title)
    plt.show()

# ---- Step 6: Run Search ----
start, goal = 'Panadura', 'Ratnapura'

ucs_path, ucs_cost = uniform_cost_search(graph, start, goal)
astar_path, astar_cost = astar_search(graph, start, goal, heuristic)

print("Uniform Cost Search Path:", ucs_path, " | Cost:", ucs_cost)
print("A* Search Path:", astar_path, " | Cost:", astar_cost)

# ---- Step 7: Show Visualization ----
draw_graph(graph, ucs_path, "Uniform Cost Search Route")
draw_graph(graph, astar_path, "A* Search Route")
