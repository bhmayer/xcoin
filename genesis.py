from coin import Block, Transaction, Ledger
import pickle
import helper

#Generate the first block of the chain
def genesis():
    value = 1
    genesis_transaction = Transaction(0, value, -1, 0)
    genesis_transactions = [genesis_transaction]
    genesis_block = Block(genesis_transactions, 0, 0)
    helper.label_transactions(genesis_block, 0)
    genesis_block.set_hash()
    return Ledger([genesis_block])

ledger = genesis()

pickle.dump(ledger, open( "ledger.p", "wb" ))





