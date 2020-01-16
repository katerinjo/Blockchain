# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json

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
    hashed = hashlib.sha256(maybe_valid).hexdigest()
    return hashed[:3] == '000'

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # TODO
    block_string = json.dumps(block)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    return proof