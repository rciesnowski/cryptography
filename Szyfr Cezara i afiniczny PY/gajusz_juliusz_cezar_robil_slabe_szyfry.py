# Rafał Ciesnowski 253982

import sys
from math import gcd

class Cezar:
    def szyfrowanie(self, plain, k):
        if k not in range(26): print("bledny klucz, ale sprobujemy")
        crypto = ""
        for i in plain:
            x = chr(ord('A') + ((ord(i) + k - ord('A')) % 26)) if i.isalpha() and i.isupper() else chr(ord('a') + ((ord(i) + k - ord('a')) % 26)) if i.isalpha() else i
            crypto += x
        with open("crypto.txt", "w") as file:
            file.write(crypto)

    def odkoduj(self, crypto, k):
        decrypt = ""
        for i in crypto:
            x = chr(ord('A') + ((ord(i) - k - ord('A')) % 26)) if i.isalpha() and i.isupper() else chr(ord('a') + ((ord(i) - k - ord('a')) % 26)) if i.isalpha() else i
            decrypt += x
        return decrypt

    def odszyfrowywanie(self, crypto, k):
        if k not in range(26): print("bledny klucz, ale sprobujemy")
        with open("decrypt.txt", "w") as file:
            file.write(self.odkoduj(crypto, k))

    def kryptoanaliza1(self, crypto, extra):
        zlamane = False
        for k in range(26):
            if extra == self.odkoduj(crypto[:2], k):
                zlamane = True
                with open("key-found.txt", "w") as file:
                    file.write(str(k))
                self.odszyfrowywanie(crypto, k)
                break
        if not zlamane: print("Nie udalo sie zlamac szyfru")

    def kryptoanaliza2(self, crypto):
        decrypt = ""
        for k in range(26):
            decrypt += self.odkoduj(crypto, k) + "\n"
        with open("decrypt.txt", "w") as file:
            file.write(decrypt)

class Afiniczny:
    def szyfrowanie(self, plain, a, b):
        if (gcd(a,26) !=1 ) or (a not in range(26)) or (b not in range(26)): print("bledny klucz, ale sprobujemy")
        crypto = ""
        for i in plain:
            x = chr(ord('A') + ((a * (ord(i) - ord('A')) + b) % 26)) if i.isalpha() and i.isupper() else chr(ord('a') + ((a * (ord(i) - ord('a')) + b) % 26)) if i.isalpha() else i
            crypto += x
        with open("crypto.txt", "w") as file:
            file.write(crypto)

    def odkoduj(self, crypto, a, b):
        decrypt = ""
        for potencjalne_a_ in range(26):
            if (a * potencjalne_a_) % 26 == 1:
                a_ = potencjalne_a_
                for i in crypto:
                    x = chr(ord('A') + (int((ord(i) - ord('A') - b) * a_) % 26)) if i.isalpha() and i.isupper() else chr(ord('a') + (int((ord(i) - ord('a') - b) * a_) % 26)) if i.isalpha() else i
                    decrypt += x
                break
        return decrypt

    def odszyfrowywanie(self, crypto, a, b):
        if (gcd(a,26) !=1 ) or (a not in range(26)) or (b not in range(26)): print("bledny klucz, ale sprobujemy")
        with open("decrypt.txt", "w") as file:
            file.write(self.odkoduj(crypto, a, b))

    def kryptoanaliza1(self, crypto, extra):
        zlamane = False
        for b in range(26):
            for a in range(26):
                if gcd(a, 26) == 1:
                    if self.odkoduj(crypto[:2], a, b) == extra:
                        zlamane = True
                        with open("key-found.txt", "w") as file:
                            file.write(str(a) + " " + str(b))
                        self.odszyfrowywanie(crypto, a, b)
                        break
        if not zlamane: print("Nie udało się złamać szyfru")

    def kryptoanaliza2(self, crypto):
        decrypt = ""
        for a in range(26):
            if gcd(a, 26) == 1:
                for b in range(26):
                    decrypt += self.odkoduj(crypto, a, b) + "\n"
        with open("decrypt.txt", "w") as file:
            file.write(decrypt)


if (__name__ == "__main__") & (len(sys.argv) == 3):
    szyfr = sys.argv[1]
    dzialanie = sys.argv[2]
    if szyfr == "-c":
        cezar = Cezar()
        if dzialanie == "-e":
            with open('plain.txt', 'r') as file:
                plain = file.read()
            with open('key.txt', 'r') as file:
                key = file.read().split()
                k = int(key[0])
            cezar.szyfrowanie(plain, k)
        elif dzialanie == "-d":
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            with open('key.txt', 'r') as file:
                key = file.read().split()
                k = int(key[0])
            cezar.odszyfrowywanie(crypto, k)
        elif dzialanie == "-j":
            with open('extra.txt', 'r') as file:
                extra = file.read()
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            cezar.kryptoanaliza1(crypto, extra)
        elif dzialanie == "-k":
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            cezar.kryptoanaliza2(crypto)
    elif szyfr == "-a":
        afiniczny = Afiniczny()
        if dzialanie == "-e":
            with open('plain.txt', 'r') as file:
                plain = file.read()
            with open('key.txt', 'r') as file:
                key = file.read().split()
                a = int(key[0])
                b = int(key[1])
            afiniczny.szyfrowanie(plain, a, b)
        elif dzialanie == "-d":
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            with open('key.txt', 'r') as file:
                key = file.read().split()
                a = int(key[0])
                b = int(key[1])
            afiniczny.odszyfrowywanie(crypto, a, b)
        elif dzialanie == "-j":
            with open('extra.txt', 'r') as file:
                extra = file.read()
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            afiniczny.kryptoanaliza1(crypto, extra)
        elif dzialanie == "-k":
            with open('crypto.txt', 'r') as file:
                crypto = file.read()
            afiniczny.kryptoanaliza2(crypto)
else:
    print("Program o nazwie cezar powinien umożliwiać wywołanie z linijki rozkazowej z następującymi opcjami:jedna z dwóch:\n"
              "-c (szyfr Cezara),\n"
              "-a (szyfr afiniczny),\n"
              "oraz jedna z czterech:\n"
              "-e (szyfrowanie),\n"
              "-d (odszyfrowywanie),\n"
              "-j (kryptoanaliza z tekstem jawnym),\n"
              "-k (kryptoanaliza wyłącznie w oparciu o kryptogram)\n"
              "Program będzie czytał dane z pewnych plików i zapisywał na inne, nazwy tych plików są z góry ustalone:\n"
              "plain.txt: plik z tekstem jawnym (jeden wiersz, litery i spacje),\n"
              "crypto.txt: plik z tekstem zaszyfrowanym,\n"
              "decrypt.txt: plik z tekstem odszyfrowanym,\n"
              "key.txt: plik zawierający klucz, (jeden wiersz, w którym pierwsza liczba oznacza przesunięcie, druga współczynnik dla szyfru afinicznego, liczby oddzielone są spacją)\n"
              "extra.txt: plik zawierający pomocniczy tekst jawny w przypadku kryptoanalizy z tekstem jawnym i zaszyfrowanym,\n"
              "key-found.txt: plik zawierający znaleziony klucz w przypadku kryptoanalizy z tekstem jawnym i zaszyfrowanym.\n"
              "Program szyfrujący czyta tekst jawny i klucz i zapisuje tekst zaszyfrowany. Jeśli klucz jest nieprawidłowy, zgłasza jedynie błąd.\n"
              "Program odszyfrowujący czyta tekst zaszyfrowany i klucz i zapisuje tekst jawny. Jeśli klucz jest nieprawidłowy, zgłasza błąd. Dla szyfru afinicznego częścią zadania jest znalezienie odwrotności dla liczby a podanej jako część klucza – nie można zakładać, że program odszyfrowujący otrzymuje tę odwrotność.\n"
              "Program łamiący szyfr z pomocą tekstu jawnego czyta tekst zaszyfrowany, tekst pomocniczy i zapisuje obliczony klucz i odszyfrowany tekst. Jeśli niemożliwe jest obliczenie klucza, zgłasza sygnał błędu.\n"
              "Program łamiący szyfr bez pomocy tekstu jawnego czyta jedynie tekst zaszyfrowany i zapisuje jako tekst jawny wszystkie możliwe kandydatury (25 dla szyfru Cezara, 312 dla szyfru afinicznego).\n"
              "Program w żadnym wypadku nie ma prawa żądać istnienia plików niewymaganych dla danej opcji. Pliki, do których zapisujemy powinny być utworzone gdyby nie istniały.")