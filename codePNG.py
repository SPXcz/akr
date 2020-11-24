"""
    FILE codePNG bol vytvoreny pre nacitanie obrazku vo formate
    PNG, z ktoreho spravi maticu RGBa a naopak z matice spravi 
    PNG obrazok, dalej tu najdes funkciu, ktora kontroluje typ
    formatu
    ukazka matice ->   [[R, G, B, a], 
                        [R, G, B, a],
                        ....
                        [R, G, B, a]]
    Funkcie:
        checkType(imgName) - kontroluje typ obrazku
        getImgSize(imgName) - zistuje sirku a vysku obrazku
        getMaxSizeText(imgName) - pocita maximalny pocet znakov
                                pre vstupny text
        imgToMatrix(imgName) - z obrazku spravi maticu dat, base10
        matrixToImg(imgName, matrixData) - z matice spravi obrazok
"""
try:
    from PIL import Image
    import numpy as np
except Exception as e:
    print("'codePNG.py' EXCEPTION modul: {}".format(e))


"""
    Input: str (example.png) - nazov obrazku, alebo cesta k nemu
    Output: string - vrati format obrazku, napr. PNG, JPEG,...
    Pomocna funkcia, ktora vrati format vstupneho obrazku.
"""
def checkType(imgName):
    try:
        with Image.open(imgName, "r") as img:
            return img.format
    except IOError:
        print("ERROR checkType({}), can't open!".format(imgName))


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu
    Output: int, int - sirka a vyska obrazku
    Pomocna funkcia pre zistenie sirky a vysky obrazku.
"""
def getImgSize(imgName):
    try:
        with Image.open(imgName, "r") as img:
            return img.size
    except IOError:
        print("ERROR getImgSize({}), can't open!".format(imgName))


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu
    Output: int - pocet pixelov v obrazku
    Pomocna funkcia, ktora zisti max pocet znakov, ktore je mozne
    ulozit do obrazku. 
    Odcita velkost hashu a prazdny point.
"""
def getMaxSizeText(imgName):
    with Image.open(imgName, "r") as img:
        width, height = img.size
        # 514 = (hashSize*2) + 2 .. hashSize-256b, 4b-RGBA, 2px-NULL point 
        maxSize = int((width * height) / 2 - 2)
        return maxSize


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu 
    Output: array - matica obrazku
    Funkcia ma za ulohu, z obrazku spravit maticu kde budu 
    ulozene jednotlive pixely v mode 'RGBa'
"""
def imgToMatrix(imgName):
    try:
        with Image.open(imgName, "r") as img:
            imgRGBA = img.convert("RGBA")
            matrixData = np.array(list(imgRGBA.getdata()))
            return matrixData
    except OSError:
        print("ERROR imgToArray({}), can't open!".format(imgName))


"""
    Input: str, array - nazov obrazku je povodny obrazok 
                        napr. example.png
    Output - ulozi novy obrazok (stego_example.png)
    Funkcia, ktora z matice zrealizuje obrazok vo formate PNG.
"""
def matrixToImg(imgName, matrixData):
    width, height = getImgSize(imgName)
    if matrixData is not None:
        matrixData = matrixData.reshape(height, width, 4)
        img = Image.fromarray(matrixData.astype('uint8'), mode="RGBA")
        imgName = imgName.split(".")
        img.save("./data/{}_stego.{}".format(imgName[0], imgName[1]))
    else:
        print("Matrix is empty....")

