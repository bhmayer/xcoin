from coin import Block, Transaction, Ledger
import pickle

#special genesis transaction
class God_Transaction:
    def __init__ (self, value):
        self.output_value = value

#Generate the first block of the chain
def genesis():
    value = 1
    god_transaction = God_Transaction(value)
    genesis_transaction = Transaction(god_transaction, value, "-1", "0")
    genesis_transactions = [genesis_transaction]
    genesis_block = Block(genesis_transactions, 0, 0)
    return Ledger([genesis_block])

ledger = genesis()

pickle.dump(ledger, open( "ledger.p", "wb" ))





