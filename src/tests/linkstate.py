## @package linkstate
#  This simulates linkstate Routing Protocol using the Dijkstra algorithm.
import sys
from dijkstar import Graph, find_path, NoPathError
## Build a graph from a list of edges.
#  @param edges List of tuples (source, destination, cost).
#  @return Graph object populated with edges and costs.
def build_graph(edges):
    graph = Graph()
    for src, dest, cost in edges:
        graph.add_edge(src, dest, {'cost': cost})
        graph.add_edge(dest, src, {'cost': cost})
    return graph

## Populate link-state information for all nodes.
#  @param edges Initial list of edges in the network.
#  @return List of edges representing complete link-state information.
def populate_linkstate_info(edges):
    lsi_database = {src: set() for src, _, _ in edges}
    lsi_database.update({dest: set() for _, dest, _ in edges})
    for src, dest, cost in edges:
        lsi_database[src].add((src, dest, cost))
        lsi_database[dest].add((dest, src, cost))
    complete_lsi = set().union(*lsi_database.values())
    for node in lsi_database:
        lsi_database[node] = complete_lsi  
    return list(complete_lsi)

## Cost for edge traversal.
#  @param u Source node.
#  @param v Destination node.
#  @param edge Edge data.
#  @param prev_edge Previous edge data
#  @return Cost of the edge.
def edge_cost_func(u, v, edge, prev_edge):
    return edge['cost']

## Calculate shortest paths between all nodes.
#  @param graph Graph object representing the network.
#  @param nodes List of nodes in the graph.
#  @return Dictionary mapping node pairs to their shortest path and cost.
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
                    results[node][target] = ([], float('inf'))
            else:
                results[node][target] = ([node], 0)
    return results

## Print shortest paths to an output file.
#  @param paths Dictionary of shortest paths and costs.
#  @param messages_file_path Path to the file containing messages.
#  @param output_file_path Path to the output file.
def print_shortest_paths(paths, messages_file_path, output_file_path):
    messages_dict = {}
    with open(messages_file_path, 'r') as msg_file:
        for line in msg_file:
            parts = line.strip().split(' ', 2)
            if len(parts) == 3:
                src, dest = map(int, parts[:2])
                message = parts[2]
                messages_dict[(src, dest)] = message
    with open(output_file_path, 'a') as file:
        for (src, dest), message in messages_dict.items():
            if src in paths and dest in paths[src] and paths[src][dest][0]:
                path, cost = paths[src][dest]
                hops_str = ' '.join(map(str, path))
                file.write(f"from {src} to {dest} cost {cost} hops {hops_str} message {message}\n")
            else:
                file.write(f"from {src} to {dest} cost infinite hops unreachable message {message}\n")
            file.write("\n")

## Print shortest path forwarding tables to an output file.
#  This function iterates over all source nodes in the network, listing the next hop and total cost for each destination reachable from the source.
#  @param paths Dictionary mapping source and destination nodes with their paths and costs
#  @param output_file_path String path to output file
def print_shortest_paths1(paths, output_file_path):
    with open(output_file_path, 'a') as file:
        for src, targets in paths.items():
            for dest, (path, cost) in targets.items():
                if len(path) > 1:
                    file.write(f"{dest} {path[1]} {cost}\n")
                else:
                    file.write(f"{dest} {path[0]} {cost}\n")
            file.write("\n")

## Apply a single change to the network topology.
#  @param edges Current list of edges.
#  @param change Tuple representing the change to apply.
#  @return Updated list of edges.
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
    # Command line arguments.
    topology_file_path = sys.argv[1]
    messages_file_path = sys.argv[2]
    changes_file_path = sys.argv[3]
    output_file_path = 'output.txt' 

    # Reads the tpology from the file and stores it as a list of edges
    edges = []
    with open(topology_file_path, 'r') as file:
        for line in file:
            src, dest, cost = map(int, line.strip().split())
            edges.append((src, dest, cost))

    # Generate the complete topology to simulate routing
    complete_edges = populate_linkstate_info(edges)
    network_graph = build_graph(complete_edges)
    nodes = set(sum(([src, dest] for src, dest, _ in edges), []))
    paths = calculate_shortest_paths(network_graph, nodes)

    # Writes the initial routing information
    print_shortest_paths1(paths, output_file_path)
    print_shortest_paths(paths, messages_file_path, output_file_path)

    # Apply changes and recalculate routing
    with open(changes_file_path, 'r') as changes_file:
        for line in changes_file:
            change = tuple(map(int, line.strip().split()))
            apply_single_change(edges, change)

            # Recompute with updated topology
            complete_edges = populate_linkstate_info(edges)
            network_graph = build_graph(complete_edges)
            paths = calculate_shortest_paths(network_graph, nodes)

            print_shortest_paths1(paths, output_file_path)
            print_shortest_paths(paths, messages_file_path, output_file_path)






