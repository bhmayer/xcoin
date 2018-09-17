import datetime
import helper

#Ledger class for holding blocks
class Ledger:
    def __init__ (self, blocks):
        self.blocks = blocks

    def add (self, block):
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
    def __init__ (self, input_transaction, output_value, sender, receiver):
        self.input_transaction = input_transaction
        self.input_value = input_transaction.output_value
        self.output_value = output_value
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


        
