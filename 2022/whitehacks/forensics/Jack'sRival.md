# Jack's Rival
This challenge provides us with a password protected zip file, judging from the name and description of the challenge, we can see that we are supposed to use John The Ripper to break the password.
We use the popular rockyou.txt wordlist for this challenge.

```console
john-the-ripper.zip2john treasures.zip > hash
john-the-ripper --wordlist=rockyou.txt hash
john-the-ripper --show hash
```

And we see that the password is myroomisblue, extracting the file we get the flag `WH2022{W3_wi11_w3_w1ll_r0cky0u}`
