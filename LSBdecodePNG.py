# @file SteganoCBTencode.py
# @author Michal Kaiser(221034)
# @version 0.2
# @date 2020-11-23
# @copyright Copyright (c) 2020
#
# Časť projektu steganografie obrazku, kde je spracované dekodovanie textu
# z obrázku, v ktorom bol text zakodovaný na najmenej príznakové bity.
try:
    import inputMenu as Mn
    import hashlib
    import numpy as np
except Exception as e:
    print("LSBdecodePNG.py EXCEPTION modul: {}".format(e))


# @brief funkcia na konvertovanie decimalneho cisla z matice do stringu z binárnymi hodnotami
#        s maximalnou decimalnou hodnotou 255 a minimalnou 0
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


# @brief funkcia na prevedenie celej matice do binarneho kodu
#
# @param matrix_of_img      matica RGBA vytvorena z obrazku
# @return binary_stream     retazec znakov pozostavajuci z binarneho kodu
def matrixToBinary(matrix_of_img):
    try:
        text = ""
        binary_stream = ''
        for i in range(0, len(matrix_of_img)):
            for j in range(0, len(matrix_of_img[i])):
                binary_matrix = decimalToBinary(matrix_of_img[i][j])
                binary_stream = binary_stream + binary_matrix
                if binary_matrix == "0":
                    raise ValueError("binarna hodnota matrixu neni v oktalovom tvare")
                if 64 == len(binary_stream):
                    lsb = getLSB(binary_stream)
                    if lsb == '00000011':
                        return text
                    text = text + binaryToUTF8(lsb)
                    binary_stream = ""
        return text
    except(ValueError, TypeError):
        print("Matica je v nespravnom formate")


def matrixToBinary2(matrix_of_img):
    try:
        text = ''
        binary_stream = ''
        for i in range(0, len(matrix_of_img)):
            for j in range(0, len(matrix_of_img[i])):
                binary_matrix = decimalToBinary(matrix_of_img[i][j])
                binary_stream = binary_stream + binary_matrix
                if binary_matrix == "0":
                    raise ValueError("binarna hodnota matrixu neni v oktalovom tvare")
                if 64 == len(binary_stream):
                    lsb = getLSB(binary_stream)
                    text = text + binaryToUTF8(lsb)
                    binary_stream = ""
        return text
    except(ValueError, TypeError):
        print("Matica je v nespravnom formate")


# @brief Funkcia na ziskanie posledneho priznakoveho bitu z retazca
#        kde kazda osmica bitu predstavuje jeden z paramterov R, G, B, A
#        a na konci kazdej osmice je najmenej vyznamovy bit, do ktoreho
#        sa uklada po jednom bite binarny kod textu
#
# @param binary_stream      retazec bianrnej hodnoty matice
# @return lsb               retazec binarnej hodnoty textu, ktora bola
#                           zakodovana do poslednych priznakovych bitov
#                           matice obrazku
def getLSB(binary_stream):
    try:
        lsb = ''
        one_char = ""
        j = 0
        while binary_stream != "":
            px = binary_stream[:8]
            lsb = lsb + px[-1]
            j += 1
            if j == 8:
                one_char = lsb[-8:]
                j = 0
            binary_stream = binary_stream[8:]
        return lsb
    except(ValueError, TypeError):
        print("Value or Type error occurred")


# @brief dekodovanie binarneho retazca do kodovej sady znakov UTF-8
#
# @param lsb             vstup je binarna hodnota textu ktory bol zakodovany do obrazku
# @return utf_str        vystup funkcie je string s kodovacou sadou UTF-8
def binaryToUTF8(lsb):
    binary_values = lsb.split()
    ascii_string = ""
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character
    return ascii_string


# @brief Funkcia na vypocet hashu sha o bitovej dlzke 256 bitov
#
# @param message        Sprava dekodovana z obrazku v UTF-8 kodovani
# @return hs            Funkcia vracia hodnotu hashu danej spravy
def hash_of_message(message):
    try:
        hash_of_mess = hashlib.sha256(message.encode()).hexdigest()
        return hash_of_mess
    except(ValueError, TypeError):
        print("Value or Type error occurred")


# @brief Funkcia, ktora zoberie hash ulozeny na koniec matice obrazku,
#        ktory sa bude porovnavat s vypocitanym hashom dekodvanej spravy
#
# @param matrix_of_img  Matica obrazku vo formate matica ([[R, G, B, A],...])
# @return hash            Funckia Vrati dekodovany hash
def get_hash_from_end(matrix):
    hash_end = np.flip(matrix[-512//len(matrix[0]):])
    hash_string = matrixToBinary2(hash_end)
    return hash_string


# @brief Funkcia na porovnanie hashu zakodovaneho v obrazku a hashu vypocitaneho
#       z dekodovaneho obrazku, ak sa rovnaju, tak funkcia vypise spravu, ak nie
#       tak oznami chybu v zakodovani spravy
#
# @param hs_mess        hash z dekodovaneho textu
# @param hs_end_of_img  hash zakodovany na konci matice
# @param message        sprava vo formate string
def compare_hash(hs_mess, hs_end_of_img, message):
    try:
        if hs_mess == hs_end_of_img:
            print(message)
        else:
            print("Sprava bola pomenena ")
    except(TypeError, ValueError):
        print("Value or Type error occurred")


def export(path):
    if __name__ == "__main__":
        # @brief Kontorlná matica na akúšku, kde su v matici ulozene hodnoty pixelov [R, G, B, A]
        matrix1, _ = Mn.encodeImgFormat(path)
        mess = matrixToBinary(matrix1)
        hash_of_me1 = hash_of_message(mess)
        print(hash_of_me1)
        hash_end1 = get_hash_from_end(matrix1)
        print(hash_end1)
        compare_hash(hash_of_me1, hash_end1, mess)
        print(mess)
