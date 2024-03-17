from network import Network
import sys

INFINITY = 99999

def bellman_ford(dst, routers, links):
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






if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("wrong number of arguments provided to program")
        sys.exit(1)
    topologyFile = sys.argv[1]
    messageFile = sys.argv[2]
    changesFile = sys.argv[3]

    network = Network(topologyFile, messageFile, changesFile)
    network.build_network()
    #print(network.graph)