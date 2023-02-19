import os
import requests
import json
from bitcoinrpc.bitcoinrpc import BitcoinRpc

# TODO: maybe we don't need jsonrpc
# from jsonrpc import ServiceProxy

# Get environment variables
rpc_user = os.environ['RPC_USER']
rpc_password = os.environ['RPC_PASSWORD']
rpc_host = "localhost"
rpc_port = 8332

bitcp = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

# Block count
print(bitcp.get_block_count())
print(type(bitcp.get_block_count()))