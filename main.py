blockchain = []

def add_transaction():
    """Adds any transaction user makes to the blockchain"""
    amount = float(input('ENTER AMOUNT TO BE TRANSACTED: '))
    if len(blockchain) < 1:
        blockchain.append([amount])
    else:
        blockchain.append([blockchain[-1], amount])

def view_transaction():
    """Provides the transaction stored upon blockchain"""
    print('OUTPUTTING BLOCKCHAIN...')
    for blocks in blockchain:
        print(blocks)
        print('*'*20)

def verify():
    """Verifies the hashes stored in blockchain with previous hashes"""
    is_valid = True
    for chain_index in range(1, len(blockchain)):
        if blockchain[chain_index][0] == blockchain[chain_index - 1]:
            is_valid = True
        else:
            is_valid = False
    return is_valid


def invalid():
    print('Something went wrong. Please try again')

while True:
    print('1. ADD TRANSACTION')
    print('2. VIEW BLOCKCHAIN')
    print('q. QUIT')
    choice = input('ENTER YOUR CHOICE:  ')
    if choice == '1':
        add_transaction()
    elif choice == '2':
        view_transaction()
    elif choice == 'q':
        break
    else:
        invalid()
    if not verify():
        view_transaction()
        invalid()
        break

print('.'*20)
print ("Done!!!!")