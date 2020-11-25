from PIL import Image, ImageFilter
import numpy

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

        imgName = imgName.split(".jpg")[0]
        img.save(imgName+"_stego.jpg")
        img.close()
        return imgName+"_stego.jpg"
    else:
        return None

def main():
    imgName = './data/meme.jpg'
    data = imgToArray(imgName)
    print(arrayToImg(imgName, data))
    