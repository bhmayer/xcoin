import pickle
import nacl.encoding
import nacl.signing
import nacl.bindings
import random
import string

def generateRandomSeed():
    #generate random 32 character seed
    letters = string.ascii_lowercase

    seed = "".join(random.choice(letters) for i in range(32))


    signing_key = nacl.signing.SigningKey(seed.encode("ascii"))
    verify_key = signing_key.verify_key
    pubkey = verify_key.encode(encoder=nacl.encoding.HexEncoder)

    pickle.dump(seed, open( "seed.p", "wb" ))