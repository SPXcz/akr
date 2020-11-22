from PIL import Image
import numpy as np

"""
    FILE codePNG bol vytvoreny pre nacitanie obrazku vo formate
    PNG, z ktoreho spravi maticu RGBa a naopak z matice spravi 
    PNG obrazok, dalej tu najdes funkciu, ktora kontroluje typ
    formatu
    hodnoty matice su base10
    ukazka matice ->   [[R, G, B, a], 
                        [R, G, B, a],
                        ....
                        [R, G, B, a]]
"""

"""
    Input: str (example.png) - nazov obrazku, alebo cesta k nemu
    Output: string - vrati format obrazku, napr. PNG, JPEG,...
    Pomocna funkcia, ktora vrati format vstupneho obrazku.
"""
def checkType(imgName):
    try:
        img = Image.open(imgName)
        return img.format
    except IOError:
        print("ERROR checkType({})".format(imgName))


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu
    Output: int, int - sirka a vyska obrazku
    Pomocna funkcia pre zistenie sirky a vysky obrazku.
"""
def getImgSize(imgName):
    width, height = Image.open(imgName, "r").size
    return width, height


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu
    Output: int - pocet pixelov v obrazku
    Pomocna funkcia, ktora zisti max pocet znakov, ktore je mozne
    ulozit do obrazku. 
    Odcita velkost hashu a prazdny point.
"""
def getMaxSizeText(imgName):
    img = Image.open(imgName, "r")
    width, height = img.size
    # 514 = (hashSize*2) + 2 .. hashSize-256b, 4b-RGBA, 2px-NULL point 
    maxSize = int((width * height) / 2 - 514)
    return maxSize


"""
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu 
    Output: array - matica obrazku
    Funkcia ma za ulohu, z obrazku spravit maticu kde budu 
    ulozene jednotlive pixely v mode 'RGBa'
"""
def imgToArray(imgName):
    try:
        imgRGBA = Image.open(imgName, "r").convert("RGBA")
        arrayData = np.array(list(imgRGBA.getdata()))
        
        return arrayData
    except OSError:
        print("Cannot open: " + imgName)


"""
    Input: str, array
    Output - ulozi novy obrazok (stego_example.png)
    Funkcia, ktora z matice zrealizuje obrazok vo formate PNG.
"""
def arrayToImg(imgName, arrayData):
    width, height = getImgSize(imgName)
    if arrayData is not None:
        arrayData = arrayData.reshape(height, width, 4)
        img = Image.fromarray(arrayData.astype('uint8'), mode="RGBA")
        img.save("stego_"+imgName)
    else:
        print("ArrayData is empty....")

