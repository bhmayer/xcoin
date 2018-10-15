import pickle
import nacl.encoding
import nacl.signing
import nacl.bindings

#Put 32 character string here
seed = "00000000000000000000000000000000"

signing_key = nacl.signing.SigningKey(seed.encode("ascii"))
verify_key = signing_key.verify_key
pubkey = verify_key.encode(encoder=nacl.encoding.HexEncoder)

pickle.dump(seed, open( "seed.p", "wb" ))