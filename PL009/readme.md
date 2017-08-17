# Write-Up rozwiązania misji PL 009 z Gynvael Stream PL
[link do YT](https://www.youtube.com/watch?v=wd3L04QNRHI)

Zadanie: [link do zadania](http://gynvael.vexillium.org/ext/3e2998dccb887cfdffd86ec658bd42d44ea4e477_misja009.txt)

Write-up: **Artur Nowak**



**Treść zadania**



```
MISJA 009            goo.gl/q49Fw7                  DIFFICULTY: ██████░░░░ [6/10]
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅
Do naszych techników trafiło nagranie, w postaci pliku dźwiękowego, z osobliwymi
piskami. Nagranie otrzymaliśmy od lokalnego radioamatora i możesz je pobrać
poniżej:

  https://goo.gl/NeJHD2

Jeśli możesz, wyręcz naszych techników w zdekodowaniu wiadomości - są obecnie
zajęci naprawą naszego elektrohydroturbobulbulatora.

Powodzenia!

--

Odzyskaną wiadomość umieść w komentarzu pod tym video :)
Linki do kodu/wpisów na blogu/etc z opisem rozwiązania są również mile widziane!

P.S. Rozwiązanie zadania przedstawię na początku kolejnego livestreama.

```




**Analiza dostarczonego pliku Wav**

Plik Wav jaki otrzymałem to plik mono, na którym słyszę naprzemiennie dwa tony  - brzmią one jak DTMF więc jest to pierwsze co sprawdzam.

Otwieram plik dowolnym programem do analizy plików dźwiękowych (skorzystałem z Audacity - darmowy):

  ![Plik Wav](https://github.com/nowakartur/GynvaelMissions/raw/master/PL009/img/wav.png)

Analiza częstotliwości wskazuje że dominujące w pliku są dwie częstotliwości: około 500 Hz i około 1200 Hz. Porównując do z opisem standardu DTMF z [Wikipedii](https://pl.wikipedia.org/wiki/DTMF) całkowicie się to nie potwierdza. W pliku mam naprzemiennie dwie sinusoidy, a w DTMF powinienem mieć mieszane częstotliwości wskazujące na konkretny znak (pozycję znaku w tabeli).



**Podejście zerojedynkowe**

Być może każda częstotliwość (skoro są tylko dwie) oznacza inny stan bitowy, czyli jedna z nich jest "zerem", a druga "jedynką". Próbuję takiego podejścia.

Mógłbym tu użyc jakichś zaawansowanych technik mierzenia częstotliwości w pliku, ale w związku z tym, że plik ma tylko 2 minuty 16 sekund, mogę to zrobić "na ucho"...

Po odłuchaniu pliku otrzymałem taki zapis zerojedynkowy:

```
0110001001001110101001101000111010101110101001100111011011000110100111100000010011101010100001100100111001001110100101101111011001001110
```

Jeśli moja hipoteza jest prawdziwa to ilość bitów powinna się dzielić przez 8.. sprawdzam:

```python
Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> len("0110001001001110101001101000111010101110101001100111011011000110100111100000010011101010100001100100111001001110100101101111011001001110")/8
17
>>>
```

Ilość bitów jest podzielna przez 8 więc być może idę dobrym tropem.


**Skypt i rozwiązanie**

Piszę prosty skrypt w pythonie, który zamieni ciąg bitów na 8 bitowe słowa, a następnie wypisze ich reprezantację w ASCII:

```python
msg="0110001001001110101001101000111010101110101001100111011011000110100111100000010011101010100001100100111001001110100101101111011001001110"

for i in range(0,len(msg),8):
    t = msg[i:i+8]
    print chr(int(t,2)),
```

i otrzymuję:

```
b N � � � � v � �  � � N N � � N
```

No z pewnością nie jest to rozwiązanie, szukam dalej.

Po wypisaniu wszystkich słów 8 bitowych dostaję taką listę:

```
01100010
01001110
10100110
10001110
10101110
10100110
01110110
11000110
10011110
00000100
11101010
10000110
01001110
01001110
10010110
11110110
01001110
```

Po chwili zastanawiania się widzę, że:
- żaden z dolnych bitów nie jest zapalony (byłoby to dziwne żeby ciąg znaków składał się tylko z parzystych kodów ASCII)
- niektóre z najwyższych bitów są zapalone (to się nie może zdarzyć w ASCII gdzie wszystkie drukowalne znaki są poniżej 128 czyli mają najwyższy bit zgaszony 0x01111111)


Pierwsza moja myśl to, że źle przypisałem jedynki i zera do częstotliwości w pliku wav, ale to nie może być to (po odwróceniu nadal miałbym niektóre górne bity zapalone)

Kolejna myśl to może w każdym 8bitowym słowie należy odwrócić kolejność znaków.. spróbuję:

```python
msg="0110001001001110101001101000111010101110101001100111011011000110100111100000010011101010100001100100111001001110100101101111011001001110"


for i in range(0,len(msg),8):
    t = msg[i:i+8]
    t = t [::-1]
    print chr(int(t,2)),
```

Otrzymuję rozwiązanie:
```
F r e q u e n c y   W a r r i o r
```
