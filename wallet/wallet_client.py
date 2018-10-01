from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json
import pickle

class WalletClient(LineReceiver):

    def __init__(self, message, response):
        self.message = message
        self.response = response
        self.state = "NEW"

    def connectionMade(self):
        self.state = "CONNECTED"
        self.sendLine(pickle.dumps(self.message))
        

    def connectionLost(self, reason):
        self.state = "OLD"
        reactor.stop()

    def lineReceived(self, line):
        self.state = "Received"
        self.response = line
        self.transport.loseConnection()

class WalletClientFactory(ClientFactory):

    def __init__(self, message, response):
        self.message = message
        self.response = response

    def buildProtocol(self, addr):
        return WalletClient(self.message, self.response)


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())

def send_message(message):
    response = ""
    reactor.connectTCP("127.0.0.1", 8123, WalletClientFactory(message, response))
    reactor.run()
    return response
