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
            block_height = int(line_split[0])
            if block_height > end_height:
                break
            elif block_height >= start_height and block_height <= end_height:
                block_hashes.append(line_split[9].strip())
    return block_hashes

def write_tx_types_data(block_hashes, start_height, end_height):
    # Count the number of transactions output of each type
    # Create or reset the file
    with open(f'./txs_types_stats/{start_height}_to_{end_height}.csv', 'w') as f1:
        f1.write('')
    data_by_date = {}
    cur_date = ""
    for block_hash in block_hashes:
        block = bitrpc.get_block(block_hash, 2)
        block_time = block['time']
        block_time = datetime.utcfromtimestamp(block_time).strftime('%Y-%m-%d')
        if block_time != cur_date and cur_date != "":
            with open(f'./txs_types_stats/{start_height}_to_{end_height}.csv', 'a') as f1:
                f1.write(cur_date + ', ')
                for script_type in data_by_date[cur_date]:
                    # Write type
                    f1.write(script_type + ': ')
                    f1.write(str(data_by_date[cur_date][script_type]) + ', ')
                f1.write('\n')
            cur_date = block_time
            del data_by_date[cur_date]
        for tx in block['tx']:
            for vout in tx['vout']:
                script_type = vout['scriptPubKey']['type']
                if block_time in data_by_date:
                    if script_type in data_by_date[block_time]:
                        data_by_date[block_time][script_type] += 1
                    else:
                        data_by_date[block_time][script_type] = 1
                else:
                    data_by_date[block_time] = {}
                    data_by_date[block_time][script_type] = 1

    # Write down last day
    with open(f'./txs_types_stats/{start_height}_to_{end_height}.csv', 'a') as f1:
        f1.write(cur_date + ', ')
        for script_type in data_by_date[cur_date]:
            # Write type
            f1.write(script_type + ': ')
            f1.write(str(data_by_date[cur_date][script_type]) + ', ')
        f1.write('\n')

    # pubkey, witness_v0_keyhash: 4763, nulldata: 22, pubkeyhash: 2885, scripthash: 4480, witness_v0_scripthash: 663, witness_v1_taproot: 52
    # with open(f'./txs_types_stats/{start_height}_to_{end_height}.csv', 'w') as f1:
    #     for date in data_by_date:
    #         f1.write(date + ', ')
    #         for script_type in data_by_date[date]:
    #             # Write type
    #             f1.write(script_type + ': ')
    #             f1.write(str(data_by_date[date][script_type]) + ', ')
    #         f1.write('\n')

# main function
if __name__ == "__main__":
    start_height = int(input("Enter a starting block height: "))
    end_height = int(input("Enter an ending block height: "))
    if start_height > end_height:
        print("Error: starting block is greater than ending block")
        exit(1)
    # Get all block hashes
    block_hashes = block_hashes_by_heights(start_height, end_height)
    
    # Get the number of transactions of each type per day
    write_tx_types_data(block_hashes, start_height, end_height)
    