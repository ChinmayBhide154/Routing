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
'''
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
    '''
'''
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
'''
'''
def generate_forwarding_tables(lsa_database, output_file):
    with open(output_file, 'w') as file:
        # Iterate over each node in the network as the source
        for source_node in sorted(lsa_database.keys()):
            # Compute shortest paths from the current source node
            shortest_paths = compute_shortest_paths(lsa_database, source_node)
            
            file.write(f"Forwarding Table for Node {source_node}:\n")
            file.write("Destination NextHop PathCost\n")
            
            # Ensure destinations are processed in order
            for dest in sorted(shortest_paths.keys()):
                path, cost = shortest_paths[dest]
                if len(path) > 1:
                    next_hop = path[1]  # Next hop is the second node in the path
                else:
                    next_hop = "Direct"  # Directly connected or self
                
                # Write the forwarding table entry
                file.write(f"{dest} {next_hop} {cost}\n")
            file.write("\n")
'''

if __name__ == '__main__':
    # API Documentation: https://pypi.org/project/Dijkstar/
    #links = [
    #    (1, 2, 8),
    #    (2, 3, 3),
    #    (2, 5, 4),
    #    (4, 1, 1),
    #    (4, 5, 1),
        # More links as needed...
    #]

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

    #lsa_database = flood_lsa(links)
    #print(lsa_database)
    #shortest_paths = compute_shortest_paths(lsa_database, 1)
    

    #for dest, (path, cost) in shortest_paths.items():
    #    print(f"Shortest path from 1 to {dest}: {path} with cost {cost}")

    # Example usage
    #output_file = "C:\\Git Repositories\\Routing\\src\\output.txt"
    #generate_forwarding_tables(lsa_database, output_file)
    #print(f"Forwarding tables have been output to {output_file}.")

    
