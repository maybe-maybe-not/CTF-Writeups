# Encryptdle
Written by m0n0valu3nce

> The quest to get Flag-Chan!~~
## Provided Files 
[Challenge File](./assets/jagacha/jagacha.py)

Note: I am unsure of the correctness of the script, as a mistake was made in the distributed script. It should not affect the explaination of the exploit, however it does affect the specifics of what I am outputting. 

## Solution
In this chalange, we are to get realy lucky. We can do one of 2 operations, `I'm Feeling Lucky!` and try and retrive flag-chan, or `Roll a Gacha`. 

In `Roll a Gacha`, a random number is generated via `num = rand.getrandbits(64)`. From that number, a character's stats are assigned based on the 64 bit number generated. 

In `I'm Feeling Lucky!`, if you guess the random number generated via `num = rand.getrandbits(32)`, flag-chan is returned to you. §(*￣▽￣*)§

On to the exploit. It is a well known fact that the `random` libary should not be known to generate **anything** used for encryption, due to its peudorandom nature (`os.random()` should be used for such purposes). This problem is a testiment to that, and we showcase why this is the case. 

Using the libary found in [here](https://github.com/tna0y/Python-random-module-cracker), we feed in sufficiently many integers into the libary until it can predict the random number that will be selected. From there, using the libary to predict the next 64 bits solves the problem.

The only last thing worth noting is that python's `random` libary generates random bits 32 bits at a time. This means that when it generates 64 random bits, it actually is generating 32 random bits _twice_. Sepcifically, if it generates the bits: `r1, r2`, then the outputted string will be: `r2r1`. This is important in the implementation of the challange. 

_The code is found in [here](./assets/jagacha/solve.py)_

```py
import random, time
from randcrack import RandCrack
from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

io = remote("157.245.52.169", 32048) 

rc = RandCrack()

arr = []

# While we cant predict the state of random, this should take 624 predictions
while (not rc.state):
	io.recvuntil(b'>')
	io.sendline(b'1')
	io.recvuntil(b'Here are the stats of your character:\n')
	seed = 0
	check = []
	
	for j in range(4):
		line = io.recvline()
		stat = line.split(b" ")[1][:-1]
		statChanged = int(stat.decode("ascii"))
		check.append(line)
		seed = (seed << 16) + statChanged
	arr.append(seed)
	rc.submit(seed & 0xffffffff)
	rc.submit(seed >> 32)
	
	assert f"STR: {seed>>48 & 0xffff}\n".encode() == check[0]
	assert f"DEX: {seed>>32 & 0xffff}\n".encode() == check[1]
	assert f"INT: {seed>>16 & 0xffff}\n".encode() == check[2]
	assert f"LUK: {seed & 0xffff}\n".encode() == check[3]

# Predict the next number and sumbit the flag
pred = rc.predict_getrandbits(64)
print(pred)

io.recvuntil(b'>')
io.sendline(b'2')
io.recvuntil(b':')
pred = str(pred).encode("ascii")
print(pred)
io.sendline(pred)

io.interactive()
```

Flag: `STF22{W@IFU5_L@1FU5}`
