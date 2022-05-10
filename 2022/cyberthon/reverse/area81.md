## Area 81
#### Written by Halogen and m0n0valu3nce

> Our intel suggests that APOCALYPSE's HQ is located at a highly secured facility called Area 81. Getting through their external fortifications isn't a problem because we can all just naruto run all the way to their entrance. However, there is an digital panel at the entrance that requires a passcode.
>
> We need you to reverse engineer the program, and find the correct passcode!

There is two parts to this challenge, finding the code and doing the actual reverse.

[Halogen, please insert your part here]

(As such, output string which we want to match is `e2baace4a88cefaab6e0b8acec988ce398ace0ba9eecb2ace19bbaefaa8ee198aee9bb8cec9bbae798acefa8aee2baace0b88ce2b3bae388b2e0b3baefa9a6eab2ae`)

From here, we are to reverse the following code:
```java
ArrayList encode = new ArrayList();
byte[] var2 = var0;
int length = var0.length;

for(int i = 0; i < length; ++i) {
    byte chr = var2[i];
    byte cur_val = 0;


    for(int j = 0; j < 8; ++j) {
        cur_val = (byte)(cur_val + ((chr >> 7 - j & 1) << j));
    }

    encode.add(cur_val);
}

ArrayList output = new ArrayList();

for(length = 0; length < encode.size(); ++length) {
    output.add(encode.get(length));
    if (length % 2 != 0) {
        output.add((byte)0);
        output.add((byte)0);
    }
}

return new String(WeirdGlyphs.toByteArray(output), Charset.forName("UTF-32LE"));
```

Recall that we wish to attain the following output string: `e2baace4a88cefaab6e0b8acec988ce398ace0ba9eecb2ace19bbaefaa8ee198aee9bb8cec9bbae798acefa8aee2baace0b88ce2b3bae388b2e0b3baefa9a6eab2ae`

We use Cyberchef for this. 

```java
for(length = 0; length < encode.size(); ++length) {
    output.add(encode.get(length));
    if (length % 2 != 0) {
        output.add((byte)0);
        output.add((byte)0);
    }
}

return new String(WeirdGlyphs.toByteArray(output), Charset.forName("UTF-32LE"));
```
To reverse this, we shall `code -> from_hex -> encode_text (UTF-32LE) -> to_binary`
> 10101100 00101110 00000000 00000000 00001100 01001010 00000000 00000000 10110110 11111010 00000000 00000000 
>
> 00101100 00001110 00000000 00000000 00001100 11000110 00000000 00000000 00101100 00110110 00000000 00000000 
>
> 10011110 00001110 00000000 00000000 10101100 11001100 00000000 00000000 11111010 00010110 00000000 00000000 
>
> 10001110 11111010 00000000 00000000 00101110 00010110 00000000 00000000 11001100 10011110 00000000 00000000 
>
> 11111010 11000110 00000000 00000000 00101100 01110110 00000000 00000000 00101110 11111010 00000000 00000000 
>
> 10101100 00101110 00000000 00000000 00001100 00001110 00000000 00000000 11111010 00101100 00000000 00000000 
>
> 00110010 00110010 00000000 00000000 11111010 00001100 00000000 00000000 01100110 11111010 00000000 00000000 
>
> 10101110 10101100 00000000 00000000

We now remove all chunks of 16 `00000000 00000000`. 

> 10101100 00101110 00001100 01001010 10110110 11111010 
> 00101100 00001110 00001100 11000110 00101100 00110110 
> 10011110 00001110 10101100 11001100 11111010 00010110 
> 10001110 11111010 00101110 00010110 11001100 10011110 
> 11111010 11000110 00101100 01110110 00101110 11111010 
> 10101100 00101110 00001100 00001110 11111010 00101100 
> 00110010 00110010 11111010 00001100 01100110 11111010 
> 10101110 10101100

```java
ArrayList encode = new ArrayList();
byte[] var2 = var0;
int length = var0.length;

for(int i = 0; i < length; ++i) {
    byte chr = var2[i];
    byte cur_val = 0;


    for(int j = 0; j < 8; ++j) {
        cur_val = (byte)(cur_val + ((chr >> 7 - j & 1) << j));
    }

    encode.add(cur_val);
}
```
To reverse this, we shall do the following on Cyberchef: 
`reverse -> from_binary -> reverse`
Note that this is the case, as `cur_val = (byte)(cur_val + ((chr >> 7 - j & 1) << j));` merely reverses the bits in every byte. (minus `-` gets processed before the rightshift)

We get: `5t0Rm_4p0c4lyp53_hq_th3y_c4nt_5t0p_4LL_0f_u5`

> Cyberthon{5t0Rm_4p0c4lyp53_hq_th3y_c4nt_5t0p_4LL_0f_u5}