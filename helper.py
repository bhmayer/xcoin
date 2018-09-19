import hashlib

#Function to get all transactions associated with an address
def get_transactions (ledger, address):
    transactions = []
    #Go through blockchain and find all transactions for address
    for block in ledger.blocks:
        for transaction in block.transactions:
            if transaction.receiver == address or transaction.sender == address:
                transactions.append(transaction)
                #print("Sender:" + transaction.sender + "; Receiver:" + transaction.receiver + "; Value:" + str(transaction.output))
    return transactions

#Check balance of coins for address, assumes all transactions in ledger are valid
def check_balance(ledger, address):

    #List of all transactions
    transactions = get_transactions(ledger, address)

    #Balance of wallet
    balance = 0

    #Sums up value of transactions, needs update for more complete transaction handeling
    for entry in transactions:
        if entry.receiver == address:
            balance += entry.value
        if entry.sender == address:
            balance -= entry.value
    return balance 


#Label and assign hash value to transactions once assigned to block
def label_transactions(block, block_num):
    counter = 0
    for transaction in block.transactions:
        transaction.set_block(block_num)
        transaction.set_number(counter)
        transaction.set_hash()

#Get list of unspent transactions for a user
def get_unspent_transactions(ledger, address):
    transactions = get_transactions(ledger, address)
    spent_transactions = []
    for transaction in transactions:
        spent_transactions.append(transaction.input_transaction_hash)
    
    unspent_transactions = []
    for transaction in transactions:
        if (transaction.hash not in spent_transactions) & (transaction.receiver == address):
            unspent_transactions.append(transaction)
        
    return unspent_transactions

#Check transaction for validity
def valid_transaction(transaction, ledger, unspent_transactions):
    return 0