from dijkstar import Graph, find_path


if __name__ == '__main__':
    # API Documentation: https://pypi.org/project/Dijkstar/
    graph = Graph()
    graph.add_edge(1, 2, 8)
    graph.add_edge(2, 3, 4)
    graph.add_edge(2, 5, 4)
    graph.add_edge(4, 1, 1)
    graph.add_edge(4, 5, 1)
    path_info = find_path(graph, 1, 3)
    path = path_info.nodes
    print(path)
    
