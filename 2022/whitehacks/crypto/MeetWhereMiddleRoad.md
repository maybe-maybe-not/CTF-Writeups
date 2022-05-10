# Meet where? Middle Road

In this challenge, we are first given the file ```secure_aes.py```. In here, there are two functions, ```get_new_key()``` and ```encrypt(data, key1, key2)```.
When running the challenge on their instance, we are presented with the following output:
```
Welcome to my personal encryption project
Where to meet next:
OIKYobAWO8WuvmnhgCXU6kmMkHrkVKUsEyX34EzQbIkpwRMDIOM4RIlb9NssrsEM
Test out this secure encryption scheme:
> owo whats this uwu
D1aJw0bizViFlxpx0llJqnUITWTKRHP2nORZzYtyqh4=
```
The program starts by generating two keys ```key1``` and ```key2``` using the ```get_new_key()``` function which serve as parameters for ```encrypt(data, key1, key2)```.
It prints out an encrypted version of the flag and an encrypted version of the input string with the same two keys generated in the program.

Let's take a look at ```get_new_key()```

```py
# Some say 0 is not a good number.
def get_new_key() -> bytes:
    digits = b"123456789"
    fav_event = b"wH1t3H@cK5_"
    while len(fav_event) < AES_KEY_SIZE:
        fav_event += bytes([digits[randint(0, 8)]])
    return fav_event
```

```get_new_key()``` would output at bytestring of length 16 with a fixed base string ```b"wH1t3H@cK5_"``` followed by 5 random digits from 1 to 9. 
This means we have a relatively small keyspace, only ```9^5 = 59049``` possible keys! Perhaps some bruteforcing is to be had...
Now, let's look at the encryption function itself
```py
# Encrypting twice will make AES even stronger!
def encrypt(data, key1, key2):
    cipher1 = AES.new(key1, mode=AES.MODE_ECB)
    ct = cipher1.encrypt(pad(data, AES.block_size))
    cipher2 = AES.new(key2, mode=AES.MODE_ECB)
    ct = cipher2.encrypt(ct)
    ct = b64encode(ct).decode("utf-8")
    return ct
```

Double encryption using AES in ECB mode... ECB is semantically weak, where identical plaintext will heed indentical ciphertext. 
With this, if we have a ciphertext and known key, we'll be able to trivially retrieve the plaintext.

Encrypting twice is definitely suspect, and the challenge name would nudge one in the right direction. What we should employ is a Meet in the Middle Attack!

Essentially, if we have known plaintext P and ciphertext C with an encryption function ENC and decryption function DEC, we have that

```C = ENC(ENC(P, key1), key2)``` and ```P = DEC(DEC(C, key2), key1)```
Now, we note that ```ENC(P, key1) == DEC(C, key2)``` as given by the above. Ergo, we can solve ```key1``` and ```key2``` by simply looking for two keys that fulfill this relationship.
What's convenient is that our key search space is really small, which means we basically calculate all possible values of ```ENC(P, key1)```, then using C, keep calculating values of ```DEC(C, key2)``` until we hit a match.
```py
from random import randint
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
AES_KEY_SIZE = 16
# generating all keys
all_keys = []
from itertools import product
digits = b"123456789"
all_combo = [x for x in product(range(9), repeat=5)] # generates all combinations of digits 
for combo in all_combo:
    base = b"wH1t3H@cK5_"
    for n in combo:
        base += bytes([digits[n]])
    all_keys.append(base)
known_ciphertext = "D1aJw0bizViFlxpx0llJqnUITWTKRHP2nORZzYtyqh4="
known_ciphertext = base64.b64decode(known_ciphertext.encode("utf-8")) # don't forget to encode in utf-8
known_plaintext = "owo whats this uwu"
# this will store our values of ENC(P, key1)
cipher_dict = {}
for key in all_keys:
    cipher1 = AES.new(key, mode=AES.MODE_ECB)
    ct = cipher1.encrypt(pad(known_plaintext.encode("utf-8"), AES.block_size))
    cipher_dict[ct] = key
key1 = ""
key2 = ""
# now, we generate values of DEC(C, key2) until we meet in the middle
for key in all_keys:
    cipher2 = AES.new(key, mode=AES.MODE_ECB)
    ct = cipher2.decrypt(known_ciphertext)
    if ct in cipher_dict: # found the key
        print(f'the keys are {key} and {cipher_dict[ct]}\n')
        key1 = cipher_dict[ct]
        key2 = key
```

Once the two keys are obtained, all that's left is to decrypt our encrypted flag!

```py
ct = "OIKYobAWO8WuvmnhgCXU6kmMkHrkVKUsEyX34EzQbIkpwRMDIOM4RIlb9NssrsEM"
ct = base64.b64decode(ct.encode("utf-8"))
cipher2 = AES.new(key2, mode=AES.MODE_ECB)
ct = cipher2.decrypt(ct)
cipher1 = AES.new(key1, mode=AES.MODE_ECB)
ct = cipher1.decrypt(pad(ct, AES.block_size))
print(f'Flag: {ct}\n')
```
Our program output is as such:

```
the keys are b'wH1t3H@cK5_93792' and b'wH1t3H@cK5_51962'
Flag b"WH2022{M1dDl3_R0@d_15_tH3_b3sT_pLAc3_2_m33T}\x04\x04\x04\x04\xc0\x19\xc9\xab'\xdes|Z\x95f\xce\xb5\xdazw"
```

Our flag is ```WH2022{M1dDl3_R0@d_15_tH3_b3sT_pLAc3_2_m33T}``` 🙂