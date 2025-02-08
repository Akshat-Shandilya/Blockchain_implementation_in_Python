# Blockchain.py

import Database
from Block import Block 
import time

class Blockchain:
    def __init__(self, _difficulty):
        self.chain = []
        self.difficulty = _difficulty
        self.mempool = []
        self.accounts = {}  
        self.address_to_college_id = {}  
        self.db = Database.Database()
        self.accounts = self.db.load_accounts()
        self.db.load_blockchain(self)
        self.mempool = self.db.load_mempool()
        for college_id, account in self.accounts.items():
            self.address_to_college_id[account.address] = college_id
    
    def add_account(self, account):
        self.accounts[account.college_id] = account
        self.address_to_college_id[account.address] = account.college_id
        self.db.save_accounts(self.accounts)   

    def get_account_balance(self, address):
        college_id = self.address_to_college_id.get(address)
        if not college_id:
            return 0.0             
        # Just return the stored balance since it's already updated when mining blocks
        account = self.accounts[college_id]
        return round(float(account.balance), 8)
        
    def get_pending_transactions(self, address):
        return sum(float(tx.amount) for tx in self.mempool if tx.sender == address)
    
    def add_to_mempool(self, transaction):
        try:
            current_balance = self.get_account_balance(transaction.sender)
            pending_amount = self.get_pending_transactions(transaction.sender)
            available_balance = current_balance - pending_amount
            transaction_amount = round(float(transaction.amount), 8)
            if available_balance >= transaction_amount:
                self.mempool.append(transaction)
                self.db.save_mempool(self.mempool)
                return True
            return False
        except Exception as e:
            print(f"Error in add_to_mempool: {str(e)}")
            return False
    
    def update_accounts(self, block):
        if not isinstance(block.data, list):
            return
            
        for transaction in block.data:
            sender_college_id = self.address_to_college_id.get(transaction.sender)
            receiver_college_id = self.address_to_college_id.get(transaction.receiver)
            
            if sender_college_id and sender_college_id in self.accounts:
                self.accounts[sender_college_id].balance = round(
                    float(self.accounts[sender_college_id].balance) - float(transaction.amount),
                    8
                )
            if receiver_college_id and receiver_college_id in self.accounts:
                self.accounts[receiver_college_id].balance = round(
                    float(self.accounts[receiver_college_id].balance) + float(transaction.amount),
                    8
                )
        self.db.save_accounts(self.accounts)
        
    def create_block_from_mempool(self):
        if len(self.mempool) < 3:
            return None  

        selected_transactions = self.mempool[:3]
        del self.mempool[:3]  
        
        block_number = len(self.chain) + 1
        block = Block(selected_transactions, block_number, time.time())
        self.db.save_mempool(self.mempool)
        return block

    def mine_block(self, block):
        if not block:
            return False
            
        if self.chain:
            block.previous_block_hash = self.chain[-1].block_hash
        
        while True:
            block.block_hash = block.generate_block_hash()
            if block.block_hash[:self.difficulty] == "0" * self.difficulty:
                self.chain.append(block)
                self.update_accounts(block)
                self.db.save_blockchain(self)
                break
            else:
                block.nonce += 1
        return True