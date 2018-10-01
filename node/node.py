#Python file for running node
from coin import Ledger, Block, Transaction
import pickle
import hashlib
import helper
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json

#Import python ledger object, data type to be update to allow easier modifictaion
ledger = pickle.load( open( "ledger.p", "rb" ) )

#Enter address for node block rewards
miner_address = int(input("Enter miner address: "))

class Node(LineReceiver):

    def __init__(self, new_transactions):
        self.new_transactions = new_transactions
        self.state = "NEW"

    def connectionMade(self):
        self.state = "CONNECTED"

    def connectionLost(self, reason):
        self.state = "OLD"

    def lineReceived(self, line):
        message = pickle.loads(line)
        print("message_received")
        if message[0] == 0:
            print(ledger.check_balance(miner_address))
            self.sendLine(str(ledger.check_balance(miner_address)).encode('UTF-8'))

class NodeFactory(Factory):

    def __init__(self):
        self.new_transactions = []

    def buildProtocol(self, addr):
        return Node(self.new_transactions)

reactor.listenTCP(8123, NodeFactory())
reactor.run()