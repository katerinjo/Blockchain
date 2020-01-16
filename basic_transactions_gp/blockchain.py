# Paste your version of blockchain.py from the client_mining_p
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            # TODO
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Append the chain to the block
        self.chain.append(block)

        # Return the new block
        return block

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        byteslike = json.dumps(block).encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(byteslike)

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        hex_hash = raw_hash.hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        maybe_valid = f'{block_string}{proof}'.encode()
        print(maybe_valid)
        hashed = hashlib.sha256(maybe_valid).hexdigest()
        print(hashed)
        return hashed[:6] == '000000'

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return len(self.current_transactions) - 1


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    for required in ['proof', 'id']:
        if required not in data:
            return jsonify({
                'message': f'missing required field {required}'
                }), 400
    proof = data['proof']

    block_string = json.dumps(blockchain.last_block, sort_keys=True)
    if blockchain.valid_proof(block_string, proof):
        sender = '0' # here
        recipient = data['id']
        amount = 1
        blockchain.new_transaction(sender, recipient, amount)

        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            # TODO: Send a JSON response with the new block
            'message': 'New Block Forged',
            'new_block': block
        }

        return jsonify(response), 200
    else:
        return jsonify({'message': 'invalid proof'}), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify({'block': blockchain.last_block})

@app.route('/transactions/new', methods=['POST'])
def transactions_new():
    data = request.get_json()
    for required in ['sender', 'recipient', 'amount']:
        if required not in data:
            return jsonify({
                'message': f'missing required field {required}'
                }), 400
    index = blockchain.new_transaction(
        data['sender'], data['recipient'], data['amount'])
    return jsonify({
        'transaction index': index
    }), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
