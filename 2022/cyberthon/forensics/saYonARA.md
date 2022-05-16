# saYonARA
> Jessie and James were identified to be members of the APOCALYPSE.
> They have devised a secret form of communication, sending each other messages by first encrypting it with a monoalphabetic rotation cipher, followed by Base64 encoding, and embedding the final ciphertext into an executable file.
> This file is then hidden within a directory of files. Using YARA, help us uncover their encoded message and crack the cipher!
## Provided Files
They provided a zip file which is REALLY HUGE. All you need to know is that it is heavily nested and composed of thousands of files :)
## Solution
So... YARA, huh
We're not told to wrap the flag in `Cyberthon` so chances are it'll be contained within the file as well.
In a YARA rule, if we're looking for a Base64 encoded string, it's safest to include all possible encodings for this _just in case_.
So we have `ascii wide base64 base64wide` for our rules.

Using a simple python script, we generate ourselves our YARA rules.
```py
def encrypt(text,s):
    result = ""
 
    # traverse text
    for i in range(len(text)):
        char = text[i]
        result += chr(ord(char) + s)
 
    return result

flagHeader = "Cyberthon"
print('rule base64_ascii_ascii {')
print('  strings:')
for i in range(26):
    print(f'    ${chr(97+i)} = "{encrypt(flagHeader, i)}" ascii wide base64 base64wide')
print('  condition:')
for i in range(26):
    print(f'${chr(97+i)} or ', end = '')
print('}')
```
However, we still haven't accounted for the files being executable. Most Windows executable files have `This Program Cannot Be Run in DOS Mode` somewhere in the file, so let's just add a rule looking for the string `DOS`.
This turns our final YARA ruleset into:
```
rule base64_ascii_ascii {
  strings:
    $b = "Dzcfsuipo" ascii wide base64 base64wide
    $c = "Eadgtvjqp" ascii wide base64 base64wide
    $d = "Fbehuwkrq" ascii wide base64 base64wide
    $e = "Gcfivxlsr" ascii wide base64 base64wide
    $f = "Hdgjwymts" ascii wide base64 base64wide
    $g = "Iehkxznut" ascii wide base64 base64wide
    $h = "Jfilyaovu" ascii wide base64 base64wide
    $i = "Kgjmzbpwv" ascii wide base64 base64wide
    $j = "Lhknacqxw" ascii wide base64 base64wide
    $k = "Milobdryx" ascii wide base64 base64wide
    $l = "Njmpceszy" ascii wide base64 base64wide
    $m = "Oknqdftaz" ascii wide base64 base64wide
    $n = "Ploreguba" ascii wide base64 base64wide
    $o = "Qmpsfhvcb" ascii wide base64 base64wide
    $p = "Rnqtgiwdc" ascii wide base64 base64wide
    $q = "Soruhjxed" ascii wide base64 base64wide
    $r = "Tpsvikyfe" ascii wide base64 base64wide
    $s = "Uqtwjlzgf" ascii wide base64 base64wide
    $t = "Vruxkmahg" ascii wide base64 base64wide
    $u = "Wsvylnbih" ascii wide base64 base64wide
    $v = "Xtwzmocji" ascii wide base64 base64wide
    $w = "Yuxanpdkj" ascii wide base64 base64wide
    $x = "Zvyboqelk" ascii wide base64 base64wide
    $y = "Awzcprfml" ascii wide base64 base64wide
    $z = "Bxadqsgnm" ascii wide base64 base64wide
    $a1 = "DOS"
  condition:
    ($b or $c or $d or $e or $f or $g or $h or $i or $j or $k or $l or $m or $n or $o or $p or $q or $r or $s or $t or $u or $v or $w or $x or $y or $z) and $a1
}
```
Very cool. We run `yara -r yara.rule ./transmitted/` (using `-r` for recursive searching) and just look through all the files we get.

```
❯ yara -r yara.rule ./transmitted/
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/Av3hKWkE32/yYMoIOlFC.exe
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/FZQGGhY/9kDbFXn/r2T2TX2De.exe
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/FZQGGhY/yYETeOg4c34/CiFF7H5WTmt/NrplXjIZ2.exe
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/Hx7RytrcpzY/Arp47g5/hojXDVijA.zip
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/l0VkDKg9P5/kyLkncaL/qNECIuRdM0/s=20K7q4UB.exe
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/ruRWCjQ/8hDSsaL2x41/DJO=yFB/ytmoxGzI.exe
base64_ascii_ascii ./transmitted//transmitted/7c67cNFEp3/VmF3Wady/8Yq2Hd22/ZD2QoUBNyOa/Z5xTrAts.exe
base64_ascii_ascii ./transmitted//transmitted/BYpu3yuK/Ljo39YbboJs/24oDvy5/sYufklwhu9/1d8KOqNsE.exe
base64_ascii_ascii ./transmitted//transmitted/BYpu3yuK/Ljo39YbboJs/nLCexqRv/wZ4SOFykL/jB94XVyWB.exe
base64_ascii_ascii ./transmitted//transmitted/BYpu3yuK/Ljo39YbboJs/w2zH3FT/85Ft8QfYvC.exe
base64_ascii_ascii ./transmitted//transmitted/BYpu3yuK/VMIGFoP/k89t9qK/F0sZ36IL.exe
base64_ascii_ascii ./transmitted//transmitted/BYpu3yuK/X6nnnOhc44/rvwsqdt3/IEWkjd3/3j9RQzEPmZt.exe
base64_ascii_ascii ./transmitted//transmitted/DIubtbn/0mEtLW3/HoA1LGlp3/OcrYDK6MO0I.exe
base64_ascii_ascii ./transmitted//transmitted/DIubtbn/4Q2ZtO5kS/uuj6vICCZg/33NUUwamvtj/ny=Hhm9GguZ.exe
base64_ascii_ascii ./transmitted//transmitted/DIubtbn/ED22vjohH/GlBgD8aq3pt/UIVifPv.exe
base64_ascii_ascii ./transmitted//transmitted/EcxusLbj/B0oJUsi=a/lbs0xDe/dpEUZmSR/CNfTdjCC.exe
base64_ascii_ascii ./transmitted//transmitted/FDzqDGRd80/uTnOF4D=w5/E6Rg1AFf1/iqiHJInlhgD.exe
base64_ascii_ascii ./transmitted//transmitted/FDzqDGRd80/uTnOF4D=w5/77LlYOwP41/buOfQcU7.exe
base64_ascii_ascii ./transmitted//transmitted/nrCB9lP/4p=nsfv/0SIhv1utg3/iSOO6Lqfjuq/HxHdu69.exe
base64_ascii_ascii ./transmitted//transmitted/nrCB9lP/baoWSEln/2bbalEi7/wY3rZbTro/3L=5R5j.exe
```

With a very limited search pool, we cat out the file `transmitted/7c67cNFEp3/Av3hKWkE32/yYMoIOlFC.exe` and get the following
```
MZ����@���      �!�L�!This program cannot be run in DOS mode.
$Hi JamEs, lets protect the world from devastation and unite all people within the nation.SmZpbHlhb3Z1ezFfZGEwX2lsYW8zQ19pbHphNTU1fQ==regards,JessiE�0�H`P}<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level='asInvoker' uiAccess='false' />
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
 ,�����������ء���Ȣ��p���������%
```
Let's just decode that Base64 string and then spam ROT13 with different offsets

Flag: `Cyberthon{0_wt9_beth2V_best444}`
