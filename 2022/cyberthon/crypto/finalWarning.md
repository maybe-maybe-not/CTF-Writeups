# Final Warning
> (I forgor)
## Provided Files
[Link under assets](./assets/FinalWarning)
## Solution

We first try and check the file type. However, when we compare the magic bytes against a [file signature table](https://www.garykessler.net/library/file_sigs.html), we notice that it does not correspond with anything .

However, we also notice that the majority of the bits are `62 D3`. This motivates us to xor it against the entire file. After we do this, the magic bytes turn into `42 4D`, or a `.bmp` file. Hence: 

```py
def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

with open("Final Warning", "rb") as f:
    x = f.read()

print(len(x))

y = xor(x,bytes.fromhex("62D3")*2722030)

with open("test.txt", "wb") as g:
    g.write(y)

with open("test.bmp", "wb") as g:
    g.write(y)
```

Flag: `CTF{m4y83_m4y83_n07}`