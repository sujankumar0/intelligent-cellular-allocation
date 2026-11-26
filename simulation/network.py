import networkx as nx

def create_network(n_cells: int = 6):
    """Create a small illustrative cellular layout and its interference graph."""
    if n_cells != 6:
        raise ValueError("This starter simulation currently supports exactly 6 cells.")
    graph = nx.Graph()
    graph.add_nodes_from([f"BS{i}" for i in range(1, n_cells + 1)])
    # Ring neighbors plus two cross-links. Adjacent cells may not share a channel.
    edges = [
        ("BS1", "BS2"), ("BS2", "BS3"), ("BS3", "BS4"),
        ("BS4", "BS5"), ("BS5", "BS6"), ("BS6", "BS1"),
        ("BS1", "BS4"), ("BS2", "BS5"), ("BS3", "BS6")
    ]
    graph.add_edges_from(edges)
    return graph
