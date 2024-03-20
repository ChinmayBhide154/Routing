class Network:
    def __init__(self, topologyFile, messageFile, changesFile):
        self.topologyFile = topologyFile
        self.messageFile = messageFile
        self.changesFile = changesFile
        self.graph = []
        self.messages = []
        self.routing_tables = {}
    '''    
    def initRoutingTables(self):
        for source, dest, cost in self.graph:
            if source not in self.routing_tables:
                self.routing_tables[source] = {}
            if dest not in self.routing_tables:
                self.routing_tables[dest] = {}
            self.routing_tables[source][dest] = cost
            self.routing_tables[dest][source] = cost

    def build_network(self):
        with open(self.topologyFile, 'r') as topology:
            for line in topology:
                node1, node2, cost = map(int, line.split())
                self.graph.append((node1, node2, cost))

    def parseMessages(self):
        with open(self.messageFile, 'r') as messages:
            for line in messages:
                node1, node2, message_text = messages.readline().strip().split(maxsplit=2)
                self.messages.append((node1, node2, message_text))


    def computeDV(self, router_id):
    # Use Bellman-Ford algorithm to update routing table based on neighbors' distance vectors
    # Ensure router_id is in the routing tables
        if router_id not in self.routing_tables:
            print(f"Router ID {router_id} not found in the routing tables.")
            return

        for source in self.routing_tables:
            # Skip if the source is the same as the router_id
            if source == router_id:
                continue

            for dest in self.routing_tables[source]:
                # Skip if the destination is the router itself
                if dest == router_id:
                    continue

                # Compute the new cost if possible
                source_to_dest_cost = self.routing_tables[source].get(dest, float('inf'))
                router_to_source_cost = self.routing_tables[router_id].get(source, float('inf'))
                existing_cost_to_dest = self.routing_tables[router_id].get(dest, float('inf'))

                # Calculate new cost and update if it's cheaper
                new_cost = router_to_source_cost + source_to_dest_cost
                if new_cost < existing_cost_to_dest:
                    self.routing_tables[router_id][dest] = new_cost
                    print(f"Updated cost to {dest} through {source} to {new_cost}")
    ''' 
    def bellman_ford(self, dst, routers, links):
        INFINITY = float('inf')
        distance = {}
        nexthop = {}
        
        for r in routers:
            distance[r] = INFINITY
            nexthop[r] = None

        distance[dst] = 0

        #for _ in range(len(routers) - 1):
        for (r1, r2, dist) in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = r1

        return distance, nexthop
    ''' 
    def print_routing_tables(self):
        for router, table in self.routing_tables.items():
            print(f"Router {router}: {table}")
    ''' 






    

    

    

    

                