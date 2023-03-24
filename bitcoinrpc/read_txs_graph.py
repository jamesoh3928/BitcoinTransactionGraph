import networkx as nx

# Read graph file in txs_graph
def read_txs_graph(file_path):
    # read the edge list file
    with open(file_path) as f:
        edges = [line.strip().split() for line in f]

    # create a new directed multigraph
    MDG = nx.MultiDiGraph()

    # add the edges to the graph
    for edge in edges:
        MDG.add_edge(edge[0], edge[1], weight=float(edge[2]))

    # TODO delete
    # print the nodes and edges in the graph
    print("Nodes:", MDG.nodes())
    print("Edges:", MDG.edges(data=True))
    return MDG

# main function
if __name__ == "__main__":
    # Get transaction of given time range
    read_txs_graph("txs_graph/datetime/txs_2023.01.01.09.00.00_2023.01.01.09.15.00.edgelist")