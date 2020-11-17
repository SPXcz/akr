import binascii

#Sem si mmůžete zajít, když potřebujete něco zakódovat nebo rozkódovat z/do UTF-8
#Stačí si naimportovat tento soubor pomocí - from textCodeDecode import TextCodeDecode

class TextCodeDecode:
    def getHexFromString(self, str):
        self.string = str
        self.hex = str.encode('UTF-8', 'strict').hex()
        return self.hex
    
    def getStringFromHex(self, hex):
        self.hex = hex
        self.string = hex.fromhex().decode('UTF-8', 'strict')
        return self.string


def main():
    decoder = TextCodeDecode()
    decoder.getHexFromString('ahoj')
    print(decoder.hex)
    decoder.getStringFromHex(decoder.hex)
    print(decoder.string)

main()