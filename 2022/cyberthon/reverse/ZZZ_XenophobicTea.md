# [CSIT] ZZZ XenophobicTea
Written by Halogen, m0n0valu3nce and scuffed <3
## Problem Statement
> We have found the encryption program that APOCALYPSE uses to send encrypted messages.  
  >
> It comes with a key checker module which is helpful but... it does not come with the decryption module... zzz...  
  
Wait a minute, this encryption algorithm looks familiar...
Using ghidra, we can easily decompile the code and find this very useful section of the code.
```c
bool keyVerification(byte *param_1) {
    bool uVar1;
    
    if (((((((((((param_1[0xd] ^ param_1[4]) == 0xf) &&
        ((int)(char)param_1[3] * (int)(char)param_1[10] == 0x1450)) &&
        ((int)(char)param_1[6] + (int)(char)param_1[3] == 0x84)) &&
        // ... Many many if statements later
        // ... All similar in style (char1) operator (char2) == value                                       
        ((int)(char)param_1[1] % (int)(char)param_1[5] == 0x18)) &&
        ((param_1[10] ^ param_1[9]) == 9)))))))))))))))))))) {
        uVar = 1;
    }
    else uVar = 0;
    return uVar;
}
```

Then, we used z3 to get the key `Xx_AP0CALYP$E_xX`. 

Code:
```py
from z3 import *
from sympy import *

'''INSERT VARIABLES A TO P'''

s = Solver()

'''INSERT CONDITIONS'''
'''NOTE: THE FAST WAY TO AUTOMATE THIS PART IS TO REPLACE ALL BRACKETS WITH A \n AND PRUNE FROM THERE'''

if s.check() == sat:
    m = s.model()
    print(m)
```

Afterwards, we look at another section of the decompiled code to determine what to do with our key.
```c
void encodeKey(void)

{
    long lVar1;
    undefined local_59 [8];
    undefined8 filename;
    undefined local_49;
    uint local_48 [4];
    byte key [20];
    uint local_24;
    FILE *local_20;
    int local_18;
    uint local_14;
    uint local_10;
    int i;
    
    printf("Enter key for encryption: ");
    __isoc99_scanf(&DAT_00108065,key);
    i = 0;
    while (i < 4) {
        local_48[i] = (uint)key[i << 2] << 0x18 | (uint)key[i * 4 + 1] << 0x10 |
                      (uint)key[i * 4 + 2] << 8 | (uint)key[i * 4 + 3];
        i = i + 1;
    }
                    /* "cne.gal" */
    filename = 0x636e652e67616c66;
    local_49 = 0;
    local_20 = fopen((char *)&filename,"r+");
    fseek(local_20,0,2);
    lVar1 = ftell(local_20);
    local_24 = (uint)lVar1;
    rewind(local_20);
    local_10 = local_24 >> 3;
    if ((local_24 & 7) != 0) {
        local_10 = local_10 + 1;
    }
    lVar1 = ftell(local_20);
    local_14 = (uint)lVar1;
    local_18 = 0;
    while (local_18 < (int)local_10) {
        fseek(local_20,(ulong)local_14,0);
        fread(local_59,1,8,local_20);
        FUN_001011d5(local_59,local_48,local_48);
        fseek(local_20,(ulong)local_14,0);
        fwrite(local_59,1,8,local_20);
        memset(local_59,0,8);
        local_14 = local_14 + 8;
        local_18 = local_18 + 1;
    }
    fclose(local_20);
    return;
}
```

[scuffed, insert your half completed reverse code?]