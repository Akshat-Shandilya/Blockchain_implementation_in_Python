#Block.py

import Utils
import time

class Block:
    def __init__(self, _data=None, _number=0, _timestamp=None):
        self.data = _data if _data else []  # Data is a list of transactions
        self.number = _number
        self.timestamp = _timestamp if _timestamp else time.time()
        self.previous_block_hash = "0" * 64
        self.nonce = 0
        self.block_hash = self.generate_block_hash()
        
    def add_transaction(self, transaction):
        self.data.append(transaction)
        
    def generate_block_hash(self):
        transactions_string = ""
        if isinstance(self.data, list):
            for tx in self.data:
                transactions_string += tx.transaction_hash
        else:
            transactions_string = str(self.data)
            
        return Utils.hash256(
            transactions_string,
            self.previous_block_hash,
            self.number,
            self.nonce,
            self.timestamp
        )