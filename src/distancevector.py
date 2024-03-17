from network import Network
import sys

def dv():
    return 1


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