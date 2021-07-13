import hashlib
import json
from collections import OrderedDict

import hash_util

# GENESIS_BLOCK to initialize blockchain
GENESIS_BLOCK = {
    'last_hash': '',
    'transaction_index': 0,
    'transactions': [],
    'proof': 1
}
# reward miners to add open transaction to our blockchain
MINING_REWARD = 10
blockchain = [GENESIS_BLOCK]
open_transaction = []
owner = input('ENTER YOUR NAME: ')
participants = {owner}


def transaction_details():
    """takes the details of tx (amount, recipient)"""
    sender = owner
    amount = float(input('ENTER AMOUNT TO BE TRANSACTED: '))
    received_by = input('ENTER THE RECEIVER OF THE COIN: ')
    return amount, received_by, sender


def add_transaction(receiver, amount, sender):
    """details entered by user is added to list of open transaction"""
    transaction = OrderedDict([
        ('sender', sender),
        ('receiver', receiver),
        ('amount', amount)
    ])
    if check_balance(transaction):
        open_transaction.append(transaction)
        participants.add(sender)
        participants.add(receiver)
        return True
    invalid()


def get_balance(participant):
    """returns the net balance in current owner's account"""
# make a list of all tx in blockchain where owner is sender
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    pending_balance = [tx['amount']
                       for tx in open_transaction if participant == tx['sender']]
    tx_sender.append(pending_balance)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

# make a list of all tx in blockchain where owner is receiver
    tx_receiver = [[tx['amount'] for tx in block['transactions']
                    if tx['receiver'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_receiver:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def check_balance(transaction):
    user_balance = get_balance(transaction['sender'])
    return user_balance >= transaction['amount']


# def hash_block(block):
#     """hashes a block & converts it into string"""
#     return hashlib.sha256(json.dumps(block, sort_keys= True).encode()).hexdigest()


# def valid_proof(transactions, last_hash, proof):
#     guess = (str(transactions)+str(last_hash)+str(proof)).encode()
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     return guess_hash[0:2] == '00'


# def proof_of_work():
#     last_block = blockchain[-1]
#     last_hash = hash_util.hash_block(last_block)
#     proof = 0
#     while not valid_proof(open_transaction, last_hash, proof):
#         proof += 1
#     return proof


def mine_block():
    """Adds all the open transaction to the blockchain"""
    last_block = blockchain[-1]
    hash_value = hash_util.hash_block(last_block)
    proof = hash_util.proof_of_work(blockchain, open_transaction)

    reward_block = OrderedDict([
        ('sender', 'SYSTEM'),
        ('receiver', owner),
        ('amount', MINING_REWARD)
    ])
    new_balance = (get_balance(owner)) + 10
    print('New balance = ' + str(new_balance))
    copied_tx = open_transaction[:]
    copied_tx.append(reward_block)

    block = {
        'last_hash': hash_value,
        'transaction_index': len(blockchain),
        'transactions': copied_tx,
        'proof': proof
    }
    blockchain.append(block)
    return True


def view_transaction():
    """Gives all the transaction stored on blockchain"""
    print('-'*50)
    print('-'*50)
    print('OUTPUTTING BLOCKCHAIN...')
    for blocks in blockchain:
        print(blocks)
        print('*'*120)


def verify():
    """Verifies the hashes stored in blockchain with previous hashes"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['last_hash'] != hash_util.hash_block(blockchain[index-1]):
            return False
        if not hash_util.valid_proof (block['transactions'][:-1], block['last_hash'], block['proof']):
            print('INVALID PROOF OF WORK')
            return False
        return True


def invalid():
    print(blockchain)
    print('-'*120)
    print('Something went wrong. Please try again')
    return False


blockchain_status = True

while blockchain_status:
    print('1. ADD TRANSACTION')
    print('2. MINE BLOCKS')
    print('3. VIEW TRANSACTION')
    print('4. SHOW PARTICIPANTS')
    print('h. TO MANIPULATE CHAIN')
    print('q. QUIT')
    choice = input('ENTER YOUR CHOICE:  ')
    if choice == '1':
        tx_data = transaction_details()
        amount, receiver, sender = tx_data
        if add_transaction(receiver, amount, sender):
            print('TRANSACTION SUCCESSFUL')
            print('New balance = {:.3f}'.format((get_balance(owner))))
        else:
            print('INSUFFICIENT FUND')
            print('Total balance = {:.3f}'.format((get_balance(owner))))

    elif choice == '2':
        if mine_block():
            open_transaction = []

    elif choice == '3':
        view_transaction()

    elif choice == '4':
        print(participants)

    elif choice == 'q':
        break

    elif choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'victim', 'receiver': 'hacker', 'amount': 100.0}]
            }

    else:
        blockchain_status = invalid()

    if not verify():
        print('-'*120)
        print('INVALID BLOCKCHAIN')
        blockchain_status = invalid()

print('.'*120)
print("Done!!!!")
