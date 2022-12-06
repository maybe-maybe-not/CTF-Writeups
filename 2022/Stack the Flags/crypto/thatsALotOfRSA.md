# Encryptdle
Written by m0n0valu3nce
## Provided Files 
[Challenge File](./assets/thatsALotOfRSA/rsa_challenge.py)

[Other Assets](./assets/thatsALotOfRSA/pubkeys.zip)

## Solution
In this challenge, we are given 20000 public keys, containing pairs of $(n, k)$. The server will then do the following 200 times:

1. Pick 2 random keys, and pick 1 prime from each key.
2. Multiply them together and provide it to us as $n_i$.

Then, we are tasked to find a prime factor for every $n_i$.

A native solution would be to take the gcd between every $n_i$ with all public keys $m_j$. If the gcd is non-zero, we have found the solution, and may move on. However, running this and timing how long it takes to compute the gcds, we notice that it takes... 13 seconds (locally). Because my PC is slow, this solution isnt fast enough, so we have to think harder (Note: this solution is already fast enough for some PCs, smh pay to win challenge). 

One is immediately tempted to do Binary Search, checking if the factor lies in the first 10k factors, then the first 5k, etc etc. However, noting that we just have to shave off 30% of our time, we dont have to cry in the implementation hell that is BSTA. 

Instead, I opted to do _bucketting_. This technique makes us check the 20000 public keys in groups. We multiply the numbers $m_{10k+1}$ to  $m_{10k+10}$ to form $M_k$. We then query $\gcd(n_i, M_k)$. If this is a factor of $n_i$, we can just output that, and move on to the next number. If it outputs $n$, we may just check all 10 of them to find a factor. 

This reduces the amount of time needed to query everything to about 7 seconds (locally), giving us enough time to read and output the factors. 

_The code is found in [here](./assets/thatsALotOfRSA/solve.py)_

```py

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
```

Flag: `STF22{rsa_823564830a826421}`
