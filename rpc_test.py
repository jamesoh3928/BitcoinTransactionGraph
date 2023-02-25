import os
from bitcoinrpc.bitcoinrpc import BitcoinRpc

# TODO: maybe we don't need jsonrpc
# from jsonrpc import ServiceProxy

# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']
rpc_host = "localhost"
rpc_port = 8332

bitcp = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

# Block count
# block_count = bitcp.get_block_count()
# print(block_count)
# print(type(block_count))

# Blockchain info
# blockchain_info = bitcp.get_blockchain_info()
# print(blockchain_info)
# print(type(blockchain_info))

# Block
block_hash = "0000000000000000000576954cbe6d679b00dac060459b6b2c31155a869839ad"
# block = bitcp.get_block(block_hash, 2)
# print(block['tx'][1])
# print(len(block['tx']))
# print(block)
# print(type(block))
print(bitcp.get_block(block_hash, 1))
# Note: the hexadecimal represnetation is very long
# print(bitcp.get_block(block_hash, 0))

# Raw transaction
# txid = "2b57f1d6abaed67ce6c64f144b708a8955cc9ecfdd8086fd4d6da10bec67cf2a"
# blockhash = "0000000000000000000576954cbe6d679b00dac060459b6b2c31155a869839ad"
# raw_transaction1 = bitcp.get_raw_transaction(txid, True, blockhash)
# print(raw_transaction1)
# raw_transaction2 = bitcp.get_raw_transaction(txid, False, blockhash)
# print(raw_transaction2)

# Decode raw transaction
# raw_transaction = "010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff6403a9dc0b2cfabe6d6d72f32ad84e77ad37136a756cdb25b2fcedf1183c253fbfff559a26b04c5c003310000000f09f909f092f4632506f6f6c2f6e00000000000000000000000000000000000000000000000000000000000000000000000500b80100000000000004f39d6026000000001976a914c825a1ecf2a6830c4401620c3a16f1995057c2ab88ac0000000000000000266a24aa21a9edea9878243548859c3ebe240738a7b40c5e5c95da1b0c21b8409c91cff7523c500000000000000000266a244861746861cf505fd19bbb2e23f298a195db01a4b1086866be496d214043e96b0589666300000000000000002c6a4c2952534b424c4f434b3aabc0dbe3e53c470e79ccc39a5452fc304275111fbc364c93da1a732a004d529f01200000000000000000000000000000000000000000000000000000000000000000e6bb7e3e"
# decoded_transaction = bitcp.decode_raw_transaction(raw_transaction)
# print(decoded_transaction)
# print(type(decoded_transaction))

# Get mempool transactions
# mempool_transactions2 = bitcp.get_raw_mempool(True, False)
# print(mempool_transactions2)
# print(len(mem))
# mempool_transactions3 = bitcp.get_raw_mempool(False, True)
# print(mempool_transactions3)
# mempool_transactions4 = bitcp.get_raw_mempool()
# print(mempool_transactions4)
# print(type(mempool_transactions2))