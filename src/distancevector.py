from network import Network
import sys

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
    nexthop = {r: None for r in routers}

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


if __name__ == '__main__':
    #if len(sys.argv) != 4:
     #   print("wrong number of arguments provided to program")
      #  sys.exit(1)

    #topologyFile = sys.argv[1]
    #messageFile = sys.argv[2]
    #changesFile = sys.argv[3]
    topology = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
    ]

    # Running the simulation
    final_distance_vectors, final_next_hops = distance_vector_routing(topology)
    print("Distance Vectors:")
    print(final_distance_vectors)
    print("Next Hops:")
    print(final_next_hops)
    #topologyFile = "C:\\Git Repositories\\Routing\\src\\topology.txt"
    #messageFile = "C:\\Git Repositories\\Routing\\src\\message.txt"
    #changesFile = "C:\\Git Repositories\\Routing\\src\\changes.txt"
