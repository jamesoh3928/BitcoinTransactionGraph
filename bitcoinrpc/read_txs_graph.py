import networkx as nx

# Read graph file in txs_graph
def read_txs_graph(file_path):
    print(f"Reading {file_path}")
    MG = nx.read_weighted_edgelist(f"{file_path}")
    # Add things you want to do
    print(dict(MG.degree(weight='weight')))

# main function
if __name__ == "__main__":
    # Get transaction of given time range
    read_txs_graph("txs_graph/datetime/txs_2023.01.01.09.00.00_2023.01.01.09.15.00.edgelist")