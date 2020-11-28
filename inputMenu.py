"""
    FILE inputMenu bol vytvoreny pre nacitanie vsetkych potrebnych 
    vstupnych udajov - nazov obrazku, vstupny text, hash vstupneho
    textu
    Funkcie:
        checkInputText(maxText) - kontrola vstupneho textu
        encodeImgFormat(imgName) - podla formatu vrati maticu obrazku
        encodeMatrixFormat(imgFormat, imgName, matrixData) 
                        - z matice zrealizuje obrazok podla formatu
        maxSizeText(imgName) - zistuje max pocet znakov pre vstupny
                                text
        getAllParameters() - najdolezitejsia funkcia, vola vsetky potrebne 
                    funkcie a vracia vsetky potrebne parametre
    IMPORT -> napr. 'import inputMenu as iM'
        pristup k jednotlivym funkciam ->  iM.inputMenu()
"""
try:
    import hashlib
    import codePNG as cP
    import codeJpg as cJ
except Exception as e:
    print("'inputMenu.py', EXCEPTION modul: {}".format(e))


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


"""
    Input: str - nazov obrazku, alebo cesta k nemu.
    Output: array, str - matica obrazku, zalezi podla formatu
    Funkcia ma za ulohu ulahcit pracu uzivatelovi, aby nemusel manualne
    zadavat format obrazku. Podla zisteneho formatu zavola vhodnu
    funkciu pre zakodovanie obrazku do matice.
"""
def encodeImgFormat(imgName):
    imgFormat = cP.checkType(imgName)

    if imgFormat == "PNG":
        return cP.imgToMatrix(imgName), imgFormat
    elif imgFormat == "JPEG":
        return cJ.rgbToRgba(cJ.imgToArray(imgName)), imgFormat
    else:
        print("{} - nevhodny format!!".format(imgFormat))


"""
    Input: array, str - maticu obrazku, format obrazku
    Output: zavola funkciu pre ulozenie obrazku
    Funkcia bola navrhnuta pre opatovne zostavenie obrazku podla
    zadaneho formatu. Tato funkcia sa zavola po pouziti LSB metody.
    Cize v matici bude ulozena sprava.
"""
def encodeMatrixFormat(imgName, matrixData): 
        return cP.matrixToImg(imgName, matrixData)
        

"""
    Input: str - nazov obrazku
    Output: int - max povoleny pocet znakov pre spravu
    Funkcia sluzi k zistenie max poctu znakov vstupnej spravy.
"""
def maxSizeText(imgName):
    return cP.getMaxSizeText(imgName)

