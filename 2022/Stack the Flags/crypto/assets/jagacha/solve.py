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