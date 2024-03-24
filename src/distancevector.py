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
    graph = parse_topology(topology)
    routers = list(graph.keys())
    links = [(r1, r2, graph[r1][r2]) for r1 in graph for r2 in graph[r1]]

    distance_vectors = {}
    next_hops = {}
    paths = {}

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
                    # Assuming next hop can be derived from next_hops dictionary
                    next_hop = next_hops[router].get(dst, None)
                    cost = distance_vectors[router][dst]
                    file.write(f"{dst} {next_hop if next_hop else 'None'} {cost}\n")
            file.write("\n")  # Newline for separation between routers
            for src, dst, message_text in messages:
                if src in next_hops and dst in next_hops[src]:
                    path = [src]
                    current = src
                    while current != dst:
                        current = next_hops[current][dst]
                        path.append(current)
                    cost = distance_vectors[src][dst]
                    path_str = ' -> '.join(map(str, path))
                    file.write(f"from {src} to {dst} cost {cost} hops {path_str} message {message_text}.\n")


def read_changes(changes_file_path='C:\\Users\\death\\Routing\\src\\changes.txt'):
    """
    Reads changes from a file and returns them as a list of tuples.
    """
    changes = []
    with open(changes_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                r1, r2, cost = map(int, parts)
                changes.append((r1, r2, cost))
    return changes

def find_path(source, destination, next_hops):
    if source == destination:
        return [source]

    path = [source]
    current = source

    while current != destination:
        # Retrieve the next hop for the current node towards the destination
        next_hop = next_hops[current]

        # Check for loops or incorrect next hop
        if next_hop == current or next_hop in path:
            #print(f"Loop or incorrect next hop detected from {current} to {destination}. Next hop: {next_hop}")
            return None

        path.append(next_hop)
        current = next_hop
        # Break if no progress is made (shouldn't happen with correct next hop data)
        if current == destination:
            break

    return path



def read_messages(messages_file_path='C:\\Users\\death\\Routing\\src\\message.txt'):
    """
    Reads messages from a file and returns them as a list of tuples.
    """
    messages = []
    with open(messages_file_path, 'r') as msg_file:
        for line in msg_file:
            parts = line.strip().split(' ', 2)  # Split on the first two spaces only
            if len(parts) == 3:
                src, dest, message = parts
                src, dest = int(src), int(dest)  # Convert src and dest to integers
                messages.append((src, dest, message))
    return messages

def get_complete_paths(distance_vectors, next_hops):
    output = []
    for src_router in sorted(distance_vectors.keys()):
        for dst_router in sorted(distance_vectors[src_router].keys()):
            if src_router == dst_router:
                continue
            path = [src_router]
            next_router = src_router
            while next_router != dst_router:
                next_router = next_hops[next_router].get(dst_router)
                if next_router is None:
                    break
                path.append(next_router)
            if next_router is not None:
                cost = distance_vectors[src_router][dst_router]
                path_str = ' -> '.join(map(str, path))
                output.append(f"from {src_router} to {dst_router} cost {cost} hops {path_str}")
    return '\n'.join(output)

def append_specific_message_paths(output_file_path, distance_vectors, next_hops, messages):
    """
    Appends specific message paths based on current routing information to the output file.
    """
    with open(output_file_path, 'a') as file:
        for src, dst, message_text in messages:
            path = [src]
            current = src
            while current != dst:
                current = next_hops[current].get(dst, None)
                if current is None:  # Break if there's no valid next hop
                    break
                path.append(current)
            if current:
                cost = distance_vectors[src][dst]
                hops_str = ' '.join(map(str, path))
                file.write(f"from {src} to {dst} cost {cost} hops {hops_str} message {message_text}.\n")
        file.write("\n")  # Ensure there's a newline after appending message paths



if __name__ == '__main__':
    topology = [
        (1, 2, 8),
        (2, 3, 3),
        (2, 5, 4),
        (4, 1, 1),
        (4, 5, 1)
    ]

    # Read messages from the file instead of hardcoded messages
    messages = read_messages('C:\\Users\\death\\Routing\\src\\message.txt')
    distance_vectors, next_hops = distance_vector_routing(topology)
    write_output_file(distance_vectors, next_hops, messages, 'output.txt', append_mode=False)

    changes = read_changes('C:\\Users\\death\\Routing\\src\\changes.txt')
    for change in changes:
        r1, r2, cost = change
        if cost == -999:  # Remove link
            topology = [(src, dst, c) for src, dst, c in topology if not ((src == r1 and dst == r2) or (src == r2 and dst == r1))]
        else:  # Add/update link
            # Remove existing link if present
            topology = [(src, dst, c) for src, dst, c in topology if not ((src == r1 and dst == r2) or (src == r2 and dst == r1))]
            topology.append((r1, r2, cost))  # Add new/updated link

        # Recalculate routing tables after each change
    distance_vectors, next_hops = distance_vector_routing(topology)
    write_output_file(distance_vectors, next_hops, [], 'output.txt', append_mode=False)
    append_specific_message_paths('output.txt', distance_vectors, next_hops, messages)

    # Processing changes
    for change in changes:
        # Apply the change...

        # Recalculate routing tables after each change
        distance_vectors, next_hops = distance_vector_routing(topology)

        # Append the updated router tables to 'output.txt'
        write_output_file(distance_vectors, next_hops, [], 'output.txt', append_mode=True)

        # Append the updated specific message paths
        append_specific_message_paths('output.txt', distance_vectors, next_hops, messages)