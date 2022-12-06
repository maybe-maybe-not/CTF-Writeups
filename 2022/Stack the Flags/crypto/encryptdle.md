# Encryptdle
Written by m0n0valu3nce
## Provided Files 
[Challenge File](./assets/encryptdle/server.py)

## Solution
The server provides us with a interface which allows us to play Encryptdle! Specifically, they:

1. Pad the string into the form: `Your string, FLAG, \x00 (or null bytes)`, and truncate it to 32 bits.
2. Encrypt the padded string via AES CBC.
3. Output the encoded string, together with what letters are in the correct positions / in the string.

It is worth noting that the server is evaluating these requests via an API. This allows us to access this API via the `requests` module, and do not limit us to 10 guesses. 

From here, we analyse the request format. Specifically, the string is truncated after 32 bits. Then, we may attempt a `padding oracle`. 

For sake of illustration, let us assume that the flag is `STF22{flag}`. Then, we query the following strings:
```
AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAA?
AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAX
```
In the first string, `?` denotes the first character of the flag. Then, if we brute force `X` to be every character, the two hashes will eventually match for some `X`. We may then repeat this for the next character.
```
AAAA AAAA AAAA AAAA AAAA AAAA AAAA AA??
AAAA AAAA AAAA AAAA AAAA AAAA AAAA AASX
```
Notably, we reduce the number of `A`s at the start by 1, so that the first 2 characters of the flag are being brute forced. However, we already know that the first character of the flag is `S`, hence only need to brute force the lasst character. Again, we may repeat this:
```
AAAA AAAA AAAA AAAA AAAA AAAA AAAA A???
AAAA AAAA AAAA AAAA AAAA AAAA AAAA AST?

AAAA AAAA AAAA AAAA AAAA AAAA AAAA ????
AAAA AAAA AAAA AAAA AAAA AAAA AAAA STF?

AAAA AAAA AAAA AAAA AAAA AAAA AAA? ????
AAAA AAAA AAAA AAAA AAAA AAAA AAAS TF2?

(etc etc)
```

By doing this, we eventually retrieve the entire flag. 

_The code is found in [here](./assets/encryptdle/solver.py)_

```py
import requests

#print(chr(128))

s = requests.session()
outLong = b''
out = b''

block0 = b'00000000000000000000000000000000'

# Converts the API call to the hash
def jsonToString(data):
    out = b''
    for i in data:
        out += i["letter"].encode("ascii")
    return out

# Encrypts the data
def encrypt(data):
    r = requests.post("http://157.245.52.169:30385/api/compare", params={"guess":data.decode('ascii')})
    recieve = r.json()
    return(jsonToString(recieve))

e1 = encrypt(block0)[32:]
e2 = b''

# While the flag has not ended with a `}`
while (outLong == b'' or outLong[-1]!=b'}'):
    # To match is the first string (`AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAA?`)
    toMatch = b''
    if (len(out) == 31):
        toMatch = block0
    while (len(toMatch) + len(out) < 31):
        toMatch = b'0' + toMatch
    
    # Brute forcing what X is in (`AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAX`)
    for i in range(33,126):
        toAdd = i.to_bytes(1, byteorder='big')
        new = toMatch + outLong + toAdd
        
        # Encrypt the 2 strings
        e1 = encrypt(toMatch)
        e2 = encrypt(new)

        # Ignore this line, it is for a more general case
        buffer = len(toMatch)//64 + len(outLong)//64

        # If the 2 encrypted texts match, then X = ?
        if (e1 == e2):
            # Store the data into `outLong`
            outLong += i.to_bytes(1, byteorder='big')
            print(toMatch, new)
            print(e1[64*buffer:64*buffer + 64])
            print(e2[64*buffer:64*buffer + 64])
            print()
            out = outLong
            # Ignore this line, it is for a more general case
            while (len(out) >= 32):
                out = out[32:]
            break
# Print the final result
print(outLong)
```

Flag: `STF22{iNS3CuR3!_S+4+iC_IVs!!}`

## Additional Comments On the Techniques Used

Notably, this technique can be further generalised, which is why the code above have some additional lines which do not seem relevant to the challange. In fact, for ECB and CBC block chaining, this method is applicable. For ECB, we may use this method to check for the first block (as in this question). Then, we attempt to do the same procedure on the second block. To do this, we pad both strings with `MAX_SIZE - 1` 'A's to begin. Assuming a block size of 16, 

```
AAAA AAAA AAAA AAA? ???? ???? ???? ????
AAAA AAAA AAAA AAAS TF22 {iNS 3CuR 3!_X 

AAAA AAAA AAAA AA?? ???? ???? ???? ????
AAAA AAAA AAAA AAST F22{ iNS3 CuR3 !_SX  

AAAA AAAA AAAA A??? ???? ???? ???? ????
AAAA AAAA AAAA ASTF 22{i NS3C uR3! _S+X

(etc etc, X denotes the brute forced character)
```