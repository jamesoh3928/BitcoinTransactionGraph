# All dates in this program in based on UTC time

import os
from bitcoinrpc import BitcoinRpc
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt

# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']

# Set up bitcoin rpc
rpc_host = "localhost"
rpc_port = 8332
bitrpc = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

def tx_graph_datetime(start_datetime, end_datetime):
    """ Core function that is being currently used in this program
    Get transaction data of given datetime (start_datetime is included, end_datetime is excluded)
    Format of datetime: %Y/%m/%d %H:%M:%S (always UTC)
    """
    # Convert datetime in format yyyy/mm/dd hh:mm:ss to UNIX epoch time
    start_datetime = datetime.strptime(start_datetime, "%Y/%m/%d %H:%M:%S")
    end_datetime = datetime.strptime(end_datetime, "%Y/%m/%d %H:%M:%S")
    filename = write_graph(start_datetime, end_datetime)
    print(f"Graph saved to {filename}")
    return filename

def write_graph(start_datetime, end_datetime):
    """Directly write graph data to the file instead of creating networkx object
    Parse each transaction and write parsed output to the file 
    "./txs_graph/datetime_with_height/txs_{start_in_filename}_{end_in_filename}.edgelist"
    """
    start_timestamp = start_datetime.timestamp()
    end_timestamp = end_datetime.timestamp()
    start_in_filename = start_datetime.strftime("%Y.%m.%d.%H.%M.%S")
    end_in_filename = end_datetime.strftime("%Y.%m.%d.%H.%M.%S")
    filename = f"./txs_graph/datetime_with_height/txs_{start_in_filename}_{end_in_filename}.edgelist"

    # Get all block hashes
    block_hashes = block_hashes_by_stamps(start_timestamp, end_timestamp)

    # Create or reset the file
    with open(filename, 'w') as f1:
        f1.write('')

    for block_hash in block_hashes:
        print("Getting block data for block hash: " + block_hash)
        block_data = bitrpc.get_block(block_hash, 2)
        print("Got block data for block hash: " + block_data['hash'])
        block_height = block_data['height']
        miner_address = [None]
        for tx in block_data['tx']:
            transactions = parse_tx(tx, miner_address)
            for transaction in transactions:
                # from, to, amount, block_height
                print(transaction)
                with open(filename, 'a') as f:
                    f.write(f"{transaction[0]}, {transaction[1]} {transaction[2]} {block_height}\n")

    return filename

def tx_graph_date(start_date, end_date):
    """ -----Not being used currently-----
    Get transaction data of given date (start_date is included, end_date is excluded)
    """
    # Convert date in format yyyy/mm/dd to UNIX epoch time
    start_timestamp = datetime.strptime(start_date, "%Y/%m/%d").timestamp()
    end_timestamp = datetime.strptime(end_date, "%Y/%m/%d").timestamp()
    graph = tx_graph_timestamp(start_timestamp, end_timestamp)
    nx.write_weighted_edgelist(graph, f"./txs_graph/date/txs_{start_date}_{end_date}.edgelist")
    print(f"Graph saved to ./txs_graph/date/txs_{start_date}_{end_date}.edgelist")
    return f"./txs_graph/date/txs_{start_timestamp}_{end_timestamp}.edgelist"

def tx_graph_timestamp(start_timestamp, end_timestamp):
    """Not being used currently
    Create networkx graph object of transaction for given timestamp
    """
    # Get all block hashes
    block_hashes = block_hashes_by_stamps(start_timestamp, end_timestamp)

    transactions = []
    for block_hash in block_hashes:
        print("Getting block data for block hash: " + block_hash)
        block_data = bitrpc.get_block(block_hash, 2)
        print("Got block data for block hash: " + block_hash)
        transactions.extend(block_data['tx'])

    return txs_to_multi_graph(transactions)

def parse_tx(tx, miner_address):
    """ Parse transaction in the format of (input addr, output addr, amount)
    Add edge that represents transcation fee to given miner address (the type of miner address \
    should be a list, e.g. [miner_addr]). 
    If there are multiple inputs and outputs in the transactions, it consumes each input in given
    order to match with output For instance, if input1 = 2 and input2 = 4, output1 = 3 and output2 = 2, 
    there will be edges of (input1_addr, output1_addr, 2), (input2_addr, output1_addr1, 1),
    (input2_addr, output2_addr, 3), (input2_addr, miner_addr, 1)).
    """
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
        if 'address' not in prev_output['scriptPubKey']:
            continue
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

    # For each input, create an edge to output address until all values are used
    # if all values are used, then create an edge to the next input address
    edges = []
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
    """ Parse all the transactions in the given list.
    """
    result = []
    miner_address = [None]
    for tx in txs:
        edges = parse_tx(tx, miner_address)
        result.extend(edges)
    return result

def txs_to_multi_graph(txs):
    """ Create networkx multi graph object of transaction for given transactions
    """
    # Create graph
    MG=nx.MultiDiGraph()    
    # Add nodes
    print("start parsing txs")
    MG.add_weighted_edges_from(parse_txs(txs))
    return MG

def block_heights_by_stamps(start_timestamp, end_timestamp):
    """Get all block heights for given timestamp range
    If our 'assets/blocks_data_total.csv' file does not contain block data for the given timestamp range,
    then we will return an empty list (if it does, try running get_block_data.py to add more block data)
    """

    block_heights = []
    with open('./assets/blocks_data_total.csv', 'r') as f1:
        lines = f1.readlines()
        lines = lines[1:]
        for line in lines:
            block_time = line.split(',')[2]
            # Convert type time_utc to UNIX epoch time
            block_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            if block_time >= start_timestamp and block_time < end_timestamp:
                block_heights.append(int(line.split(',')[0]))
    return block_heights

def block_hashes_by_stamps(start_timestamp, end_timestamp):
    """Get all block hashes for given timestamp range
    If our 'assets/blocks_data_total.csv' file does not contain block data for the given timestamp range,
    then we will return an empty list (if it does, try running get_block_data.py to add more block data)
    """
    
    block_hashes = []
    with open('./assets/blocks_data_total.csv', 'r') as f1:
        lines = f1.readlines()
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

# Currently, not drawing visible graph (too many edges)
def draw_graph(MG):
    """ Draw graph of given multigraph
    """
    plt.figure(1)
    nx.draw(MG, with_labels=True, font_weight='bold')
    plt.show()

# main function
if __name__ == "__main__":
    # Get transaction of given time range
    start_datetime = input("Enter start datetime (YYYY/MM/DD HH:MM:SS): ")
    end_datetime = input("Enter end datetime (YYYY/MM/DD HH:MM:SS): ")
    filename = tx_graph_datetime(start_datetime, end_datetime)
