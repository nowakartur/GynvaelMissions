# Gynvael Stream EN Mission 012 Write-Up
[youtube link](https://www.youtube.com/watch?v=4Xo_FAx6P0A)

Mission: (http://gynvael.vexillium.org/ext/a5da6349803f65783958b51c3b9fd15c3c35c0d5_mission012.txt)

Write-up: **Artur Nowak**



**Mission 012:**



```
Welcome back agent 1336.
No mail.
> mission --take
MISSION 012               goo.gl/qudiHJ             DIFFICULTY: ██░░░░░░░░ [2╱10]
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

Our agents managed to install a hardware keylogger in suspects computer. After
they retrieved it and dumped the recorded data, here is what showed up:

  58 f0 58 1b f0 1b 58 f0 58 44 f0 44 2d f0 2d 2d f0 2d 35 f0 35 41 f0 41 29
  f0 29 59 43 f0 43 f0 59 29 f0 29 23 f0 23 44 f0 44 31 f0 31 52 f0 52 2c f0
  2c 29 f0 29 1b f0 1b 4d f0 4d 24 f0 24 1c f0 1c 42 f0 42 29 f0 29 12 42 f0
  42 f0 12 24 f0 24 35 f0 35 32 f0 32 44 f0 44 1c f0 1c 2d f0 2d 23 f0 23 49
  f0 49

Could you help us decoded it to know what was typed?

Good luck!

---------------------------------------------------------------------------------

If you decode the answer, put it in the comments under this video! If you write
a blogpost / post your solution online, please add a link in the comments too!

P.S. I'll show/explain the solution on the stream in ~two weeks.
```


**Recorded data**

There are 102 hex digits provided by a hardware keylogger. I think it has to be scancodes.
Scancodes in this message can be scancode turning ON some key (for example 58), and scancode turning OFF this same key (f0 58).

All I need to do is find table with all available scancodes and just translate message.

**Scancode table**

I found scancode table here: [http://www.computer-engineering.org/ps2keyboard/scancodes2.html]

But.... this table is quite big, so lets do it in Javascript :)

**Javascript**


I will use Chrome Javascript Console to write some JS script:

![javascript in chrome](https://github.com/nowakartur/GynvaelMissions/raw/master/EN012/img/jsconsole.png)


First, I need to inject jQuery to scancode page:

```javascript
var script = document.createElement('script');script.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js";document.getElementsByTagName('head')[0].appendChild(script);
```

done :) ,now I can traverse page DOM and find what I need

Next, some variable initialization

```javascript
msg = "58 f0 58 1b f0 1b 58 f0 58 44 f0 44 2d f0 2d 2d f0 2d 35 f0 35 41 f0 41 29 f0 29 59 43 f0 43 f0 59 29 f0 29 23 f0 23 44 f0 44 31 f0 31 52 f0 52 2c f0 2c 29 f0 29 1b f0 1b 4d f0 4d 24 f0 24 1c f0 1c 42 f0 42 29 f0 29 12 42 f0 42 f0 12 24 f0 24 35 f0 35 32 f0 32 44 f0 44 1c f0 1c 2d f0 2d 23 f0 23 49 f0 49"
b = msg.split(" ")
i=0
answer = []
```

and search for scancode table in DOM:
```javascript
var t = $("table table").first()
```

Now, I can iterate by message items with this loop:

```javascript
while (i<b.length){
	if (b[i]=="f0") {
		i = i + 2;
		continue
    }
	o = t.find("td:contains('"+ b[i].toUpperCase() +"')").prev("td").children().first().text()
	answer.push(o)
	i++
}
```

When loop detect key OFF scancode (f0 XX) it just skip this two elements. In any other cases it just search appropriate key for given scancode in DOM using:

```javascript
 t.find("td:contains('"+ b[i].toUpperCase() +"')").prev("td").children().first().text()
```

Finally I need to print the answer:
```javascript
console.log(answer)
```

The answer is (in scancodes)
```
["CAPS", "S", "CAPS", "O", "R", "R", "Y", ",", "SPACE", "R SHFT", "I", "SPACE", "D", "O", "N", "'", "T", "SPACE", "S", "P", "E", "A", "K", "SPACE", "L SHFT", "K", "E", "Y", "B", "O", "A", "R", "D", "."]
```

![javascript in chrome](https://github.com/nowakartur/GynvaelMissions/raw/master/EN012/img/answer.png)

**Answer**

Clearing answer from unnecessary data gave me:

```
Sorry, I don't speak Keyboard.
```
