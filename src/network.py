class Network:
    def __init__(self, graph):
        self.graph = graph

    def build_network(self, file):
        with open(file, 'r') as topology:
            for line in topology:
                node1, node2, cost = map(int, line.split())
                self.graph.append([node1, node2, cost])

                