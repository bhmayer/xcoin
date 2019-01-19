"""
Protocols and classes for running a node on the network
"""


from coin import Ledger, Block, Transaction
import pickle
import hashlib
import helper
from twisted.internet.protocol import Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, stdio
from twisted.internet.task import LoopingCall
import json
import nacl.encoding
import nacl.signing
from decimal import *

def nodeID(addr):
    """Helper function to create nodeid"""
    return addr.host + "_" + str(addr.port)

class NodeProtocol(LineReceiver):
    """ Protocol for each individual peer connection """

    def __init__(self, addr, factory):
        self.state = "NEW"
        self.addr = addr
        self.factory = factory

    def connectionMade(self):
        self.state = "CONNECTED"
        #self.sendLine(b"connected")
        print("connected")

    def connectionLost(self, reason):
        self.state = "OLD"

    def sendData(self, code, data):
        message_data = [code, data]
        message = json.dumps(message_data)
        self.sendLine(message.encode("ascii"))

    def sendPing(self):
        self.sendData("ping", "")

    def requestPeers(self):
        """ Request peer list from another node """
        self.sendData("sendPeers", "")

    def lineReceived(self, line):
        line = line.decode("ascii")
        message = json.loads(line)
        

        # Dispatch the command to the appropriate method.  Note that all you
        # need to do to implement a new command is add another do_* method.
        command = message[0]
        data = message[1]
        #print("message_received: " + command)


        try:
            method = getattr(self, 'do_' + command)
        except:
            pass
        else:
            try:
                method(data)
            except Exception as e:
                pass

    def do_newBlock(self, data):
        self.factory.newBlockExcept(data,self.addr.host)

    def do_getBlock(self, data):
        self.factory.newBlockNoSend(data)

    def do_returnNextBlock(self, hash_value):
        """ Return the next block after the provided hash """

        break_next_cycle = False

        for block in self.factory.ledger.blocks:
            if break_next_cycle == True:
                """Breaking cycle"""
                self.sendData("getBlock", block.dump())
                break
            elif block.hash == hash_value:
                break_next_cycle = True
    
    def do_ping(self, data):
        self.sendData("pong", "")
    
    def do_pong(self, data):
        #Make this mark the peer for no deletion
        pass

    def do_sendPeers(self,data):
        """ Respond to a request for a peer list """

        peerList = []

        for peer in self.factory.peers:
            peerList.append(peer)

        self.sendData("receivePeers", peerList)


    def do_receivePeers(self,data):
        """ Receive peers from another node """
        
        self.factory.receivePeers(data)

class CommandProtocol(LineReceiver):
    """Protocol for receiving input from the command line"""

    delimiter = b'\n' # unix terminal style newlines. remove this line
                      # for use with Telnet

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.sendLine(b"Web checker console. Type 'help' for help.")

    def lineReceived(self, line):
        # Ignore blank lines
        if not line: return
        line = line.decode("ascii")

        # Parse the command
        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]

        # Dispatch the command to the appropriate method.  Note that all you
        # need to do to implement a new command is add another do_* method.
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError as e:
            self.sendLine(b'Error: no such command.')
        else:
            try:
                method(*args)
            except Exception as e:
                self.sendLine(b'Error: ' + str(e).encode("ascii"))

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command"""
        if command:
            doc = getattr(self, 'do_' + command).__doc__
            self.sendLine(doc.encode("ascii"))
        else:
            commands = [cmd[3:].encode("ascii")
                        for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine(b"Valid commands: " + b" ".join(commands))

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine(b'Goodbye.')
        self.transport.loseConnection()

    def do_balance(self):
        """Return balance of an address"""
        self.sendLine(b"Balance: " + str(self.factory.balance(self.factory.my_address)).encode('ascii'))
        
    def do_send(self, value, address):
        """Send value ammount"""
        value = Decimal(value)
        if value == 0:
            self.sendLine(b"Transaction must be non-zero")
            return
        address = address.encode("ascii")
        unspent_transactions = helper.get_unspent_transactions_user(self.factory.ledger, self.factory.my_address)
        total = 0
        input_transactions = []
        for unspent in unspent_transactions:
            total = total + unspent.value
            input_transactions.append(unspent.hash)
            if total >= value:
                new_transaction = Transaction(input_transactions, value, self.factory.my_address, address)
                signature = self.factory.signing_key.sign(new_transaction.verify_dump().encode("ascii"), encoder=nacl.encoding.HexEncoder).signature
                new_transaction.sign(signature)
                self.factory.new_transactions.append(new_transaction)
                return
        self.sendLine(b"Insufficient balance")

    def do_bootstrap(self):
        """ Make connection to mirror node """
        self.factory.reactor.connectTCP("127.0.0.1", self.factory.PEER_PORT, self.factory)

    def do_update(self):
        """ Create new block """
        self.factory.update()
        self.sendLine(b"New block created")

    def do_address(self):
        """ Return the address for the node """
        self.sendLine(self.factory.my_address)

    def do_status(self):
        """ Check current status of the node """
        self.sendLine(str(self.factory.ledger.block_num()).encode('UTF-8'))
        self.sendLine(str(self.factory.ledger.current_block_hash()).encode('UTF-8'))

    def do_get(self):
        """ For testing, allows me to request the next block """
        self.factory.get()

    def __checkSuccess(self, pageData):
        msg = "Success: got {} bytes.".format(len(pageData))
        self.sendLine(msg.encode("ascii"))

    def __checkFailure(self, failure):
        msg = "Failure: " + failure.getErrorMessage()
        self.sendLine(msg.encode("ascii"))

    def connectionLost(self, reason):
        # stop the reactor, only because this is meant to be run in Stdio.
        self.factory.reactor.stop()

    def do_list(self):
        self.factory.listPeers()

    def do_test(self):
        """ test command for debugging current problem """
        self.factory.requestPeers()


class NodeFactory(ClientFactory):
    def __init__(self, input_reactor, ledger, my_address, signing_key, PEER_PORT, MY_IP):
        self.new_transactions = []
        self.peers = {}
        self.reactor = input_reactor
        self.ledger = ledger
        self.my_address = my_address
        self.signing_key = signing_key
        self.PEER_PORT = PEER_PORT
        self.MY_IP = MY_IP
        self.peers_ip_list = [MY_IP]

    def buildProtocol(self, addr):
        if addr.host not in self.peers_ip_list:
            newProtocol = NodeProtocol(addr, self)
            self.peers[nodeID(addr)] = newProtocol
            self.peers_ip_list.append(addr.host)
            return newProtocol

    def buildCommandProtocol(self):
        self.cmd_line = CommandProtocol(self)
        return self.cmd_line

    def userOutput(self, msg):
        """ Output a message through the command line """
        self.cmd_line.sendLine(msg.encode("ascii"))

    def balance(self, address):
        """ Return the balance of an address """
        return self.ledger.check_balance(address)

    def update(self):
        """ Add a new block to the ledger will be replace with mining """
        new_block = Block(self.new_transactions, self.my_address, self.ledger.current_block_hash())
        if self.ledger.update(new_block):
            self.sendPeers("newBlock", new_block.dump())
        else:
            print("Invalid block")
        print("sent block")
        self.new_transactions = []

    def newBlock(self, block):
        try:
            block = Block.from_json(block)
            if self.ledger.add(block):
                print("Received new block!")
                self.sendPeers("newBlock", block.dump())
            # else:
            #     print("Invalid block")
            self.new_transactions = []
        except Exception as e:
            print(e)

    def newBlockExcept(self, block, do_not_send_peer):
        """ Send block to everyone except do_not_send_peer, usually the sender """
        try:
            block = Block.from_json(block)
            if self.ledger.add(block):
                print("Received new block!")
                self.sendPeersExcept("newBlock", block.dump(), do_not_send_peer)
            # else:
            #     print("Invalid block")
            self.new_transactions = []
        except Exception as e:
            print(e)

    def newBlockNoSend (self, block):
        """ Receive a block and do not send it, useful when asking for older blocks """
        try:
            block = Block.from_json(block)
            if self.ledger.add(block):
                print("Received new block!")
            # else:
            #     print("Invalid block")
            self.new_transactions = []
        except Exception as e:
            print(e)
    
    def sendPeers(self, code, data):
        for peer in self.peers:
            self.peers[peer].sendData(code, data)

    def sendPeersExcept(self, code, data, do_not_send_peer):
        """ Send data to all peers except one, this is usually the sender """
        for peer in self.peers:
            if peer != do_not_send_peer:
                self.peers[peer].sendData(code, data)

    def listPeers(self):
        for peer in self.peers:
            print(peer)

    def get(self):
        """ Requests new block, for testing """
        self.sendPeers("returnNextBlock", self.ledger.current_block_hash())

    def pingPeers(self):
        for peer in self.peers:
            self.peers[peer].sendPing()

    def requestPeers(self):
        """ for trigering code that will be put on a looping call """
        for peer in self.peers:
             self.peers[peer].requestPeers() 
    
    def receivePeers(self, data):
        for peer in data:
            peer_ip = peer.split("_")[0]
            if peer_ip not in self.peers_ip_list:
                self.reactor.connectTCP(peer_ip, self.PEER_PORT, self)

def maintainPeerList(factory):
    """ Looping call function for maintaing a list of peers """
    factory.requestPeers()

