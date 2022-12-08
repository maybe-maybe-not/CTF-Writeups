# guthib actions
by scuffed and Halogen
> Problem Description
> Jaga visits a software development company that uses a custom CI/CD system to build executables for their software every 30 seconds. While CI/CD is a good practice in the industry, just like other companies in this world of vulnerabilities, the system administrators forgot to close a guest account on the build system. Rumour has it that the login details for this account can be found easily in one of the provided files. Luckily, this account does not have root access and cannot access the confidential information stored in the root directory...or can it?
## Solution
The challenge provides us with a lot of helpful files, namely the Dockerfile, `build.sh` and `build.py`.
Inspecting `build.py`, we get an idea of what we wish to achieve
```py
import subprocess
subprocess.call(['pyinstaller',  '-F',  '--distpath', '/root', '/root/flag.py'])
```
Reading this, it seems like whatever the output binary of the pyinstaller should give us the flag.
Going back a step, let us look at the Dockerfile:
```dockerfile
...

RUN useradd -m -c 'Restricted guest account' guest && \
    echo 'guest:guest' | chpasswd

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN (crontab -l ; echo "* * * * * /root/build.sh") | crontab

...
```
We now have a login that we can use when we ssh into the machine, `guest:guest`. We also see that the `build.sh` script is run every minute via crontab. So what does `build.sh` contain exactly?
```sh
#!/bin/bash
cd /tmp  # dump all the temp files Pyinstaller may generate in the temp dir
cp /root/build.py build.py
python3 build.py >/dev/null 2>&1  # build flag printing binary
rm -r *
```
So we see that it copies over `build.py` to a `tmp` directory, runs it, and then clears out the directory. Upon ssh, we notice that `tmp` is actually writeable under the guest account...

### Idea One: Appending to `build.py`
In most crontab privilege escalation situations, you want the cronjob to run a script of your liking under the permissions of the user that calls it, which in this instance is root.

However, an issue here seems to be that any version of `build.py` you drop into `tmp` gets overwritten due to the `cp` command... Furthermore, it gets deleted right after!

Something of note is how the deletion is performed: by calling `rm -r *`

Here, we have what's called a **wildcard injection** attack, where we can essentially pass flags to a command through the wildcard. How?

Reading the `man` page for `rm`, we see that there's an `-i` flag which would require user confirmation before a delete occurs. Since its being run as a cronjob, no user interaction will come through and deletion does not occur. To pass this wildcard, we introduce a file called `-i` into the working directory...

```sh
touch -- -i
```
After adding this file, if we were to create our own `build.py` first, it does not get deleted after the cronjob is run. But what now? 

The first attempt at this challenge involved an attempt at a timing attack. What if we were able to intercept the cronjob and after `cp` is called, we append our own line of code to `build.py` right before it is run?

To achieve this, I wrote a simple one line bash command which will repeatedly append a line to the `build.py` script

```sh
echo "import subprocess\nsubprocess.call(['pyinstaller',  '-F',  '--distpath', '/tmp', '/root/flag.py'])" >> build.py
```
Reading the pyinstaller docs, this should reroute the binary installation directory to `/tmp`, which would allow us to obtain the result of this command. However, no such thing happened...


### Idea Two: Leveraging `cp`
Revisiting the challenge a few hours later, Halogen gave the idea to try leveraging the nature of `cp`. If you specify an existing directory instead of a filename, `cp` will write the file into that directory instead.

And so, we create a directory called `build.py` by calling `mkdir build.py`. A minute later and `/root/build.py` has been copied INTO the `build.py` directory!
So far so good, no matter that the permissions on `build.py` leave it unwritable, we have at least managed to circumvent the `cp`. But what next?

We now need `python3 build.py >/dev/null 2>&1` to run `build.py`, but `build.py` is now a directory. However, `python` _can_ "run" a directory if its a module!

With this in mind, I created a `__main.py__` file
```sh
echo "import subprocess\nsubprocess.call(['pyinstaller',  '-F',  '--distpath', '/home/guest', '/root/flag.py'])" >> __main__.py
```
A minute later, and by looking at the output of `ls -la` we can see that the directory has in fact been run by python. But no output??

This was when it hit, why the hell do I have to replicate the pyinstaller command when I can just copy `flag.py` wholesale?
Deleting `__main.py__`, we replace it with
```sh
echo "import os\nos.system('cp /root/flag.py /home/guest/flag.py')" >> __main__.py
```
A minute later, and we have the flag!

Flag: `STF22{5up3r_5U5_5y5t3m_m0du13!_a0d66b3e608fe2b38ddf77d679fbde6b74e231f54c469a081f04dc65004360f8}`
