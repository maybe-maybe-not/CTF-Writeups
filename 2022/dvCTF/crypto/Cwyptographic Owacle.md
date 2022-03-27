# Cwyptographic Owacle
owo? uwu?
We're given a python script which details what the oracle on the server does
```py 
import ecdsa
import random
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

FLAG = b'dvCTF{XXXXXXXXXXXXXXXXXXX}'

def encrypt_flag(priv):

    key = long_to_bytes(priv)
    cipher = AES.new(key, AES.MODE_ECB)
    text = cipher.encrypt(pad(FLAG, 16))
    print(text.hex())

m = 0

print("Hiii ~~ Pwease feel fwee to use my sooper dooper cwyptographic owacle! ~~~~~~")
while True:

    print("[1] > Sign your own message ≧◡≦")
    print("[2] > Get the signed flag uwu ~~ ")
    print("[3] > Quit (pwease don't leave me)")
    try:
        n = int(input())
        if n<0 or n>3:
            raise
    except:
        print("Nice try ಥ_ಥ")
        exit(1)
    if n==1:
        msg = input("What's your message senpai? (●´ω｀●) > ")
        G = ecdsa.NIST256p.generator
        order = G.order()
        print(order)
        priv = random.randrange(1,order)
        Public_key = ecdsa.ecdsa.Public_key(G, G * priv)
        Private_key = ecdsa.ecdsa.Private_key(Public_key, priv)

        k = random.randrange(1, 2**128) if m==0 else int(time.time())*m

        m = int(hashlib.sha256(msg.encode()).hexdigest(),base=16)
        sig = Private_key.sign(m, k)
        print (f"Signature (r,s): ({sig.r},{sig.s})")
    elif n==2:
        if m==0:
            G = ecdsa.NIST256p.generator
            order = G.order()
            print(order)
            priv = random.randrange(1,order)
        encrypt_flag(priv)

    else:
        print("Cya (◕︵◕) ")
        exit(1)
```

So this script uses ECDSA in order to get the signature of our message. Noting that they use `G = ecdsa.NIST256p.generator` it means that the order is consistent where `G = 115792089210356248762697446949407573529996955224135760342422259061068512044369`
A way we could defeat ECDSA is if we would be able to obtain the nonce, `k`.
If we have the nonce, we would be able to recover the private key as we also have the values `r` and `s` (and of course our message `m`)

Looking at how the nonce is generated, a vulnerability presents itself
```py 
k = random.randrange(1, 2**128) if m==0 else int(time.time())*m
```
If `m != 0`, then the nonce is `int(time.time()) * m`, which means if we can control `m`, we can retreive the nonce during that 1 second window by also running `time.time()`
Looking at the code, there is a way to control `m`! Note that the value of `m` is reused from the previous time a message is signed. 
Furthermore, if the value of `m` is set, then the value of `priv` that was used in the signing of `m` would be reused to sign the flag!

So, we have the following
```
1. Input a known message and calculate its hash m
2. Input the same message again, and this time calculate the nonce using time.time() and m from before
3. Retrieve the private key using the values of r and s provided
4. Request for the signed flag
5. Decrypt the flag using the private key
6. Win
```

Let's put this all together in one nice script.

```py
import ecdsa
import libnum
import hashlib
import sys
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

from pwn import *

message = b'owo whats this'
m = int(hashlib.sha256(message).hexdigest(), base=16)

connection = remote('challs.dvc.tf', 2601)
for n in range(4):
    print(connection.recvline())

connection.sendline(b'1')
connection.sendline(message)
for n in range(4):
    connection.recvline()
connection.sendline(b'1')
connection.sendline(message)

k = int(time.time()) * m

signature = (connection.recvline().decode('utf-8')).split(',')
for n in range(3):
    connection.recvline()
connection.sendline(b'2')

flag_hash = connection.recvline().decode('utf-8')[:-2]

r = int(signature[1][5:])
s = int(signature[2][:-3])

G = ecdsa.NIST256p.generator
order = G.order()

r_inv = libnum.invmod(r, order)
priv = (r_inv * ((k * s) - m)) % order
key = long_to_bytes(priv)
cipher = AES.new(key, AES.MODE_ECB)
text = cipher.decrypt(bytearray.fromhex(flag_hash))
print(text)
```
And we get the flag `dvCTF{y0u_h4v3_500p32_d00p32_c2yp70_5kill5_uwu}`!!! 
