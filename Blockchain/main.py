import random
from web3 import Web3
import requests
from pathlib import Path
from flask import Flask, request, render_template
import webbrowser

# Set up Flask app
app = Flask(__name__)
# HTML routes
@app.route('/')
def index():
    return render_template('index.html')

# Connect to Hardhat node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545/'))

# Set the contract address and ABI
contract_address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
contract_abi = [
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_accessCode",
          "type": "uint256"
        }
      ],
      "name": "getCID",
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
          "internalType": "address",
          "name": "user",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_accessCode",
          "type": "uint256"
        }
      ],
      "name": "grantAccess",
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
        },
        {
          "internalType": "uint256",
          "name": "_accessCode",
          "type": "uint256"
        }
      ],
      "name": "revokeAccess",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_cid",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_accessCode",
          "type": "uint256"
        }
      ],
      "name": "storeCID",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
   
#web3.storage api token
web3storage_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEM4OTdFNTAxRTRFRjc2MTNFZUFlNTdkNUI5QUUwN2FmOGY3RTAwNjAiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODUzNzY3NzYwNDEsIm5hbWUiOiJzZWN1cmUgZGF0YSBzdG9yYWdlIn0.nRiYTlJO4zyBIthWEI1oVGsaum3YuBV2J9xHJipHO44'


# Generate a random 6-digit number
def random_num():
    random_number = random.randint(100000, 999999)
    return random_number


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
def upload_cid_to_blockchain(cid, access_code, account):
    Contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    w3.eth.default_account = account
    tx_hash = Contract.functions.storeCID(cid, access_code).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def grant_access(admin_account,account_access,access_code):

    Contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    w3.eth.default_account = admin_account
    user_address = account_access
    tx_hash = Contract.functions.grantAccess(user_address,access_code).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt
def revoke_access(admin_account,account_access,access_code):

    Contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    w3.eth.default_account = admin_account
    user_address = account_access
    tx_hash = Contract.functions.revokeAccess(user_address,access_code).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def get_cid(admin_account,access_code):
    w3.eth.default_account = admin_account
    Contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    cid = Contract.functions.getCID(access_code).call()
    return cid

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    cid = upload_file_to_web3storage(file.filename)
    access_code=random_num()
    receipt = upload_cid_to_blockchain(cid,access_code, request.form['account'],)
    return f'File uploaded.<br>Transaction Hash: {receipt.transactionHash.hex()}<br>From: {receipt["from"]}<br>To: {receipt.to}.<br><br> Your access code is : {access_code}.<br>**Remember your access code**'

@app.route('/allow', methods=['POST'])
def grantAccess():
    admin_account =request.form['admin_account']
    account_access = request.form['account_access']
    access_code = int( request.form['access_code'])
    receipt = grant_access(admin_account,account_access,access_code)
    return f'**Access set for account:- {account_access} **.<br><br>Transaction Hash: {receipt.transactionHash.hex()}<br>From: {receipt["from"]}<br>To: {receipt.to}'

@app.route('/disallow', methods=['POST'])
def revokeAccess():
    admin_account =request.form['admin_account']
    account_revokeAccess = request.form['account_revokeAccess']
    access_code = int( request.form['access_code'])
    receipt = revoke_access(admin_account,account_revokeAccess,access_code)
    return f'**Access has been removed  for account:- {account_revokeAccess} **.<br><br>Transaction Hash: {receipt.transactionHash.hex()}<br>From: {receipt["from"]}<br>To: {receipt.to}'

@app.route('/get', methods=['POST'])
def getCID():
    admin_account =request.form['admin_account']
    private_key = request.form['private_key']
    access_code = int( request.form['access_code'])
    data = get_cid(admin_account,access_code)
    ipfs_link = f"https://{data}.ipfs.w3s.link/"

    return webbrowser.open(ipfs_link)


if __name__ == '__main__':
    app.run(debug=True)