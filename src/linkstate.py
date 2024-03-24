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

def print_shortest_paths(paths, messages_file_path='C:\\Users\\death\\Routing\\src\\message.txt', output_file_path='C:\\Users\\death\\Routing\\src\\output.txt'):
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

def print_shortest_paths1(paths):
    with open('C:\\Users\\death\\Routing\\src\\output.txt', 'a') as file:
        for src, targets in paths.items():
            print(f"Paths from node {src}:")
            for dest, (path, cost) in targets.items():
                if len(path) > 1:
                    file.write(f"{dest} {path[1]} {cost} \n")
                else:
                    file.write(f"{dest} {path[0]} {cost} \n")
            file.write(f"\n")

def apply_single_change(edges, change):
    src, dest, new_cost = change
    # Update or add the link
    found = False
    for i, (s, d, _) in enumerate(edges):
        if s == src and d == dest:
            if new_cost == -999:
                edges.pop(i)  # Remove the link if cost is -999
            else:
                edges[i] = (src, dest, new_cost)  # Update existing link
            found = True
            break
    if not found and new_cost != -999:
        edges.append((src, dest, new_cost))  # Add new link



if __name__ == '__main__':
    # Original edges
    edges = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
    ]

    changes_file_path = 'C:\\Users\\death\\Routing\\src\\changes.txt'

    # Simulate the "flooding" to distribute LSI across all nodes
    complete_edges = populate_linkstate_info(edges)
    
    # Build the network graph with the complete LSI known by all nodes
    network_graph = build_graph(complete_edges)
    
    # Continue with your existing process
    nodes = {1, 2, 3, 4, 5}
    paths = calculate_shortest_paths(network_graph, nodes)
    print_shortest_paths1(paths)
    print_shortest_paths(paths)

    with open(changes_file_path, 'r') as changes_file:
        for line in changes_file:
            change = tuple(map(int, line.strip().split()))
            apply_single_change(edges, change)  # Apply the change
            
            # Rebuild the graph, recalculate paths, and reprint after each change
            network_graph = build_graph(edges)
            paths = calculate_shortest_paths(network_graph, nodes)
            print_shortest_paths1(paths)
            print_shortest_paths(paths)
            #print_shortest_paths1(paths)









