# Forgery
written by scuffed
> We intercepted some signed messages from the APOCALYPSE financier.
>
> To prevent them from funding their operations we intend to deplete their funds. To do this, we need to be able to sign messages as if they were signed by their financier.
>
> Help us figure out how to forge the signature on the message "Give me $2179" and the verify.py script will be able to give u the flag!

## Solution
This challenge is a fairly basic RSA Signature forgery attack using known ciphertexts which are provided in the file `intercepted_signatures.tsv`. 

The basic principle of this attack is as follows:

If we have known signatures with known plaintext, we can multiply them together to get a new signature corresponding to a new plaintext.

e.g. `s1 = c1^d mod n` and `s2 = c2^d mod n`. Then the signature for some `c3 = c1 * c2` is `s1 * s2 = (c1 * c2)^d mod n`

So let's start by factorising the message we wish to forge.
```
>>> int.from_bytes(b'Give me $2179', 'big')                                                                             
5657838595347917049855824967481  
```
Running this number through `FactorDB` gives us `5657838595347917049855824967481 = 751 · 9619 · 17491 · 21589 · 34613 · 63907 · 937661`

Scanning through `intercepted_signatures.tsv`, we discover that all of these factors are already in the file!
```
b'\x00DS' == 17491
b'\x00\x02\xef' == 751
b'\x0eN\xbd' == 937661
b'\x00TU' == 21589
b'\x00\x875' == 34613
b'\x00\xf9\xa3' == 63907
b'\x00%\x93' == 9619
```
Even better still, as these are all the factors we need without any additional exponents or cross multiplication, we can naively multiply all their signatures together and get the answer.

Our final signature is thus `0x455e040110bedaa32e84ffb609b47529e8cd727c3fba79e56a893f1c90f0d250f687e4ffb63b8da8fe7c0f1137fb58062452712709fad891e09c9f4b4d666e7b30ed6f88d42ede6e596c9e6ad74852c6f6a471293b50ae36e110046f091f7b10f6ad38c83648a09bfc7ea0661c459a5d5cbe6654e06be231dfb967a1fb9f0323`

Flag: `Cyberthon{622baa8e5758e4c2d3cd1056499f1153a0e0b4ccc200d6da6888e5c0849b7071}`
