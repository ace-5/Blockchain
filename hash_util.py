import hashlib
import json

def hash_block(block):
    """hashes a block & converts it into string"""
    return hashlib.sha256(json.dumps(block, sort_keys= True).encode()).hexdigest()


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions)+str(last_hash)+str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[0:2] == '00'


def proof_of_work(blockchain, open_transaction):
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof (open_transaction, last_hash, proof):
        proof += 1
    return proof