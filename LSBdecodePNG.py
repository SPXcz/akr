# @file SteganoCBTencode.py
# @author Michal Kaiser(221034)
# @version 0.1
# @date 2020-11-23
# @copyright Copyright (c) 2020
#
# Časť projektu steganografie obrazku, kde je spracované dekodovanie textu
# z obrázku, v ktorom bol text zakodovaný na najmenej príznakové bity.

import hashlib

from numpy import *

# @brief Kontorlná matica na akúšku, kde su v matici ulozene hodnoty pixelov [R, G, B, A]
matrix1 = array([[78, 87, 154, 254], [128, 58, 200, 255], [124, 88, 6, 254], [8, 10, 27, 255]])


# @brief funkcia na konvertovanie decimalneho cisla z matice do stringu z binárnymi hodnotami
#
# @param num        hodnota jedneho z decimalnych cisiel(R, G, B, A) z matice
# @return binary    vracia binarny hodnotu cisla v stringu
def decimalToBinary(num):
    binary = bin(num).replace("0b", "")
    if 8 >= len(binary):
        nulls = (8 - len(binary)) * "0"
        binary = nulls + binary
    else:
        print("cislo je prilis velke")
    return binary


# @brief funkcia na prevedenie celej matice do binarneho kodu
#
# @param matrix_of_img      matica RGBA vytvorena z obrazku
# @return binary_stream     retazec znakov pozostavajuci z binarneho kodu
def matrixToBinary(matrix_of_img):
    binary_stream = ''
    for i in range(0, len(matrix_of_img)):
        for j in range(0, len(matrix_of_img[i])):
            binary_stream = binary_stream + decimalToBinary(matrix_of_img[i][j])
    return binary_stream


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
    lsb = ''
    one_char = " "
    j = 0
    while one_char != '00000011':
        if binary_stream != '':
            px = binary_stream[:8]
            lsb = lsb + px[-1]
        j += 1
        if j == 8:
            one_char = lsb[-8:]
            j = 0
        binary_stream = binary_stream[8:]
    return lsb


# @brief dekodovanie binarneho retazca do kodovej sady znakov UTF-8
#
# @param lsb             vstup je binarna hodnota textu ktory bol zakodovany do obrazku
# @return utf_str        vystup funkcie je string s kodovacou sadou UTF-8
def binaryToUTF8(lsb):
    lsb = lsb[:-8]
    print(lsb)
    binary_values = lsb.split()
    ascii_string = ""
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character
    utf_str = ascii_string.encode("utf-8")
    return utf_str


# @brief Funkcia na vypocet hashu sha o bitovej dlzke 256 bitov
#
# @param message        Sprava dekodovana z obrazku v UTF-8 kodovani
# @return hs            Funkcia vracia hodnotu hashu danej spravy
def hash_of_message(message):
    hs = hashlib.sha256(message).hexdigest()
    return hs


# @brief Funkcia, ktora zoberie hash ulozeny na koniec matice obrazku,
#        ktory sa bude porovnavat s vypocitanym hashom dekodvanej spravy
#
# @param matrix_of_img  Matica obrazku vo formate matica ([[R, G, B, A],...])
# @return hash            Funckia Vrati dekodovany hash
def get_hash_from_end(matrix_of_img):
    print("zatial nic")


# @brief Funkcia na porovnanie hashu zakodovaneho v obrazku a hashu vypocitaneho
#       z dekodovaneho obrazku, ak sa rovnaju, tak funkcia vypise spravu, ak nie
#       tak oznami chybu v zakodovani spravy
#
# @param hs_mess        hash z dekodovaneho textu
# @param hs_end_of_img  hash zakodovany na konci matice
# @param message        sprava vo formate string
def compare_hash(hs_mess, hs_end_of_img, message):
    if hs_mess == hs_end_of_img:
        print(message)
    else:
        print("Sprava bola pomenena ")


print(matrixToBinary(matrix1))
text_output = getLSB(matrixToBinary(matrix1))
print(getLSB(matrixToBinary(matrix1)))
print(type(text_output))
utf = binaryToUTF8(text_output)
print(utf)
print(hash_of_message(utf))
