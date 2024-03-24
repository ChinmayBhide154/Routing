import sys

def parse_topology(file_path):
    """
    Reads the topology from a file and returns it as a list of tuples.
    Each line in the file should be in the format: r1 r2 dist
    """
    topology = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                r1, r2, dist = parts
                topology.append((int(r1), int(r2), int(dist)))
    return topology

def bellman_ford(dst, routers, links):
    INFINITY = float('inf')
    distance = {r: INFINITY for r in routers}
    nexthop = {r: None for r in routers}

    distance[dst] = 0
    nexthop[dst] = dst  # The next hop from the destination to itself is the destination

    # Initialize distances and next hops for direct neighbors of the destination
    for r1, r2, dist in links:
        if r1 == dst:
            nexthop[r2] = r2
            distance[r2] = dist
        elif r2 == dst:
            nexthop[r1] = r1
            distance[r1] = dist

    # Relax edges repeatedly
    for _ in range(len(routers) - 1):
        for r1, r2, dist in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = nexthop[r1] if nexthop[r1] is not None else r1
            if distance[r2] + dist < distance[r1]:
                distance[r1] = distance[r2] + dist
                nexthop[r1] = nexthop[r2] if nexthop[r2] is not None else r2

    # Construct paths for each router to the destination
    return distance, nexthop



def distance_vector_routing(topology):
    """
    Simulates the Distance Vector Routing Protocol using the Bellman-Ford algorithm.
    """
    # Assuming topology is already a list of tuples (r1, r2, dist)
    routers = list(set([link[0] for link in topology] + [link[1] for link in topology]))
    links = topology

    distance_vectors = {}
    next_hops = {}

    for router in routers:
        distance_vectors[router], next_hops[router] = bellman_ford(router, routers, links)

    return distance_vectors, next_hops


def write_output_file(distance_vectors, next_hops, messages, output_file_path='output.txt', append_mode=False):
    """
    Writes the forwarding table and paths for messages to the output file.
    """
    mode = 'a' if append_mode else 'w'
    with open(output_file_path, mode) as file:
        # Write the forwarding table for each router
        for router in sorted(distance_vectors.keys()):
            for dst in sorted(distance_vectors[router].keys()):
                if distance_vectors[router][dst] != float('inf'):
                    next_hop = next_hops[router].get(dst, None)
                    cost = distance_vectors[router][dst]
                    file.write(f"{dst} {next_hop if next_hop else 'None'} {cost}\n")
            file.write("\n")  # Separation between router
        for src, dst, message_text in messages:
            if src in next_hops and dst in next_hops[src] and dst in distance_vectors[src] and distance_vectors[src][dst] != float('inf'):
                path = [src]
                current = src
                while current != dst:
                    next_router = next_hops[current].get(dst, None)
                    if not next_router:  # Handle case where next hop is None or not found
                        path = None
                        break
                    path.append(next_router)
                    current = next_router
                
                if path:  # Path exists
                    cost = distance_vectors[src][dst]
                    hops_str = ' '.join(map(str, path))
                    file.write(f"from {src} to {dst} cost {cost} hops {hops_str} message {message_text}.\n")
                else:  # Path does not exist
                    file.write(f"from {src} to {dst} cost infinite hops unreachable message {message_text}.\n")
            else:  # Destination unreachable
                file.write(f"from {src} to {dst} cost infinite hops unreachable message {message_text}.\n")

            file.write("\n")  # Ensure there's a newline after appending message paths



def read_changes(changes_file_path):
    changes = []
    with open(changes_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                r1, r2, cost = map(int, parts)
                changes.append((r1, r2, cost))
    return changes


def read_messages(file_path):  # Corrected parameter name to file_path
    """
    Reads messages from a file and returns them as a list of tuples.
    """
    messages_list = []  # Renamed variable to avoid confusion with the function parameter
    with open(file_path, 'r') as msg_file:  # Corrected to use file_path
        for line in msg_file:
            parts = line.strip().split(' ', 2)  # Split on the first two spaces only
            if len(parts) == 3:
                src, dest, message = parts
                src, dest = int(src), int(dest)  # Convert src and dest to integers
                messages_list.append((src, dest, message))
    return messages_list


def apply_changes_to_topology(topology, changes):
    updated_topology = topology[:]
    for src, dest, cost in changes:
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

    # Use the provided file paths instead of hardcoded paths
    initial_topology = parse_topology(topology_file)  # Assume you have a function to read topology from a file
    messages = read_messages(message_file)
    changes = read_changes(changes_file)

    # Initial routing simulation
    distance_vectors, next_hops = distance_vector_routing(initial_topology)
    write_output_file(distance_vectors, next_hops, messages, 'output.txt', append_mode=False)

    # Apply each change and recalculate routing
    for change in changes:
        updated_topology = apply_changes_to_topology(initial_topology, [change])
        distance_vectors, next_hops = distance_vector_routing(updated_topology)
        write_output_file(distance_vectors, next_hops, messages, 'output.txt', append_mode=True)
