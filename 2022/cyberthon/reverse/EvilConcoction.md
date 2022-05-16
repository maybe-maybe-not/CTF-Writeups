# Evil Concoction
> This recipe was found in the kitchen of an APOCALYPSE member. 
> Word on the street is that he was a wizard, and imbued this recipe with a browser-based spell. 
> Wonder what it does...
## Provided Files
[elixir_of_the_malware_whisperer.pdf](./assets/elixir_of_the_malware_whisperer.pdf)
## Solution
Likely some embeded JS inside the file... But how do we get it out?

We wanna look through whatever objects the pdf may contain first, so we use [pdfid.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/pdfid.py)

```
❯ python pdfid.py elixir_of_the_malware_whisperer.pdf
PDFiD 0.2.8 elixir_of_the_malware_whisperer.pdf
 PDF Header: %PDF-1.4
 obj                  187
 endobj               187
 stream                14
 endstream             14
 xref                   2
 trailer                2
 startxref              2
 /Page                  2
 /Encrypt               0
 /ObjStm                0
 /JS                    1
 /JavaScript            2
 /AA                    0
 /OpenAction            0
 /AcroForm              0
 /JBIG2Decode           0
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          0
 /XFA                   0
 /Colors > 2^24         0

```
That JS section looks pretty relevant.

Using the script [pdf-parser.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/pdf-parser.py) we first search for JS and see what it gives us

```
❯ python pdf-parser.py --search JS elixir_of_the_malware_whisperer.pdf
obj 183 0
 Type:
 Referencing: 184 0 R

  <<
    /JS 184 0 R
    /S /JavaScript
  >>
```

We can see there's a reference to object 184, so let's dump the raw contents of it

```
❯ python pdf-parser.py --object 184 --raw --filter elixir_of_the_malware_whisperer.pdf > pdf.js
```

The final JS obtained is 
```js
var flag = [0xcb, 0xb, 0x15, 0x41, 0x7a, 0xaa, 0xef, 0xd7, 0xff, 0xdd, 0x66, 0x18, 0x69, 0xe, 0x23, 0x59, 0xe6, 0xc2, 0xe6, 0xc, 0xd, 0xee, 0x7, 0x6c, 0xfd, 0x85, 0x66, 0xbe, 0xd5, 0x9b, 0x8f, 0x6e, 0x69, 0x58, 0xe6, 0x88, 0x93, 0x5, 0x4e, 0x63, 0x4a, 0x8d, 0x1c, 0x5b, 0x4, 0x57, 0x81, 0x4d, 0x57, 0x2b, 0x8, 0xf8, 0xf1, 0xbb, 0x1e, 0xd8, 0x96, 0x6a, 0xd0, 0x97, 0x9d, 0x8a, 0x37,
0xd0, 0x57, 0x28, 0x49, 0x58, 0xa2, 0x61, 0x3c, 0x54, 0xb0, 0x49, 0x46, 0x9c, 0x9d, 0xee, 0x51, 0x4d, 0xad, 0x2f, 0x86, 0xdd, 0x46, 0xa8, 0x2f, 0xb7, 0xb8, 0x36, 0xd1, 0x34, 0x62, 0xa8, 0x69, 0x58, 0x1e, 0x57, 0x6c, 0x5f, 0xc8, 0x2d, 0x47, 0xcb, 0x82, 0xe, 0x73, 0x60, 0x48, 0x12, 0x6a, 0x6a, 0x39, 0x2c, 0x1a, 0x54, 0x3f, 0x32, 0xad, 0x93, 0xc7, 0xaa, 0xcb, 0xf6, 0xe9, 0x48, 0x34, 0x2, 0x2a, 0x25, 0x7c, 0x7a, 0x50, 0xcb, 0x29, 0x1a, 0x48, 0xbb, 0x6, 0x33, 0xf9, 0x67, 0xd8, 0xdf, 0xf9, 0xf0, 0x8a, 0x53, 0x1, 0x2a, 0x1d, 0x45, 0xc0, 0xde, 0xc0, 0xfd, 0x83, 0xfc, 0x48, 0xb7, 0x23, 0xc, 0x7c, 0x7b, 0x71, 0x50, 0xeb, 0xf3, 0xd1, 0x74, 0x14, 0xac, 0xd3, 0xf0, 0xff, 0x40, 0x15, 0x99, 0x45, 0x39, 0x5, 0x28, 0x6, 0x1b, 0xaa, 0xfa, 0x16, 0x14, 0x66, 0x8, 0x3f, 0x7e, 0xb2, 0x9d, 0xc7, 0x96, 0x92, 0x8b, 0xf9, 0xda, 0x89, 0xed, 0xf6, 0xe8, 0x6b, 0x6f, 0x5d, 0x48, 0xd7, 0xd, 0xb9, 0x49, 0x34, 0xf1, 0xc4, 0xc7, 0x8d, 0xc4, 0xa0, 0x5b, 0x6a, 0x70, 0x12, 0xd2, 0x1d, 0x7d, 0x59, 0x53, 0x8a, 0xe0, 0xc8, 0x55, 0x28, 0xfc, 0x3c, 0xc2, 0xda, 0xb9, 0xe7, 0xbe, 0x9b, 0xbc, 0xcf, 0x3, 0x6b, 0x64, 0x36, 0x6c, 0x13, 0xb3, 0x9c, 0xc4, 0x63, 0x32, 0xae, 0x25, 0xc7, 0xb9, 0x1b, 0x2f, 0x10, 0xcc, 0x21, 0x5d, 0x7d, 0x7b, 0x29, 0xcb, 0x28, 0x38, 0xc7, 0x84, 0xe1, 0xae, 0xe7, 0x4d, 0x5b, 0xbd, 0x1f, 0x9d, 0xe5, 0x8d, 0xb1, 0xfe]

var elixir = []
var elixir_amount = 0

var instructions = {
    amplify: function(ingredient_src, amplifier) {
        return (ingredient_src ^ amplifier ^ elixir_amount) & 0xff
    },

    add: function(ingredient, amplifier, factor) {
        ingredient_src = ""
        amplifier_src = ""

        if(ingredient == "Fennel Silk")
            ingredient_src = 0x46

        if(ingredient == "Amanita Cap")
            ingredient_src = 0x41
        if(amplifier == "Luminous Cap Dust")
            amplifier_src = 0x4C

        if(amplifier == "Gengko Brush Hair")
            amplifier_src = 0x47

        for(var i = 0; i < factor; ++i) {
            elixir.push(instructions.amplify(ingredient_src, amplifier_src))
            elixir_amount += 1
        }
    },

    stir: function() {
        var seed = 188 ^ 210

        for(var i = 0; i < elixir_amount; ++i) {
            var swap = Math.abs(Math.floor((Math.sin(seed++) * 10000))) % elixir_amount

            var tmp = elixir[swap]
            elixir[swap] = elixir[i]
            elixir[i] = tmp
        }
    },

    shake: function() {
        for(var i = 0; i < elixir_amount; ++i) {
            var swap = Math.floor(Math.random() * elixir_amount)

            elixir[i] ^= elixir[swap]
            elixir[swap] ^= elixir[i]
            elixir[i] ^= elixir[swap]
        }
    },

    boil: function() {
        elixir = elixir.slice(114, elixir_amount)
    },

    drink: function(magic_word) {
        if(magic_word == "Patience") {
            res = String.fromCharCode(flag[0] ^ elixir[0])
            for(var i = 1; i < elixir.length; ++i) {
                res += String.fromCharCode(flag[i] ^ flag[i - 1] ^ elixir[i])
            }
        }
    }
}
```
From the document, we had the instructions
```
Add (in this order only!)
Fennel Silk (amplifed by Luminous Cap Dust by a factor of 188)
Amanita Cap (amplified by Gengko Brush Hair by a factor of 210)
Stir gently (never shake an elixir!)
Boil
Chant a magic word
Drink up!
```
So let's just follow as they say...
```js
instructions.add("Fennel Silk", "Luminous Cap Dust", 188)
instructions.add("Amanita Cap", "Gengko Brush Hair", 210)
instructions.stir()
instructions.boil()
instructions.drink("Patience")
console.log(res)
```  
And we get the following output:
```
Hey! If you're reading this it means you've found out that there's no shortcut, like a potion, in malware reverse engineering.
Hook onto the small details
Stay calm
Possess an undying will
Be creative
Coupled with alot of patience
And you'll realise
Cyberthon{1t_w4s_1n_y0u_a11_a10ng}
```
  
Flag: `Cyberthon{1t_w4s_1n_y0u_a11_a10ng}`
