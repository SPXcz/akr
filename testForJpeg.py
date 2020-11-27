import numpy as np
from random import randrange
import codeJpg as cJ


def randList():
    return list(randrange(0, 255) for i in range(3))


def getRandomMatrix(sizeM):
    matrix = np.array([randList() for i in range(sizeM)])
    return matrix


def maxSize(img):
    w, h = cJ.getImgSize(img)
    return w * h

def compareMatrix(origM, newM):
    for y in range(len(origM)):
        for x in range(3):
            # print("{} <=> {}".format(origM[y][x], newM[y][x]))
            origM[y][x] = abs(origM[y][x] - newM[y][x])
    return origM


def getMaxNumber(maxNum, num):
    if maxNum <= num:
        return num
    else:
        return maxNum


def aritmeticMatrix(matA, matB):
    matrix = compareMatrix(matA, matB)
    sumNum, maxNum = 0, 0

    for y in range(len(matrix)):
        for x in range(3):
            sumNum += matrix[y][x]
            maxNum = getMaxNumber(maxNum, matrix[y][x])
    return  sumNum / len(matrix), maxNum


def main():
    listData = [[]]
    for i in range(100):
        img1 = "data/meme.jpg"
        origMatrix = getRandomMatrix(maxSize(img1))
        cJ.arrayToImg(img1, origMatrix)
        
        img2 = "data/meme_stego.jpg"
        matA = cJ.imgToArray(img2)
        cJ.arrayToImg(img2, matA)
        
        img3 = "data/meme_stego_stego.jpg"
        matB = cJ.imgToArray(img3)

        aritNum = aritmeticMatrix(matA, matB)
        listData.append(aritNum)
        print("{}.  | {} ".format(i, aritNum))

"""
    snazil som sa to ulozit automaticky do suboru, ale 
    nejak som to nezvladol :D ... ale takci tak to ucel 
    splnilo... najprv ti ukazuje cislovenie a dalsie je priemer
    a posledny je maximaln y rozdiel v matici
"""
main()