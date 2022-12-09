# HEATKEEB

## Original Challenge Description

> Jaga had gained interest in custom keyboards and has created a platform to create your own keebs!
> We know we created his custom keeb on the 22nd of September 2022, at 12:00:00 SGT. Oddly specific but we know it's true.

HeatKeeb was a web challenge that had a website for users to create custom keyboard designs. After specifying colors for the keys and texts on their keyboard design, the website would give you a token to access your design. There was an interface that allowed users to edit their keyboard colors, view their design, and type in some text where the user could then view a heatmap overlayed on their keyboard based off which letters were in the text inputed. Lastly, there was a page to check if a word was a user's "favorite" word, inputting the last text that was previously inputted into the heatmap generation would count as a favorite word.

Looking at the code for the favorite words page, we see a check that would allow us to get the flag
```py
@app.post('/text')
def flag(request: Request, text: str = Form(...)):
    if 'token' in request.session:
        with shelve.open('keebdb') as db:
            token = request.session['token']
            if token in db:
                if token == ADMIN_TOKEN and text.upper() == KEY:
                    return templates.TemplateResponse("flag.html", {"request": request, "word": text, "flag": FLAG})
                elif text.upper() == db[token]['text']:
                    return templates.TemplateResponse("flag.html", {"request": request, "word": text})
    return templates.TemplateResponse("flag.html", {"request": request})
```
It seems like if we used the admin token and gave some sort of key as the input text, the page would render with the flag. Lets see how the admin's token was generated

```py
@app.post("/build")
def build(request: Request, name: str = Form(...), frameColor: str = Form(...), keyColor: str = Form(...), textColor: str = Form(...), specialColor: str = Form(...)):
    t = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
    seed = int(t.timestamp())
    random.seed(seed)
    token = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
    with shelve.open('keebdb') as db:
        db[token] = {
            'name': name,
            'frameColor': hex_to_rgb(frameColor),
            'keyColor': hex_to_rgb(keyColor),
            'textColor': hex_to_rgb(textColor),
            'specialColor': hex_to_rgb(specialColor),
            'text': 'default'
        }
    img = draw_keeb(name, hex_to_rgb(frameColor), hex_to_rgb(keyColor), hex_to_rgb(textColor), hex_to_rgb(specialColor))
    img.save(f'keebs/keeb-{token}.png')
    request.session['token'] = token
    return templates.TemplateResponse("build.html", {"request": request, "resp": "Success!", "token": token})

```
If we head over to the keyboard creation page, we see a few lines that generate a random token, however the seed used is the timestamp (GMT+8) when the keyboard was created. Given that the challenge description gives us the time Jaga created his keyboard, we can easily recreate his token.

Converting 22/09/22 12PM SGT to unix time, we get 1663819200.
```py
seed = 1663819200
random.seed(seed)
token = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
print(token)
```
Reusing the token generation code, this prints out gxpqSQwZGhMLh0wA as the token. Nice! We now have access to Jaga's keyboard... except the token did not work, I thought maybe I was supposed to use GMT+0 or AM instead of PM but none of the other timestamps were giving me the correct token. After about an hour of staring at the code and trying different combinations, I eventually filed a support ticket to get a sanity check. A few minutes later, I see this announcement in the discord.
![image](https://user-images.githubusercontent.com/42673064/206583735-5b193d80-26f1-4f53-a668-46c755d7c704.png)

Needless to say I was annoyed that I had wasted my time but at least I knew I was on the right track, using the correct time as the seed, we get the correct token: rMwwbpMkzAwyRoWs. But this is only the first half of the challenge, I still had to figure out the key, luckily we are able to get some information about the key.
```py
adminName = 'j4g4h1ms3lf'
adminFrame = hex_to_rgb('#000000')
adminKeys = hex_to_rgb('#dcdedb')
adminText = hex_to_rgb('#000000')
adminKeys = hex_to_rgb('#98b5bb')
with shelve.open('keebdb') as db:
    db[ADMIN_TOKEN] = {
            'name': adminName,
            'frameColor': adminFrame,
            'keyColor': adminKeys,
            'textColor': adminText,
            'specialColor': adminKeys,
            'text': KEY
        }
```
In the shelve database, the key is stored in the text field, this field is what is used to generate the heatmap design, going to view our heatmap using Jaga's token, we see the following image:
![image](https://user-images.githubusercontent.com/42673064/206584277-26999b94-c35a-456e-a5d8-1faff9132888.png)
I then traced the highlighted keys on my own keyboard to get the letters "asertghnil". Now I had to find the correct permutation of these letters to use as the key. I fed these letters into a unscrambler website and the possible candidates it gave me was either "Earthlings" or "Slathering". Earthlings was the correct word and the flag returned was `STF22{h34t_k3yb04rD}`, giving me first blood on this challenge in my category.

