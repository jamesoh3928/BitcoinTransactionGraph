TODO
1. Address: payment destination vs public key identifier
2. Update readme
- Re-read the transaction types in Mastering Bitcoin: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch06.asciidoc
3. Maybe serialize object (try and compare the size of the file)


Maybe Later
1. Use pickle to serialize the object (maybe later)
3. pip freeze > requirements.txt (if new pip is added)

Future:
1. Try to construct the graph with data that do not have address fields
Keegan's code: https://github.com/kjk6690/Cryptocurrency-Research/blob/main/old_data/block_724784.adjlist

 <!-- During meeting -->
 1. Discussion 
 2. SSH setup
 3. Try git pull
 4. Run one day of transaction data

# Bitcoin Transaction Graph

## Setup
### Virtual enviromnet/Install dependencies
1. Create virtual env: `python3 -m venv <venv_name>`
2. Activate virtual env: `source <venv_name>/bin/activate` - different command depending on platform: https://docs.python.org/3/library/venv.html#:~:text=Shell-,Command,-to%20activate%20virtual
- For Windows: source graph/Scripts/activate
3. To deactivate virtual env: `deactivate`
4. Within the virtual environment, run `pip install -r requirements.txt` in the terminal (TODO: I have to froze the dependencies after I am done with development)

### Set Environment Variables
You would have to set `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` as environment variables, since we do not want to include sensitive information in source code.
1. Open terminal
2. Type set on Windows or env on macOS or Linux to see a list of current environment variables.
3. If the `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` is not already listed, you can set it using the set command on Windows or export command on macOS or Linux. For example, on Windows you can set the MY_VAR variable to the value hello by typing `set MY_VAR=hello`. On macOS or Linux, you can set the same variable using `export MY_VAR=hello`.
4. Set `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` based on your authentication. 


## How to Interpret Graph

### Types of Transactions


## How to use BitcoinRPC
## How add new block data
