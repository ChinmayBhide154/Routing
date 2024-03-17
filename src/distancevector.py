from network import Network

graph = []

network = Network(graph)
network.build_network("C:/Git Repositories/Routing/src/topology.txt")
print(network.graph)