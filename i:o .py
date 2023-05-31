'''Code to uplode data on web3.storage get its CID (Content Identifier which is kind of hash of ipsf protocol)
and uplode it to blockchain and also recive data using CID from ipsf
'''
'''  pip install requests
     pip install web3
     pip install pyweb3


'''


# Ethereum network URL
import requests
from web3 import Web3
import json
from pyweb3.storage import File, Web3Storage
ethereum_url = 'YOUR_ETHEREUM_NETWORK_URL'

# Contract address
contract_address = 'YOUR_CONTRACT_ADDRESS'


contract_abi = json.loads('CONTRACT_ABI')


web3 = Web3(Web3.HTTPProvider(ethereum_url))

# Create a web3.storage instance
storage = Web3Storage()

# Function to upload a file to web3.storage


def upload_file_to_web3storage(file_data):

    file = File(file_data)

    cid = storage.store_file(file)

    return cid

# Function to retrieve a file from web3.storage using the CID


def retrieve_file_from_web3storage(cid):

    file = storage.get(cid)

    file_data = file.data

    return file_data

# Function to upload a file and store the CID on the blockchain


def upload_and_store(file_data):

    cid = upload_file_to_web3storage(file_data)

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    tx_hash = contract.functions.storeCID(cid).transact()

    receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return cid

# Function to retrieve a file from the blockchain using the CID and fetch content from web3.storage


def retrieve_file(cid):

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    stored_cid = contract.functions.getStoredCID().call()

    if stored_cid == cid:

        file_data = retrieve_file_from_web3storage(cid)
        return file_data
    else:
        raise Exception(
            "CID does not match the stored value on the blockchain.")


if __name__ == '__main__':
    # Code for file upload and retrieval
    ...
