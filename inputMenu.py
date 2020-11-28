"""
    FILE inputMenu bol vytvoreny pre nacitanie vsetkych potrebnych 
    vstupnych udajov - nazov obrazku, vstupny text, hash vstupneho
    textu
    Funkcie:
        checkInputText(maxText) - kontrola vstupneho textu
        encodeImgFormat(imgName) - podla formatu vrati maticu obrazku
    IMPORT -> napr. 'import inputMenu as iM'
        pristup k jednotlivym funkciam ->  iM.checkInputText()




        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        TOTO VYMATEM :D :D
        lebo je to ybztocneeeee...... treba sa odkazat na codePNG.py
        tam najdete vsetko
"""
try:
    import codePNG as cP
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
    if imgFormat == "JPEG":
        imgName = cP.jpegToPng(imgName)
    return cP.imgToMatrix(imgName), imgFormat

