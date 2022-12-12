# Rafał Ciesnowski 253982

import random
import math
import sys


def encrypt(pub_name, plain_name):
    p, g, h = [int(i) for i in open(pub_name, "r").readlines()]
    m_array = bytearray(open(plain_name, "r").read(), 'utf-16')
    print("otworzyłem pliki:\n\t" + pub_name + "\t" + plain_name)
    if len(open(plain_name, "r").read()) > len(open(pub_name, "r").readlines()[0]):
        print("błąd:\n\tm > p")
        return
    z = []
    j = -32
    for i in range(len(m_array)):
        if i % 32 == 0:
            j += 32
            z.append(0)
        z[j // 32] += m_array[i] * (2 ** (8 * (i % 32)))
    cipher_pairs = []
    for i in z:
        y = random.randint(0, p)
        c = pow(g, y, p)
        d = (i * pow(h, y, p)) % p
        cipher_pairs.append([c, d])
    open("crypto.txt", "w").write("".join([str(pair[0]) + " " + str(pair[1]) for pair in cipher_pairs]))
    print("zapisano plik:\n\tcrypto.txt")


def decrypt(priv_name, cryp_name):
    private_txt = open(priv_name, "r").readlines()
    c_array = open(cryp_name, "r").read().split()
    print("otworzyłem pliki:\n\t" + priv_name + "\t" + cryp_name)
    p = int(private_txt[0])
    x = int(private_txt[2])
    plaintext = []
    if not len(c_array) % 2 == 0:
        print("blad")
        return
    for i in range(0, len(c_array), 2):
        c = int(c_array[i])
        d = int(c_array[i + 1])
        s = pow(c, x, p)
        plain = (d * pow(s, p - 2, p)) % p
        plaintext.append(plain)
    bytes_array = []
    for num in plaintext:
        for i in range(32):
            temp = num
            for j in range(i + 1, 32):
                temp = temp % (2 ** (8 * j))
            letter = temp // (2 ** (8 * i))
            bytes_array.append(letter)
            num = num - (letter * (2 ** (8 * i)))
    open("decrypt.txt", "w").write("".join([ch for ch in bytearray(b for b in bytes_array).decode("utf-16", "ignore") if ch != '\x00']))
    print("zapisano plik:\n\tdecrypt.txt")


def signature(priv_name, mes_name):
    private_txt = open(priv_name, "r").readlines()
    message_txt = open(mes_name, "r").read()
    print("otworzyłem pliki:\n\t" + priv_name + "\t" + mes_name)
    p, g, x = [int(i) for i in private_txt]
    m = int(message_txt)
    while 1:
        k = random.randint(1, p-2)
        if math.gcd(k, p-1) == 1: break
    r = pow(g, k, p)
    s = pow(k, -1, p-1) * (m - x * r) % (p - 1)
    open("signature.txt", "w").write(str(r) + "\n" + str(s))
    print("zapisano:\n\tsignature.txt")


def verify(sig_name, mes_name, pub_name):
    signature_txt = open(sig_name, "r").readlines()
    message_txt = open(mes_name, "r").read()
    public_txt = open(pub_name, "r").readlines()
    print("otworzyłem pliki:\n\t" + sig_name + "\t" + mes_name + "\t" + pub_name)
    p, g, y = [int(i) for i in public_txt]
    r, s = [int(i) for i in signature_txt]
    m = int(message_txt)
    if r < 1 or r > p - 1: result = False
    else:
        v1 = pow(y, r, p) % p * pow(r, s, p) % p
        v2 = pow(g, m, p)
        result = v1 == v2
    open("verify.txt", "w").write(str(result))
    print("zapisano:\n\tverify.txt")


if (__name__ == "__main__") & (len(sys.argv) == 2):
    if sys.argv[1] == "-k":
        elgamal_txt = open("elgamal.txt", "r").readlines()
        print("otworzyłem plik:\n\telgamal.txt")
        x = random.randint(1, int(elgamal_txt[0]))
        h = pow(int(elgamal_txt[1]), x, int(elgamal_txt[0]))
        open("private.txt", "w").write(elgamal_txt[0] + elgamal_txt[1] + '\n' + str(x))
        open("public.txt", "w").write(elgamal_txt[0] + elgamal_txt[1] + '\n' + str(h))
        print("zapisano pliki:\n\tprivate.txt\tpublic.txt")
    elif sys.argv[1] == "-e":
        encrypt("public.txt", "plain.txt")
    elif sys.argv[1] == "-d":
        decrypt("private.txt", "crypto.txt")
    elif sys.argv[1] == "-s":
        signature("private.txt", "message.txt")
    elif sys.argv[1] == "-v":
        verify("signature.txt", "message.txt", "public.txt")
    else:
        print("błąd\n\tcoś się nie udało - przeczytaj tresc zadania")
else:
    print("błąd\n\tcoś się nie udało - przeczytaj tresc zadania")