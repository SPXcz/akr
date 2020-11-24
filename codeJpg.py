from PIL import Image, ImageFilter
import numpy

#Pak smazat a nahradit romanovou funkcí
def getImgSize(imgName):
    width, height = Image.open(imgName, "r").size
    return width*height

def imgToArray(path):
    """
    param path - String - Cesta k jpg souboru
    return arrayData - int[int[]] - Decimální matice reprezentující pixely (RGB)
    """

    with Image.open(path) as img:
        imgMat = img.convert('L')
        arrayData = numpy.array(list(imgMat.getdata()))
        print(arrayData)
    
    return arrayData

def arrayToImg(imgName, data):
    """
    param matrice - int[int[]] - Decimální matice reprezentující pixely (RGB)
    param imgName - String - Jméno souboru
    return path - String - Cesta k jpg souboru
    """
    #size = getImgSize('./data/meme.jpg')
    size = 65500

    if data is not None:
        data = data.reshape(size)
        img = Image.fromarray(data.astype('uint8'), mode="L")
        img.save(imgName)
        img.close()
        return imgName
    else:
        return None

def main():
    data = imgToArray('./data/meme.jpg')
    print(arrayToImg("./data/test.jpg", data))
    

main()