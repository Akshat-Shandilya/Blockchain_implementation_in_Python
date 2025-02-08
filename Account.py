# Accounts.py

class Account:

    def __init__(self, _college_id, _address, _private_key, _balance):  
        self.college_id = _college_id
        self.address = _address
        self.private_key = _private_key
        self.balance = _balance
    
    def can_spend(self, amount):
        return self.balance >= amount
    
    def to_dict(self):
        return {
            "college_id": self.college_id,
            "address": self.address,
            "private_key": self.private_key,
            "balance": self.balance
        }
