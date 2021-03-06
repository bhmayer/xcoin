"""

Helper functions for the coin.py blockchain data structure file

"""

import hashlib
import coin
import copy
import nacl
from decimal import *

#Function to get all transactions associated with an address
def get_transactions_user (ledger, address):
    transactions = []
    #Go through blockchain and find all transactions for address
    for block in ledger.blocks:
        for transaction in block.transactions:
            if transaction.receiver == address or transaction.sender == address:
                transactions.append(transaction)
                #print("Sender:" + transaction.sender + "; Receiver:" + transaction.receiver + "; Value:" + str(transaction.output))
    return transactions

def get_transactions (ledger):
    transactions = []
    #Go through blockchain and find all transactions for address
    for block in ledger.blocks:
        for transaction in block.transactions:
            transactions.append(transaction)
    return transactions

#Check balance of coins for address, assumes all transactions in ledger are valid
def check_balance(ledger, address):

    #List of all transactions
    transactions = get_transactions_user(ledger, address)

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
def get_unspent_transactions_user(ledger, address):
    transactions = get_transactions_user(ledger, address)
    spent_transactions = []
    for transaction in transactions:
        spent_transactions.extend(transaction.input_transaction_hashes)
    
    unspent_transactions = []
    for transaction in transactions:
        if (transaction.hash not in spent_transactions) & (transaction.receiver == address):
            unspent_transactions.append(transaction)
        
    return copy.deepcopy(unspent_transactions)

#Get unspent transactions for the ledger
def get_unspent_transactions(ledger):
    blocks = ledger.blocks
    spent_transactions = []
    for block in blocks:
        for transaction in block.transactions:
            spent_transactions.extend(transaction.input_transaction_hashes)
    
    unspent_transactions = []
    for block in blocks:
        for transaction in block.transactions:
            if (transaction.hash not in spent_transactions):
                unspent_transactions.append(transaction)

    return copy.deepcopy(unspent_transactions)

#Check transaction for validity
def valid_transaction (transaction, ledger, unspent_transactions):
    for unspent_transaction in unspent_transactions:
        if transaction.input_transaction_hash == unspent_transaction.hash:
            if transaction.value <= unspent_transaction.value:
                transaction.set_input_value(unspent_transaction.value)
                unspent_transaction.value = unspent_transaction.value - transaction.value
                return True
    return False

#Function for preparing block for publication
def process_block (block, ledger):
    unspent_transactions = get_unspent_transactions(ledger)
    valid_transactions = []
    input_transactions = []

    #Iterate through and verify correct balance for input transactions
    for transaction in block.transactions:
        
        #Verify user signed transaction
        if transaction.verify():
            
            #Check value of input transactions is sufficient for value of the transaction 
            total = 0
            inputs = []
            for unspent_transaction in unspent_transactions:
                if unspent_transaction.hash in transaction.input_transaction_hashes:
                    
                    #Make sure the sender owns the transaction
                    if unspent_transaction.receiver == transaction.sender:
                        total = total + unspent_transaction.value
                        inputs.append(unspent_transaction)

            #Set new input_transaction values to generate change            
            if total >= transaction.value:
                for input_transaction in inputs:
                    if total > 0:
                        if total >= input_transaction.value:
                            total = total - input_transaction.value
                            input_transaction.value = 0
                        else:
                            input_transaction.value = input_transaction.value - total
                            total = 0
                    input_transactions.extend(inputs)
                valid_transactions.append(transaction)


    #Return change
    for transaction in input_transactions:
        if transaction.value > 0:
            change_transaction = coin.Transaction(transaction.hash, transaction.value, transaction.receiver, transaction.receiver)
            valid_transactions.append(change_transaction)

    return valid_transactions
        
#Check block is valid
def valid_block (block, ledger):
    unspent_transactions = get_unspent_transactions(ledger)
    used_input_transactions = []
    for transaction in block.transactions:
        
        #Check if non-change transactions have valid signature
        if transaction.sender != transaction.receiver:
            if transaction.verify() == False:
                print("transaction not verified")
                return False

        #Check value of input transactions is sufficient for value of the transaction 
        total = 0
        inputs = []
        for unspent_transaction in unspent_transactions:
            if unspent_transaction.hash in transaction.input_transaction_hashes:
                #Make sure the sender owns the transaction
                if unspent_transaction.receiver == transaction.sender:
                    total = total + unspent_transaction.value
                    inputs.append(unspent_transaction)

        #Set new input_transaction values to generate change            
        if total >= transaction.value:
            for input_transaction in inputs:
                if total > 0:
                    if total >= input_transaction.value:
                        total = total - input_transaction.value
                        input_transaction.value = 0
                    else:
                        input_transaction.value = input_transaction.value - total
                        total = 0
                used_input_transactions.extend(inputs)
        else:
            return False
        
        

    for transaction in used_input_transactions:
        if transaction.value != 0:
            print("incorrect change")
            return False

    return True
                    


#Return change on block
def return_change(block):
    change_transactions = []
    for transaction in block.transactions:
        if transaction.value < transaction.input_value:
            change = coin.Transaction(transaction.input_transaction_hash, transaction.input_value - transaction.value, transaction.sender, transaction.sender)
            change_transactions.append(change)
    return change_transactions

#Return reward transaction for miner
def reward(block, miner_reward):
    reward_transaction = coin.Transaction("0", miner_reward, nacl.encoding.HexEncoder.encode(b"miner_reward"), block.processor)
    reward_transaction.sign(nacl.encoding.HexEncoder.encode(b"signed"))
    return reward_transaction

#Check if reward transaction is valid, ensures not sending from another users or transactions
def valid_reward(transaction, miner_reward):
   x = transaction.value == miner_reward
   y = transaction.sender == nacl.encoding.HexEncoder.encode(b"miner_reward")
   z = transaction.input_transaction_hashes == ["0"]
   return x and y and z

def check_nonce(hash_value, nonce, POW_difficulty):
    target = ""
    for _ in range(POW_difficulty):
        target = target + "0"
    
    result = hashlib.sha256((hash_value+str(nonce)).encode('utf-8')).hexdigest()

    if result[:POW_difficulty] == target:
        return True
    
    return False


        
        

