## @file distancevector
#  This simulates Distance Vector Routing Protocol using the Bellman-Ford algorithm.
import sys

## Parse the topology from a file and return it as a list of tuples.
#  @param file_path Path to the file containing the topology data.
#  @return List of tuples representing the topology where each tuple is (r1, r2, dist).
def parse_topology(file_path):
    """
    Reads the topology from a file and returns it as a list of tuples.
    Each line in the file should be in the format: r1 r2 dist
    """
    topology = [] # Initialize an empty list to store topology
    with open(file_path, 'r') as file: # Opens file in read mode
        for line in file:        # Iterates over each line in the file
            parts = line.strip().split()    # Splits the line into parts
            if len(parts) == 3:         # Checks if there are 3 parts
                r1, r2, cost = parts    # Unpacks the parts into r1, r2, and cost
                topology.append((int(r1), int(r2), int(cost)))  # Appends the tuple to the topology list
    return topology   # Returns the list of tuples to make up the topology

## Implementation of the Bellman-Ford algorithm to compute routing tables.
#  @param dst Destination router.
#  @param routers List of all routers.
#  @param links List of links between routers as tuples (r1, r2, dist).
#  @return Tuples with distance and next hops for each router.
def bellman_ford(dst, routers, links):
    INFINITY = float('inf') # Defines infinite cost
    # Initialize all distances as inf and all hops as none
    distance = {r: INFINITY for r in routers}
    nexthop = {r: None for r in routers}

    # Set the distance of a router and its relative distance to itself as 0.
    distance[dst] = 0
    nexthop[dst] = dst
    
    # Update the next hops for the destination router
    for r1, r2, dist in links:
        if r1 == dst:   # If the first router is the destination
            nexthop[r2] = r2 
            distance[r2] = dist 
        elif r2 == dst: # If the second router is the destination
            nexthop[r1] = r1 
            distance[r1] = dist
    # Iteratively finds the shortest paths
    for _ in range(len(routers) - 1):
        for r1, r2, dist in links:
            # If the distance to r2 through r1 is shorter
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = nexthop[r1] if nexthop[r1] is not None else r1
            # If the distance to r1 through r2 is shorter
            if distance[r2] + dist < distance[r1]:
                distance[r1] = distance[r2] + dist
                nexthop[r1] = nexthop[r2] if nexthop[r2] is not None else r2

    return distance, nexthop

## Simulate distance vector routing protocol.
#  @param topology List of tuples representing the topology.
#  @return Tuples with distance vectors and next hops.
def distance_vector_routing(topology):
    """
    Simulates the Distance Vector Routing Protocol using the Bellman-Ford algorithm.
    """
    # Creates a list of routers from the topology
    routers = list(set([link[0] for link in topology] + [link[1] for link in topology]))
    links = topology

    distance_vectors = {}
    next_hops = {}
    # For every router, calculate the shortest paths to all other routers
    for router in routers:
        # Utilize the Bellman-Ford algorithm to calculate shortest paths and next hops
        distance_vectors[router], next_hops[router] = bellman_ford(router, routers, links)

    return distance_vectors, next_hops

## Write the routing table and paths for messages to an output file.
#  @param distance_vectors Distance vectors for each router.
#  @param next_hops Next hop information for each router.
#  @param messages List of message tuples to be routed.
#  @param output_file_path Path to the output file.
#  @param append_mode Boolean flag to append to the file if True.
def write_output_file(distance_vectors, next_hops, messages, output_file_path='output.txt', append_mode=False):
    """
    Writes the forwarding table and paths for messages to the output file.
    """
    mode = 'a' if append_mode else 'w'
    with open(output_file_path, mode) as file:
        # Iterate over each router to create a forwarding table
        for router in sorted(distance_vectors.keys()):
            for dst in sorted(distance_vectors[router].keys()):
                if distance_vectors[router][dst] != float('inf'):
                    next_hop = next_hops[router].get(dst, None)
                    cost = distance_vectors[router][dst]
                    file.write(f"{dst} {next_hop if next_hop else 'None'} {cost}\n")
            file.write("\n")
        # Iterate over each message to write its path.
        for src, dst, message_text in messages:
            if src in next_hops and dst in next_hops[src] and dst in distance_vectors[src] and distance_vectors[src][dst] != float('inf'):
                path = [src]
                current = src
                while current != dst:
                    next_router = next_hops[current].get(dst, None)
                    if not next_router:  
                        path = None
                        break
                    path.append(next_router)
                    current = next_router
                
                if path:
                    cost = distance_vectors[src][dst]
                    hops_str = ' '.join(map(str, path))
                    file.write(f"from {src} to {dst} cost {cost} hops {hops_str} message {message_text}.\n")
                else:
                    file.write(f"from {src} to {dst} cost infinite hops unreachable message {message_text}.\n")
            else:
                file.write(f"from {src} to {dst} cost infinite hops unreachable message {message_text}.\n")

            file.write("\n")

## Read changes from a file.
#  @param changes_file_path Path to the file containing changes.
#  @return List of change tuples.
def read_changes(changes_file_path):
    changes = []
    with open(changes_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                r1, r2, cost = map(int, parts)
                changes.append((r1, r2, cost))
    return changes

## Read messages from a file.
#  @param file_path Path to the file containing messages.
#  @return List of message tuples.
def read_messages(file_path):
    """
    Reads messages from a file and returns them as a list of tuples.
    """
    messages_list = [] 
    with open(file_path, 'r') as msg_file:
        for line in msg_file:
            parts = line.strip().split(' ', 2) 
            if len(parts) == 3:
                src, dest, message = parts
                src, dest = int(src), int(dest)
                messages_list.append((src, dest, message))
    return messages_list

## Apply changes to the topology.
#  @param topology Current topology as a list of tuples.
#  @param changes List of changes as tuples to be changed.
#  @return Updated topology as a list of tuples.
def apply_changes_to_topology(topology, changes):
    updated_topology = topology[:]  # Create a copy of the topology to change
    for src, dest, cost in changes: # Intreate over each change
        if cost == -999:  # Remove the link
            updated_topology = [link for link in updated_topology if not ((link[0] == src and link[1] == dest) or (link[0] == dest and link[1] == src))]
        else:  # Add or update the link
            # Remove existing link if present
            updated_topology = [link for link in updated_topology if not ((link[0] == src and link[1] == dest) or (link[0] == dest and link[1] == src))]
            # Add the new or updated link
            updated_topology.append((src, dest, cost))
    return updated_topology


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: ./dvr <topologyFile> <messageFile> <changesFile>")
        sys.exit(1)

    topology_file = sys.argv[1]
    message_file = sys.argv[2]
    changes_file = sys.argv[3]

    # Initial setup and routing.
    initial_topology = parse_topology(topology_file)
    messages = read_messages(message_file)
    changes = read_changes(changes_file)

    distance_vectors, next_hops = distance_vector_routing(initial_topology)
    write_output_file(distance_vectors, next_hops, messages, 'output.txt', append_mode=False)

    # Apply changes to initial setup and redo routing.
    for change in changes:
        updated_topology = apply_changes_to_topology(initial_topology, [change])
        distance_vectors, next_hops = distance_vector_routing(updated_topology)
        write_output_file(distance_vectors, next_hops, messages, 'output.txt', append_mode=True)
