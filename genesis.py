from coin import Block, Transaction, Ledger
import pickle

#Generate the first block of the chain
def genesis():
    value = 1
    genesis_transaction = Transaction(0, value, -1, 0)
    genesis_transactions = [genesis_transaction]
    genesis_block = Block(genesis_transactions, 0, 0)
    return Ledger([genesis_block])

ledger = genesis()

pickle.dump(ledger, open( "ledger.p", "wb" ))





