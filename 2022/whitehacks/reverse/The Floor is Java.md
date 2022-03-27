# The Floor is Java

We are first provided with a `Reverse.class` file and the encoded string `,hj*Y/bOi-(Tm0"0qH,O[d2!'@qG-(-6`
Passing the class through an online Java decompiler, we have the following:
```java
import java.util.Scanner;

// 
// Decompiled by Procyon v0.5.36
// 

public class Reverse
{
    public static String encode_1(final String s) {
        final String[] split = s.split("");
        String s2 = "";
        for (int i = 0; i < s.length(); i += 2) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, split[i]);
        }
        for (int j = 1; j < s.length(); j += 2) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, split[j]);
        }
        return s2;
    }
    
    public static String encode_2(final String s) {
        final char[] charArray = s.toCharArray();
        final int[] array = { 39, 18, 16, 3, 2, 10, 14, 4, 11, 37, 8, 5, 6, 31, 9, 12 };
        final int length = array.length;
        for (int i = 0; i < charArray.length; ++i) {
            final char[] array2 = charArray;
            final int n = i;
            array2[n] -= (char)array[i % length];
        }
        String s2 = "";
        for (int j = 0; j < charArray.length; ++j) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;C)Ljava/lang/String;, s2, charArray[j]);
        }
        return s2;
    }
    
    public static String encode_3(final String s) {
        final String[] split = s.split("");
        String s2 = "";
        for (int i = s.length() / 2; i < s.length(); ++i) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, split[i]);
        }
        for (int j = 0; j < s.length() / 2; ++j) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, split[j]);
        }
        return s2;
    }
    
    public static String encode_4(final String s) {
        final char[] charArray = s.toCharArray();
        for (int i = 0; i < s.length() / 2; ++i) {
            final int n = s.length() - i - 1;
            final char c = charArray[i];
            charArray[i] = charArray[n];
            charArray[n] = c;
        }
        String s2 = "";
        for (int j = 0; j < charArray.length; ++j) {
            s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;C)Ljava/lang/String;, s2, charArray[j]);
        }
        return s2;
    }
    
    public static void main(final String[] array) {
        final Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your string: ");
        final String nextLine = scanner.nextLine();
        scanner.close();
        System.out.println(encode_3(encode_4(encode_1(encode_2(nextLine)))));
    }
}
```

Let's pick apart the encoding functions in reverse order and undo their operations.

`encode_3` has two for loops, one starting at `i = s.length()/2` and the other starting at `j = 0`, both sweeping across `s.length()`. 
This essentially takes the first half of the original string and swaps it with the second half, so I just cut and paste in Notepad to get `qH,O[d2!'@qG-(-6,hj*Y/bOi-(Tm0"0`

`encode_4` also sweeps across half the total string length, and at each position `i` it also calculates the position `n = s.length()-i-1`, which is the "mirrored" position (the i-th position from the right).
By virtue of laziness, I just did this quickly in Python shell.
```
>>> str = list(r"""qH,O[d2!'@qG-(-6,hj*Y/bOi-(Tm0"0""")
>>> for i in range(int(len(str)/2)):
...     str[i], str[len(str)-i-1] = str[len(str)-i-1], str[i]
...
>>> str = "".join(str)
>>> str
'0"0mT(-iOb/Y*jh,6-(-Gq@\'!2d[O,Hq'
```
`encode_1` iterates through all the even positions and concatenates, then all the odd positions and contatenates. So to undo this operation, we just have to take the character at position `i`, then the character at `i + s.length()/2`, and repeat until we hit the end of the string.
```
>>> str2 = ""
>>> for i in range(int(len(str)/2)):
...     str2 += str[i]
...     str2 += str[i + int(len(str)/2)]
...
>>> str2
'06"-0(m-TG(q-@i\'O!b2/dY[*Oj,hH,q'
```
Finally, `encode_2` takes each character of the string and minuses an ASCII offset from `array`. The inverse operation of minus is addition, so we just... do that.
```
>>> str2 = list(str2)
>>> arr = [39, 18, 16, 3, 2, 10, 14, 4, 11, 37, 8, 5, 6, 31, 9, 12]
>>> for i in range(len(str2)):
...     str2[i] = chr(ord(str2[i]) + arr[i % len(arr)])
...
>>> str2 = "".join(str2)
>>> str2
'WH2022{1_l0v3_r3v3r51ng_5tr1ng5}'
```

