# 4 Paths of Pain
by Halogen, etc... <put name here\>
> Problem Description
## Provided Files
[Link under assets](./assets/)
## Solution
You open the website and wow how empty!
Inspect element reveals a hidden parameter `?nopain=haha`
Now obviously, when haha is returned back onto the screen, you have to try every possible injection (XXS, SSTI, SQL, etc) just to try and run some code.
With this, we got a hit on SSTI (payload: `nopain={{7+7}}`) and we perform a typical SSTI to access the system `?nopain={{request.application.__globals__.__builtins__.__import__('os').popen(cat app.py').read()}}`

On `app.py` we see this piece of code
```python
app.route('/defendthevillagefrompain', methods=['GET']) 
def page3(): 
	try: return send_file('./blueprint.img') 
	except Exception as e: return str(e) 
```
So we visit it and get `blueprint.img`.

Inside `blueprint.img` we get a "github repository" and a lot of folders. Sifting through them all (and with a lot of pain) we find `secret-message.txt` with the message:
"The last hiding place is located at pollylester/defendingkonohafrompain"

And that is where we got stuck for like a day... pain and suffering 😔

It was here where we had the insane idea to search on docker hub, and we did find [pollylester/defendingkonohafrompain](https://hub.docker.com/r/pollylester/defendingkonohafrompain) and a base64 encoded string `U1RGMjJ7cDQxbl8xc180MTFfdGgzX3M0bTN9`. Decoding it reveals the flag

Flag: `STF22{p41n_1s_411_th3_s4m3}`