from PIL import Image, ImageFilter
import numpy
import re

#Pak smazat a nahradit romanovou funkcí
def getImgSize(imgName):
    with Image.open(imgName, "r") as img:
        width, height = img.size

    return width, height

def getMaxSizeText(imgName):
    """
    Input: str (exampe.png) - nazov obrazku, alebo cesta k nemu
    Output: int - pocet pixelov v obrazku

    Pomocna funkcia, ktora zisti max pocet bajtů, ktore je moznes
    ulozit do obrazku. 
    Odcita velkost hashu a prazdny point.
    """
    with Image.open(imgName, "r") as img:
        width, height = img.size
        # 514 = (hashSize*2) + 2 .. hashSize-256b, 4b-RGBA, 2px-NULL point
        maxSize = ((3 * width * height) - 514) // 8
        return maxSize

def imgToArray(path):
    """
    param path - String - Cesta k jpg souboru
    return arrayData - int[int[]] - Decimální matice reprezentující pixely (RGB)

    Funkcia ma za ulohu, z obrazku spravit maticu kde budu 
    ulozene jednotlive pixely v mode 'RGB'
    """
    try:
        with Image.open(path) as img:
            width, height = img.size
            data = img.load()
    except OSError:
        print("ERROR imgToArray({}), can't open!".format(path))

    row = []
    for x in range(width):
        for y in range(height):
            r, g, b = data[x,y]
            row.append(r)
            row.append(g)
            row.append(b)
    
    imgMat = numpy.array(row)
    imgMat = imgMat.reshape(len(row) // 3, 3)

    return imgMat

def arrayToImg(imgName, matrixIn):
    """
    param matrice - int[int[]] - Decimální matice reprezentující pixely (RGB)
    param imgName - String - Jméno souboru
    return path - String - Cesta k jpg souboru

    Output - ulozi novy obrazok (stego_example.png)
    Funkcia, ktora z matice zrealizuje obrazok vo formate JPG.

    NEPOUŽÍVÁNO
    """

    width, height = getImgSize(imgName)
    size = width, height

    if matrixIn is not None:
        img = Image.new("RGB", size)
        imgData = img.load()
        for x in range(width):
            for y, point in zip(range(height), matrixIn):
                r, g, b = point
                imgData[x, y] = (r, g, b)
            matrixIn = matrixIn[height:]

        imgName = re.findall(r"[\w']+", imgName)
        img.save("data/{}_stego.{}".format(imgName[-2], imgName[-1]), format='JPEG', quality=100)
        img.close()
        return "data/{}_stego.{}".format(imgName[-2], imgName[-1])
    else:
        return None

def rgbToRgba(rgbMat):
    """
    param matrice - int[int[]] - Decimální matice reprezentující pixely (RGB) - Nx3
    return path - int[int[]] - Decimální matice reprezentující pixely (RGBA) - Nx4

    Funkce přidává jeden sloupec k RGB matici pro reprezentaci průhlednosti (A). 
    Průhlednost je automaticky nastavena na 255 - řádná průhlednost.
    Fukce se používá při převodu z jpg na png.
    """

    fivefive = []
    for a in rgbMat:
        fivefive.append(255)
    
    ffRow = numpy.array(fivefive).reshape(len(rgbMat), 1)
    rgbaMat = numpy.c_[rgbMat, ffRow]
    return rgbaMat


def main():
    imgName = './data/meme.jpg'
    data = imgToArray(imgName)
    print(rgbToRgba(data))

main()
    