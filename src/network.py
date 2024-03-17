class Network:
    def __init__(self, topologyFile, messageFile, changesFile):
        self.topologyFile = topologyFile
        self.messageFile = messageFile
        self.changesFile = changesFile
        self.graph = []
        self.messages = []

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

    

    

                