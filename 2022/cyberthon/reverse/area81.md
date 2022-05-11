## Area 81
#### Written by Halogen and m0n0valu3nce

> Our intel suggests that APOCALYPSE's HQ is located at a highly secured facility called Area 81. Getting through their external fortifications isn't a problem because we can all just naruto run all the way to their entrance. However, there is an digital panel at the entrance that requires a passcode.
>
> We need you to reverse engineer the program, and find the correct passcode!

There is two parts to this challenge, finding the code and doing the actual reverse.

Firstly, we decompile the `.jar` file. This part is pretty simple, since we got IntelliJ on our side.

```java
// Import statements excluded

public class Area81 { 
    public Area81() { } 
    public static void main(String[] var0) throws Exception { 
        Area81Loader var1 = new Area81Loader(); 
        Class var2 = var1.findClass(); 
        Method var3 = var2.getMethod("main", String[].class); 
        var3.invoke((Object)null, null); 
    } 
}

class Area81Loader extends ClassLoader { 
    Area81Loader() { } 
    public Class findClass() throws Exception { 
        byte[] var1 = this.loadClassData(); 
        return this.defineClass("WeirdGlyphs", var1, 0, var1.length); 
    } 
    private byte[] loadClassData() throws Exception { 
        byte[] var1 = new byte[]{-112, -108, -115, -100, -111, -110, -116, -110, -64, -114, -117, -116, -48, -114, -117, -110}; 
        byte[] var2 = this.getClass().getResourceAsStream("/WeirdGlyphs.class").readAllBytes(); 
        Cipher var3 = Cipher.getInstance("AES"); 
        var3.init(2, new SecretKeySpec(var1, 0, var1.length, "AES")); 
        byte[] var4 = var3.doFinal(var2); 
        return var4; 
    } 
}
```
From the code, specifically the `loadClassData()` in `Area81Loader` Class, we notice that the `WeirdGlyphs.class` file is decrypted using AES with the key as `var1`.
Applying the same code, we can get a decoded `WeirdGlyphs.class`, as given below.
```java
// import statments excluded

public class WeirdGlyphs {  
    public WeirdGlyphs() {  
    }  
  
    public static void main(String[] var0) throws IOException {  
        String var1 = "⺬䨌襁ฬ옌㘬ພ첬\u16fa搜ᘮ黌웺瘬郞⺬ฌ⳺㈲\u0cfa辶겮";  
        printBanner();  
        System.out.print("Verification Phrase => ");  
        BufferedReader var2 = new BufferedReader(new InputStreamReader(System.in));  
        String var3 = var2.readLine();  
        if (encodeData(var3.getBytes()).equals(var1)) {  
            System.out.println("The Flag is Cyberthon{" + var3 + "}");  
        } else {  
            System.out.println("[ INTRUDER ALERT! ]");  
        }  
  
    }  
  
    public static void printBanner() {  
        System.out.println("───────────────────────────────────────────────────────────────────────────────────────────");  
        System.out.println("─██████████████─████████████████───██████████████─██████████████─██████████████─████████───");  
        System.out.println("─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░██───");  
        System.out.println("─██░░██████░░██─██░░████████░░██───██░░██████████─██░░██████░░██─██░░██████░░██─████░░██───");  
        System.out.println("─██░░██──██░░██─██░░██────██░░██───██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██───");  
        System.out.println("─██░░██████░░██─██░░████████░░██───██░░██████████─██░░██████░░██─██░░██████░░██───██░░██───");  
        System.out.println("─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░██───");  
        System.out.println("─██░░██████░░██─██░░██████░░████───██░░██████████─██░░██████░░██─██░░██████░░██───██░░██───");  
        System.out.println("─██░░██──██░░██─██░░██──██░░██─────██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██───");  
        System.out.println("─██░░██──██░░██─██░░██──██░░██████─██░░██████████─██░░██──██░░██─██░░██████░░██─████░░████─");  
        System.out.println("─██░░██──██░░██─██░░██──██░░░░░░██─██░░░░░░░░░░██─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░██─");  
        System.out.println("─██████──██████─██████──██████████─██████████████─██████──██████─██████████████─██████████─");  
        System.out.println("───────────────────────────────────────────────────────────────────────────────────────────");  
    }  
  
    public static String encodeData(byte[] var0) {  
        ArrayList var1 = new ArrayList();  
        byte[] var2 = var0;  
        int var3 = var0.length;  
  
        for(int var4 = 0; var4 < var3; ++var4) {  
            byte var5 = var2[var4];  
            byte var6 = 0;  
  
            for(int var7 = 0; var7 < 8; ++var7) {  
                var6 = (byte)(var6 + ((var5 >> 7 - var7 & 1) << var7));  
            }  
  
            var1.add(var6);  
        }  
  
        ArrayList var8 = new ArrayList();  
  
        for(var3 = 0; var3 < var1.size(); ++var3) {  
            var8.add((Byte)var1.get(var3));  
            if (var3 % 2 != 0) {  
                var8.add((byte)0);  
                var8.add((byte)0);  
            }  
        }  
  
        return new String(toByteArray(var8), Charset.forName("UTF-32LE"));  
    }  
  
    public static byte[] toByteArray(ArrayList<Byte> var0) {  
        byte[] var1 = new byte[var0.size()];  
  
        for(int var2 = 0; var2 < var0.size(); ++var2) {  
            var1[var2] = (Byte)var0.get(var2);  
        }  
  
        return var1;  
    }  
}
```

From here, we are to reverse the following code in `enocdeData()`, such that the output matches the string in `main`:
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

From above, we wish to attain the following output string: 
UTF-8 Encoded: `"⺬䨌襁ฬ옌㘬ພ첬\u16fa搜ᘮ黌웺瘬郞⺬ฌ⳺㈲\u0cfa辶겮"` 
Hex: `e2baace4a88cefaab6e0b8acec988ce398ace0ba9eecb2ace19bbaefaa8ee198aee9bb8cec9bbae798acefa8aee2baace0b88ce2b3bae388b2e0b3baefa9a6eab2ae`

We use [Cyberchef](https://gchq.github.io/CyberChef/) for this. 
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