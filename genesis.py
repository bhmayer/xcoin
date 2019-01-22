"""

Program to create the genesis block

"""

from coin import Block, Transaction, Ledger
import pickle
import helper
import nacl.encoding
import nacl.signing
import nacl.bindings

seed = pickle.load( open("seed.p", "rb") )
signing_key = nacl.signing.SigningKey(seed.encode("ascii"))
verify_key = signing_key.verify_key
pubkey = verify_key.encode(encoder=nacl.encoding.HexEncoder)


#Generate the first block of the chain
def genesis():
    value = 1
    genesis_transaction = Transaction("0", value, -1, pubkey)
    genesis_transactions = [genesis_transaction]
    genesis_block = Block(genesis_transactions, 0, 0)
    helper.label_transactions(genesis_block, 0)
    genesis_block.set_block_number(0)
    genesis_block.set_hash()
    return Ledger([genesis_block])

ledger = genesis()

pickle.dump(ledger, open( "ledger.p", "wb" ))





