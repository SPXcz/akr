"""
File stegano.py byl vytvoren ze ucelem ulozeni zpravy, koncoveho znaku a hashe do
matice v dec tvaru

Funkce:
  hash(message) - funkce pro hashovani zpravy
  messageToBinary(message) - funkce, ktera prevadi zpravu do binarniho kodu
  encode - nejdulezitejsi funkce, funkce pomoci metodz LSB meni posledni
    bit cisla v binarnim podle zpravy v binarnim kouu. Do matice se od konce
    uklada hash v binarnim tvaru stejne jako v predchozim tvaru. Hash slouzi
    k overeni zda bylo s daty nejak nakladano. Je to bezpecnostni prvek

    IMPORT -> napr 'import stegano as st
    pristup k funkcim -> st.stegano()
"""
import numpy as np
import hashlib
import inputMenu as iM
import codePNG

"""
  Input: string - zprava kterou zada uzivatel
  Output: string - return zahashovana data v binarnim tvaru

  Funkce, ktera na zaklade vstupniho testu vraci zhashovany text pomoci sha256
"""
def messageToHash(message):
  hashMessage = hashlib.sha256(message.encode('utf-8')).hexdigest()
  return messageToBinary(hashMessage)

"""
  Input: string - zprava ktera ma byt prevedena do binarniho kodu
  Output: string - zprava v binarnim kodu

  Pomocna funkce, ktera slouzi k prevadeni stringu do binarniho tvaru
"""

def messageToBinary(message):
  if (len(message) == 0):
    print("Zadna data")
  else:
    return ''.join([format(ord(i), "08b") for i in message]) #vratim zpravu v binarnim kodu

"""
Output: array, string - matice obrazku, format obrazku

Hlavni funkce tohoto filu, ktera pomoci metody LSB meni posledni byt matice v binarnim tvaru
na konec zpravy je zasifrovan koncovy znak 00001010, ktery slouzi k signalizci konce textu
pri desteganografii. Od konce matice je opet pomoci metody LSB ukladan binarni kod
zhasovane vstupni zpravy. Ulozeny hash ma bezpecnostni prvek, pomoci ktereho se bude v dalsich
funkci overovat zda nebyla data nejak upravovana
"""
def lsbMetrixMessage():
  imgName, imgFormat, metrixData, text = iM.getAllParameters()

  #pomocne funkce k prochazeni matice ve tvaru RGBA (tvar RGB - n=3, m=0)
  n = 4 
  m = 0

  b_message = messageToBinary(text) + "00000111" #do b message ukladam zpravu binarnim kodu, ukladam ukoncujici retezec

  total_items = metrixData.size #pocet prvku v matici se kterymi je mozne pracovat
  req_pixels = len(b_message) #pocet potrebnych prvku pro zpravu 
  index = 0
  for p in range(total_items): #celkem 64 
    for q in range(m,n): #od 0 do 3 -> tudiz projde 4 cisla
      if (index < req_pixels):
          metrixData[p][q] = int(bin(metrixData[p][q])[2:-1] + b_message[index],2) #prevedu do decimalu, binarni kod, ktery je zbaven 0b a posledniho cisla. Na posledni cislo se prida cislo binarniho kodu odpovidajiciho indexu
          index +=1
  return imgFormat, metrixData, text, imgName, total_items, n , m

def lsbMetrixHash():
  imgFormat, metrixData, text, imgName, total_items, n , m = lsbMetrixMessage()

  b_hash_message = messageToHash(text)
  req_pixels = len(b_hash_message)
  metrixData = np.flip(metrixData)
  
  index = 0
  print(metrixData)
  print(b_hash_message)
  for p in range(total_items): #celkem 64 
    for q in range(m,n): #od 0 do 3 -> tudiz projde 4 cisla
      if (index < req_pixels):
          metrixData[p][q] = int(bin(metrixData[p][q])[2:-1] + b_hash_message[index],2) #prevedu do decimalu, binarni kod, ktery je zbaven 0b a posledniho cisla. Na posledni cislo se prida cislo binarniho kodu odpovidajiciho indexu
          index +=1
  metrixData = np.flip(metrixData)
  print(metrixData)
  return imgFormat, metrixData, imgName

def main():
  lsbMetrixHash()
