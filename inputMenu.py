"""
    FILE inputMenu bol vytvoreny pre nacitanie vsetkych potrebnych 
    vstupnych udajov - nazov obrazku, vstupny text, hash vstupneho
    textu
    Funkcie:
        checkInputText(maxText) - kontrola vstupneho textu
        encodeImgFormat(imgName) - podla formatu vrati maticu obrazku
        encodeMatrixFormat(arrayData, imgFormat) - z matice zrealizuje
                                                obrazok podla formatu
        maxSizeText(imgName) - zistuje max pocet znakov pre vstupny
                                text
        mainMenu() - najdolezitejsia funkcia, vola vsetky potrebne 
                    funkcie a vracia vsetky potrebne parametre
    IMPORT -> napr. 'import inputMenu as iM'
        pristup k jednotlivym funkciam ->  iM.inputMenu()
"""
import hashlib
import codePNG as cP


"""
    Input: int - max pocet znakov, ktorych je mozne vlozit do obrazku
    Output: str - return vstupneho textu
    Pomocna funkcia, ktora je urcena pre nacitanie vstupneho textu
    a zaroven kontroluje max pocet znakov textu, ak je text vacsi nez
    max pocet znakov, rekurzivne sa zavola znovu tato funkcia.
"""
def checkInputText(maxText):
    try:
        text = str(input("Message[max {}]: ".format(maxText))).rstrip()
    except InterruptedError:
        print("ERROR checkInputText(), end of program...")
    else:
        if len(text) <= maxText:
            return text
        else:
            return checkInputText(maxText)


"""
    Input: str - nazov obrazku, alebo cesta k nemu
    Output: array, str - matica obrazku, zalezi podla formatu
    Funkcia ma za ulohu ulahcit pracu uzivatelovi, aby nemusel manualne
    zadavat format obrazku. Podla zisteneho formatu zavola vhodnu
    funkciu pre zakodovanie obrazku do matice.
"""
def encodeImgFormat(imgName):
    imgFormat = cP.checkType(imgName)

    if imgFormat == "PNG":
        return cP.imgToMatrix(imgName), imgFormat
    elif imgFormat == "JPG":
        # ondrejova funkcia pre JPG
        pass
    else:
        print("{} - nevhodny format!!".format(imgFormat))


"""
    Input: array, str - maticu obrazku, format obrazku
    Output: zavola funkciu pre ulozenie obrazku
    Funkcia bola navrhnuta pre opatovne zostavenie obrazku podla
    zadaneho formatu. Tato funkcia sa zavola po pouziti LSB metody.
    Cize v matici bude ulozena sprava.
"""
def encodeMatrixFormat(imgName, matrixData, imgFormat):
    if imgFormat == "PNG":
        return cP.matrixToImg(imgName, matrixData)
    elif imgFormat == "JPG":
        # ondrejova funkcia pre obnovenie JPG
        pass
        

"""
    Input: str - nazov obrazku
    Output: int - max povoleny pocet znakov pre spravu
    Funkcia sluzi k zistenie max poctu znakov vstupnej spravy.
"""
def maxSizeText(imgName):
    imgFormat = cP.checkType(imgName)
    if imgFormat == "PNG":
        return cP.getMaxSizeText(imgName)
    elif imgFormat == "JPG":
        # ondrejova funcia pre zistenie poctu pixelov
        pass 


"""
    Output: str, array, str, str - format obrazku,matica obrazku,
                                vstupny text, hash z textu
    Hlavna funkcia pre ziskanie vsetkych parametrov...
    Dajme tomu, ze to je ako konstruktor, vzdy sa musi zavolat
    na zaciatku celeho programu...
"""
def mainMenu():
    try:
        imgName = str(input("Image name(napr pic.png): ")).rstrip()
        matrixData, imgFormat = encodeImgFormat(imgName)
        maxText = maxSizeText(imgName)
        text = checkInputText(maxText)
        hashText = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return imgFormat, matrixData, text, hashText
    except:
        print("Zadali ste nespravny parameter!!!!")
        return 0, 0, None, None

