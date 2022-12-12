import os
import itertools

funkcje = ["md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum", "b2sum"]
personale = ["personal.txt", "personal_.txt"]

def zapisz_bity(hasz):
    return [''.join(str(bin(int(znak, 16))[2:].zfill(4)) for znak in itertools.takewhile(lambda x: x != ' ', wiersz)) for wiersz in hasz]

def porownaj_bity(i_skrot):
    roznice = len([i for i,j in zip(personal[i_skrot], personal_[i_skrot]) if i != j])
    string = "\ncat hash.pdf personal.txt | " + funkcje[i_skrot] + "\ncat hash.pdf personal_.txt | " + funkcje[i_skrot] + "\n" + hash_txt[i_skrot][:-4] + "\n" + hash_txt[i_skrot + 1][:-4] + "\n" + "Liczba rozniacych sie bitow: " + str(roznice) + " z " + str(len(personal[i_skrot])) + ", procentowo: " + str(roznice * 100 // len(personal[i_skrot])) + "%\n"
    return string

os.system("> hash.txt")
for funkcja in funkcje:
    for plik in personale:
        komenda = "cat hash.pdf " + plik + " | " + funkcja + " >> hash.txt"
        os.system(komenda)
        
hash_txt = open("hash.txt", 'r').readlines()

personal = zapisz_bity([hash_txt[i].rstrip() for i in range(0,len(hash_txt), 2)])
personal_ = zapisz_bity([hash_txt[i].rstrip() for i in range(1,len(hash_txt), 2)])

diff = open("diff.txt", 'w+')
diff.write(''.join(porownaj_bity(i) for i in range(len(personal))))

print("program zakonczył działanie")

#253982