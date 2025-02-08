# Database.py

import json
import os
import Transaction
import Block
import Account 

class Database:
    def __init__(self, blockchain_file="blockchain.txt", mempool_file="mempool.txt", accounts_file="accounts.txt"):
        self.blockchain_file = blockchain_file
        self.mempool_file = mempool_file
        self.accounts_file = accounts_file

    def save_accounts(self, accounts):
        with open(self.accounts_file, "w") as file:
            for college_id, account in accounts.items():
                file.write(f"{college_id},{account.address},{account.private_key},{account.balance}\n")
            
    def load_accounts(self):
        accounts = {}
        try:
            with open(self.accounts_file, "r") as file:
                for line in file:
                    college_id, address, private_key, balance = line.strip().split(',')
                    accounts[college_id] = Account.Account(college_id, address, private_key, float(balance))
        except FileNotFoundError:
            print("No accounts file found. Creating new one.")
        return accounts        

    def save_blockchain(self, blockchain):
        chain_data = []
        for block in blockchain.chain:
            block_data = {
                "number": block.number,
                "timestamp": block.timestamp,
                "previous_block_hash": block.previous_block_hash,
                "nonce": block.nonce,
                "block_hash": block.block_hash,
                "data": [tx.to_dict() for tx in block.data] if isinstance(block.data, list) else block.data
            }
            chain_data.append(block_data)
        with open(self.blockchain_file, 'w') as f:
            json.dump(chain_data, f, indent=4)
            
    def load_blockchain(self, blockchain):
        if not os.path.exists(self.blockchain_file):
            return
        try:
            with open(self.blockchain_file, 'r') as f:
                chain_data = json.load(f)
            for block_data in chain_data:
                transactions = []
                if isinstance(block_data["data"], list):
                    for tx_data in block_data["data"]:
                        tx = Transaction.Transaction(
                            tx_data["sender"],
                            tx_data["receiver"],
                            tx_data["amount"],
                            tx_data["timestamp"]
                        )
                        transactions.append(tx)
                else:
                    transactions = block_data["data"]
                block = Block.Block(transactions, block_data["number"], block_data["timestamp"])
                block.previous_block_hash = block_data["previous_block_hash"]
                block.nonce = block_data["nonce"]
                block.block_hash = block_data["block_hash"]
                blockchain.chain.append(block)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid blockchain file found or file is corrupted.")
            
    def save_mempool(self, transactions):
        mempool_data = [tx.to_dict() for tx in transactions]
        with open(self.mempool_file, 'w') as f:
            json.dump(mempool_data, f, indent=4)
            
    def load_mempool(self):
        if not os.path.exists(self.mempool_file):
            return []
        try:
            with open(self.mempool_file, 'r') as f:
                mempool_data = json.load(f)
            transactions = []
            for tx_data in mempool_data:
                tx = Transaction.Transaction(
                    tx_data["sender"],
                    tx_data["receiver"],
                    tx_data["amount"],
                    tx_data["timestamp"]
                )
                transactions.append(tx)
            return transactions
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid mempool file found or file is corrupted.")
            return []