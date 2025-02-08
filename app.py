# app.py
 
import streamlit as st
import secrets
import time
from Account import Account
from Transaction import Transaction
from Blockchain import Blockchain

def generate_keys():
    private_key = secrets.token_hex(32)
    address = "0x" + secrets.token_hex(20)
    return address, private_key

def initialize_blockchain():
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = Blockchain(4)

def login_page():
    st.title("🐧 GORLECOIN 🐧")
    college_id = st.text_input("Enter your Kerberos ID").strip()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            if college_id:
                blockchain = st.session_state.blockchain
                if college_id in blockchain.accounts:
                    st.session_state.logged_in = True
                    st.session_state.current_user = college_id
                    st.rerun()
                else:
                    st.error("Kerberos ID not registered!")
    
    with col2:
        if st.button("Register New ID"):
            if college_id:
                blockchain = st.session_state.blockchain
                if college_id in blockchain.accounts:
                    st.error("Kerberos ID already registered!")
                else:
                    address, private_key = generate_keys()
                    new_account = Account(college_id, address, private_key, _balance=1.0)  
                    blockchain.add_account(new_account)
                    st.success(f"""
                    Registration successful! Please save these credentials:
                    College ID: {college_id}
                    Address: {address}
                    Private Key: {private_key}
                    Initial Balance: 1 Coin
                    """)
            else:
                st.error("Please enter a Kerberos ID!")

def main_page():
    st.title("🐧 GORLECOIN 🐧")
    blockchain = st.session_state.blockchain
    current_account = blockchain.accounts[st.session_state.current_user]
    
    st.sidebar.header("Your Account")
    st.sidebar.text(f"Kerberos ID: {current_account.college_id}")
    st.sidebar.text(f"Address: {current_account.address[:10]}...")
    current_balance = blockchain.get_account_balance(current_account.address)
    st.sidebar.text(f"Current Balance: {current_balance} Coins")

    pending_amount = blockchain.get_pending_transactions(current_account.address)
    if pending_amount > 0:
        st.sidebar.text(f"Pending Transactions: {pending_amount} Coins")
        st.sidebar.text(f"Available Balance: {current_balance - pending_amount} Coins")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["Create Transaction", "Mine Block", "View Blockchain"])
    
    with tab1:
        st.header("Create New Transaction")
        
        other_accounts = [
            (acc.college_id, acc.address) 
            for college_id, acc in blockchain.accounts.items() 
            if college_id != st.session_state.current_user
        ]
        
        receiver_selection = st.selectbox(
            "Select Receiver (College ID - Address)",
            [f"{cid} - {addr[:10]}..." for cid, addr in other_accounts]
        )
        
        amount = st.number_input("Amount (Coins)", min_value=0.1, value=1.0, step=0.1)
        
        if st.button("Create Transaction"):
            receiver_id = receiver_selection.split(" - ")[0]
            receiver_account = blockchain.accounts[receiver_id]
            transaction = Transaction(current_account.address, receiver_account.address, amount)
            
            if blockchain.add_to_mempool(transaction):
                st.success("Transaction added to mempool!")
            else:
                st.error("Transaction failed! Insufficient balance.")
                
        st.subheader("Current Mempool")
        if not blockchain.mempool:
            st.info("No pending transactions in mempool")
        else:
            for idx, tx in enumerate(blockchain.mempool):
                sender_id = blockchain.address_to_college_id.get(tx.sender, "Unknown")
                receiver_id = blockchain.address_to_college_id.get(tx.receiver, "Unknown")
                with st.expander(f"Transaction {idx+1}"):
                    st.text(f"From: {sender_id} ({tx.sender[:10]}...)")
                    st.text(f"To: {receiver_id} ({tx.receiver[:10]}...)")
                    st.text(f"Amount: {tx.amount} Coins")
                    st.text(f"Timestamp: {time.ctime(tx.timestamp)}")    
    
    with tab2:
        st.header("Mine New Block")
        
        if st.button("Mine Block from Mempool"):
            if not blockchain.mempool:
                st.warning("Mempool is empty!")
            else:
                with st.spinner("Mining block..."):
                    block = blockchain.create_block_from_mempool()
                    if block and blockchain.mine_block(block):
                        st.success("Block mined successfully!")
                    else:
                        st.error("Failed to mine block!")
    
    with tab3:
        st.header("Blockchain Explorer")
        
        for block in blockchain.chain:
            with st.expander(f"Block #{block.number} | Hash: {block.block_hash[:15]}..."):
                st.text(f"Previous Hash: {block.previous_block_hash}")
                st.text(f"Nonce: {block.nonce}")
                st.text(f"Timestamp: {time.ctime(block.timestamp)}")
                
                if isinstance(block.data, list):
                    st.subheader("Transactions:")
                    for tx in block.data:
                        sender_id = blockchain.address_to_college_id.get(tx.sender, "Unknown")
                        receiver_id = blockchain.address_to_college_id.get(tx.receiver, "Unknown")
                        st.text(f"From: {sender_id} ({tx.sender[:10]}...)")
                        st.text(f"To: {receiver_id} ({tx.receiver[:10]}...)")
                        st.text(f"Amount: {tx.amount} Coins")
                        st.text("---")
                else:
                    st.text(f"Data: {block.data}")

def main():
    initialize_blockchain()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        main_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
