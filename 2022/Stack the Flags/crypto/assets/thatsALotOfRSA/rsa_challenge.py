import os
from Crypto.PublicKey import RSA
import random
import signal

privkeydir = os.getenv('PRIVKEYS')
keys = os.listdir(privkeydir)

FLAG = os.getenv('FLAG')
ans = []
nstr = ''
for i in range(200):
    k1file, k2file = random.sample(keys, 2)
    k1 = RSA.import_key(open(f'{privkeydir}/{k1file}').read())
    k2 = RSA.import_key(open(f'{privkeydir}/{k2file}').read())
    p = random.choice([k1.p,k1.q])
    q = random.choice([k2.p,k2.q])
    n = p * q
    nstr += f'n[{i}] = {n}\n'
    ans.append((p,q))
print(nstr)    
signal.alarm(10)
print("10 seconds")
wrong = False
for i in range(200):
    print(f'p[{i}] = ?')
    pans = int(input())
    if pans not in ans[i]:
        print('Wrong!')
        wrong = True
        break

if not wrong:
    print(open(FLAG).read())
