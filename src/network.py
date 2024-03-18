class Network:
    def __init__(self, topologyFile, messageFile, changesFile):
        self.topologyFile = topologyFile
        self.messageFile = messageFile
        self.changesFile = changesFile
        self.graph = []
        self.messages = []
        self.routing_tables = {}
        

    def build_network(self):
        with open(self.topologyFile, 'r') as topology:
            for line in topology:
                node1, node2, cost = map(int, line.split())
                self.graph.append([node1, node2, cost])

    def parseMessages(self):
        with open(self.messageFile, 'r') as messages:
            for line in messages:
                node1, node2, message_text = messages.readline().strip().split(maxsplit=2)
                self.messages.append([node1, node2, message_text])

    def receiveDV(self, router_id):
        for source, dest, cost in self.graph:
            if source != router_id:
                continue

            if dest not in self.routing_tables:
                self.routing_tables[dest] = {}

            (self.routing_tables[dest])[source][dest] = cost

    def computeDV(self, router_id):
        distance_vector = {router_id: 0}
        # Update the distance vector from self.graph
        for source, dest, cost in self.graph:
            if source != router_id:
                continue
            if dest not in self.routing_tables:
                self.routing_tables[dest] = {}
            self.routing_tables[dest][source] = cost

        # Iterate over the routing tables to compute the distance vector
        for dest, routes in self.routing_tables.items():
            if dest == router_id:
                continue
            min_cost = float('inf')
            for source, cost in routes.items():
                if source == router_id:
                    continue
                if source in distance_vector:
                    min_cost = min(min_cost, distance_vector[source] + cost)
            distance_vector[dest] = min_cost

        return distance_vector






    

    

    

    

                