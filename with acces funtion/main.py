from web3 import Web3
import requests
from pathlib import Path
from flask import Flask, request, render_template

# Set up Flask app
app = Flask(__name__)

# Connect to Hardhat node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545/'))

# Set the contract address and ABI
contract_address = '0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e'
contract_abi = [
    {
      "inputs": [],
      "name": "ShareAccess",
      "outputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "user",
              "type": "address"
            },
            {
              "internalType": "bool",
              "name": "authenticity",
              "type": "bool"
            }
          ],
          "internalType": "struct Upload.Access[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "allow",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "disallow",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_user",
          "type": "address"
        }
      ],
      "name": "get_cid",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_cid",
          "type": "string"
        }
      ],
      "name": "store_cid",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
# Set the Web3.Storage API token
web3storage_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEM4OTdFNTAxRTRFRjc2MTNFZUFlNTdkNUI5QUUwN2FmOGY3RTAwNjAiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODUzNzY3NzYwNDEsIm5hbWUiOiJzZWN1cmUgZGF0YSBzdG9yYWdlIn0.nRiYTlJO4zyBIthWEI1oVGsaum3YuBV2J9xHJipHO44'  # Replace with your Web3.Storage API token

# Upload file to web3.storage and get CID
def upload_file_to_web3storage(file_path):
    headers = {
        'Authorization': f'Bearer {web3storage_token}'
    }
    with open(file_path, 'rb') as file:
        response = requests.post('https://api.web3.storage/upload', files={'file': file}, headers=headers)
        response_data = response.json()
        return response_data['cid']

# Upload CID to the blockchain
# Upload CID to the blockchain
def upload_cid_to_blockchain(cid, account, private_key):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    w3.eth.default_account = account
    tx_hash = contract.functions.store_cid(cid).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt




# Set access for a given account
def set_access(account, access, selected_account, private_key):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    nonce = w3.eth.get_transaction_count(selected_account)
    txn = contract.functions.allow(account).buildTransaction({
        'from': selected_account,
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# HTML routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    cid = upload_file_to_web3storage(file.filename)
    receipt = upload_cid_to_blockchain(cid, request.form['account'], request.form['private_key'])
    return f'File uploaded. CID: {cid}<br>Transaction Hash: {receipt.transactionHash.hex()}<br>Block Hash: {receipt.blockHash.hex()}<br>From: {receipt["from"]}<br>To: {receipt.to}'

@app.route('/allow', methods=['POST'])
def access():
    account = request.form['account']
    access = request.form['access']
    receipt = set_access(account, access, request.form['admin_account'], request.form['admin_private_key'])
    return f'Access set for account {account}.<br>Transaction Hash: {receipt.transactionHash.hex()}<br>Block Hash: {receipt.blockHash.hex()}<br>From: {receipt["from"]}<br>To: {receipt.to}'

if __name__ == '__main__':
    app.run(debug=True)
