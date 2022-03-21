# The Poem of Knowledge

This challenge provides us with a txt file [Poem Of Knowledge.txt](https://github.com/maybe-maybe-not/CTF-Writeups/files/8312547/Poem.Of.Knowledge.txt) and the description provides us with a string `17-73-24-55-84-101-141-44-54-49-10-123-62-131-114-67-47-46-60-83-84`. The flag for this challenge is simply the first character of the nth word for each integer in the string. A simple python script was used after removing the extra new lines between paragraphs.

```py
with open("Poem Of Knowledge.txt", 'r') as f:
  poem = f.read()
  poem = poem.replace('\n', ' ')
  words = poem.split(' ')
  key = [int(i) for i in "17-73-24-55-84-101-141-44-54-49-10-123-62-131-114-67-47-46-60-83-84".split('-')]
  print(''.join([words[i-1][0] for i in key]))
```

Which gives us the flag content `IHopeYouhadagreattime`
