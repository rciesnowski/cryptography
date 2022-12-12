# Rafał Ciesnowski 253982
import sys
import re

class Xor:
    def przygotuj(self, dlugosc=17):
        orig = open('orig.txt', 'r').readlines()
        plain = ""
        for l in orig:
            l = re.sub("[,.!?:;'\-0-9]", '', l)
            l = l.lower()
            l = l[:dlugosc]
            plain += l + "\n"
        with open("plain.txt", "w") as file:
            file.write(plain)

    def szyfruj(self, keyAscii, plainAscii):
        crypto = ""
        for line in plainAscii:
            crypto += "".join([chr(line[i] ^ keyAscii[i]) for i in range(len(keyAscii))])+"\n"
        return crypto

    def koduj(self):
        key = open('key.txt', 'r').read()
        keyAscii = [ord(c) for c in key]

        plain = open('plain.txt', 'r').readlines()
        plainAscii = [[ord(c) for c in line] for line in plain]

        with open('crypto.txt', "w") as file:
            file.write(self.szyfruj(keyAscii, plainAscii))

    def kryptoanalizuj(self):
        crypto = open('crypto.txt', 'r').readlines()
        cryptoAscii = [[ord(c) for c in line] for line in crypto]
        keyAscii = [0] * (len(crypto[0])-1)

        for line in cryptoAscii:
            for i in range(len(line)-1):
                if line[i] > 64 or line[i] == 0: keyAscii[i] = line[i] ^ 32

        with open('decrypt.txt', "w") as file:
            file.write(self.szyfruj(keyAscii, cryptoAscii))


if (__name__ == "__main__") & (len(sys.argv) == 2):
    dzialanie = sys.argv[1]
    xor = Xor()
    if dzialanie == "-p": xor.przygotuj(len(open('key.txt', 'r').read()))
    elif dzialanie == "-e": xor.koduj()
    elif dzialanie == "-k": xor.kryptoanalizuj()
else:
    print("Zasadą szyfru jednorazowego jest niepowtarzalność klucza. E(k,m)=k⊕m; D(k,c)=k⊕c. Jeśli dwie wiadomości są zaszyfrowane tym samym kluczem k, to można obliczyć m1⊕m2=c1⊕c2. Znajomość xor dwu wiadomości niesie już pewne informacje, a każda uzyskana informacja jest z definicji złamaniem szyfru, nawet jesli nie prowadzi do całkowitego odszyfrowania tekstu.\n"
          "Założymy, że szyfrowane są wyłącznie litery i spacje, być może dla ułatwienia będzie można założyć, że litery są wyłącznie małe. Założymy też, że cały tekst (angielski) jest kodowany standardowo kodem ascii, tzn spacja ma numer 32, a litery 97-122. W notacji heksagonalnej spacja jest równa 0x00100000 a małe litery 0x011..... W sposób xor dwóch liter zaczyna się od trzech zer, a  xor litery i spacji ma na początku 010. Wiedząc, że m1⊕m2 ma pierwsze trzy bity 010 wiemy, że jeden ze znaków jest spacją więc m1⊕m2⊕00100000 jest drugim ze znaków, nie wiadomo którym. Jeśli mamy do dyspozycji m1⊕m2 i m2⊕m3 i np. pierwsza para ma spację a druga nie ma, to wiadomo, że spacją jest m1, i wyliczamy m2 i m3. Jeśli obie mają spacje, to prawdopodobnie jest to m2 i wyliczamy pozostałe znaki. Inny przypadek byłby możliwy, gdyby m3⊕m1=00000000 czyli m1=m3. Wówczas być może m1 i m3 byłyby spacjami, a m2 jakimś znakiem. Jeśli znamy więcej przykładów kryptogramów powstałych z użyciem tego samego klucza, to jest duża szansa, na odtworzenie dokładnych tekstów.\n"
          "Program o nazwie xor powinien umożliwiać wywołanie z linijki rozkazowej z następującymi opcjami:\n"
          "-p (przygotowanie tekstu do przykładu działania),\n"
          "-e (szyfrowanie)\n,"
          "-k (kryptoanaliza wyłącznie w oparciu o kryptogram)\n"
          "Nazwy plików są następujące:\n"
          "orig.txt: plik zawierający dowolny tekst,\n"
          "plain.txt: plik z tekstem zawierającym co najmniej kilkanaście linijek równej długości, np. 64,\n"
          "key.txt: plik zawierający klucz, który jest ciągiem dowolnych znaków podanej wyżej długości,\n"
          "crypto.txt: plik z tekstem zaszyfrowanym, każda jego linijka jest operacją ⊕ z kluczem,\n"
          "decrypt.txt: plik z tekstem odszyfrowanym.\n"
          "Uwaga: pod uwagę będą brane wyłącznie programy z kryptoanalizą.")