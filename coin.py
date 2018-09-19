import datetime
import helper
import hashlib

#Ledger class for holding blocks
class Ledger:
    def __init__ (self, blocks):
        helper.label_transactions(blocks[0], 0)
        self.blocks = blocks

    def add (self, block):
        helper.label_transactions(block, len(self.blocks))
        self.blocks.append(block)

    def check_balance(self, address):
        return helper.check_balance(self, address)
                

#Block class for holding transactions
class Block:
    def __init__ (self, transactions, processor, hash):
        self.timestamp = datetime.datetime.now().timestamp()
        self.transactions = transactions
        self.processor = processor
        self.hash = hash


#Transaction class representing the sending of coin
class Transaction:
    def __init__ (self, input_transaction_hash, value, sender, receiver):
        self.input_transaction_hash = input_transaction_hash
        self.value = value
        self.sender = sender
        self.receiver = receiver
        self.block = -1
        self.number = -1
    
    #Set which block the transaction has been recorded in
    def set_block (self, x):
        self.block = x
    
    #Set the transaction number
    def set_number (self, x):
        self.number = x

    def set_hash (self):
        print(self.input_transaction_hash)
        print(hash(self.input_transaction_hash))
        print(self.number)
        hash_value = str(self.input_transaction_hash) + str(self.value) + str(self.sender) + str(self.receiver) + str(self.block) + str(self.number)
        print(hash_value)
        self.hash = hashlib.sha256(hash_value.encode('utf-8')).hexdigest()
        print(self.hash)

        
