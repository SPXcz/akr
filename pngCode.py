from PIL import Image
import numpy as np


def checkType(imgName):
    """The function detects image format (PNG, JPEG,...)
        return string"""
    return Image.open(imgName).format


def getImgSize(imgName):
    """Function return image size - WIDTH and HEIGHT"""
    width, height = Image.open(imgName).size
    return width, height


def imgToArray(imgName):
    """Function generates a matrix from the image
        return matrix ([[R,G,B,a], [R,G,B,a],...]) base10,
        and max number of char for the input text"""
    try:
        imgRGBA = Image.open(imgName, "r").convert("RGBA")
        arrayData = np.array(list(imgRGBA.getdata()))
        # 514 = (hashSize*2) + 2 .. hashSize-256b, 4b-RGBA, 2px-NULL point 
        maxText = int((len(arrayData) / 2) - 514)
        return arrayData, maxText
    except OSError:
        print("Cannot open: " + imgName)


def arrayToImg(imgName, arrayData, width, height):
    """Function generates an image from the matrix, 
        new image is save as 'stego_' + imgName"""
    if arrayData is not None:
        arrayData = arrayData.reshape(height, width, 4)
        img = Image.fromarray(arrayData.astype('uint8'), mode="RGBA")
        img.save("stego_"+imgName)
    else:
        print("ArrayData is empty....")

