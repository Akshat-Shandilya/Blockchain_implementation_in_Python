# Blockchain Implementation in Python

This project implements a **college-based blockchain system** using **Python** and **Streamlit** for the frontend. Students can register/login with their **College ID**, make transactions, mine blocks, and explore the blockchain.

---

## Features

✅ **User Authentication**: Users can log in or register using their **College ID**. Each new user receives **1 coin** by default.

✅ **Account Dashboard**: Users can view their **balance**, **pending transactions**, and **account details**.

✅ **Transactions & Mempool**: Users can send coins to others, with transactions stored in `mempool.txt` until mined.

✅ **Mining Blocks**: The system selects **three transactions** from the mempool and mines a new block, adding it to `blockchain.txt`.

✅ **Blockchain Explorer**: Users can view all blocks and transactions stored in the blockchain.

✅ **Persistent Storage**: Data is saved across sessions in three files:
   - `accounts.txt` → Stores user account details (College ID, Address, Balance, etc.).
   - `mempool.txt` → Stores pending transactions before they are mined.
   - `blockchain.txt` → Stores all mined blocks.

---

## Installation

### **1️⃣ Prerequisites**
Ensure you have **Python 3.8+** installed.

```sh
python --version
```

### **2️⃣ Install Dependencies**
Run the following command to install required packages:

```sh
pip install streamlit
```

---

## Running the Application

### **Start the Streamlit App**
Run the following command in the project directory:

```sh
streamlit run app.py
```

This will open the app in your web browser.

---

## Usage Guide

### **🔹 Login/Register**
1. Enter your **College ID**.
2. Click **Login** if you already have an account.
3. Click **Register** to create a new account (you'll get **1 coin** by default).

### **🔹 Create Transactions**
1. Go to **"Create Transaction"** tab.
2. Select a **receiver** from the dropdown list.
3. Enter the **amount** (minimum: 0.1 coins).
4. Click **Create Transaction** → Transaction is added to the **mempool**.

### **🔹 Mine a Block**
1. Go to **"Mine Block"** tab.
2. Click **Mine Block from Mempool**.
3. A new block is created using **three transactions** from the mempool.

### **🔹 View Blockchain**
1. Go to **"Blockchain Explorer"** tab.
2. Expand any block to view its **transactions** and **metadata**.

---

## File Structure

```plaintext
📂 College-Blockchain-System
│── app.py                # Streamlit frontend
│── Blockchain.py         # Blockchain logic
│── Block.py              # Block structure
│── Transaction.py        # Transaction structure
│── Account.py            # User account class
│── Database.py           # Handles file storage (accounts, mempool, blockchain)
│── accounts.txt          # Stores user accounts
│── mempool.txt           # Stores pending transactions
│── blockchain.txt        # Stores mined blocks
│── README.md             # Project documentation
```

## License
This project is **open-source** under the **MIT License**.

