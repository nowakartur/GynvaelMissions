# Write-Up rozwiązania misji PL 008 z Gynvael Stream PL [link do YT](https://www.youtube.com/watch?v=3hGK87NTXmw)

Zadanie: [link do zadania](http://gynvael.vexillium.org/ext/70809d8a8c51f6963a882f906dd21c18bd37428b_misja008.txt)

Write-up: **Artur Nowak**



**Treść zadania**

Jak widzimy zadanie ocenione jest w skali trudności na 9 / 10 więc jest to, jak do tej pory, najtrudniejsza misja jaką otrzymaliśmy. Nie przejmujemy sie tym :)

```
MISJA 008            goo.gl/gg4QcA                  DIFFICULTY: █████████░ [9/10]
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

Otrzymaliśmy dość nietypową prośbę o pomoc od lokalnego Instytutu Archeologii.
Okazało się, iż podczas prac remontowych studni w pobliskim zamku odkryto
niewielki tunel. Poproszono nas abyśmy skorzystali z naszego autonomicznego
drona wyposażonego w LIDAR (laserowy skaner odległości zamontowany na obracającej
się platformie) do stworzenia mapy tunelu.

Przed chwilą dotarliśmy na miejsce i opuściliśmy drona do studni. Interfejs I/O
drona znajduje się pod poniższym adresem:

  http://gynvael.coldwind.pl/misja008_drone_output/

Powodzenia!

--

Korzystając z powyższych danych stwórz mapę tunelu (i, jak zwykle, znajdź tajne
hasło). Wszelkie dołączone do odpowiedzi animacje są bardzo mile widziane.

Odzyskaną wiadomość (oraz mapę) umieśc w komentarzu pod tym video :)
Linki do kodu/wpisów na blogu/etc z opisem rozwiązania są również mile widziane!

HINT 1: Serwer może wolno odpowiadać a grota jest dość duża. Zachęcam więc do
cache'owania danych na dysku (adresy skanów są stałe dla danej pozycji i nigdy
nie ulegają zmianie).

HINT 2: Hasło będzie można odczytać z mapy po odnalezieniu i zeskanowaniu
centralnej komnaty.

P.S. Rozwiązanie zadania przedstawie na początku kolejnego livestreama.
```

Druga podpowiedź wskazuje, że rozwiązanie odczytamy z wygenerowanej przez Drona mapy centralnej komnaty, prawdopodobnie będziemy musieli odtworzyć całą mapę.



**Podręcznik operatora Drona**

Do zadania otrzymaliśmy podręcznik operatora z kilkoma dodatkowymi wskazówkami.


  ![podrecznik](https://github.com/nowakartur/GynvaelMissions/raw/master/PL008/img/podrecznik.png)

Mamy więc skan pomieszczenia zrobiony co 1 metr, w każdą stronę co 10 stopni, zapisując w każdym skanie swoją aktualną pozycję i odległości do ścian. To powinno umożliwić zbudowanie mapy całego obszaru.

Opcje jakie nam zostają:
- poruszanie się przy krawędzi i na tej podstawie budowanie planu (ryzykowne jeśli autor przygotował się na taką ewentualność lub jeśli plan pomieszczeń uniemożliwi zastosowanie tej metody)
- napisanie algorytmu w którym będziemy sami sterowali poruszaniem się po komnatach w zależności od tego jak daleko mamy do ściany - rozwiązanie najbardziej eleganckie jednak wymagające największych nakładów pracy
- metoda brute force - stworzenie mapy na podstawie wszystkich skanów jakie wykonał dron parsując jedynie zapisane pozycje drona z krótych skan był robiony

**Brute Force**

Użyjemy metody brute force. W pierwszej kolejności pobieramy plik startowy drona i skryptem w pythonie iterujemy po wszystkich możliwych kierunkach jakie mógł wykonać dron.
Skrypt będzie sprawdzał czy ma już w bazie plik skanu i jeśli go ma nie będzie pobierał go ponownie.
Dodatkowo w związku z dużym obiciążeniem strony autora i występującymi błędami typu "Internal Server Error 500" musimy mieć możliwość restartu skrptu od dowolnego momentu i wznowienia jego pracy bez konieczności zaczynania jego pracy na nowo (stąd też na początku działania skryptu skanujemy wszystkie pliki które mamy już pobrane).

Skrypt wygląda tak:


```python
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

```



Skrypt pobiera pliki utworzone przez drona (.txt) a następnie skanuje je w poszukiwaniu ciągu znaków określających kolejne pliki skanów, wyszukujemy linii wyglądających podobnie do "MOVE_SOUTH: 0d825143bf3476dc5df8ee736a61e4f3.txt". Używamy regexpa:
```
"MOVE_[A-Z]{4,5}: (.+)"
```


Jeśli znajdziemy takie linie dodajemy same nazwy plików do kolejki pobierania:

```python
for s in re.findall(patern, c):
    if s[-4:]==".txt":
        queue.append(s)
```

Każdy pobrany plik jest poddawany takiemu samemu skanowaniu i po znalezieniu w nim nazw plików kolejnych skanów wrzucamy je do kolejki pobierania.


Po pobraniu wszystkich plików (ponad 187 000):

![scans](https://github.com/nowakartur/GynvaelMissions/raw/master/PL008/img/scans.png)

możemy przystąpić do rysowania mapy.


**Mapa**

W każdym pliku skanu mamy otrzymujemy (w drugiej linii pliku) zapisaną pozycję drona z której zrobiono skan:

![scan](https://github.com/nowakartur/GynvaelMissions/raw/master/PL008/img/scan.png)

W związku z tym potrzebujemy:
- ustalić maksymalne rozmiary mapy czyli znaleźć maksymalną pozycję X i Y na jakiej przebywał dron
- strorzyć bitmapę z zaznaczonymi miejscami które dron odwiedził i gdzie go nie było (czyli gdzie natrafił na ścianę)


Skrypt python:

```python
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

```

Skrypt iteruje po wszystkich pobranych uprzednio plikach szukając w nich pozycji z jakich był robiony skan a nastepnie dodaje je do listy z której później tworzy mapę.

Wynik działania skryptu:

![p2](https://github.com/nowakartur/GynvaelMissions/raw/master/PL008/img/p2.png)

i otrzymana mapa:

![map](https://github.com/nowakartur/GynvaelMissions/raw/master/PL008/img/map.png)

Hasło odczytujemy z centralnej komnaty.
