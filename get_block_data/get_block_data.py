import os
import sys
sys.path.insert(0, '../')
from bitcoinrpc.bitcoinrpc import BitcoinRpc

# Get environment variables
rpc_user = os.environ['BITCOIN_RPC_USER']
rpc_password = os.environ['BITCOIN_RPC_PASSWORD']

# Setup bitcoin rpc
rpc_host = "localhost"
rpc_port = 8332
bitrpc = BitcoinRpc(rpc_user, rpc_password, rpc_host, rpc_port)

def get_blocks_by_month():
    """ Get all blocks from all the files in "block_by_month" directory.
    Note that it will overwrite existing blocks_data_total.csv file.
    """
    blocks_by_month = './blocks_by_month'
    filenames = []
    for filename in os.listdir(blocks_by_month):
        if filename.endswith('.csv'):
            filenames.append(filename)
    filenames.sort()
    rows = []

    for filename in filenames:
        added = set()
        with open(blocks_by_month + '/' + filename, 'r') as f2:
            lines = f2.readlines()
            for line in reversed(lines):
                block_height = line.split(',')[0]
                if block_height == 'Height':
                    continue
                block_height_int = int(block_height)
                rows.append(line)
                added.add(block_height_int)
    
    rows = list(set(rows))
    rows.sort(key=lambda x: int(x.split(',')[0]))

    # Add block hash at the end of row
    for i in range(len(rows)):
        block_height = int(rows[i].split(',')[0])
        rows[i] = rows[i].strip() + ',' + bitrpc.get_block_hash(block_height)
        print("Added block hash for block height: ", block_height)

    with open('blocks_data_total.csv', 'w') as f:
        f.write('height,relayed_by,time_utc,tx_count,reward_btc,size_kb,fees_btc,average_tx_fees_btc,volume_btc, block_hash\n')
        for row in rows:
            f.write(row)

    print("\nAdded all block data from all the files to blocks_data_total.csv\n")

def get_number_of_blocks():
    """ Get number of blocks in blocks_data_total.csv file.
    """
    with open('blocks_data_total.csv', 'r') as f:
        lines = f.readlines()
        print("Total number of blocks: ", len(lines) - 1)

def verify_missing_blocks():
    """ Check if there is any gaps in blocks_data_total.csv file.
    """
    missing_blocks = []
    block_heights = []
    with open('blocks_data_total.csv', 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            line = lines[i]
            block_height = line.split(',')[0]
            block_heights.append(int(block_height))
    for i in range(1, len(block_heights)):
        if block_heights[i] != block_heights[i - 1] + 1:
            print("Missing block: ", block_heights[i - 1] + 1)
            for block in range(block_heights[i - 1] + 1, block_heights[i]):
                missing_blocks.append(block)

    if len(missing_blocks) == 0:
        print("\nNo missing blocks\n")
    else:
        print("\nTotal number of missing blocks: ", len(missing_blocks))
        print("Missing following blocks: ", missing_blocks, "\n")

def add_new_file(file_path):
    """ Add data from a file in "blocks_data_month" directory to "blocks_data_total.csv" file.
    Note that if file format is corrupted, this function will not work. Make sure that files
    in "blocks_data_month" directory is downloaded from BTC.com block explorer, and "blocks_data_total.csv"
    file is in correct format.
    """
    last_line = ''
    with open('blocks_data_total.csv', 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
    current_block_height = int(last_line.split(',')[0])
    with open('blocks_data_total.csv', 'a') as f:
        current_block_height = int(last_line.split(',')[0]) + 1
        with open(file_path, 'r') as f2:
            lines = f2.readlines()[1:]
            lines.reverse()
            if int(lines[0].split(',')[0]) > current_block_height:
                print("Adding this file will cause missing blocks. Make sure you do not have any gaps in your block data.\n")
                print("Failed to add file: ", file_path, "to blocks_data_total.csv\n")
                return
            for line in lines:
                block_height = int(line.split(',')[0])
                if block_height < current_block_height:
                    continue
                f.write(line.strip() + '\n')

def add_block_hashes(start_height, end_height):
    """ Add block hashes to "blocks_data_total.csv" file for blocks in given height range.
    """
    with open('blocks_data_total.csv', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                continue
            line = lines[i]
            line_split = line.split(',')
            block_height = int(line_split[0])
            # Skip if block height lower that start_height or it it's already added
            if block_height < start_height or len(line_split) >= 10:
                continue
            elif block_height > end_height:
                break
            block_hash = bitrpc.get_block_hash(block_height)
            if block_hash == -1:
                print("Error: block hash not found for block height: ", block_height)
            else:
                print("Retrieved block hash for block height: ", block_height)
            lines[i] = line.strip() + ',' + block_hash + '\n'
    with open('blocks_data_total.csv', 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    while True:
        print("1. Get all blocks from all the files")
        print("2. Get number of blocks in blocks_data_total.csv")
        print("3. Add new files to blocks_data_total.csv")
        print("4. Verify if we don't have missing blocks in blocks_data_total.csv")
        print("5. Add block hashes to blocks_data_total.csv")
        print("6. Exit")
        command = int(input("Enter command (only integer is allowed): "))
        if command == 1:
            get_blocks_by_month()
        elif command == 2:
            get_number_of_blocks()
        elif command == 3:
            file_path = input("Enter file path: ").strip()
            print(f"Adding {file_path} to blocks_data_total.csv")
            add_new_file(file_path)
        elif command == 4:
            verify_missing_blocks()
        elif command == 5:
            start_height = int(input("Enter start height: "))
            end_height = int(input("Enter end height: "))
            add_block_hashes(start_height, end_height)
        elif command == 6:
            break
        else:
            print("Unknown command")
