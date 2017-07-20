import urllib2
import os,re,sys

folder = sys.path[0] + "\\scans\\"
base="http://gynvael.coldwind.pl/misja008_drone_io/scans/"
start = "68eb1a7625837e38d55c54dc99257a17.txt"

queue=[]
queue.append(start)


def get_file(filename):
    if os.path.exists(folder + filename):
        print "already have file: " + filename
        return

    print "getting file: " + filename
    content = urllib2.urlopen(base + filename).read()

    scan_it(content)

    f = open(folder + filename, "w")
    f.write(content)
    f.close()


def scan_it(c):
    patern = "MOVE_[A-Z]{4,5}: (.+)" # MOVE_SOUTH: 0d825143bf3476dc5df8ee736a61e4f3.txt

    for s in re.findall(patern, c):
        if s[-4:]==".txt":
            queue.append(s)


for scanname in os.listdir(folder):
    ff = open(folder + scanname,"r")
    c = ff.read()
    ff.close()
    scan_it(c)

while len(queue):
    get_file(queue.pop())
