# What does the cow say?
Written by Halogen
## Problem Statement
> We've got intel that APOCALYPSE has an important file within this webserver named "flag.txt".  
>   
> Please help us retrieve its contents.  
>   
> The URL for this challenge:  
> http://chals.cyberthon22f.ctf.sg:40201
## Solution
From randomly inserting messages, we can see that a cow responses using some bash command
![[cowsay.png]]
From this we see that the message is just plugged into the code, making it vulnerable to command line injection.
But upon inspection (`Inspect Element`), we note the function used to submit the message.
```js
function logSubmit(form, event) {
    event.preventDefault();
    const url = "/cowsay";

    let msg = form["msg"].value;
    msg = msg.replace(/\n/g, "\\n").replace(/\'/g, "\\x27");
    msg = `'${msg}'`;
    fetch(url, {
        method : "POST",
        headers:{
            msg
        },
    }).then(
        response => response.json()
    ).then(
        response => {
            let output = response["output"]
            let cmd = response["cmd"]
            document.getElementById("output").innerText = output;
            document.getElementById("cmd").innerText = cmd;
        }
    );
}
```
We see that we can just communicate directly with the program using "/cowsay".
So we can do a `POST` request with the form value `msg` = `"$(cat ../usr/local/flag/here/flag.txt)"`
With that, we get a cow that states the flag 🥳

Flag: `Cyberthon{1_L0V3_W4GYU}`