import datetime
import helper
import hashlib
import json

#Ledger class for holding blocks
class Ledger:
    def __init__ (self, blocks):
        helper.label_transactions(blocks[0], 0)
        self.blocks = blocks

    def add (self, block):

        #Check validity of transactions
        if helper.valid_block(block, self) == False:
            return False
        
        #Add transaction to return change to sender
        change_transactions = helper.return_change(block)

        #extend block with change transactions
        block.extend_transactions(change_transactions)

        #Label transactions with block number and order and assign hashes
        helper.label_transactions(block, len(self.blocks))  
        self.blocks.append(block)
        return True

    def check_balance(self, address):
        return helper.check_balance(self, address)

    def block_num(self):
        return len(self.blocks)
                

#Block class for holding transactions
class Block:
    def __init__ (self, transactions, processor, hash):
        self.timestamp = datetime.datetime.now().timestamp()
        self.transactions = transactions
        self.processor = processor
        self.hash = hash

    def extend_transactions(self, x):
        self.transactions.extend(x)

    #Converts block to JSON
    def dump(self):
        block_data = [self.timestamp, self.processor, self.hash]
        transaction_data = []
        for transaction in self.transactions:
            transaction_data.append(transaction.dump())
        data = [block_data, transaction_data]
        return json.dumps(data)

    #Load block from JSON
    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        block_data = data[0]
        transaction_data = data[1]
        transactions = []
        for transaction in transaction_data:
            transactions.append(Transaction.from_json(transaction))
        block = cls(transactions, block_data[1], block_data[2])
        block.timestamp = block_data[0]
        return block



#Transaction class representing the sending of coin
class Transaction:
    def __init__ (self, input_transaction_hash, value, sender, receiver):
        self.input_transaction_hash = input_transaction_hash
        self.value = value
        self.sender = sender
        self.receiver = receiver
        self.block = -1
        self.number = -1
        self.input_value = 0
        self.hash = -1
    
    #Set which block the transaction has been recorded in
    def set_block (self, x):
        self.block = x
    
    #Set the transaction number
    def set_number (self, x):
        self.number = x

    def set_input_value (self, x):
        self.input_value = x

    def set_hash (self):
        hash_value = str(self.input_transaction_hash) + str(self.value) + str(self.sender) + str(self.receiver) + str(self.block) + str(self.number)
        self.hash = hashlib.sha256(hash_value.encode('utf-8')).hexdigest()

    #Converts transaction to JSON
    def dump(self):
        data = [self.input_transaction_hash, self.value, self.sender, self.receiver, self.block, self.number, self.input_value, self.hash]
        return json.dumps(data)

    #Load object from JSON
    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        obj = cls(data[0], data[1], data[2], data[3])
        obj.block = data[4]
        obj.number = data[5]
        obj.input_value = data[6]
        obj.hash = data[7]
        return obj




        
