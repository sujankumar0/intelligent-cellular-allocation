import math
from models.q_learning import TabularQLearner
from simulation.interference import assign_channels

def users_to_channels(users, users_per_channel=13, max_per_cell=8):
    return min(max_per_cell, max(1, int(math.ceil(float(users) / users_per_channel))))

def allocate_fca(graph, loads, total_channels=24):
    # Fixed baseline: each cell receives a fixed set, then requests are served
    # only up to the fixed per-cell quota. The same channel pattern is reused
    # only where the graph permits it.
    fixed = {node: 4 for node in graph.nodes}
    return assign_channels(graph, fixed, total_channels)

def allocate_dca(graph, loads, total_channels=24):
    requested = {node: users_to_channels(loads[node]) for node in graph.nodes}
    return assign_channels(graph, requested, total_channels)

def allocate_proposed(graph, predicted_loads, actual_loads, total_channels=24):
    learner = TabularQLearner(max_channels=8).train()
    requested = {}
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        neighbor_pressure = sum(actual_loads[n] for n in neighbors) / max(1, len(neighbors))
        requested[node] = learner.choose_channels(predicted_loads[node], neighbor_pressure)
    assigned = assign_channels(graph, requested, total_channels)
    return assigned, requested
