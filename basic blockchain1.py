import datetime
import hashlib
import json
from flask import Flask, jsonify

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        nonce = 0
        prev = "0"
        data = {
            'index': 1,
            'nonce': nonce,
            'timestamp': str(datetime.datetime.now()),
            'prev': prev
        }
        HASH = self.calculate_hash(data)
        while HASH[:4] != '0000':
            nonce += 1
            data['nonce'] = nonce
            HASH = self.calculate_hash(data)
        block = {
            'index': 1,
            'nonce': nonce,
            'timestamp': data['timestamp'],
            'prev': data['prev'],
            'HASH': HASH
        }
        self.chain.append(block)
   


    def create_block(self, prev_block):
        prev_hash = prev_block['HASH']
        prev_nonce = prev_block['nonce']
        index = prev_block['index'] + 1
        timestamp = str(datetime.datetime.now())
        nonce = self.calculate_nonce(prev_hash, prev_nonce, index, timestamp)
        data = {
            'index': index,
            'nonce': nonce,
            'timestamp': timestamp,
            'prev': prev_hash
        }
        HASH = self.calculate_hash(data)
        block = {
            'index': index,
            'nonce': nonce,
            'timestamp': timestamp,
            'prev': prev_hash,
            'HASH': HASH
        }
        self.chain.append(block)

    def calculate_hash(self, data):
        block_str = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def calculate_nonce(self, prev_hash, prev_nonce, index, timestamp):
        nonce = 0
        while True:
            data = {
                'index': index,
                'timestamp': timestamp,
                'prev': prev_hash,
                'nonce': nonce
            }
            HASH = self.calculate_hash(data)
            if HASH[:4] == '0000':
                return nonce
            else:
                nonce += 1

    def get_previous_block(self):
        return self.chain[-1]

    def get_blockchain(self):
        return self.chain


blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    blockchain.create_block(prev_block)
    block = blockchain.get_previous_block()
    response = {
        'message': 'Block mined successfully!',
        'index': block['index'],
        'nonce': block['nonce'],
        'timestamp': block['timestamp'],
        'prev': block['prev'],
        'HASH': block['HASH']
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = blockchain.get_blockchain()
    response = {
        'chain': chain,
        'length': len(chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
