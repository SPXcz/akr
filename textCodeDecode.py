import sys

#Sem si mmůžete zajít, když potřebujete něco zakódovat nebo rozkódovat z/do UTF-8
#Stačí si naimportovat tento soubor pomocí - from textCodeDecode import TextCodeDecode

#Input: int - Decimální reprezentace int
#Output: int[] - Pole int bytů
#Pomocná funkce pro reprezentaci čísla jako pole bytů. bytes() vyžaduje reprezentaci dat jako je výstup této funkce.
def decToArray(dec):
    retArray = []
    while(dec > 0):
        retArray.append(dec % 256)
        dec = dec // 256
    return reversed(retArray)

#Třída TextCodeDecode má implicitní konstruktor. Uchovává data (jak řetězovou reprezentaci self.string, tak int reprezenatci self.dec).
#Vždy při zavolání nějaké z metod se atributy aktualizují. Není potřeba s nimi pracovat, protože oboje metody mají výstupy.
#Před použitím nějaké z metod si musíte vytvořit instanci (wow)
class TextCodeDecode:

    #Input: String - Řetězec UTF-8 znaků.
    #Output: int - base10 reprezentace řetězce
    #Tato metoda aktualizuje self.str a self.dec a převede řetězec na base10 int reprezentaci UTF-8
    def getDecFromString(self, str):
        self.string = str
        self.dec = int.from_bytes(str.encode('UTF-8', 'strict'), "big")
        return self.dec

    #Input: String - base10 reprezentace řetězce
    #Output: int - Řetězec UTF-8 znaků. 
    #Inverzní metoda k getDecFromString. Tato metoda aktualizuje self.dec a self.str a převede base10 int reprezentaci UTF-8 na řetězec
    def getStringFromDec(self, dec):
        self.dec = dec
        self.string = bytes(decToArray(dec)).decode('UTF-8', 'strict')
        return self.string


#Příklad použití. Spustit si to můžete napsaním "main()" pod definici této funkce
def main():
    decoder = TextCodeDecode() #Konstuktor
    decoder.getDecFromString('ahoj') #Zkusíme zakódovat řetězec
    print(decoder.dec) #Vytiskneme ho (atribut třídy)
    decoder.getStringFromDec(decoder.dec) #Získáme řetězec
    print(decoder.string) #Vytiskneme ho