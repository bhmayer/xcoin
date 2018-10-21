import datetime
import helper
import hashlib
import json
import nacl.signing
import nacl.exceptions

miner_reward = 0.1

#Ledger class for holding blocks
class Ledger:
    def __init__ (self, blocks):
        self.blocks = blocks

    def update (self, block):

        #Get valid transactions
        block.transactions = helper.process_block(block, self)

        #Miner reward transaction
        reward_transaction = helper.reward(block, miner_reward)
        block.transactions.append(reward_transaction)

        #Label transactions with block number and order and assign hashes
        helper.label_transactions(block, len(self.blocks))

        block.set_hash()  
        self.blocks.append(block)
        return True

    #Add new block sent from another node
    def add (self, block):

        #Check if we are in the right part of the tree
        if self.current_block_hash() != block.prev_hash:
            print("incorrect hash")
            return False

        #Pop reward transaction from last part of the node
        reward_transaction = block.transactions.pop()

        #Check if transactions are valid
        if helper.valid_block(block, self) == False:
            print("invalid transactions")
            return False

        #Check if reward is valid, SECURITY VULNERABILITY, CAN PUT ANYONE AS SENDER AND STEAL MONEY
        if reward_transaction.value != miner_reward:
            ("miner reward incorrect")
            return False

        #Add back reward transaction
        block.transactions.append(reward_transaction)

        #Check if hashes was properly computed
        helper.label_transactions(block, len(self.blocks))
        hash = block.hash
        block.set_hash()
        if block.hash != hash:
            print("could not duplicate hash")
            return False

        self.blocks.append(block)
        return True
        

    def check_balance(self, address):
        return helper.check_balance(self, address)

    def block_num(self):
        return len(self.blocks)

    def current_block_hash(self):
        return self.blocks[-1].hash
                

#Block class for holding transactions
class Block:
    def __init__ (self, transactions, processor, prev_hash):
        self.timestamp = datetime.datetime.now().timestamp()
        self.transactions = transactions
        self.processor = processor
        self.prev_hash = prev_hash
        self.hash = -1

    #Extends transactions for block processing
    def extend_transactions(self, x):
        self.transactions.extend(x)

    #Set hash of the block
    def set_hash(self):
        hash_value = str(self.timestamp) + str(self.processor) + str(self.prev_hash)
        for transaction in self.transactions:
            hash_value = hash_value + str(transaction.hash)
        self.hash = hashlib.sha256(hash_value.encode('utf-8')).hexdigest()

    #Converts block to JSON
    def dump(self):
        block_data = [self.timestamp, self.processor.decode("ascii"), self.prev_hash, self.hash]
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
        block = cls(transactions, block_data[1].encode("ascii"), block_data[2])
        block.timestamp = block_data[0]
        block.hash = block_data[3]
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
        self.signature = "0".encode("ascii")
    
    #Set which block the transaction has been recorded in
    def set_block (self, x):
        self.block = x
    
    #Set the transaction number
    def set_number (self, x):
        self.number = x

    #add signature to transaction
    def sign (self, signature):
        self.signature = signature

    #verify transaction
    def verify (self):
        try:
            verify_key = nacl.signing.VerifyKey(self.sender, encoder=nacl.encoding.HexEncoder)
            message = nacl.encoding.HexEncoder.encode(self.verify_dump().encode("ascii"))
            verify_key.verify(message, self.signature, encoder=nacl.encoding.HexEncoder)
        except nacl.exceptions.BadSignatureError:
            print("invalid transaction")
            return False
        return True

    #Set the input_value of the function, can this functionality be removed?
    def set_input_value (self, x):
        self.input_value = x

    #Set the hash for the transaction
    def set_hash (self):
        hash_value = str(self.input_transaction_hash) + str(self.value) + str(self.sender) + str(self.receiver) + str(self.block) + str(self.number) + str(self.signature)
        self.hash = hashlib.sha256(hash_value.encode('utf-8')).hexdigest()

    #Converts transaction to JSON
    def dump(self):
        data = [self.input_transaction_hash, self.value, self.sender.decode("ascii"), self.receiver.decode("ascii"), self.block, self.number, self.input_value, self.hash, self.signature.decode("ascii")]
        return json.dumps(data)

    #Dump without signature and block information for verification
    def verify_dump(self):
        data = [self.input_transaction_hash, self.value, self.sender.decode("ascii"), self.receiver.decode("ascii")]
        return json.dumps(data)

    #Load object from JSON
    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        obj = cls(data[0], data[1], data[2].encode("ascii"), data[3].encode("ascii"))
        obj.block = data[4]
        obj.number = data[5]
        obj.input_value = data[6]
        obj.hash = data[7]
        obj.signature = data[8].encode("ascii")
        return obj




        
