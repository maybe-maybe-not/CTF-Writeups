# Secret Chest of Rick
by scuffed and m0n0valu3nce
> Problem Description
> The Secret Chest of Rick contains unfathomable secret that may allow you to turn the tide in times of need. You may, however, incur the wrath of Rick if you fail to decipher the code.
> 
> Help Jaga to uncover secret of the chest.

## Solution
Secret Chest of Rick is a challenge which tests grit. To quote Wikipedia,
> In psychology, grit is a positive, non-cognitive trait based on an individual's perseverance of effort combined with the passion for a particular long-term goal or end state.

We are first presented with an exe file
... #TODO: Go home and find the files to this challenge to detail the py extraction

We are now left with a python script which we can work with.

The first important part of the script is the following:
```py
    try:
        D = len(v) * len(v)
        x = lambda f, n: f(f, n)
        y = lambda f, n: chr(n % D) + f(f, n // D) if n else ''
        r = m(x(y, int(v)).encode()).hexdigest()
        if 'deb2742ec3cb41518e26aa2d89' not in r:
            raise Exception
    except:
        print('Incorrect passcode! Exiting...')
        exit(1)
```

To even progress with the challenge, we first have to get an md5 hash which contains the partial hash as provided. Oof.
A few hours after first starting on this challenge, I noticed a suspicious file that was included in the decompilation result named `a86850`.
```py
```

Flag: `STF22{p41n_1s_411_th3_s4m3}`
