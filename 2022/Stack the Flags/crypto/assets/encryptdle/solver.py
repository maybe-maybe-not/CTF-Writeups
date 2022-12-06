
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

        
