# TODO: transfer bitcoin data to graph objects
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
    start_timestamp = datetime.strptime(start_datetime, "%Y/%m/%d %H:%M:%S").timestamp()
    end_timestamp = datetime.strptime(end_datetime, "%Y/%m/%d %H:%M:%S").timestamp()
    graph = tx_graph_timestamp(start_timestamp, end_timestamp)
    start_in_filename = start_timestamp.strftime("%Y.%m.%d.%H.%M.%S")
    end_in_filename = end_timestamp.strftime("%Y.%m.%d.%H.%M.%S")
    nx.write_weighted_edgelist(graph, "./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist")
    print("Graph saved to ./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist")
    return "./txs_graph/datetime/txs_{start_in_filename}_{end_in_filename}.edgelist"

# Block data format
# Verbosity 2
# {'hash': '000000008be5151fa84c4eeec998e61cbcfdaf8123d610381d7e3c8c25af57d2', 'confirmations': 765338, 'height': 13367, 'version': 1, 'versionHex': '00000001', 'merkleroot': 'b43ef9ae423dcbcf0d0f838af1a9e3731d5a4ce9ebb0f8d12c9ab9c0f3f6d164', 'time': 1241514988, 'mediantime': 1241511732, 'nonce': 1714531103, 'bits': '1d00ffff', 'difficulty': 1, 'chainwork': '0000000000000000000000000000000000000000000000000000343834383438', 'nTx': 1, 'previousblockhash': '000000009ec410c470dd1d1e4dfbd6f67041893512903509ebe97e099cbeb548', 'nextblockhash': '000000001563e67bc1ed5022e837d97d34c3e78ed33e02d3051e177542c2bd3b', 'strippedsize': 216, 'size': 216, 'weight': 864, 'tx': [{'txid': 'b43efx9ae423dcbcf0d0f838af1a9e3731d5a4ce9ebb0f8d12c9ab9c0f3f6d164', 'hash': 'b43ef9ae423dcbcf0d0f838af1a9e3731d5a4ce9ebb0f8d12c9ab9c0f3f6d164', 'version': 1, 'size': 135, 'vsize': 135, 'weight': 540, 'locktime': 0, 'vin': [{'coinbase': '04ffff001d025e03', 'sequence': 4294967295}], 'vout': [{'value': 50.0, 'n': 0, 'scriptPubKey': {'asm': '044de751fd55346bda4070074b493981d024c26f2c3ebdf61822b642f8568e056b6ab0f26da7486f9f057eb31093154ee0740584e7347ae8c3212a66431f9d0353 OP_CHECKSIG', 'desc': 'pk(044de751fd55346bda4070074b493981d024c26f2c3ebdf61822b642f8568e056b6ab0f26da7486f9f057eb31093154ee0740584e7347ae8c3212a66431f9d0353)#fk322vlq', 'hex': '41044de751fd55346bda4070074b493981d024c26f2c3ebdf61822b642f8568e056b6ab0f26da7486f9f057eb31093154ee0740584e7347ae8c3212a66431f9d0353ac', 'type': 'pubkey'}}], 'hex': '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0804ffff001d025e03ffffffff0100f2052a010000004341044de751fd55346bda4070074b493981d024c26f2c3ebdf61822b642f8568e056b6ab0f26da7486f9f057eb31093154ee0740584e7347ae8c3212a66431f9d0353ac00000000'}]}
def tx_graph_timestamp(start_timestamp, end_timestamp):
    # Get all of blocks' heights within timerange
    # block_heights = block_heights_by_stamps(start_timestamp, end_timestamp)

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
    # TODO IMPORTANT
    pass

def parse_tx(tx):
    # Calculate the total amount of inputs and outputs
    # TODO: for now assume that transaction data contains address information
    # TEST with: 4ef6d37bc1110e1a49ab2f1724c82a5a3bd38bc25777284d8b13894059e77eae
    # [{'txid': 'd3df0446522e514be223fe5affdce073222c113be2be8101e531d425e2598585', 'vout': 1, 'scriptSig': {'asm': '30440220509f2115e5f611bf0de6c5c2b8427f201586f4ce2ecb238b157098ac7a9bfdb202201de2ee97e3b2175ab037f4f43c54d6ba6601645ef8387bb3dedbbea6dd262017[ALL] 03548d2343a187741496b4e7983f962ec26c70d69d1b047877646453b8986f5c85', 'hex': '4730440220509f2115e5f611bf0de6c5c2b8427f201586f4ce2ecb238b157098ac7a9bfdb202201de2ee97e3b2175ab037f4f43c54d6ba6601645ef8387bb3dedbbea6dd262017012103548d2343a187741496b4e7983f962ec26c70d69d1b047877646453b8986f5c85'}, 'sequence': 4294967293}]
    input_addr_amount = []
    inputs = tx["vin"]
    for input in inputs:
        if 'coinbase' in input:
            continue
        ind = input["vout"]
        prev_output = bitrpc.get_raw_transaction(input["txid"], True)['vout'][ind]
        input_addr_amount.append((prev_output['scriptPubKey']['address'], prev_output['value']))
    
    output_addr_amount = []
    outputs = tx["vout"]
    for output in outputs:
        # print(output)
        # TODO: we can skip null data, but need to do more research on what data we are skipping
        if 'address' not in output['scriptPubKey']:
            continue
        if 'coinbase' in input:
            # TODO maybe come up with better representation
            input_addr_amount.append((-1, output['value']))
        output_addr_amount.append((output['scriptPubKey']['address'], output['value']))

    # TODO: check if input and output values are equal (including transaction fee)
    sum_input = sum([input_amount for _, input_amount in input_addr_amount])
    sum_output = sum([output_amount for _, output_amount in output_addr_amount])
    tx_fee = sum_input - sum_output
    # if 'coinbase' not in input:
    #     sum_output += tx['fee']
    # if sum_input != sum_output:
    #     print("ERROR: input and output values are not equal")
    #     print("sum_input", sum_input)
    #     print("sum_output (including transaction fee)", sum_output)
    #     print("input_addr_amount", input_addr_amount)
    #     print("output_addr_amount", output_addr_amount)
    #     print("tx fee", tx['fee'])
    #     # print("tx", tx)
    #     return []

    edges = []
    # For each input, create an edge to output address until all values are used
    # if all values are used, then create an edge to the next input address
    output_ind = 0
    # TODO: transaction fee (for now, just add to first input address)
    if tx_fee > 0:
        edges.append((input_addr_amount[0][0], -1, tx_fee))
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
    
    # TODO: change this to check if all input values are used (sum values in edges)
    sum_edges = round(sum([edge_amount for _, _, edge_amount in edges]), 8)
    if sum_edges != round(sum_input, 8):
        print("ERROR: sum of edges is not equal to sum of input values")
        print("sum_edges", sum_edges)
        print("sum_input", sum_input)
        print("edges", edges)
        print("input_addr_amount", input_addr_amount)
        print("output_addr_amount", output_addr_amount)
        # print("tx", tx)
        return []
    # if output_ind < len(output_addr_amount):
    #     print("ERROR: not all output values are used")
    # print("edges", edges)
    return edges

def parse_txs(txs):
    result = []
    for tx in txs:
        result.extend(parse_tx(tx))
    return result

def txs_to_multi_graph(txs):
    # Create graph
    MG=nx.MultiGraph()    
    # Add nodes
    print("start parsing txs")
    # print(parse_txs(txs))
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
    with open('./assets/blocks_data_total_copy.csv', 'r') as f1:
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
    # Get transaction of given time range
    filename = tx_graph_datetime("2023/01/01 00:00:00", "2023/01/01 11:59:59")
    print(f"Reading {filename}")
    MG = nx.read_weighted_edgelist(f"{filename}")
    print(dict(MG.degree(weight='weight')))
    # G = nx.Graph()
    # G.add_edge('A', 'B', weight=2.0)
    # G.add_edge('B', 'C', weight=3.0)

    # nx.write_weighted_edgelist(G, "txs_graph/datetime/txs_test_test.edgelis")

