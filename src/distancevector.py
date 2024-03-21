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
'''
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
'''
def bellman_ford(dst, routers, links):
    """
    Runs the Bellman-Ford algorithm for a given destination router and prints paths.
    """
    INFINITY = float('inf')
    distance = {r: INFINITY for r in routers}
    nexthop = {r: None for r in routers}

    distance[dst] = 0
    nexthop[dst] = dst  # The next hop from the destination to itself is the destination

    for _ in range(len(routers) - 1):
        for (r1, r2, dist) in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = r1
            if distance[r2] + dist < distance[r1]:  # Check the path in reverse as well
                distance[r1] = distance[r2] + dist
                nexthop[r1] = r2

    # Now, let's find and print the path for each router to the destination
    paths = {}
    for router in routers:
        path = []
        current = router
        while current is not None:
            path.append(current)
            if current == dst:
                break
            current = nexthop[current]
        path.reverse()  # Reverse the path since we built it backwards
        paths[router] = path

    # Print paths
    for router, path in paths.items():
        print(f"Path from {router} to {dst}: {' -> '.join(map(str, path))}")
    
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
    paths = {}

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

def find_path(source, destination, next_hops, path=None):
    """
    Recursively finds the path from source to destination using the next hops.
    """
    # Initialize the path list on the first call
    if path is None:
        path = [source]

    # Base case: If source is the same as destination, the path is complete
    if source == destination:
        return path

    # If there is no next hop from source to destination, return None
    if destination not in next_hops[source] or next_hops[source][destination] is None:
        return None

    # Recursive case: get the next hop toward the destination
    next_hop = next_hops[source][destination]
    
    # Detect loops: if next_hop is already in the path, we have a loop
    if next_hop in path:
        return None
    
    # Append the next hop to the path
    path.append(next_hop)
    
    # Recursively find the rest of the path
    return find_path(next_hop, destination, next_hops, path)


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


    # Writing to output file as per the requirement
    write_output_file(final_distance_vectors, final_next_hops, messages)

    # Returning the final distance vectors and next hops to check correctness
    print(final_distance_vectors, final_next_hops, "C:\\Git Repositories\\Routing\\src\\output.txt")


    # Example usage:
    source = 1
    destination = 4
    # Assume next_hops is a dictionary of dictionaries
    # next_hops = { ... }

    path = find_path(source, destination, final_next_hops)
    if path:
        print("Path found:", " -> ".join(map(str, path)))
    else:
        print(f"No path found from {source} to {destination}.")

