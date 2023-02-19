import requests
import json

class BitcoinRpc():
    def __init__(self, rpc_user, rpc_password, rpc_host, rpc_port):
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port

    def get_block_count(self) -> int:
        """Returns the number of blocks of Bitcoin.

        Returns:
            int: The current block count
        """
        url = f"http://{self.rpc_user}:{self.rpc_password}@{self.rpc_host}:{self.rpc_port}"
        headers = {'content-type': 'application/json'}
        payload = json.dumps({
            "method": "getblockcount",
            "params": [],
            "jsonrpc": "2.0",
            "id": "0"
        })
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            result = json.loads(response.text)['result']
            return result
        else:
            print("Error during get_block_count:", response.status_code, response.reason)
            return -1