from coin import Ledger, Block, Transaction
import pickle
import hashlib
import helper

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
        unspent = helper.get_unspent_transactions(ledger, int(command[2]))
        new_transaction = Transaction(unspent[0].hash, unspent[0].value, int(command[2]), int(command[3]))
        new_transactions.append(new_transaction)

    elif command[0] == "unspent":
        unspent = helper.get_unspent_transactions(ledger, int(command[1]))
        for un in unspent:
            print(un.value)


