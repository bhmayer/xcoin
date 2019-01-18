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

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mirror", help="run node as a mirror", action="store_true")
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
elif args.peer:
    ledger_dir = "ledger.p"
    seed_dir = "seed.p"
    PORT = 8123
    PEER_PORT = 8123
    BOOTSTRAP_ADDRESS = args.address
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

factory = NodeFactory(reactor, ledger, my_address, signing_key, PEER_PORT)

if args.peer:
    reactor.connectTCP(BOOTSTRAP_ADDRESS, PEER_PORT, factory) 
elif args.bootstrap:
    reactor.connectTCP("10.0.18.40", PEER_PORT, factory) 
else:
    stdio.StandardIO(factory.buildCommandProtocol())

def maintainPeerList(factory):
    """ Looping call function for maintaing a list of peers """
    factory.requestPeers()

# if (not args.mirror) & (not args.peer) & (not args.bootstrap):
#     lc = LoopingCall(maintainPeerList, factory)
#     lc.start(5)

reactor.listenTCP(PORT, factory)
reactor.run()