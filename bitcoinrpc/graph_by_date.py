# Add documentation saying that every time is in UTC
import os
from bitcoinrpc import BitcoinRpc
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt

# Networkx
# https://networkx.org/documentation/stable/tutorial.html

# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']
rpc_host = "localhost"
rpc_port = 8332
bitrpc = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

# TODO: when excel file does not have data, it will return error or call RPC manually
# Get transaction data of given date (start_date is included, end_date is excluded)
def tx_graph_date(start_date, end_date):
    # Convert date in format yyyy/mm/dd to UNIX epoch time
    start_timestamp = datetime.strptime(start_date, "%Y/%m/%d").timestamp()
    end_timestamp = datetime.strptime(end_date, "%Y/%m/%d").timestamp()
    graph = tx_graph_timestamp(start_timestamp, end_timestamp)
    nx.write_weighted_edgelist(graph, f"./txs_graph/date/txs_{start_date}_{end_date}.edgelist")
    print(f"Graph saved to ./txs_graph/date/txs_{start_date}_{end_date}.edgelist")
    return f"./txs_graph/date/txs_{start_timestamp}_{end_timestamp}.edgelist"

# Get transaction data of given datetime (start_datetime is included, end_datetime is excluded)
# Format of datetime: %Y/%m/%d %H:%M:%S (always UTC)
def tx_graph_datetime(start_datetime, end_datetime):
    # Convert datetime in format yyyy/mm/dd hh:mm:ss to UNIX epoch time
    start_datetime = datetime.strptime("2023/01/01 09:00:00", "%Y/%m/%d %H:%M:%S")
    end_datetime = datetime.strptime("2023/01/01 09:15:00", "%Y/%m/%d %H:%M:%S")
    start_timestamp = start_datetime.timestamp()
    end_timestamp = end_datetime.timestamp()
    graph = tx_graph_timestamp(start_timestamp, end_timestamp)
    start_in_filename = start_datetime.strftime("%Y.%m.%d.%H.%M.%S")
    end_in_filename = end_datetime.strftime("%Y.%m.%d.%H.%M.%S")
    nx.write_weighted_edgelist(graph, f"./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist")
    print(f"Graph saved to ./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist")
    return f"./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist"

# Block data format
def tx_graph_timestamp(start_timestamp, end_timestamp):
    # Get all block hashes
    block_hashes = block_hashes_by_stamps(start_timestamp, end_timestamp)

    transactions = []

    for block_hash in block_hashes:
        print("Getting block data for block hash: " + block_hash)
        block_data = bitrpc.get_block(block_hash, 2)
        print("Got block data for block hash: " + block_hash)
        transactions.extend(block_data['tx'])

    # TODO
    # Locking script = scriptPubKey
    return txs_to_multi_graph(transactions)

def script_to_address(script):
    # TODO IMPORTANT (after reading transaction section of Mastering Bitcoin)
    pass

def parse_tx(tx, miner_address):
    # Calculate the total amount of inputs and outputs
    # TODO: for now, only consider transactions that contain `address` field
    input_addr_amount = []
    inputs = tx["vin"]
    is_coinbase = False
    for input in inputs:
        if 'coinbase' in input:
            is_coinbase = True
            continue
        ind = input["vout"]
        prev_output = bitrpc.get_raw_transaction(input["txid"], True)['vout'][ind]
        input_addr_amount.append((prev_output['scriptPubKey']['address'], prev_output['value']))
    
    output_addr_amount = []
    outputs = tx["vout"]
    for output in outputs:
        # We skip null data, but need to do more research on what data we are skipping
        if 'address' not in output['scriptPubKey']:
            continue
        if is_coinbase:
            input_addr_amount.append((-1, output['value']))
            miner_address[0] = output['scriptPubKey']['address']
        output_addr_amount.append((output['scriptPubKey']['address'], output['value']))

    # Check if input and output values are equal (including transaction fee)
    sum_input = sum([input_amount for _, input_amount in input_addr_amount])
    sum_output = sum([output_amount for _, output_amount in output_addr_amount])
    tx_fee = sum_input - sum_output

    edges = []
    # For each input, create an edge to output address until all values are used
    # if all values are used, then create an edge to the next input address
    output_ind = 0

    # transaction fee (for now, just add output to miner)
    if tx_fee > 0:
        output_addr_amount.append((miner_address[0], tx_fee))

    for input_addr, input_amount in input_addr_amount:
        while output_ind < len(output_addr_amount):
            output_addr, output_amount = output_addr_amount[output_ind]
            if input_amount == 0:
                break
            if input_amount >= output_amount:
                edges.append((input_addr, output_addr, output_amount))
                input_amount -= output_amount
                output_ind += 1
            else:
                edges.append((input_addr, output_addr, input_amount))
                output_amount -= input_amount
                # Update output amount in place 
                output_addr_amount[output_ind] = (output_addr, output_amount)
                input_amount = 0
    
    # Check if all input values are used (sum values in edges)
    sum_edges = round(sum([edge_amount for _, _, edge_amount in edges]), 8)
    if sum_edges != round(sum_input, 8):
        print("ERROR: sum of edges is not equal to sum of input values")
        print("sum_edges", sum_edges)
        print("sum_input", sum_input)
        print("edges", edges)
        print("input_addr_amount", input_addr_amount)
        print("output_addr_amount", output_addr_amount)
        return []
    
    return edges

def parse_txs(txs):
    result = []
    miner_address = [None]
    for tx in txs:
        # TODO clean up
        test = parse_tx(tx, miner_address)
        # TODO delete
        print(test)
        result.extend(test)
    return result

def txs_to_multi_graph(txs):
    # Create graph
    MG=nx.MultiDiGraph()    
    # Add nodes
    print("start parsing txs")
    MG.add_weighted_edges_from(parse_txs(txs))
    return MG

def block_heights_by_stamps(start_timestamp, end_timestamp):
    block_heights = []
    with open('./assets/blocks_data_total.csv', 'r') as f1:
        lines = f1.readlines()
        # TODO: maybe stop after extra 11 lines if slow
        # Scan through blockchain until it sees the end date, and 11 extra since 
        # the chain accepts a block that is higher than median timestamp of 11 blocks
        # https://bitcoin.stackexchange.com/questions/915/why-dont-the-timestamps-in-the-block-chain-always-increase
        lines = lines[1:]
        for line in lines:
            block_time = line.split(',')[2]
            # Convert type time_utc to UNIX epoch time
            block_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            if block_time >= start_timestamp and block_time < end_timestamp:
                block_heights.append(int(line.split(',')[0]))
    return block_heights

def block_hashes_by_stamps(start_timestamp, end_timestamp):
    block_hashes = []
    with open('./assets/blocks_data_total.csv', 'r') as f1:
        lines = f1.readlines()
        # TODO: maybe stop after extra 11 lines if slow
        # Scan through blockchain until it sees the end date, and 11 extra since 
        # the chain accepts a block that is higher than median timestamp of 11 blocks
        # https://bitcoin.stackexchange.com/questions/915/why-dont-the-timestamps-in-the-block-chain-always-increase
        lines = lines[1:]
        for line in lines:
            line_split = line.split(',')
            block_time = line_split[2]
            # Convert type time_utc to UNIX epoch time
            block_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            if block_time >= start_timestamp and block_time < end_timestamp:
                if len(line_split) < 10:
                    block_hashes.append("0")
                else:
                    block_hashes.append(line_split[9].strip())
    return block_hashes

def draw_graph(MG):
    plt.figure(1)
    nx.draw(MG, with_labels=True, font_weight='bold')
    plt.show()

# main function
if __name__ == "__main__":
    # bitcoinrpc test
    # print(bitrpc.list_unspent())

    # Get transaction of given time range
    filename = tx_graph_datetime("2023/01/01 00:00:00", "2023/01/02 00:00:00")
    print(f"Reading {filename}")
    MG = nx.read_weighted_edgelist(f"{filename}")
    print(dict(MG.degree(weight='weight')))

    # Get transaction data of given block hash
    # print(bitrpc.get_block("00000000000000000000ab6f2ba297568c9f7b1cdabb02ace83f1c18ac0642a3", 2))

    # Test parse_tx
    # Read from test.txt and load entire file into JSON, and run parse_tx
    # block_data = bitrpc.get_block("00000000000000000000ab6f2ba297568c9f7b1cdabb02ace83f1c18ac0642a3", 2)
    # txs = block_data['tx']
    # print(parse_txs(txs))

