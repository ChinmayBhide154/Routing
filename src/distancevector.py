def parse_topology(topology):
    """
    Parses the topology file and returns a graph represented as a dictionary of dictionaries.
    """
    graph = {}
    for r1, r2, dist in topology:
        if r1 not in graph:
            graph[r1] = {}
        graph[r1][r2] = dist
        if r2 not in graph:
            graph[r2] = {}
        graph[r2][r1] = dist  # Assuming the graph is undirected
    return graph

def bellman_ford(dst, routers, links):
    """
    Runs the Bellman-Ford algorithm for a given destination router.
    """
    INFINITY = float('inf')
    distance = {r: INFINITY for r in routers}
    nexthop = {r: dst for r in routers}

    distance[dst] = 0

    for _ in range(len(routers) - 1):
        for (r1, r2, dist) in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = r1

    return distance, nexthop

def distance_vector_routing(topology):
    """
    Simulates the Distance Vector Routing Protocol using the Bellman-Ford algorithm.
    """
    graph = parse_topology(topology)
    routers = list(graph.keys())
    links = [(r1, r2, graph[r1][r2]) for r1 in graph for r2 in graph[r1]]

    distance_vectors = {}
    next_hops = {}

    for router in routers:
        distance_vectors[router], next_hops[router] = bellman_ford(router, routers, links)

    return distance_vectors, next_hops

def write_output_file(distance_vectors, next_hops, messages):
    """
    Writes the forwarding table to an output file.
    """
    with open('C:\\Git Repositories\\Routing\\src\\output.txt', 'w') as file:
        for router in sorted(distance_vectors.keys()):
            for dst in sorted(distance_vectors[router].keys()):
                if distance_vectors[router][dst] != float('inf'):
                    file.write(f"{dst} {next_hops[router][dst]} {distance_vectors[router][dst]}\n")


if __name__ == '__main__':
    topology = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
    ]

    messages = [
        (2, 1, "here is a message from 2 to 1"),
        (3, 5, "this message gets sent from 3 to 5")
    ]

    changes = [
        (2, 4, 1),
        (2, 4, -999)
    ]

    # Running the simulation
    final_distance_vectors, final_next_hops = distance_vector_routing(topology)

    # Running the simulation
    final_distance_vectors, final_next_hops = distance_vector_routing(topology)

    # Writing to output file as per the requirement
    write_output_file(final_distance_vectors, final_next_hops, messages)

    # Returning the final distance vectors and next hops to check correctness
    print(final_distance_vectors, final_next_hops, "C:\\Git Repositories\\Routing\\src\\output.txt")

