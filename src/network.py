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
        INFINITY = float('inf')
        routers = set()
        links = []
        for source, dest, cost in self.graph:
            routers.add(source)
            routers.add(dest)
            links.append((source, dest, cost))

        distance, nexthop = self.bellman_ford(router_id, routers, links)

        distance_vector = {}
        for dest in distance:
            if dest != router_id:
                distance_vector[dest] = distance[dest]

        return distance_vector
    
    def bellman_ford(self, dst, routers, links):
        INFINITY = float('inf')
        distance = {}
        nexthop = {}
        
        for r in routers:
            distance[r] = INFINITY
            nexthop[r] = None

        distance[dst] = 0

        for _ in range(len(routers) - 1):
            for (r1, r2, dist) in links:
                if distance[r1] + dist < distance[r2]:
                    distance[r2] = distance[r1] + dist
                    nexthop[r2] = r1

        return distance, nexthop






    

    

    

    

                