# Bitcoin Transaction Graph

## Setup
### Virtual enviromnet/Install dependencies
1. Create virtual env: `python3 -m venv <venv_name>`
2. Activate virtual env: `source <venv_name>/bin/activate` - different command depending on platform: https://docs.python.org/3/library/venv.html#:~:text=Shell-,Command,-to%20activate%20virtual
- For Windows: `source graph/Scripts/activate`
3. To deactivate virtual env: `deactivate`
4. Within the virtual environment, run `pip install -r requirements.txt` in the terminal

### Set Environment Variables
You would have to set `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` as environment variables, since we do not want to include sensitive information in source code.
1. Open terminal
2. Type set on Windows or env on macOS or Linux to see a list of current environment variables.
3. If the `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` is not already listed, you can set it using the set command on Windows or export command on macOS or Linux. For example, on Windows you can set the MY_VAR variable to the value hello by typing `set MY_VAR=hello`. On macOS or Linux, you can set the same variable using `export MY_VAR=hello`.
4. Set `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD` based on your authentication. 


## How to Interpret Graph Data

### Types of Transactions
There are many different types of transactions in Bitcoin, and it is hard to define a concept of "address" on transcations because transaction data only contains script to verify if the condition for using output is met, do not store anything related to "address". However, Bitcoin core does return "address" data in transaction for certain transactions based on the script. Different types of transactions use different encoding scheme, so the address does not necessarily means the address of the users in the network.

For this project, we ignored all the transactions do not contain "address" field in the transaction data. This means the vertices of output graph will not necessarily represent the user, or an account in the network. However, it still represents transactions between different users.

### Edgelist without height (directory: `bitcoinrpc/txs_graph/datetime`)
This is depricated version of the program. The program used to create networkx graph object in memory and write entire graph to the disk in once. This was inefficient way to write data to the disk because the size of the graph object was huge and memory could have been overwhelmed. Therefore, we updated the way we write data to the file when we added a block height to our data. The format of data follows:

```
from_address, to_address, weight (value transferred)
```

### Edgelist with height (directory: `bitcoinrpc/txs_graph/datetime_with_height`)
Since writing down edgelist file took very long time, we decided to add block height information to the file so that we can easily re-use the data we have written. For instance, if we have edgelist data from date1 to date2, and edgelist data from date3 to date4, but the date of those two file overlap, we will not be able to identify overlapping transactions easily if we don't know the block height of the block that transactions are included. 

The format of data follows:
```
from_address, to_address, weight (value transferred), block_height
```

Also, "-1" from_address means that the value is coming from bitcoin network. For instance, for coinbase transactions, the from address will be "-1" and to address will be miner's address.

## How add new block data
Since our program take date and time as an input, if we only use Bitcoin core JSON RPC, we would have to call RPC to find out block hashes within the time range. There might be some heuristic methods that can make this operations more efficient, but in general this seemed to be inefficient to use since all data we needed to figure out blocks within the timerange was timestamp and hash of each block. Therefore, we created a Python program `get_block_data.py` that combines block data downloaded from [BTC.com](https://explorer.btc.com/btc/blocks) block explorer and save it in local file. Then the program can call `get_block_hash` command to get a block hashes of each block. 

If you don't have existing `blocks_data_total.csv`, you will first have to go to https://explorer.btc.com/btc/blocks to download block data of each month (btc.com only allows you to export one month of block data). Then you will have to store that data in `blocks_by_month` folder. If `blocks_data_total.csv` is not up to date, you will download block data file that contains new data you want to have. For example, if the most recent data file that is contained in `blocks_by_moth` is `block_list_2023-02-22_2023-03-10.csv`, and today date is 2023/4/10, you will want to download data from March 10th to April 10th from BTC.com and store it in `blocks_by_month` folder. Note that data downloaded from BTC.com do not contain block hash data. Those hash data have to be added to the file with running command 5 of the program.

When you have all data you need you can start running program to perform different operations.

If the user run the program, the program will prompt:

```
1. Get all blocks from all the files
2. Get number of blocks in blocks_data_total.csv
3. Add new files to blocks_data_total.csv
4. Verify if we don't have missing blocks in blocks_data_total.csv
5. Add block hashes to blocks_data_total.csv
6. Exit
Enter command (only integer is allowed):
```

**Command 1**: This command will get all block data from all the files in `blocks_by_motnth` folder and write all combined data to `blocks_data_total.csv`. Note that it will overwrite the file and not block hash data will be included when this command is ran. If you don't want to lose block hash data that already exists in `blocks_data_total.csv`, you should run command 3.

**Command 2**: Print the total number of blocks that current file has.

**Command 3**: This will add block data from specified file (a file inside `blocks_by_month`). Make sure there is no gap between `blocks_data_total.csv` and new file you are adding. For example, if the last block data that `blocks_data_total.csv` has is 2023/02/10, but the beginning of new data starts at 2023/03/10, there should be an error.

Example
```
$ python get_block_data.py 
1. Get all blocks from all the files
2. Get number of blocks in blocks_data_total.csv
3. Add new files to blocks_data_total.csv
4. Verify if we don't have missing blocks in blocks_data_total.csv
5. Add block hashes to blocks_data_total.csv
6. Exit
Enter command (only integer is allowed): 3
Enter file path: blocks_by_month/block_list_2023-03-08_2023-04-08.csv
Adding blocks_by_month/block_list_2023-03-08_2023-04-08.csv to blocks_data_total.csv
```

**Command 4**: This command verify if there is no gap in `blocks_data_total.csv`. If there is missing blocks, it will print the total number of missing blocks and list of heights of blocks that are missing. If there is no missing block, it will print message indicating there is no missing blocks.

**Command 5**: This command will add block hashes for specified height to `blocks_data_total.csv`. This is crucial step if you want to use other program in this repository. Enter start height for the begining block that does not have block hash information, and enter end hegiht for the end block in `blocks_data_total.csv`.

Example:
```
$ python get_block_data.py
1. Get all blocks from all the files
2. Get number of blocks in blocks_data_total.csv
3. Add new files to blocks_data_total.csv
4. Verify if we don't have missing blocks in blocks_data_total.csv
5. Add block hashes to blocks_data_total.csv
6. Exit
Enter command (only integer is allowed): 5
Enter start height: 55001
Enter end height: 55005
Retrieved block hash for block height:  55001
Retrieved block hash for block height:  55002
Retrieved block hash for block height:  55003
Retrieved block hash for block height:  55004
Retrieved block hash for block height:  55005
```

**Command 6**: Exit the program

**Note**: After you are done with updating `blocks_data_total.csv` file, make sure you copy and paste the file into "bitcoinrpc/assets/" directory". Other programs use data from `blocks_data_total.csv` file in this directory instead of the file inside `get_block_data` directory.


## How to use BitcoinRPC
`bitcoinrpc` directory is consisted of multiple programs.

### bitcoinrpc.py
This file contains all the function that directly interact with Bitcoin core JSON RPC. You can add more function based on Bitcoin core JSON RPC documentation: https://developer.bitcoin.org/reference/rpc/. The documentation for this file is well written so it will be fairly easy to use functions in this file.

To use function in this file, you have to setup environment variables `BITCOIN_RPC_USER` and `BITCOIN_RPC_PASSWORD`, which is explained in "Setup Environment Variables" section. Then, include following code snippet to instantiate the object:

```
# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']
rpc_host = "localhost"
rpc_port = 8332
bitrpc = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)
```

### graph_by_date.py
This program takes start_datetime and end_datetime in format of "YYYY/MM/DD HH:MM:SS", and write down the graph file in `bitcoinrpc/txs_graph/datetime_with_height`. The detail about the graph file can be found in "Edgelist with height (directory: `bitcoinrpc/txs_graph/datetime_with_height`)" section. 

Example run: 

Example files can be found in `bitcoinrpc/txs_graph/datetime_with_height`.

### get_txs_types_stats.py
This program will take start_height and end_height as an input, and write down number of each transaction type per date for transaction data within the given date. The data will be written in `/txs_types_stats/{start_height}_to_{end_height}.csv`.

**Note**: All dates are based on UTC datetime.

Example run:
```
$ python get_txs_types_stats.py
Enter a starting block height: 0
Enter an ending block height: 10000
```

The example of written file looks like:
```
2023-01-01, witness_v0_keyhash: 4763, nulldata: 22, pubkeyhash: 2885, scripthash: 4480, witness_v0_scripthash: 663, witness_v1_taproot: 52, 
```
