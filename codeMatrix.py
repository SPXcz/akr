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
import codePNG as cP

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
INPUT: string - jmeno obrazku
OUPUT: int - promene, slouzici pro cyklus LSB

Pomocna funkce, ktera slouzi ke zjisteni typu matice v pripade RGBA(format PNG) bude algoritmus pracovat se 4 znaky, v pripade RGB(format JPG) pouze se 3
"""
def formatResearch(imgName):
  imgFormat, _= iM.getAllParameters(imgName)
  if imgFormat == "PNG":
    n = 4 
    m = 0
  elif imgFormat == "JPEG":
    n = 3
    m = 0
  return n, m
  
"""
Output: array, string - matice obrazku, format obrazku

Hlavni funkce tohoto filu, ktera pomoci metody LSB meni posledni byt matice v binarnim tvaru
na konec zpravy je zasifrovan koncovy znak 00000011, ktery slouzi k signalizci konce textu
pri desteganografii. Od konce matice je opet pomoci metody LSB ukladan binarni kod
zhasovane vstupni zpravy. Ulozeny hash ma bezpecnostni prvek, pomoci ktereho se bude v dalsich
funkci overovat zda nebyla data nejak upravovana

Matice ma tvar bud [[255,255,255,255], [255,255,255,255]] nebo [[255,255,255], [255,255,255]]
"""

def lsbMetrixMessage(imgName, text):

  imgFormat, matrixData = iM.getAllParameters(imgName)
  n, m = formatResearch(imgName)

  b_message = messageToBinary(text) + "00000011" #do b message ukladam zpravu binarnim kodu, ukladam ukoncujici retezec pro UTF8

  total_items = matrixData.size #pocet prvku v matici se kterymi je mozne pracovat
  req_pixels = len(b_message) #pocet potrebnych prvku se urcuje z delky zpravy 
  index = 0

  for p in range(total_items): 
    for q in range(m,n): #prochazi bud 3 znaky nebo 4 znaky podle formatu
      if (index < req_pixels):
        if(imgFormat == "JPEG" and matrixData[p][q] == 0):
          continue
        else:
          matrixData[p][q] = int(bin(matrixData[p][q])[2:-1] + b_message[index],2)
          index +=1
          """
          Binarni kod kazdeho znaku ma 0b100, pomoci slicingu odstranim 0b a posledni znak
          misto posledni znaku dosadim znak zhasovane zpravy v binarnim kodu. Nasledne to prevedeme zpet do dec
          """
  return imgFormat, matrixData, text, total_items

"""
output: imgFormat, matrixData, imgName - format obrazku, matice, jmeno souboru

Funcke, ktera od konce matice opet pomoci metody LSB uklada zhasovany text. Text zde ukladame jako bezpecnosti prvek abych zjistili,
zda nebylo s obrazkem nejak nakladano. Funkce je podobna jako predchozi s tim rozdilem, ze v ni pracujeme s obracenou matici. 

"""
def lsbMetrixHash(imgName, text):
  imgFormat, matrixData, text, total_items = lsbMetrixMessage(imgName, text)
  n, m = formatResearch(imgName)

  b_hash_message = messageToHash(text) #puvodni zhasovana zprava v binarnim kodu
  req_pixels = len(b_hash_message) #pocet potrebnych prvnku se urcuje z delky hashe
  matrixData = np.flip(matrixData) #otacim matici z [[64,64,64,1], [255,255,255,1]] do [[1,255,255,255], [1,64,64,1]]
  
  index = 0
  for p in range(total_items): 
    for q in range(m,n): #prochazi bud 3 znaky nebo 4 znaky podle formatu
      if (index < req_pixels):
          if(imgFormat == "JPEG" and matrixData[p][q] == 0):
            continue
          else:
            matrixData[p][q] = int(bin(matrixData[p][q])[2:-1] + b_hash_message[index],2)
          index +=1
          """
          Binarni kod kazdeho znaku ma 0b100, pomoci slicingu odstranim 0b a posledni znak
          misto posledni znaku dosadim znak zhasovane zpravy v binarnim kodu. Nasledne to prevedeme zpet do dec
          """
  matrixData = np.flip(matrixData) #otocim matici zpet
  iM.encodeMatrixFormat(imgName, imgFormat, matrixData)

def export(imgName, text):
  text = iM.checkInputText(text, iM.maxSizeText(imgName))
  lsbMetrixHash(imgName, text)
