from dijkstar import Graph, find_path

def build_graph(edges):
    graph = Graph()
    for src, dest, cost in edges:
        graph.add_edge(src, dest, {'cost': cost})
        # Assuming undirected graph for simplicity; add reverse edge
        graph.add_edge(dest, src, {'cost': cost})
    return graph

def populate_linkstate_info(edges):
    lsi_database = {src: set() for src, _, _ in edges}
    lsi_database.update({dest: set() for _, dest, _ in edges})
    for src, dest, cost in edges:
        lsi_database[src].add((src, dest, cost))
        lsi_database[dest].add((dest, src, cost))  # Assuming undirected graph
    
    # Simulate "flooding" - each node shares its LSI with all others
    complete_lsi = set().union(*lsi_database.values())
    for node in lsi_database:
        lsi_database[node] = complete_lsi  # Now every node has complete LSI
    
    # Convert the unified LSI back to the edges format
    return list(complete_lsi)


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
            file.write(f"\n")

if __name__ == '__main__':
    # Original edges
    edges = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
    ]
    
    # Simulate the "flooding" to distribute LSI across all nodes
    complete_edges = populate_linkstate_info(edges)
    
    # Build the network graph with the complete LSI known by all nodes
    network_graph = build_graph(complete_edges)
    
    # Continue with your existing process
    nodes = {1, 2, 3, 4, 5}
    paths = calculate_shortest_paths(network_graph, nodes)
    print_shortest_paths(paths)




