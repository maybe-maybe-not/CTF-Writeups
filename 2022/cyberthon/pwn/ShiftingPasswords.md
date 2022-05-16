# Shifting Passwords

## Provided Files
[shifting_passwords](./assets/shifting_passwords)

## Solution
Let's run the binary and see what it asks for

```
❯ ./shifting_passwords
Welcome APOCALYPSE! Enter the password here:
owo uwu nya
Wrong password!
```

Damn. Let's open this in Ghidra and see if we can get some further insight into how the password is generated.

```c
char * generate_random_password(void)

{
  FILE *__stream;
  char *__s;
  
  __stream = fopen("/dev/urandom","rb");
  __s = (char *)malloc(0x80);
  fgets(__s,0x80,__stream);
  fclose(__stream);
  return __s;
}
```

Looks like the password is generated just by using `/dev/urandom`. This is hella suspect because there's no stopping `urandom` from just putting a null byte at the start of the password.

```c
puts("Welcome APOCALYPSE! Enter the password here: ");
fgets(local_a8,0x80,stdin);
local_10 = (char *)generate_random_password();
iVar1 = strcmp(local_a8,local_10);
```

We see that the password check is just a `strcmp` between the input and the generated password. This is perfect! `strcmp` only compares up until the null-terminator, so if the null-terminator is the _first character_, we just need to input a blank password to win.

```py
from pwn import *
for i in range(1000):
    p = remote('chals.cyberthon22f.ctf.sg', 10201)
    p.send('\n')
    string = p.recvall()
    if b'Wrong' in string:
        print('failed')
    else:
        print(string)
        break
```

Flag: `Cyberthon{nu11_t3rm1n4t0r5}`
