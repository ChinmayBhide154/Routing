from dijkstar import Graph, find_path

def flood_lsa(links):
    # Initially, each node knows only about its direct links
    lsa_database = {src: {} for src, _, _ in links}
    lsa_database.update({dest: {} for _, dest, _ in links})
    
    # Populate the initial LSA database with direct links
    for src, dest, cost in links:
        lsa_database[src][dest] = cost
        lsa_database[dest][src] = cost  # Assuming undirected graph
    
    # Simulate flooding - each node shares its LSA with every other node
    for node in lsa_database:
        for neighbor in lsa_database:
            if node != neighbor:
                # Update neighbor's LSA database with node's information
                for dest, cost in lsa_database[node].items():
                    lsa_database[neighbor][dest] = cost
    
    return lsa_database

def compute_shortest_paths(lsa_database, start_node):
    graph = Graph()
    
    # Build the graph from the LSA database
    for src in lsa_database:
        for dest, cost in lsa_database[src].items():
            graph.add_edge(src, dest, {'cost': cost})
    
    # Compute shortest paths from start_node to all other nodes
    shortest_paths = {}
    for dest in lsa_database:
        if dest != start_node:
            path_result = find_path(graph, start_node, dest, cost_func=lambda u, v, edge, prev_edge: edge['cost'])
            shortest_paths[dest] = (path_result.nodes, path_result.total_cost)
    
    return shortest_paths


if __name__ == '__main__':
    # API Documentation: https://pypi.org/project/Dijkstar/
    links = [
        (1, 2, 7),
        (1, 3, 9),
        (2, 3, 10),
        (2, 4, 15),
        (3, 4, 11),
        # More links as needed...
    ]

    lsa_database = flood_lsa(links)
    shortest_paths = compute_shortest_paths(lsa_database, 1)

    for dest, (path, cost) in shortest_paths.items():
        print(f"Shortest path from 1 to {dest}: {path} with cost {cost}")
    '''
    graph = Graph()
    graph.add_edge(1, 2, 8)
    graph.add_edge(2, 3, 4)
    graph.add_edge(2, 5, 4)
    graph.add_edge(4, 1, 1)
    graph.add_edge(4, 5, 1)
    path_info = find_path(graph, 1, 3)
    path = path_info.nodes
    print(path)
    '''
    
