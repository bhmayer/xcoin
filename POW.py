""" Function for finding hash value of some dificulty """

import random
import hashlib
import time
import string



def find_nonce(hash_value, POW_difficulty):

    nonce = 0
    target = ""
    result = ""
    for _ in range(POW_difficulty):
        target = target + "0"

    while result[:POW_difficulty] != target:
        nonce = nonce + 1
        result = hashlib.sha256((hash_value+str(nonce)).encode('utf-8')).hexdigest()

    return nonce

if __name__ == "__main__":
   
    #letters = string.ascii_lowercase
    # hash_value = "".join(random.choice(letters) for i in range(32))
    hash_value="abcdefghijklmonp"
    print(find_nonce(hash_value, 6))