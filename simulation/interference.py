def assign_channels(graph, requested_counts, total_channels=24):
    """
    Greedy graph-color-like assignment.
    A channel cannot be reused by directly neighboring cells.
    If the pool is insufficient, some requests remain unserved.
    """
    assignments = {node: [] for node in graph.nodes}
    # Allocate larger demands first, with deterministic tie-breaking.
    order = sorted(graph.nodes, key=lambda n: (-requested_counts.get(n, 0), n))
    all_channels = list(range(1, total_channels + 1))
    for node in order:
        forbidden = set()
        for neighbor in graph.neighbors(node):
            forbidden.update(assignments[neighbor])
        available = [ch for ch in all_channels if ch not in forbidden]
        count = min(int(requested_counts.get(node, 0)), len(available))
        assignments[node] = available[:count]
    return assignments

def count_interference_violations(graph, assignments):
    violations = 0
    for a, b in graph.edges:
        violations += len(set(assignments.get(a, [])) & set(assignments.get(b, [])))
    return violations
