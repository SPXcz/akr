"""
    FILE codePNG bol vytvoreny pre nacitanie obrazku vo formate
    png a jpg, z ktorych spravi maticu, jpg sa ulozi ako png a az 
    potom sa do obrazku skryje sprava, dalej tu najdes funckie na
    kontrolu image typu, spravenie z obrazku maticu a z matice 
    obrazok, dalej kontroluje vstupny text na zaklade max 
    povoleneho mnozstva znakov pre vstupny text...
    ukazka matice ->   [[R, G, B, a], 
                        [R, G, B, a],
                        ....
                        [R, G, B, a]]
    Funkcie:
        checkType(imgName) - kontroluje format obrazku
        getImgSize(imgName) - vracia sirku a vysku obrazku
        getMaxSizeText(imgName) - vracia max pocet znakov pre 
                                    vstupny text
        saveImageName(imgName) - upravi nazov stego obrazku
        jpegToPng(imgName) - z jpg spravi png
        imgToMatrix(imgName) - z obrazku spravi maticu RGBA hodnot
        matrixToImg(imgName, matrixData) - z matice RGBA spravi
                                            obrazok
        checkInputText(maxText) - kontrola vstupneho textu
        encodeImgFormat(imgName) - podla formatu vrati maticu obrazku

    IMPORT -> napr. 'import codePNG as cP'
        pristup k jednotlivym funkciam ->  cP.checkInputText()
"""
try:
    from PIL import Image
    import numpy as np
    import re
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
        # 514=(hashSize*2)+2 ..hashSize-256b,4b-RGBA,2px-NULL point
        maxSize = int((width * height) / 2 - 516)
        return maxSize


"""
    Input: str - nazov obrazku, alebo cestu k nemu
    Output: str - cestu k obrazku
    Funkcia sluzi k tomu, ze nacita nazov obrazku a
    prisposoby nazov k ulozeniu stego obrazku.
"""    
def saveImageName(imgName):
    img = re.findall(r"[\w']+", imgName)
    
    if img[-1] == "jpg":
        return "data/{}_jpeg_stego.png".format(img[-2])
    elif img[-1] == "png":
        return "data/{}_stego.png".format(img[-2])
    else:
        return None


"""
    Input: str - nazov obrazku, alebo cesta k nemu
    Output: str - nazov obrazku, alebo cestu k nemu
    Funkcia ma za ulohu nacitat jpg obrazok a preformatovat
    ho na png. Vystup vracia nazov, alebo cestu k 
    novovytvoreneho obrazku .png .
"""
def jpegToPng(imgName):
    try:
        newName = saveImageName(imgName)
        with Image.open(imgName, "r") as img:
            img.save(newName)
            return newName
    except OSError:
        print("ERROR jpegToPng({}), can't open!".format(imgName))


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
        newName = saveImageName(imgName)
        if newName is not None:
            img.save(newName)
            return newName
        else:
            text = """The image is not saved!! The image format is not
            suported by the program!"""
            print(text)
            return None
    else:
        print("Matrix is empty....")


"""
    Input: str - nazov obrazku, alebo cesta k nemu.
    Output: array, str - matica obrazku, zalezi podla formatu
    Funkcia ma za ulohu ulahcit pracu uzivatelovi, aby nemusel manualne
    zadavat format obrazku. Podla zisteneho formatu zavola vhodnu
    funkciu pre zakodovanie obrazku do matice.
"""
def encodeImgFormat(imgName):
    imgFormat = checkType(imgName)
    if imgFormat == "JPEG":
        imgName = jpegToPng(imgName)
    return imgToMatrix(imgName), imgFormat


"""
    Input: int - max pocet znakov, ktorych je mozne vlozit do obrazku
    Output: str - return vstupneho textu
    Pomocna funkcia, ktora je urcena pre nacitanie vstupneho textu
    a zaroven kontroluje max pocet znakov textu, ak je text vacsi nez
    max pocet znakov, rekurzivne sa zavola znovu tato funkcia.
"""
def checkInputText(text, maxText):
    if len(text) <= maxText:
        return text
    else:
        try:
            text = str(input("Message[max {}]: ".format(maxText))).rstrip()
            return checkInputText(text, maxText)
        except InterruptedError:
            print("ERROR checkInputText(), end of program...")

