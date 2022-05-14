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
Let's just decode that Base64 string...
<reminder to go and look for the correct flag, it looks like what i put in discord isn't correct...>
Flag: `CTF{m4y83_m4y83_n07}`