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
