# Rafał Ciesnowski 253982

import sys

def e1(mess, cover):
    mess = open(mess).read()
    mess = bin(int(mess, 16))[2:].zfill(len(mess)*4)
    cover = open(cover, "rt", encoding="utf-8").read().splitlines()
    # usuwanie istniejących spacji na końcu wersów
    for i in range(len(cover)):
        if cover[i] != "" and cover[i][-1] == " ":
            cover[i] = cover[i][:-1]
    print("OTWARTO:\n\tmess.txt\tcover.html")
    if len(mess) > len(cover):
        print("BLAD:\n\thtml zbyt krótki")
        return ""
    for i in range(len(mess)):
        if mess[i] == "1":
            cover[i] += " \n"
        elif mess[i] == "0":
            cover[i] += "\n"
    return "".join(cover)

def e2(mess, cover):
    mess = open(mess).read()
    mess = bin(int(mess, 16))[2:].zfill(len(mess) * 4)
    # usuwanie istniejących spacji, rozdzielanie tekstu na wyrazy
    cover = open(cover, "rt", encoding="utf-8").read().split(" ")
    print("OTWARTO:\n\tmess.txt\tcover.html")
    if len(mess) > len(cover):
        print("BLAD:\n\thtml zbyt krótki")
        return ""
    for i in range(len(mess)):
        if mess[i] == "1":
            cover[i] += "  "
        elif mess[i] == "0":
            cover[i] += " "
    return "".join(cover)

def e3(mess, cover):
    mess = open(mess).read()
    mess = bin(int(mess, 16))[2:].zfill(len(mess) * 4)
    # usuwanie istniejących <div, rozdzielenie na fragmenty od otwierającego tagu div do następnego otwierającego tagu
    cover = open(cover, "rt", encoding="utf-8").read().split("<div")
    if len(mess) > len(cover):
        print("BLAD:\n\thtml zbyt krótki")
        return ""
    print("OTWARTO:\n\tmess.txt\tcover.html")
    for i in range(len(mess)):
        cover[i].replace("onkeypres=\"click\"", "")
        cover[i].replace("clas=\"hero\"", "")
        if mess[i] == "0":
            cover[i] += "<div onkeypres=\"click\" class=\"hero\""
        elif mess[i] == "1":
            cover[i] += "<div onkeypress=\"click\" clas=\"hero\""
    for i in range(len(mess), len(cover)-1):
        cover[i] += "<div"
    return "".join(cover)

def e4(mess, cover):
    mess = open(mess).read()
    mess = bin(int(mess, 16))[2:].zfill(len(mess) * 4)
    cover = open(cover, "rt", encoding="utf-8").read().split("<b>")
    
    if len(mess) > len(cover):
        print("BLAD:\n\thtml zbyt krótki")
        return ""
    print("OTWARTO:\n\tmess.txt\tcover.html")
    for i in range(len(mess)):
        # usuwanie istniejących niepotrzebnych tagów
        cover[i+1].replace("</b><b></b>", "")
        cover[i + 1].replace("<b></b><b>", "")
        if mess[i] == "0":
            cover[i+1] = cover[i+1].replace("</b>", "</b><b></b>")
        elif mess[i] == "1":
            cover[i+1] += "<b></b><b>"
    for i in range(len(mess)+1, len(cover)-1):
        cover[i] += "<b>"
    return "".join(cover)

def d1(watermark):
    watermark = open(watermark, "rt", encoding="utf-8").read().splitlines()
    print("OTWARTO:\n\twatermark.html")
    detect = ""
    for i in watermark:
        if i[-1] == " ":
            detect += "1"
        else:
            detect += "0"
    return '%0*X' % ((len(detect) + 2) // 4, int(detect[:-1], 2))

def d2(watermark):
    watermark = open(watermark, "rt", encoding="utf-8").read()
    print("OTWARTO:\n\twatermark.html")
    detect = ""
    flag = 0
    for i in range(len(watermark)-1):
        if flag == 1:
            flag = 0
        elif watermark[i] == " ":
            if watermark[i+1] == " ":
                detect += "1"
                flag = 1
            else:
                detect += "0"
    return '%0*X' % ((len(detect) + 3) // 4, int(detect, 2))

def d3(watermark):
    watermark = open(watermark, "rt", encoding="utf-8").read().split("<div")
    print("OTWARTO:\n\twatermark.html")
    detect = ""
    for line in watermark:
        if "onkeypres=\"click\" class=\"hero\"" in line:
            detect += "0"
        elif "onkeypress=\"click\" clas=\"hero\"" in line:
            detect += "1"
    return '%0*X' % ((len(detect) + 3) // 4, int(detect, 2))

def d4(watermark):
    watermark = open(watermark, "rt", encoding="utf-8").read()
    print("OTWARTO:\n\twatermark.html")
    detect = ""
    for i in range(len(watermark)-14):
        if watermark[i:i+11] == "</b><b></b>":
            detect += "0"
        elif watermark[i:i+10] == "<b></b><b>":
            detect += "1"
    return '%0*X' % ((len(detect) + 3) // 4, int(detect, 2))


if (__name__ == "__main__") & (len(sys.argv) == 3):
    tryb = sys.argv[1]
    algorytm = sys.argv[2]
    if tryb == "-e":
        if algorytm == "-1":
            with open("watermark.html", "w", encoding="utf-8") as file:
                file.write(e1("mess.txt", "cover.html"))
                print("ZAPISANO:\n\twatermark.html")
        elif algorytm == "-2":
            with open("watermark.html", "w", encoding="utf-8") as file:
                file.write(e2("mess.txt", "cover.html"))
                print("ZAPISANO:\n\twatermark.html")
        elif algorytm == "-3":
            with open("watermark.html", "w", encoding="utf-8") as file:
                file.write(e3("mess.txt", "cover.html"))
                print("ZAPISANO:\n\twatermark.html")
        elif algorytm == "-4":
            with open("watermark.html", "w", encoding="utf-8") as file:
                file.write(e4("mess.txt", "cover.html"))
                print("ZAPISANO:\n\twatermark.html")
    elif tryb == "-d":
        if algorytm == "-1":
            with open("detect.txt", "w") as file:
                file.write(d1("watermark.html"))
                print("ZAPISANO:\n\tdetect.txt")
        elif algorytm == "-2":
            with open("detect.txt", "w") as file:
                file.write(d2("watermark.html"))
                print("ZAPISANO:\n\tdetect.txt")
        elif algorytm == "-3":
            with open("detect.txt", "w") as file:
                file.write(d3("watermark.html"))
                print("ZAPISANO:\n\tdetect.txt")
        elif algorytm == "-4":
            with open("detect.txt", "w") as file:
                file.write(d4("watermark.html"))
                print("ZAPISANO:\n\tdetect.txt")
else:
    print("Przykład wywołania:\n\tpython3 stegano.py -e -1")