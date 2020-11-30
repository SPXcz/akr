from PIL import Image, ImageFilter
import numpy
import re
import codePNG as cP

#Z designových důvodů se tento soubor nepoužívá.


def getImgSize(imgName):
    """
    param imgName - String - Cesta k souboru s obrázkem
    return width, height - int, int - Šířka a výška obrázku v pixelech

    Pomocná funkce pro získání rozměrů obrázku. Kvůli otevírání souboru by neměla být v jiném with - open statmentu.
    """
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

    NEPOUŽÍVÁ SE, je nahrazena podobnou funkcí v codePNG.py
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

    Funkcia ma za ulohu, z jpg obrazku spravit maticu kde budu 
    ulozene jednotlive pixely v mode 'RGB'

    NEPOUŽÍVÁ SE, je nahrazena podobnou funkcí 
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

    NEPOUŽÍVÁNO, protože se .jpg vůbec neukládá
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

    NEPOUŽÍVÁNO, protože ukládáme .jpg přímo do .png místo do matice a pak zase do .png
    """

    fivefive = []
    for a in rgbMat:
        fivefive.append(255)
    
    ffRow = numpy.array(fivefive).reshape(len(rgbMat), 1)
    rgbaMat = numpy.c_[rgbMat, ffRow]
    return rgbaMat

#Test funkcí v souboru
def main():
    imgName = './data/meme.jpg'
    data = imgToArray(imgName)
    cP.matrixToImg(imgName, rgbToRgba(data))
    print(rgbToRgba(data))