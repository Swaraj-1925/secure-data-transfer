import requests
from tkinter import Tk, filedialog
import os
from web3 import Web3

# Set up Web3.py with your Ethereum provider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545/'))

# Contract ABI (Application Binary Interface)
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

# Contract address
contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

def upload_file_to_web3storage(file_path, token):
    api_url = 'https://api.web3.storage/upload'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/octet-stream'
    }

    with open(file_path, 'rb') as file:
        response = requests.post(api_url, headers=headers, data=file)

    print(response.status_code)
    if response.status_code == 200:
        return response.json()['cid']
    else:
        return None

def select_file_path():
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window

    file_path = filedialog.askopenfilename()
    return file_path

# Prompt the user to select a file path
file_path = select_file_path()
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEM4OTdFNTAxRTRFRjc2MTNFZUFlNTdkNUI5QUUwN2FmOGY3RTAwNjAiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODUzNzY3NzYwNDEsIm5hbWUiOiJzZWN1cmUgZGF0YSBzdG9yYWdlIn0.nRiYTlJO4zyBIthWEI1oVGsaum3YuBV2J9xHJipHO44'
file_path = os.path.normpath(file_path)
cid = upload_file_to_web3storage(file_path, token)

if cid:
    print(f'File uploaded successfully. CID: {cid}')

    # Connect to the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Set the CID in the contract
    w3.eth.default_account = w3.eth.accounts[0]  # Set the account to use for the transaction
    tx_hash = contract.functions.store_cid(cid).transact()

    # Wait for the transaction to be mined
    w3.eth.wait_for_transaction_receipt(tx_hash)


    print('CID stored in the contract.')
else:
    print('File upload failed.')
