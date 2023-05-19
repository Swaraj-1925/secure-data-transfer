import datetime #used to timestamp the block
import hashlib #used to create hash
import json #we need the Dom's function to encode the blocks before we hash them 
from flask import Flask, jsonify # we will import flask class used for web application and jsonify to return messages in postman when we interact with blockchain

class Blockchain:
    def __init__(self):
        self.chain = []  # list which will contain the blockchain
        self.create_block(proof=1, pre_hash='0')

    def create_block(self, proof, pre_hash):  # this function will create a block and add blocks to chain
        block = {                               ##this is dict which conatain what a genraly block contain
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'pre_hash': pre_hash
        }
        self.chain.append(block)
        return block

    def get_pre_block(self):
        return self.chain[-1] #-1 means it will return last block

    def proof_of_work(self, pre_proof):
        new_proof = 1   # its basicaly nounce
        check_proof = False

        while check_proof is False:
            hash_op = hashlib.sha256(str(new_proof**2 - pre_proof**2).encode()).hexdigest() #here we are creating a probelm to create a hash
            if hash_op[:4] == '0000':                                                        #for block which can minors slove to get hash
                check_proof = True                                                          # its a string because hash is string 
            else:                                                                           # encode().it convert stirng into format sha256 expect
                new_proof += 1                                                              # hexdigest() it covert the stirng into hexademicmal number
        return new_proof

    def hash(self, block):                                   #this funtion will take block as input and return its sha256 hash
        encoded_block = json.dumps(block, sort_keys=True).encode() #dumps funtion from jason labraie convert any data into stirng in jason file
        return hashlib.sha256(encoded_block).hexdigest()            #we didnt use str() because for minnig we need jason file
    

    def is_chain_valid(self, chain):  # this funtion will check if over blocks in block chain is valid for this we will chechek 1st pre hash = next hash and proof work matches the proof of work problem
        pre_block = chain[0]    # we get the 1st block from chain(the list at top)
        block_index = 1     # block number start from 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['pre_hash'] != self.hash(pre_block): #  block['pre_hash'] (dictionary)and self.hash(pre_block) it will call a hash funtion defined above
                return False

            pre_proof = pre_block['proof'] #it store proof of previous block
            proof = block['proof']
            hash_op = hashlib.sha256(str(proof**2 - pre_proof**2).encode()).hexdigest()
            if hash_op[:4] != '0000': #  block['pre_hash'] (dictionary)and self.hash(pre_block) it will call a hash funtion defined above
                return False
            pre_block = block
            block_index += 1
        return True


# Creating a web App
app = Flask(__name__)

# Creating Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET']) #part of web applicaton
def mine_block():
    pre_block = blockchain.get_pre_block() #pre_block will contain value of last block thats that all dict
    pre_proof = pre_block['proof']  #for minning we just need the "proof" key from dictionry 
    proof = blockchain.proof_of_work(pre_proof) #value of pre_proof is sent to proof_of_work funtion which will return new proof 
    pre_hash = blockchain.hash(pre_block)#data from pre_block is sent to hash funtion which will conver that data into hash
    block = blockchain.create_block(proof, pre_hash)    
    response = {                        #this data is printed
        'message': 'Congratulations!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'pre_hash': block['pre_hash']
    }
    return jsonify(response), 200

# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {                #this data is printed
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# Running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
