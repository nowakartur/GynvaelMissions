# Gynvael Stream EN Mission 009 Write-Up
[youtube link](https://www.youtube.com/watch?v=7RotbY17tKk)

Mission: (http://gynvael.vexillium.org/ext/af80bc74e37a9c5b76edbfd658903bdf2ccedd47_mission009.txt)

Write-up: **Artur Nowak**



**Mission 009:**



```
Welcome back agent 1336.
No mail.
> mission --take
MISSION 009               goo.gl/CQFtRZ             DIFFICULTY: ████████░░ [8╱10]
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

We've received an encrypted message from one of the agents-in-training. While we
are always happy with good use of modern cryptograpical protocols, it turned out
the agents-in-training didn't use one. They said it was too hard and they didn't
understand the settings and options.

"So what did you use" we asked and got the answer "oh, it was a OTP XOR". Hmm,
that's actually not so bad. We looked at the message again:

   9a 60 76 14 8b 36 5a 10 2b 91 c4 6c ab 27 92 99 f8 6a ec 5d 32 20 3d 61 8f
   c7 fb dd 02 72 bf

And then we asked for the key.

"Oh? OTP requires us to store the key? We... we didn't know that."

There we go again.

Trying to be patient we asked "what do you have" and we've received an object
file with with the cipher implementation, but without the original message (we've
been told it has been removed for security reasons, of course).

Well, it looks like a hopeless case, but take a look anyway - maybe you can
decipher the message. Here's the binary:

  https://goo.gl/ZwSwPS

GOOD LUCK!                                                  Wednesday, 2017-07-19
---------------------------------------------------------------------------------

If you decode the answer, put it in the comments under this video! If you write
a blogpost / post your solution online, please add a link in the comments too!

P.S. I'll show/explain the solution on the stream next week.

```


First of all, I'd like to say that this is my first non-polish write-up, so sorry for my not perfect english and any other mistakes :) Of course any comments are welcome :)

In this mission i have to find a way to decipher XORed data, but XORed with One-Time-Pad [wikipedia link about it](https://en.wikipedia.org/wiki/One-time_pad) - so any well known methods based on character frequencies etc. are useless in this case. Key for the one-time-pad ciphers are at least as long as encrypted message.



**Binary object file**

In mission description I found binary file used to create encrypted message. This object file (created by the compiler before linking together with other files) is rather small, so there is a hope I can find something....  I've opened binary in lister to find any clues....

![binary file in lister](https://github.com/nowakartur/GynvaelMissions/raw/master/EN009/img/binarylister.png)

File is compiled by **GCC: (x86_64-win32-seh-rev0, Built by MinGW-W64 project) 7.1.0** - this will help me later.

To look into this object file I used IDA Pro:

![binary file in IDA Pro - 01](https://github.com/nowakartur/GynvaelMissions/raw/master/EN009/img/ida_01.png)

There are a small number of functions in this binary... (main, printf, rand, srand, time64), and all of them a commonly used by any programmer so still there is a hope :)

IDA Pro has ability to decompile and create pseudocode from binary files, and after I used it...

![binary file in IDA Pro - 02](https://github.com/nowakartur/GynvaelMissions/raw/master/EN009/img/ida_02.png)

I already renamed some variables, and for example there is text in variables I named T01 - T04:
```
t01 = 'RCES EHT';
t02 = 'B SAH TE';
t03 = 'OMER NEE';
t04 = 'LOL DEV';
```

Variable T01 - T04 in  memory are located  one after another (**sp+0x20h** -> **sp+0x28h** -> **sp+0x30h** -> **sp+0x38h**) so this must be a char array:

```
signed __int64 t01; // [sp+20h]
signed __int64 t02; // [sp+28h]
__int64 t03; // [sp+30h]
__int64 t04; // [sp+38h]
```


I think this is a messsage from author (this message overwrites secret I need to find):
```
"THE SECRET HAS BEEN REMOVED LOL" :)
```

Thanks :)

I spent couple of minutes to figure out what is important and what I can skip in further analysis.

I have marked 4 blocks that seems interesting:


![binary file in IDA Pro - 03](https://github.com/nowakartur/GynvaelMissions/raw/master/EN009/img/ida_03.png)

**Block a)** - this is first usage of function time64() [function description](http://www.cplusplus.com/reference/ctime/time/) - is there some time-dependent steps ??

**Block b)** - initialization od random number generator with value received in previous block - Time function returns [unix timestamp](https://en.wikipedia.org/wiki/Unix_time) and this is seed for RNG

**Block c)** - I think this is a block creating one-time-pad key array, it uses random values and do some unspecified math operations on it (I do not know why, but i will need to reproduce this calculations)

**Block d)** - this is place where XOR operation is starting, so it must be it :). Function **_mm_xor_si128** is SSE2 powered XOR operation: [msdn desc](goo.gl/5oxH5a)


Conclusion:

Agent use randomly generated one-time-pad for XOR message data with key. Random number generator was initialized with value of current timestamp (script execution time)

**Attack**

To recreate key used by Agent I need:
- timestamp of script execution
- identical rand() function implementation as Agent used

Problem with timestamp: I think there is no information about compilation time in object file (I didn't find any), so I have to bruteforce it...  I assumed that message was created maximum one week before I got it. I will have to check 7 (days) * 24 (hours) * 60 (minutes) * 60 (seconds) timestapmps (604800!). I think it is doable :)

Problem with rand() implementations: After my short research i found there is many rand() implementations, even in C language there is huge differences (for example between glibc and MS Visual distibution): [wikipedia link](https://en.wikipedia.org/wiki/Linear_congruential_generator)

Most of rand() implementations uses something like that:

```cpp
static unsigned long int next = 1;

int rand(void) // RAND_MAX assumed to be 32767
{
    next = next * 1103515245 + 12345;
    return (unsigned int)(next/65536) % 32768;
}

void srand(unsigned int seed)
{
    next = seed;
}
```

But for 100 % sure I will generate random numbers by **GCC: (x86_64-win32-seh-rev0, Built by MinGW-W64 project) 7.1.0** (Just like Agent do).

**Scripts**

Message I need to decrypt has 31 bytes, so I will generate 32 long random numbers for every timestamp begining at the moment when I received task and ending week earlier.

Script I used to generate random numbers:

```cpp
#include <string>
#include <ctime>
#include <cstdio>

int main()
{
  int sec_in_week = 7 * 24 * 60 * 60 ; // for going back one week

  // int now = time(0);
  int now = 1500552000; // assuming no earlier then 07/20/2017 @ 12:00pm (UTC)


  for (size_t seed = now ; seed > now - sec_in_week; seed--) {
    srand(seed);
    printf("\n%d ",seed);
    for (size_t i = 0; i < 32; i++) { // generate 32 random numbers with given seed
      int s=rand();
      printf("%d ", s);
    }
  }

}
```

There was a suprise, file size generated by this script (script was executed with redirected output fo file) was over 110 MB :) Lots of random numbers :)


Python script I used for searching correct timestamp, key and finally decrypted message:


```python
import string
import sys

printable = set(string.printable)

message=[]
raw_message = "9a 60 76 14 8b 36 5a 10 2b 91 c4 6c ab 27 92 99 f8 6a ec 5d 32 20 3d 61 8f c7 fb dd 02 72 bf" # 31 bytes
for i in raw_message.split():
    message.append(int(i,16))


def test_line(line):

    # line format: seed 1st_rand 2nd_rand 3rd_rand....
    line = line.split()
    if len(line)==0: return

    seed = line[0] # first element

    key = []
    for e in line[1:]: # from second element
        randomnum = int(e)
        ret = randomnum - (randomnum *  2139127681 >> 39) - (randomnum >> 31)
        ret &= 0xff
        key.append(ret)

    decoded = []
    for i in range(len(message)):
        decoded.append(chr(message[i] ^ key[i]))

    if set(decoded).issubset(printable):
        print "seed: ", seed
        print "".join(decoded)
        quit()



folder  = sys.path[0]
randoms = open(folder + "\\" +  "randoms.txt", "r")

for line in randoms.readlines():
    test_line(line)
```


As I said before I must replicate this strange math calculations:

```python
ret = randomnum - (randomnum *  2139127681 >> 39) - (randomnum >> 31)
```

Script opens random numbers file, and line by line trying to decode message with given random numbers. Script will quit when decrypted message will contain only printable characters:

```python
printable = set(string.printable)
[...]
if set(decoded).issubset(printable):
    print "seed: ", seed
    print "".join(decoded)
    quit()
```


Script Execution:

![output](https://github.com/nowakartur/GynvaelMissions/raw/master/EN009/img/output.png)


**Done**

I have an answer:
- timestamp of script execution: 1500483661 (19/07/2017 @ 5:01pm UTC)
- decrypted message: Who needs to store keys anyway.
