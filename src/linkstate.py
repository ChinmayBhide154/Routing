from dijkstar import Graph, find_path

def build_graph(edges):
    graph = Graph()
    for src, dest, cost in edges:
        graph.add_edge(src, dest, {'cost': cost})
        # Assuming undirected graph for simplicity; add reverse edge
        graph.add_edge(dest, src, {'cost': cost})
    return graph

def calculate_shortest_paths(graph, nodes):
    results = {}
    for node in nodes:
        results[node] = {}
        for target in nodes:
            result = find_path(graph, node, target, cost_func=lambda u, v, edge, _: edge['cost'])
            results[node][target] = (result.nodes, result.total_cost)
    return results

def print_shortest_paths(paths):
    with open('C:\\Git Repositories\\Routing\\src\\output.txt', 'w') as file:
        for src, targets in paths.items():
            print(f"Paths from node {src}:")
            for dest, (path, cost) in targets.items():
                if len(path) > 1:
                    file.write(f"{dest} {path[1]} {cost} \n")
                else:
                    file.write(f"{dest} {path[0]} {cost} \n")
            print()


if __name__ == '__main__':
    # Define the edges of your network (source, destination, cost)
    edges = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
        # Add more edges as necessary
    ]

    # Build the complete network graph
    network_graph = build_graph(edges)

    # Assume all nodes in the network for simplicity
    nodes = {1, 2, 3, 4, 5}  # Update with all your nodes

    # Calculate and print shortest paths for all nodes
    paths = calculate_shortest_paths(network_graph, nodes)
    print_shortest_paths(paths)


    
