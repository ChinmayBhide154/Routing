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

def print_shortest_paths(paths, messages_file_path='C:\\Git Repositories\\Routing\\src\\message.txt', output_file_path='C:\\Git Repositories\\Routing\\src\\output.txt'):
    # Load messages from the file and parse them into a dict with (src, dest) as keys
    messages_dict = {}
    with open(messages_file_path, 'r') as msg_file:
        for line in msg_file:
            parts = line.strip().split(' ', 2)  # Split on the first two spaces only
            if len(parts) == 3:
                src, dest, message = parts
                src, dest = int(src), int(dest)  # Convert src and dest to integers
                messages_dict[(src, dest)] = message

    # Write paths and associated messages to the output file in append mode
    with open(output_file_path, 'a') as file:
        for (src, dest), message in messages_dict.items():
            if src in paths and dest in paths[src]:
                path, cost = paths[src][dest]
                if path:
                    hops_str = ' '.join(map(str, path))
                    file.write(f"from {src} to {dest} cost {cost} hops {hops_str} message {message}.\n")
                else:  # Fallback in case there's no path (which shouldn't happen in a connected graph)
                    file.write(f"from {src} to {dest} message {message}. No valid path found.\n")
            else:
                file.write(f"from {src} to {dest} message {message}. Path information not available.\n")
            file.write("\n")
'''
def print_shortest_paths(paths):
    # Load messages from the file
    with open('C:\\Git Repositories\\Routing\\src\\message.txt', 'r') as msg_file:
        messages = msg_file.readlines()
    
    # Write paths and associated messages to the output file
    with open('C:\\Git Repositories\\Routing\\src\\output.txt', 'a') as file:
        message_index = 0  # Keep track of which message we're on
        for src, targets in paths.items():
            for dest, (path, cost) in targets.items():
                if message_index < len(messages):  # Check to ensure there's a message to write
                    message = messages[message_index].strip()  # Remove newline characters
                    message_index += 1
                    hops_str = ' '.join(map(str, path))
                    file.write(f"from {src} to {dest} cost {cost} hops {hops_str} message {message}.\n")
                else:
                    message = "No message provided."

            file.write("\n")
'''
def print_shortest_paths1(paths):
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
    print_shortest_paths1(paths)
    print_shortest_paths(paths)





