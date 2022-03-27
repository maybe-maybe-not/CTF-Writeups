# Painting Spot

We are given a nice image of a painting spot.

![Sick view, bro](./paintingSpot.jpg)

Let's take a look at the metadata and see if there's anything of value. We make use of `ExifTool` to get this job done.

```
...
XP Title                        : Lugar para pintar
XP Comment                      : Óptimo local para pintar, deixei uma revisão positiva
XP Keywords                     : Pintura
...
```
Besides all the device information, these comments are really interesting. Google Translate tells us that these mean "Place to paint", "Great spot to paint, I left a positive review" and "Painting".

So we probably have to find this location on Google Maps and look at the reviews. But... How????

## Google Lens

We use a Google Product to find something on a Google Product.

Google Lens managed to find me this link with a suspiciously similar looking island, and it's in Portugal
https://www.azoreswhalewatch.com/saomiguelazores/sounds-of-the-sky-in-vila-franca-do-campo/

Going to `Vila Franca do Campo` on Google Maps and scouring the coast line, we chance upon the `Praia do Corpo Santo` beach. Looking at reviews and sorting by newest, we see the following:

```
Michel Michel
1 review
2 weeks ago
NEW
(Translated by Google) Nice view and nice place. Here is the flag: dvCTF{g3o_sp0tt3d}

(Original)
Belle vue et endroit agréable. Voici le flag: dvCTF{g3o_sp0tt3d}
```

Cool.
