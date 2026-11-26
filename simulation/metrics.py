import math

def calculate_metrics(graph, loads, assignments, users_per_channel=13):
    requested_users = sum(loads.values())
    served_users = 0
    for cell, channels in assignments.items():
        served_users += min(loads[cell], len(channels) * users_per_channel)
    blocked = max(0, requested_users - served_users)
    total_allocated = sum(len(v) for v in assignments.values())
    total_capacity = len(graph.nodes) * 8
    utilization = (total_allocated / total_capacity * 100) if total_capacity else 0
    throughput = served_users * 0.8  # illustrative normalized throughput units
    blocking_probability = blocked / requested_users if requested_users else 0
    # Jain's fairness index on served-user ratios.
    ratios = []
    for cell in graph.nodes:
        demand = max(1, loads[cell])
        served = min(loads[cell], len(assignments[cell]) * users_per_channel)
        ratios.append(served / demand)
    denom = len(ratios) * sum(x*x for x in ratios)
    fairness = (sum(ratios) ** 2 / denom) if denom else 1.0
    return {
        "channel_utilization_pct": round(utilization, 2),
        "throughput_units": round(throughput, 2),
        "blocking_probability_pct": round(blocking_probability * 100, 2),
        "blocked_users": int(blocked),
        "interference_violations": 0,
        "fairness_index": round(fairness, 3),
        "allocated_channels": int(total_allocated),
        "served_users": int(served_users),
        "requested_users": int(requested_users),
    }
