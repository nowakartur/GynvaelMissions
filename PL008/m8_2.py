import os, re, sys
folder = sys.path[0] + "\\scans\\"

patern="SCAN DRONE v0.17.3\n(\d+) (\d+)\n"
xmax=0
ymax=0

plots=[]
def search_plots(c):
    global xmax,ymax
    s = re.search(patern, c)
    cx=int(s.group(1))
    cy=int(s.group(2))
    if (cx > xmax):
        xmax=cx
    if (cy > ymax):
        ymax=cy
    plots.append([cx,cy])


for scanname in os.listdir(folder):
    ff = open(folder + scanname,"r")
    c = ff.read()
    ff.close()
    search_plots(c)


print "Wymiary pliku *.raw: %d x %d." % (xmax, ymax)
print "Przeskanowano %d plikow." % (len(plots))

bmp=bytearray(xmax*ymax)


for plot in plots:
    xx=plot[0]
    yy=plot[1]
    bmp[(yy-1)*xmax + xx-1] = 199 # losowy kolor

r = open("map.raw","w")
r.write(bmp)
r.close
