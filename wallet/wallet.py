from .coin import Ledger, Block, Transaction
import pickle
import hashlib
from . import helper
import wallet_client

#Import python ledger object, data type to be update to allow easier modifictaion
ledger = pickle.load( open("ledger.p", "rb" ))

miner_address = int(input("Wallet Address: "))

while True:
    command = input("~coin: ").split() 

    if command[0] == "balance":
        message = [0,1]
        balance = wallet_client.send_message(message)
        print(balance)
    

