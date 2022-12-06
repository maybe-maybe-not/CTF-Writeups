
#print(open('Crypto/crypto_thatsALotOfRSA/pubkeys/key_00000.pem').read())

import os
from Crypto.PublicKey import RSA
import random
import signal
import math
from datetime import datetime
from pwn import *

pubkeydir = 'Crypto/crypto_thatsALotOfRSA/pubkeys/'
keys = os.listdir(pubkeydir)

print(keys)

# fileOut = "Crypto/crypto_thatsALotOfRSA/nPublic.txt"
# f = open(fileOut, 'w')

# List of all the n
keysN = []
# Buckets
keysNDouble = []
it = 10


tot = 0
# Read all the public keys and set up the buckets **before the query**
for fileName in keys:
    key = RSA.import_key(open(f'{pubkeydir}/{fileName}').read())   
    #f.write(str(key.n) + "\n")
    keysN.append(key.n)
    if (tot % it == 0):
        keysNDouble.append(key.n)
    else:
        keysNDouble[-1] *= key.n
    tot += 1

# start the thing!
io = remote("157.245.52.169", 31322)

n = []

# reading the queries
for i in range(200):
    if i == 1:
        oldT = datetime.now()
    n.append(int(io.recvline().split(b" ")[2].decode()))


print("starting!")
# Calculate the gcd
m = []
for i in n:
    # Start from the buckets
    for jIndex in range(len(keysNDouble)):
        j = keysNDouble[jIndex]
        k = math.gcd(i, j)
        # if gcd is not 1
        if (k != 1):
            # if gcd is not the query, output it
            if (k != i):
                m.append(k)
            else:
                # otherwise, query from all 10 items in the bucket
                for newIndex in range(it*jIndex, it*jIndex+it):
                    k = math.gcd(i, keysNDouble[newIndex])
                    if (k != 1):
                        m.append(k)
            break;


io.recvline()

print(datetime.now())
print(datetime.now() - oldT)

# print out the answers
for i in range(200):
    question = io.recvline() # should equal p[i]
    print(question)
    io.sendline(str(m[i]).encode('ascii'))

print("done")

print(datetime.now())
print(datetime.now() - oldT)

io.interactive()