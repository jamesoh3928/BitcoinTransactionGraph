# Program that gets the number of transactions of each type per day

import os
from bitcoinrpc import BitcoinRpc
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt

# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']
rpc_host = "localhost"
rpc_port = 8332
bitrpc = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

def block_hashes_by_heights(start_height, end_height):
    block_hashes = []
    with open('./assets/blocks_data_total.csv', 'r') as f1:
        lines = f1.readlines()
        lines = lines[1:]
        for line in lines:
            line_split = line.split(',')
            block_height = int(line_split[1])
            if block_height > end_height:
                break
            elif block_height >= start_height and block_height <= end_height:
                block_hashes.append(line_split[9].strip())
    return block_hashes

# main function
if __name__ == "__main__":
    start_height = int(input("Enter a starting block height: "))
    end_height = int(input("Enter an ending block height: "))
    if start_height > end_height:
        print("Error: starting block is greater than ending block")
        exit(1)
    # Get all block hashes
    block_hashes = block_hashes_by_heights(start_height, end_height)

    # Count the number of transactions of each type