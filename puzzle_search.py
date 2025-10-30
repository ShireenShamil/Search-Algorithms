

import heapq

# ---- Step 1: Define the Puzzle ----
# Represented as a tuple (for immutability)
start_state = (1, 2, 3,
               4, 5, 6,
               7, 0, 8)  # 0 = empty space

goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

# Define possible moves (up, down, left, right)
moves = {
    'up': -3,
    'down': 3,
    'left': -1,
    'right': 1
}

# ---- Step 2: Helper Functions ----
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def get_neighbors(state):
    neighbors = []
    index = state.index(0)  # find empty cell

    for move, pos_change in moves.items():
        new_index = index + pos_change

        # Check move boundaries
        if move == 'left' and index % 3 == 0:
            continue
        if move == 'right' and (index + 1) % 3 == 0:
            continue
        if new_index < 0 or new_index > 8:
            continue

        # Swap blank (0) with the new position
        new_state = list(state)
        new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
        neighbors.append(tuple(new_state))

    return neighbors

# ---- Step 3: Heuristic (Manhattan Distance) ----
def manhattan_distance(state, goal):
    distance = 0
    for i, value in enumerate(state):
        if value == 0:
            continue
        goal_index = goal.index(value)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_index, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# ---- Step 4: A* Search Algorithm ----
def astar(start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + manhattan_distance(start, goal), 0, [start]))
    visited = set()

    while open_list:
        est_total, cost_so_far, path = heapq.heappop(open_list)
        state = path[-1]

        if state == goal:
            return path

        if state not in visited:
            visited.add(state)
            for neighbor in get_neighbors(state):
                new_cost = cost_so_far + 1
                est = new_cost + manhattan_distance(neighbor, goal)
                heapq.heappush(open_list, (est, new_cost, path + [neighbor]))
    return None

# ---- Step 5: Run the Solver ----
print("Initial State:")
print_state(start_state)

path = astar(start_state, goal_state)

if path:
    print("Steps to solve (A* Search):")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_state(state)
else:
    print("No solution found!")
