# Transactions.py
 
import time
from hashlib import sha256

class Transaction:
    def __init__(self, _sender, _receiver, _amount, _timestamp=None):
        self.sender = _sender
        self.receiver = _receiver
        self.amount = _amount
        self.timestamp = _timestamp if _timestamp else time.time()
        self.transaction_hash = self.calculate_hash()
        
    def calculate_hash(self):
        transaction_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return sha256(transaction_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.transaction_hash
        }
