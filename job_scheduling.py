# job_scheduling.py

import itertools
import heapq

# ---- Step 1: Define tasks ----
# Each task = (task_name, time_required, deadline, penalty_per_unit_delay)
tasks = [
    ("Task1", 3, 4, 10),
    ("Task2", 2, 3, 15),
    ("Task3", 4, 6, 20),
    ("Task4", 1, 2, 8)
]

# ---- Step 2: Calculate total penalty for a given order ----
def calculate_penalty(order):
    time = 0
    total_penalty = 0
    for task in order:
        name, duration, deadline, penalty = task
        time += duration
        delay = max(0, time - deadline)
        total_penalty += delay * penalty
    return total_penalty

# ---- Step 3: Greedy Search (sort by earliest deadline first) ----
def greedy_schedule(tasks):
    order = sorted(tasks, key=lambda t: t[2])  # sort by deadline
    total_penalty = calculate_penalty(order)
    return order, total_penalty

# ---- Step 4: A* Search (try all possible orders with heuristic) ----
def astar_schedule(tasks):
    start_state = tuple()
    goal_state_length = len(tasks)
    
    # Priority Queue: (estimated_cost, cost_so_far, current_order)
    pq = [(0, 0, start_state)]
    visited = set()
    
    while pq:
        est_total, cost_so_far, state = heapq.heappop(pq)
        
        if len(state) == goal_state_length:
            return state, cost_so_far
        
        if state in visited:
            continue
        visited.add(state)
        
        for t in tasks:
            if t not in state:
                new_state = state + (t,)
                new_cost = calculate_penalty(new_state)
                heuristic = (goal_state_length - len(new_state)) * 5  # simple heuristic
                heapq.heappush(pq, (new_cost + heuristic, new_cost, new_state))

# ---- Step 5: Run both algorithms ----
greedy_order, greedy_penalty = greedy_schedule(tasks)
astar_order, astar_penalty = astar_schedule(tasks)

print("Greedy Search (Earliest Deadline First):")
for t in greedy_order:
    print(t[0], end=" → ")
print(f"\nTotal Penalty: {greedy_penalty}")

print("\nA* Search Optimal Schedule:")
for t in astar_order:
    print(t[0], end=" → ")
print(f"\nTotal Penalty: {astar_penalty}")
