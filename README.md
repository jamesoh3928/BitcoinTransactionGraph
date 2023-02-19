# Bitcoin Transaction Graph

## Setup
### Virtual enviromnet/Install dependencies
1. Create virtual env: `python3 -m venv <venv_name>`
2. Activate virtual env: `source <venv_name>/bin/activate` - different command depending on platform: https://docs.python.org/3/library/venv.html#:~:text=Shell-,Command,-to%20activate%20virtual
- For Windows: source graph/Scripts/activate
3. To deactivate virtual env: `deactivate`
4. Within the virtual environment, run `pip install -r requirements.txt` in the terminal (TODO: I have to froze the dependencies after I am done with development)

### Set Environment Variables
You would have to set `RPC_USER` and `RPC_PASSWORD` as environment variables, since we do not want to include sensitive information in source code.
1. Open terminal
2. Type set on Windows or env on macOS or Linux to see a list of current environment variables.
3. If the `RPC_USER` and `RPC_PASSWORD` is not already listed, you can set it using the set command on Windows or export command on macOS or Linux. For example, on Windows you can set the MY_VAR variable to the value hello by typing `set MY_VAR=hello`. On macOS or Linux, you can set the same variable using `export MY_VAR=hello`.
4. Set `RPC_USER` and `RPC_PASSWORD` based on your authentication. 


## How to use it


### TODO List
1. Modularize the rpc requests (for now, only implement the ones we need)
- getblockchaininfo
- getblock
- get
- getrawtransaction
- decoderawtransaction
- getrawmempool
2. Use it to construct the graph
- calculate the data based on the input
- get all hashes of the blocks
- get all transactions
- construct a graph object