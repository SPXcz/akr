from PIL import Image, ImageFilter
import numpy
import re

#Pak smazat a nahradit romanovou funkcí
def getImgSize(imgName):
    with Image.open(imgName, "r") as img:
        width, height = img.size

    return width, height

def imgToArray(path):
    """
    param path - String - Cesta k jpg souboru
    return arrayData - int[int[]] - Decimální matice reprezentující pixely (RGB)
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

def main():
    imgName = './data/meme.jpg'
    data = imgToArray(imgName)
    print(arrayToImg(imgName, data))
    