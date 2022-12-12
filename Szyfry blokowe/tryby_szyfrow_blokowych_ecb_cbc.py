# 253982 Rafal Ciesnowski

from PIL import Image
import numpy as np
import hashlib
import bitarray

def xor(bmp_array, x1, y1, x2, y2, key):
    k = 0
    for i in range(x1, x2):
        for j in range(y1, y2):
            if key[k]:
                if bmp_array[i, j, 0] == 0 and bmp_array[i, j, 1] == 0 and bmp_array[i, j, 2] == 0: bmp_array[i, j] = [255, 255, 255]
                else: bmp_array[i, j] = [0, 0, 0]
            else:
                if bmp_array[i, j, 0] == 255 and bmp_array[i, j, 1] == 255 and bmp_array[i, j, 2] == 255: bmp_array[i, j] = [255, 255, 255]
                else: bmp_array[i, j] = [0, 0, 0]
            k += 1
    return bmp_array


class SzyfryBlokowe:
    def __init__(self, szer, wys, plik):
        self.szer_bloku = szer
        self.wys_bloku = wys
        klucz = np.random.randint(0, 2, szer * wys)
        print("\n\t\t\t\twygenerowano klucz")

        bmp = Image.open(plik)
        print(plik, "\t\tobraz otwarty pomyślnie")

        self.ecb(bmp, klucz)
        self.cbc(bmp, klucz)

    def ecb(self, bmp, key):
        bmp_array = np.array(bmp)
        bloki = self.podziel(bmp_array)
        for i in range(len(bloki)):
            bmp_array = self.szyfruj_blok(bmp_array, bloki[i][0], bloki[i][1], bloki[i][2], bloki[i][3])
        Image.fromarray(bmp_array).save('ecb_crypto.bmp')
        print("ecb_crypto.bmp\tzaszyfrowano i zapisano")

    def cbc(self, bmp, klucz):
        bmp_array = np.array(bmp)
        bloki = self.podziel(bmp_array)
        bmp_array = xor(bmp_array, bloki[0][0], bloki[0][1], bloki[0][2], bloki[0][3], klucz)
        self.szyfruj_blok(bmp_array, bloki[0][0], bloki[0][1], bloki[0][2], bloki[0][3])
        for i in range(1, len(bloki)):
            klucz_poprz = self.klucz_bloku(bmp_array, bloki[i - 1][0], bloki[i - 1][1], bloki[i - 1][2], bloki[i - 1][3])
            bmp_array = xor(bmp_array, bloki[i][0], bloki[i][1], bloki[i][2], bloki[i][3], klucz_poprz)
            bmp_array = self.szyfruj_blok(bmp_array, bloki[i][0], bloki[i][1], bloki[i][2], bloki[i][3])
        Image.fromarray(bmp_array).save('cbc_crypto.bmp')
        print("cbc_crypto.bmp\tzaszyfrowano i zapisano")

    def szyfruj_blok(self, bmp_array, x1, y1, x2, y2):
        k = 0
        klucz_bloku = self.klucz_bloku(bmp_array, x1, y1, x2, y2)
        h = hashlib.sha256()
        h.update(klucz_bloku)
        ba = bitarray.bitarray()

        ba.frombytes(h.hexdigest().encode('utf-8'))
        for i in range(x1, x2):
            for j in range(y1, y2):
                if ba[k]:
                    bmp_array[i, j] = [0, 0, 0]
                else:
                    bmp_array[i, j] = [255, 255, 255]
                k += 1
        return bmp_array

    def klucz_bloku(self, bmp_array, x1, y1, x2, y2):
        klucz = np.zeros(self.szer_bloku * self.wys_bloku)
        k = 0
        for i in range(x1, x2):
            for j in range(y1, y2):
                if bmp_array[i, j, 0] == 0 and bmp_array[i, j, 1] == 0 and bmp_array[i, j, 2] == 0:
                    klucz[k] = 1
                else:
                    klucz[k] = 0
                k += 1
        return klucz

    def podziel(self, bmp_array):
        wys = bmp_array.shape[0]
        szer = bmp_array.shape[1]
        bloki = []
        for i in range(0, wys, self.wys_bloku):
            for j in range(0, szer, self.szer_bloku):
                x1 = i
                y1 = j
                if j + self.szer_bloku > szer:
                    y2 = j + (self.szer_bloku - ((j + self.szer_bloku) - bmp_array.size[1]))
                else:
                    y2 = j + self.szer_bloku
                if i + self.wys_bloku > wys:
                    x2 = i + (self.wys_bloku - ((i + self.wys_bloku) - bmp_array.size[0]))
                else:
                    x2 = i + self.wys_bloku
                bloki.append([x1, y1, x2, y2])
        return bloki


szy = SzyfryBlokowe(5, 4, 'plain.bmp')

