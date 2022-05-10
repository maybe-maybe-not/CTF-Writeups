## [CSIT] ZZZ XenophobicTea
#### Written by Halogen, m0n0valu3nce and scuffed <3

[Halogen, insert the part where you ghidra]

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

[scuffed, insert your half completed reverse code?]