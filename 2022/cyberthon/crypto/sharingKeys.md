# Sharing Keys
Written by m0n0valu3nce
## __Problem statement__
> Some packets from APOCALYPSE got caught.
> 
> Looks like some [DHKE exchange](https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange#General_overview).
> 
> Get to the bottom of this!
## Solution
We are provided with some web packets outlining a conversation between 2 people. After using wireshark to extract the conversation, this is what we are presented with. 

```
{"req": "DHKE init0", "prime": 7928861973209, "alpha": 164626272775};;;
{"res": "DHKE stepA", "publickey": 63976384709};;;
{"req": "DHKE stepB", "publickey": 4206122221774};;;
{"res": "AES init", "key gen function": "AESkey = hashlib.md5(str(sharedKey).encode()).digest()"};;;
{"req": "AES cipher", "cipher init function": "Cipher = AES.new(AESkey, AES.MODE_CBC)"};;;
{"res": "AES ready", "need": ["iv", "ciphertext"]};;;
{"req": "AES data", "hex(iv)": "9a666609552ae95dcf7ab9a76a658875", "hex(ciphertext)": "afa4c75807cabc743309a0a2b0d043010ca7d963cbef6584cadeb6daf9e0d6359cc8da72a5f0ab74eb37505d99b9e4c0"};;;
{"res": "verify recv data", "hex(sha256(data))": "3ce9074b24082c72a9768ed91d16e805ee8cd0c618ed2e13f54f2b0034fae3c8"};;;
{"req": "verify recv data", "status": "correct", "timestamp": "Fri Jan 28 00:44:50 2022"};;;
{"res": "thank you for the flag, have a nice day!"};;;
```

Seeing the conversation, we simply have to solve the DHKE key exchange problem. However, we notice that the prime used is relatively small. (For context, the prime is usually about 128/256 bits long.) Doing some [searching](https://ctftime.org/writeup/29596) online, we notice that we may use the Pohlig Hellman algorithm to compute discrete logarithms. 

```py
from binascii import unhexlify
import hashlib

p = 7928861973209
g = 164626272775

dio = 63976384709
# jotaro = pow(g,b,p)
jotaro = 4206122221774

F = IntegerModRing(p)

a = discrete_log(F(dio), F(g))
print(a)

sharedKey = pow(jotaro, a, p)

print(sharedKey)
```
Note: for the above,  **please** use sage to run the code
From here, it suffices to decrypt the string. 

```py
from binascii import unhexlify
from Crypto.Cipher import AES
from hashlib import sha256
import hashlib



key = 3371742226716
AESkey = hashlib.md5(str(key).encode()).digest()

iv = unhexlify("9a666609552ae95dcf7ab9a76a658875")
ct = unhexlify("afa4c75807cabc743309a0a2b0d043010ca7d963cbef6584cadeb6daf9e0d6359cc8da72a5f0ab74eb37505d99b9e4c0")

cipher = AES.new(AESkey, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)
print(pt)
```

Flag: `Cyberthon{0neSt3p@taT1me_3c2ae4fa12edbeff}`