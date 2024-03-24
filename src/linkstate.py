import sys
from dijkstar import Graph, find_path, NoPathError

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

def edge_cost_func(u, v, edge, prev_edge):
    return edge['cost']

def calculate_shortest_paths(graph, nodes):
    results = {}
    for node in nodes:
        results[node] = {}
        for target in nodes:
            if node != target:
                try:
                    result = find_path(graph, node, target, cost_func=edge_cost_func)
                    results[node][target] = (result.nodes, result.total_cost)
                except NoPathError:
                    results[node][target] = ([], float('inf'))  # No path found
            else:
                results[node][target] = ([node], 0)  # Path to itself
    return results

def print_shortest_paths(paths, messages_file_path, output_file_path):
    # Load messages from the file
    messages_dict = {}
    with open(messages_file_path, 'r') as msg_file:
        for line in msg_file:
            parts = line.strip().split(' ', 2)  # Split on the first two spaces only
            if len(parts) == 3:
                src, dest = map(int, parts[:2])  # Correctly converting first two parts to integers
                message = parts[2]
                messages_dict[(src, dest)] = message

    # Write paths and messages to the output file
    with open(output_file_path, 'a') as file:
        for (src, dest), message in messages_dict.items():
            # Check if both src and dest are in the paths dict and a path exists
            if src in paths and dest in paths[src] and paths[src][dest][0]:
                path, cost = paths[src][dest]
                hops_str = ' '.join(map(str, path))
                file.write(f"from {src} to {dest} cost {cost} hops {hops_str} message {message}\n")
            else:
                # Path does not exist or one of the nodes is not in the topology
                file.write(f"from {src} to {dest} cost infinite hops unreachable message {message}\n")
            file.write("\n")




def print_shortest_paths1(paths, output_file_path):
    with open(output_file_path, 'a') as file:
        for src, targets in paths.items():
            for dest, (path, cost) in targets.items():
                if len(path) > 1:
                    file.write(f"{dest} {path[1]} {cost}\n")
                else:
                    file.write(f"{dest} {path[0]} {cost}\n")
            file.write("\n")

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
    if len(sys.argv) != 4:
        print("Usage: python lsr.py <topologyFile> <messageFile> <changesFile>")
        sys.exit(1)

    topology_file_path = sys.argv[1]
    messages_file_path = sys.argv[2]
    changes_file_path = sys.argv[3]
    output_file_path = 'output.txt'  # Define the output file path here

    # Read the initial topology from the file
    edges = []
    with open(topology_file_path, 'r') as file:
        for line in file:
            src, dest, cost = map(int, line.strip().split())
            edges.append((src, dest, cost))

    # Perform initial link state routing computations
    complete_edges = populate_linkstate_info(edges)
    network_graph = build_graph(complete_edges)
    nodes = set(sum(([src, dest] for src, dest, _ in edges), []))
    paths = calculate_shortest_paths(network_graph, nodes)

    # Initial output before applying changes
    print_shortest_paths1(paths, output_file_path)
    print_shortest_paths(paths, messages_file_path, output_file_path)

    # Read and apply changes from the changes file
    with open(changes_file_path, 'r') as changes_file:
        for line in changes_file:
            change = tuple(map(int, line.strip().split()))
            apply_single_change(edges, change)

            # Recompute with updated topology
            complete_edges = populate_linkstate_info(edges)
            network_graph = build_graph(complete_edges)
            paths = calculate_shortest_paths(network_graph, nodes)

            # Output after each change
            print_shortest_paths1(paths, output_file_path)
            print_shortest_paths(paths, messages_file_path, output_file_path)






