# @file SteganoCBTencode.py
# @author Michal Kaiser(221034)
# @version 1.0
# @date 2020-11-23
# @copyright Copyright (c) 2020
#
# Časť projektu steganografie obrazku, kde je spracované dekodovanie textu z obrázku, v ktorom bol text zakodovaný
# na najmenej príznakové bity.
#
try:
    import codePNG as cPNG
    import hashlib
    import numpy as np
except Exception as e:
    print("LSBdecode.py EXCEPTION modul: {}".format(e))


# @brief funkcia na konvertovanie decimalneho cisla z matice do stringu z binárnymi hodnotami s maximalnou decimalnou
# hodnotou 255 a minimalnou 0
#
# @param num        hodnota jedneho z decimalnych cisiel(R, G, B, A) z matice
# @return binary    vracia binarny hodnotu cisla v stringu
def decimalToBinary(num):
    try:
        if num in range(256):
            binary = bin(num).replace("0b", "")
            if 8 >= len(binary):
                nulls = (8 - len(binary)) * "0"
                binary = nulls + binary
        else:
            raise ValueError("Cislo neni z rozsahu 0 - 255")
        return binary
    except(ValueError, TypeError):
        print("Value or Type error occurred")


# @brief funkcia na prevedenie celej matice na dekodovanu spravu.
#
# @param matrix_of_img      matica RGBA vytvorena z obrazku
# @return text              retazec znakov pozostavujuci zo spravy
def matrixToMessage(matrix_of_img):
    try:
        text = ''
        binary_stream = ''
        for i in range(0, len(matrix_of_img)):
            for j in range(0, len(matrix_of_img[i])):
                binary_matrix = decimalToBinary(matrix_of_img[i][j])
                binary_stream = binary_stream + binary_matrix
                if len(binary_matrix) != 8:
                    raise ValueError("binarna hodnota matrixu neni v oktalovom tvare")
                # ak prejde matica 16 (64 bitov)px tak zoberie posledne priznakove bity a prevedie ich z binaru
                # do stringu
                if 64 == len(binary_stream):
                    lsb = getLSB(binary_stream)
                    # binarny kod znaku, ktory naznacuje koniec textu
                    if i == 1 and j == 3 and lsb != '00000010' and len(matrix_of_img) > 128:
                        raise ValueError("Na zaciatku spravy neni znak naznacujuci zaciatok textu")
                    if lsb == '00000011':
                        return text
                    text += binaryToString(lsb)
                    if lsb == '00000010':
                        text = ''
                    binary_stream = ""
        return text
    except(ValueError, TypeError) as error:
        print(error)


# @brief Funkcia na ziskanie posledneho priznakoveho bitu z retazca kde kazda osmica bitu predstavuje  jeden
#        z paramterov R, G, B, A a na konci kazdej osmice je najmenej vyznamovy bit, do ktoreho sa uklada po
#        jednom bite binarny kod textu
#
# @param binary_stream      retazec bianrnej hodnoty matice
# @return lsb               retazec binarnej hodnoty textu, ktora bola
#                           zakodovana do poslednych priznakovych bitov
#                           matice obrazku
def getLSB(binary_stream):
    try:
        lsb = ''
        i = 0
        while binary_stream != "":
            px = binary_stream[:8]
            lsb = lsb + px[-1]
            i += 1
            if i == 8:
                i = 0
            binary_stream = binary_stream[8:]
        return lsb
    except(ValueError, TypeError):
        print("Value or Type error occurred")


# @brief dekodovanie binarneho retazca do kodovej sady znakov UTF-8
#
# @param lsb             vstup je binarna hodnota textu ktory bol zakodovany do obrazku
# @return utf_str        vystup funkcie je string s kodovacou sadou UTF-8
def binaryToString(lsb):
    binary_values = lsb.split()
    string = ""
    for binary_value in binary_values:
        integer_of_bin = int(binary_value, 2)
        character = chr(integer_of_bin)
        string += character
    return string


# @brief Funkcia na vypocet hashu sha o bitovej dlzke 256 bitov
#
# @param message        Sprava dekodovana z obrazku v UTF-8 kodovani
# @return hs            Funkcia vracia hodnotu hashu danej spravy
def hashOfMessage(message):
    try:
        if message is not None:
            hash_of_mess = hashlib.sha256(message.encode()).hexdigest()
            return hash_of_mess
        else:
            raise ValueError("Hash spravy nie je mozny ziskat")
    except(ValueError, TypeError):
        print("Hash spravy nie je mozny ziskat")


# @brief Funkcia, ktora zoberie hash ulozeny na koniec matice obrazku, ktory sa bude porovnavat s vypocitanym hashom
#        dekodvanej spravy.
#
# @param matrix_of_img  Matica obrazku vo formate matica ([[R, G, B, A],...])
# @return hash            Funckia Vrati dekodovany hash
def getHashFromImg(matrix):
    hash_end = np.flip(matrix[-512 // len(matrix[0]):])
    hash_string = matrixToMessage(hash_end)
    return hash_string


# @brief Funkcia na porovnanie hashu zakodovaneho v obrazku a hashu vypocitaneho
#       z dekodovaneho obrazku, ak sa rovnaju, tak funkcia vypise spravu, ak nie
#       tak oznami chybu v zakodovani spravy
#
# @param hs_mess        hash z dekodovaneho textu
# @param hs_end_of_img  hash zakodovany na konci matice
def compareHash(hs_mess, hs_end_of_img):
    try:
        if hs_mess == hs_end_of_img:
            print("Hash spravy a hash ziskany z obrazku sa rovanju: " + hs_mess)
            return True
        else:
            print("Hash spravy a hash ziskany z obrazku sa nerovanju, obrazok moze byt poskodeny, alebo sa sprava "
                  "zakodvala nespravne\nHash spravy: " + hs_mess + "\nHash z obrazku: " + hs_end_of_img)
            return False
    except(TypeError, ValueError):
        print("Hash sprav sa neda porovnat")


def export(path):
    try:
        if path:
            matrix1, _ = cPNG.encodeImgFormat(path)
            mess = matrixToMessage(matrix1)
            hash_of_me1 = hashOfMessage(mess)
            hash_end1 = getHashFromImg(matrix1)
            cmp_hash = compareHash(hash_of_me1, hash_end1)
            if cmp_hash:
                if len(mess) < 500:
                    print("Dekodovana sprava: " + mess)
                    with open("message.txt", "w") as file:
                        file.write(mess)
                else:
                    with open("message.txt", "w") as file:
                        file.write(mess)

        else:
            raise ValueError("Cesta ku obrazku je zadane nespravne")
    except ValueError as error:
        print(error)

