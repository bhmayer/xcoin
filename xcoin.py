"""

Main file for running a blockchain node

"python xcoin.py" creates a command line interface for running the node
"python xcoin.py -d" creates a peer for running on a docker simulations without commandline input
"python xcoin.py -m" creates a peer mirror for running a peer on your local machine

"""

from node import NodeFactory

import argparse
import pickle
from twisted.internet.protocol import Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, stdio
from twisted.internet.task import LoopingCall
import nacl.encoding
import nacl.signing
from generate_seed_random import generateRandomSeed
import netifaces as ni
import network_settings as ns

#Find machine's own ip address
# ni.ifaddresses('en0')
try:
    myIP = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
except ValueError:
    myIP = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mirror", help="run node as a mirror", action="store_true")
parser.add_argument("-n", "--nirror", help="run node as a mirror", action="store_true")
parser.add_argument("-b", "--bootstrap", help="run as docker bootstrap", action="store_true")
parser.add_argument("-p", "--peer", help="run as docker peer, add additional bootstrap address", action="store_true")
parser.add_argument("address", nargs='?', help="print out if p tag", type=str)
args = parser.parse_args()
if args.mirror:
    ledger_dir = "mirror/ledger.p"
    seed_dir = "mirror/seed.p"
    PORT = 8124
    PEER_PORT = 8123
elif args.bootstrap:
    ledger_dir = "ledger.p"
    seed_dir = "seed.p"
    PORT = 8123
    PEER_PORT = 8123
    generateRandomSeed()
elif args.peer:
    ledger_dir = "peer/ledger.p"
    seed_dir = "seed.p"
    PORT = 8123
    PEER_PORT = 8123
    BOOTSTRAP_ADDRESS = args.address
    generateRandomSeed()
elif args.nirror:
    ledger_dir = "ledger.p"
    seed_dir = "seed.p"
    PORT = 8125
    PEER_PORT = 8123
else:
    ledger_dir = "ledger.p"
    seed_dir = "seed.p"
    PORT = 8123
    PEER_PORT = 8124

#Set configuration for network settings
PEER_LIST_SIZE = 30


#Import python ledger object, data type to be updated to allow easier modifictaion
ledger = pickle.load( open(ledger_dir, "rb" ) )

#Import secret key
seed = pickle.load( open(seed_dir, "rb") )
signing_key = nacl.signing.SigningKey(seed.encode("ascii"))
verify_key = signing_key.verify_key
pubkey = verify_key.encode(encoder=nacl.encoding.HexEncoder)

#Enter address for node block rewards
my_address = pubkey

factory = NodeFactory(reactor, ledger, my_address, signing_key, PEER_PORT, myIP, ns)

stdio.StandardIO(factory.buildCommandProtocol())

if args.peer:
    reactor.connectTCP(BOOTSTRAP_ADDRESS, PEER_PORT, factory) 



def maintainPeerList(factory):
    """ Looping call function for maintaing a list of peers """
    if factory.peerListSize() < ns.PEER_LIST_SIZE:
        factory.requestPeers()
        print("maintain")



def update(factory):
    factory.update()

lc = LoopingCall(maintainPeerList, factory)
# reactor.callLater(5, lc)
lc.start(20)

if args.bootstrap:
    lc2 = LoopingCall(update, factory)
    lc2.start(10)


reactor.listenTCP(PORT, factory)
reactor.run()