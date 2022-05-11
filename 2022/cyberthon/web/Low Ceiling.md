# Low Ceiling
Written by Halogen
## Problem Statement
> APOCALYPSE members frequent this server but we dont know what for. Help us find out what its for.  
> 
> The URL for this challenge: [http://chals.cyberthon22f.ctf.sg:40301/](http://chals.cyberthon22f.ctf.sg:40301/)

## Solution
Since there is almost nothing on the site, I decided to check out common files.
[http://chals.cyberthon22f.ctf.sg:40301/robots.txt](http://chals.cyberthon22f.ctf.sg:40301/robots.txt) gives a result.
> User-agent: *
> Disallow:dev

As we can see, the website does not "want" us to see this `dev` file
So we look at it, [http://chals.cyberthon22f.ctf.sg:40301/dev](http://chals.cyberthon22f.ctf.sg:40301/dev)
Going to the site, we instantly get the source code 😮

`routes/index.js`
```js
const path              = require('path');
const express           = require('express');
const router            = express.Router();

router.get('/', (req, res) => {
	secret = req.headers["secret-header"];
    if (secret == "admin"){
    	return res.sendFile(path.resolve('views/admin.html'));
    }
    return res.sendFile(path.resolve('views/index.html'));
});

router.get('/robots.txt', (req, res) => {
    res.type('text/plain');
    res.send("User-agent: *\nDisallow:dev");
});

router.get('/dev', (req, res) => {
	return res.sendFile(path.resolve('dev/source.zip'));
})

module.exports = router;
```
We note that there is a hidden `admin.html` that is displayed when we insert a secret header.
Thus we send a `GET` request with a header `{"secret-header", "admin"}` and just like that a flag is returned

Flag: `Cyberthon{l0w_ceiling_w4tch_ur_head_a6243746643baf3d}`
