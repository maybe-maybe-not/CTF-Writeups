## Old World Ciphers
#### Written by m0n0valu3nce

### __Problem statement__
> Look at the attached leaked source code.
>
> APOCALYPSE seems to be combining old world ciphers to form a slightly harder cipher.
>
>  Try decrypting the flag. Good Luck!

```py
import math
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

print('OLD WORLD CIPHERS')
flag = 'cyberthon{??????????????????????????????????????}' # allowed [a-z][0-9]{}_
vkey = '????????'                                          # [a-z], len(vkey) = 8

print('\n[ transposition step ]')
blkcnt = math.ceil(len(flag) / 7)
blocks = []
for i in range(blkcnt): blocks.append(flag[i::blkcnt])
print('\n'.join(blocks))

print('\n[ vigenère step ]')
temp = ''.join(blocks)
fenc = ''
for i,c in enumerate(temp):
  if c in alphabet:
    j = alphabet.index(c)
    k = alphabet.index(vkey[i%8])
    l = (j+k) % len(alphabet)
    d = alphabet[l]
  else:
    d = c
  fenc += d
print(fenc) 
# prints m0vr9mxaxqprlnt{_r_mg0anoqbn54cobmk60fbkomr2_4xr}
```

In this problem, the flag is put through 2 ciphers, a transposition cipher and a vigenere cipher. We know how the transposition is done; that would be easy to reverse. All that is needed is so find the key for the vigenere step. 

However, we know the flag **must** start with `cyberthon`. Hence, we may find out what the flag looks like right before the vigenere step. 

Noting that the key is 8 characters long, it is easy for one to find the key of `academic`. Then, we simply have to plug this back into the code, and reverse the code.

```py
import math
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

print('OLD WORLD CIPHERS')
flag = 'm0vr9mxaxqprlnt{_r_mg0anoqbn54cobmk60fbkomr2_4xr}' # allowed [a-z][0-9]{}_
vkey = 'academic'                                          # [a-z], len(vkey) = 8



print('\n[ vigenère step ]')
fenc = ''
for i,c in enumerate(flag):
  if c in alphabet:
    j = alphabet.index(c)
    k = alphabet.index(vkey[i%8])
    l = (j-k) % len(alphabet)
    d = alphabet[l]
  else:
    d = c
  fenc += d
print(fenc) 
# prints m0vr9mxaxqprlnt{_r_mg0anoqbn54cobmk60fbkomr2_4xr}

print(len(fenc))

print('\n[ transposition step ]')
blkcnt = math.ceil(len(fenc) / 7)
blocks = []
for i in range(blkcnt): blocks.append(fenc[i::blkcnt])
print('\n'.join(blocks))

temp = ''.join(blocks)
print("temp is: " + temp)
```

> cyberthon{simple_but_effective_e18f0791aeff12aaa}