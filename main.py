from coin import Ledger, Block, Transaction
import pickle
import hashlib

#Import python ledger object, data type to be update to allow easier modifictaion
ledger = pickle.load( open( "ledger.p", "rb" ) )

#Create unprocessed transaction variable
new_transactions = []

#Run main application
while True:
    command = input("~coin: ").split()
    if command[0] == "exit":
        pickle.dump(ledger, open( "ledger.p", "wb" ))
        break

    elif command[0] == "balance":
        print(ledger.check_balance(int(command[1])))

    elif command[0] == "update":
        new_block = Block(new_transactions, 0, 0)
        ledger.add(new_block)
        new_transactions = []

    elif command[0] == "send":
        new_transaction = Transaction(0, int(command[1]), int(command[2]), int(command[3]))
        new_transactions.append(new_transaction)
