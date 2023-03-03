import requests
import json

class BitcoinRpc():
    def __init__(self, rpc_user, rpc_password, rpc_host, rpc_port):
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.url = f"http://{self.rpc_user}:{self.rpc_password}@{self.rpc_host}:{self.rpc_port}"
        self.headers = {'content-type': 'application/json'}

    def get_block_count(self) -> int:
        """Returns the number of blocks of Bitcoin.

        Returns:
            int: The current block count
        """
        payload = json.dumps({
            "method": "getblockcount",
            "params": [],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_block_count:", response.status_code, response.reason)
            return -1
        
    def get_block_hash(self, height):
        """Returns hash of block in best-block-chain at height provided.

        Args:
            height (int): The height index

        Returns:
            string: The block hash

        """
        payload = json.dumps({
            "method": "getblockhash",
            "params": [height],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_block_hash:", response.status_code, response.reason)
            return -1
        
    def get_blockchain_info(self):
        """Returns the blockchain info. Include information of chain, blocks, headers, bestblockhash, difficulty, time, mediantime, verificationprogress, initialblockdownload, chainwork, size_on_disk, pruned, warnings.

        Returns:
            json: blockchain information

        """
        payload = json.dumps({
            "method": "getblockchaininfo",
            "params": [],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_blockchain_info:", response.status_code, response.reason)
            return -1

    def get_block(self, block_hash, verbosity=1):
        """Returns information about the block with the given hash.

        Args:
            block_hash (string): The block hash
            verbosity (int): 0 for hex encoded data, 1 for a json object, and 2 for json object with transaction data.

        Returns:
            json: block information

        """
        payload = json.dumps({
            "method": "getblock",
            "params": [block_hash, verbosity],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_block:", response.status_code, response.reason)
            return -1
        
    def get_raw_transaction(self, txid, verbose, blockhash=None):
        """Returns raw transaction representation for given transaction id. 

        By default this function only works for mempool transactions. 
        When called with a blockhash argument, getrawtransaction will return the transaction if the specified block is available and the transaction is found in that block. 
        When called without a blockhash argument, getrawtransaction will return the transaction if it is in the mempool, or if -txindex is enabled and the transaction is in a block in the blockchain.

        Args:
            txid (string): The transaction id
            verbose (boolean): If false, return a string, otherwise return a json object
            blockhash (string): The block in which to look for the transaction

        Returns:
            json: transaction information

        """

        if blockhash is None:
            payload = json.dumps({
                "method": "getrawtransaction",
                "params": [txid, verbose],
                "jsonrpc": "2.0",
                "id": "0"
            })
        else:
            payload = json.dumps({
                "method": "getrawtransaction",
                "params": [txid, verbose, blockhash],
                "jsonrpc": "2.0",
                "id": "0"
            })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_raw_transaction:", response.status_code, response.reason)
            return -1
        
    def decode_raw_transaction(self, hexstring):
        """Return a JSON object representing the serialized, hex-encoded transaction. Bitcoin JSON RPC also takes iswitness as a boolean argument, which shows whether the transaction hex is a serialized witness transaction. However, we decided to just use heuristic which is a default option.

        Args:
            hexstring (string): The transaction hex string

        Returns:
            json: transaction information

        """
        payload = json.dumps({
            "method": "decoderawtransaction",
            "params": [hexstring],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during decode_raw_transaction:", response.status_code, response.reason)
            return -1

    def get_raw_mempool(self, verbose=False, mempool_sequence=False):
        """Returns all transaction ids in memory pool as a json array of string transaction ids.

        Args:
            verbose (boolean): If false, return a list of transaction ids, otherwise return a json object
            mempool_sequence (boolean): If true, returns transactions as a json array of objects, each object contains a sequence id, transaction id and fee (in satoshis). Mempool sequence number is priority order for miners.

        Returns:
            json: transaction information

        """
        if verbose and mempool_sequence:
            print("Error during get_raw_mempool: verbose and mempool_sequence cannot be true at the same time.")
            return -1
        
        payload = json.dumps({
            "method": "getrawmempool",
            "params": [verbose, mempool_sequence],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_raw_mempool:", response.status_code, response.reason)
            return -1
        
    # TODO: 
    # savemempool
    # listunspent
    # gettxout
