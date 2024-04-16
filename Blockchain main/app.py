from flask import Flask, render_template, request, redirect
import web3
import requests
import os

app = Flask(__name__)

# Connect to the Ethereum network using Infura
w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:8545/'))

# Load the ABI (Application Binary Interface) of the Solidity contract
contract_abi =   [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "cid",
          "type": "string"
        }
      ],
      "name": "addFile",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "admin",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "fileInfo",
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
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "fileNames",
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
      "inputs": [],
      "name": "getAllFileCIDs",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        }
      ],
      "name": "getFileAdmin",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        }
      ],
      "name": "getFileCID",
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
      "inputs": [],
      "name": "getFileNames",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
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
          "internalType": "string",
          "name": "fileName",
          "type": "string"
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
          "internalType": "string",
          "name": "fileName",
          "type": "string"
        }
      ],
      "name": "revokeAccess",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

# Contract address deployed on the Ethereum network
contract_address = w3.to_checksum_address('0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9')

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        private_key = request.form['private_key']
        account = w3.eth.account.from_key(private_key)
        address = account.address
        return redirect('/dashboard?address=' + address)
    else:
        address = request.args.get('address')
        return render_template('dashboard.html', address=address)
@app.route('/upload', methods=['POST'])
def upload_file():
    address = request.form['address']
    file = request.files['file']

    # Prepare the file and metadata for Pinata API
    files = {
        'file': (file.filename, file.stream, file.content_type),
        'pinataMetadata': ('', '{"name": "' + file.filename + '"}'),
        'pinataOptions': ('', '{"cidVersion": 1}')
    }

    # Set your Pinata API key as Authorization token
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI2NWE2NjQ5Zi1lNmE5LTQzYjEtOTYyNC0wYmM0YmRmNDQ2MWMiLCJlbWFpbCI6InNhbS44MzEwMDAwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJhZWE3YTkxZjM3YjQ5NDAwOTgxNCIsInNjb3BlZEtleVNlY3JldCI6IjJmZjVlZTU3MzQzYjdmMzMxOTI0MmFjZmI3OThlNmI0MGU0OTJiMzU5ODU0MmE4NTJlZGJhN2MyYjQwNTdkMzMiLCJpYXQiOjE3MTMxNjA2NTN9.W1JVgEulXZ9B9uX_F4bxpM76UZfPJryLqhpr4cLpEy4'
    }

    # Make a POST request to Pinata API to pin the file to IPFS
    response = requests.post('https://api.pinata.cloud/pinning/pinFileToIPFS', files=files, headers=headers)
    response_data = response.json()

    # Retrieve the IPFS hash and other relevant information from the response
    cid = response_data['IpfsHash']


     
    file_name = file.filename
    
    tx_hash = contract.functions.addFile(file_name,cid).transact({'from' : address})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    
    folder_name = address
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file.save(os.path.join(folder_name, file.filename))
    transaction_details = {
        'file_name': file.filename,
        'from': address,
        'to': contract_address,
        'transaction_hash': receipt['transactionHash']
    }

    with open(os.path.join(folder_name, 'transaction_details.txt'), 'a') as f:
        f.write(str(transaction_details)+'\n') 
  
    txn=receipt['transactionHash'] 
    # Redirect to transaction details page
    tx_hash =w3.to_hex(txn)
    return redirect('/transaction?hash=' + tx_hash)


@app.route('/grant_access', methods=['POST'])
def grant_access():
    address = request.form['address']
    user_address = request.form['user_address'] 
    file = request.form['file_name']
    contract.functions.grantAccess(user_address,file).transact({'from': address})
    ST='access has been granted'
    return ST


@app.route('/revoke_access', methods=['POST'])
def revoke_access(): 
    address = request.form['address']
    user_address = request.form['user_address'] 
    file = request.form['file_name']
    contract.functions.revokeAccess(user_address,file).transact({'from': address})
    ST='access has been removed'
    return ST


@app.route('/get_all_file_names', methods=['POST'])
def get_all_file_names():
    address = request.form['address']
    
    # Get all file names stored by the address
    file_names = contract.functions.getFileNames().call({'from': address})
     
    return render_template('dashboard.html', address=address, file_names=file_names) 

@app.route('/get_cid', methods=['POST'])
def get_cid():
    address = request.form['address']
    file_name = request.form['file_name']  

    try:
        # Attempt to retrieve the CID for the file
        cid = contract.functions.getFileCID(file_name).call({'from': address})
        ipfs_link = f'https://gold-rapid-bovid-346.mypinata.cloud/ipfs/{cid}'
        return ipfs_link
    except web3.exceptions.SolidityError as e:
        # Check if the error is due to access denial
        if "You do not have access to view this file." in str(e):
            return "Access denied: You do not have permission to view this file."
        else:
            return f"Error: {str(e)}"
  
   
 

@app.route('/transaction')
def transaction_details():
    tx_hash = request.args.get('hash')
    txn = w3.eth.get_transaction(tx_hash)
    block = w3.eth.get_block(txn.blockHash)
    return render_template('transaction.html', txn=txn, block=block)


if __name__ == '__main__':
    app.run(debug=True)
