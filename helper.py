#Check balance of coins for address, assumes all transactions in ledger are valid
def check_balance(ledger, address):

    #List of all transactions
    entries = []

    #Balance of wallet
    balance = 0

    #Go through blockchain and find all transactions for address
    for block in ledger.blocks:
        for transaction in block.transactions:
            if transaction.receiver == address or transaction.sender == address:
                entries.append(transaction)
                #print("Sender:" + transaction.sender + "; Receiver:" + transaction.receiver + "; Value:" + str(transaction.output))

    #Sums up value of transactions, needs update for more complete transaction handeling
    for entry in entries:
        if entry.receiver == address:
            balance += entry.output_value
        if entry.sender == address:
            balance -= entry.output_value

    return balance

def valid_transaction(transaction, ledger):
    return 0